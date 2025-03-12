from typing import List, Dict
import openai
from datetime import datetime
import json
from pathlib import Path

class Logger:
    def __init__(self, log_file: str = "data/complete_logs.json"):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(exist_ok=True)
        if not self.log_file.exists():
            self._init_log_file()
    
    def _init_log_file(self):
        initial_structure = {
            "chat_logs": [],
            "embedding_logs": [],
            "memory_stats": {
                "total_memories": 0,
                "total_tokens_used": 0,
                "total_cost": 0.0
            }
        }
        with open(self.log_file, 'w') as f:
            json.dump(initial_structure, f, indent=2)
    
    def log_chat(self, request: Dict, response: Dict, memory_ops: Dict):
        with open(self.log_file, 'r+') as f:
            logs = json.load(f)
            logs["chat_logs"].append({
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "request": request,
                "response": response,
                "memory_operations": memory_ops
            })
            f.seek(0)
            json.dump(logs, f, indent=2)

class LLMInterface:
    def __init__(self, model: str = "gpt-4"):
        self.model = model
        self.logger = Logger()
        self.system_prompt = """You are an intelligent assistant with human-like memory capabilities. 
        You can recall past conversations and experiences, with memories becoming stronger through repeated recall.
        When using memories in your responses, try to naturally weave them into the conversation rather than 
        just listing them."""

    def generate_response(
        self, 
        user_message: str, 
        relevant_memories: List[Dict],
        chat_history: List[Dict]
    ) -> str:
        """Generate a response using the LLM with context from memories."""
        
        # Format memories for context
        memory_context = ""
        if relevant_memories:
            memory_context = "\nRelevant memories:\n" + "\n".join(
                f"- {m['content']} (Recalled {m['recall_count']} times)" 
                for m in relevant_memories
            )

        # Format recent chat history (last 5 messages)
        recent_history = chat_history[-5:] if chat_history else []
        formatted_history = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in recent_history
        ]

        # Construct messages for API call
        messages = [
            {"role": "system", "content": self.system_prompt + memory_context},
            *formatted_history,
            {"role": "user", "content": user_message}
        ]

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I apologize, but I'm having trouble generating a response right now."

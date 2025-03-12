from typing import List, Dict
import openai
from datetime import datetime

class LLMInterface:
    def __init__(self, model: str = "gpt-4"):
        self.model = model
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

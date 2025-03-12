import json
from typing import Dict, List
from pathlib import Path
import threading

class SimpleStorage:
    def __init__(self, storage_dir: str = "data"):
        self.storage_dir = Path(storage_dir)
        print(f"Initializing storage in {self.storage_dir}")  # Debug log
        self.storage_dir.mkdir(exist_ok=True)
        self.memories_file = self.storage_dir / "memories.json"
        self.chat_file = self.storage_dir / "chat_history.json"
        self.lock = threading.Lock()
        
        # Initialize files if they don't exist
        if not self.memories_file.exists():
            self._save_memories([])
        if not self.chat_file.exists():
            self._save_chat_history([])
    
    def _save_memories(self, memories: List[Dict]) -> None:
        with self.lock:
            with open(self.memories_file, 'w') as f:
                json.dump(memories, f)
    
    def _save_chat_history(self, history: List[Dict]) -> None:
        with self.lock:
            with open(self.chat_file, 'w') as f:
                json.dump(history, f)
    
    def load_memories(self) -> List[Dict]:
        with self.lock:
            with open(self.memories_file, 'r') as f:
                return json.load(f)
    
    def load_chat_history(self) -> List[Dict]:
        with self.lock:
            with open(self.chat_file, 'r') as f:
                return json.load(f)
    
    def add_memory(self, memory: Dict) -> None:
        memories = self.load_memories()
        memories.append(memory)
        self._save_memories(memories)
    
    def add_chat_message(self, message: Dict) -> None:
        history = self.load_chat_history()
        history.append(message)
        self._save_chat_history(history)
    
    def update_memory(self, memory_id: int, updates: Dict) -> None:
        memories = self.load_memories()
        for memory in memories:
            if memory['id'] == memory_id:
                memory.update(updates)
                break
        self._save_memories(memories)

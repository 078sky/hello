from typing import List
import openai
import numpy as np
from functools import lru_cache

class Vectorizer:
    def __init__(self, model: str = "text-embedding-ada-002"):
        self.model = model
        self._cache = {}

    @lru_cache(maxsize=1000)
    def get_embedding(self, text: str) -> List[float]:
        """Get embedding for text, with caching."""
        try:
            response = openai.Embedding.create(
                input=[text],
                model=self.model
            )
            return response['data'][0]['embedding']
        except Exception as e:
            print(f"Error getting embedding: {e}")
            # Return zero vector as fallback
            return [0.0] * 1536  # Ada-002 dimension 
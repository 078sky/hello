from typing import List, Dict
import numpy as np
from .consolidation import calculate_recall_probability

def find_relevant_memories(
    query_vector: List[float],
    memories: List[Dict],
    similarity_threshold: float = 0.86,
    max_memories: int = 5
) -> List[Dict]:
    """Find relevant memories based on vector similarity and recall probability."""
    relevant_memories = []
    
    for memory in memories:
        # Calculate similarity
        similarity = np.dot(query_vector, memory['vector']) / (
            np.linalg.norm(query_vector) * np.linalg.norm(memory['vector'])
        )
        
        if similarity < similarity_threshold:
            continue
            
        # Calculate recall probability
        elapsed_time = memory['last_recalled'] - memory['created_at']
        prob = calculate_recall_probability(
            relevance=similarity,
            elapsed_time=elapsed_time,
            consolidation_factor=memory['consolidation_factor']
        )
        
        if prob >= similarity_threshold:
            relevant_memories.append({
                **memory,
                'relevance': similarity,
                'recall_probability': prob
            })
    
    # Sort by relevance and limit results
    relevant_memories.sort(key=lambda x: x['relevance'], reverse=True)
    return relevant_memories[:max_memories] 
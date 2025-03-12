import math
from datetime import datetime

def sigmoid(x: float) -> float:
    """Modified sigmoid function for memory consolidation."""
    if x <= 0:
        return 0.0
    return (1 - math.exp(-x)) / (1 + math.exp(-x))

def calculate_elapsed_time(last_timestamp: float) -> float:
    """Calculate time elapsed in seconds since the timestamp."""
    now = datetime.now().timestamp()
    return now - last_timestamp

def calculate_consolidation_factor(elapsed_time: float, current_g: float = 1.0) -> float:
    """Update the consolidation factor based on elapsed time."""
    s_t = sigmoid(elapsed_time)
    return current_g + s_t

def calculate_recall_probability(
    relevance: float, 
    elapsed_time: float, 
    consolidation_factor: float
) -> float:
    """Calculate probability of recalling a memory."""
    exponent = -relevance * math.exp(-elapsed_time / max(consolidation_factor, 0.001))
    numerator = 1 - math.exp(exponent)
    denominator = 1 - math.exp(-1)
    return numerator / denominator
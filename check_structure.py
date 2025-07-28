# check_structure.py

import re

def predict_scores(text: str):
    """
    Predict scores for Clarity, Novelty, and Citation Strength using rule-based heuristics.

    Returns:
        clarity (float): Score between 0–10
        novelty (float): Score between 0–10
        citation_strength (float): Score between 0–10
    """

    # Clarity: Penalize unclear terms
    unclear_terms = ["unclear", "confusing", "ambiguous"]
    clarity_penalty = sum(text.lower().count(term) for term in unclear_terms)
    clarity = 10 - clarity_penalty

    # Novelty: Reward mentions of novel/contribution keywords
    novelty_terms = ["novel", "contribution", "original", "new approach"]
    novelty_score = sum(text.lower().count(term) for term in novelty_terms)
    novelty = 5 + novelty_score

    # Citation Strength: Count citation-style references like [1], [2]
    citation_strength = len(re.findall(r'\[\d+\]', text)) + 1  # Add 1 to avoid zero

    # Clip values between 0 and 10
    clarity = max(0, min(10, clarity))
    novelty = max(0, min(10, novelty))
    citation_strength = max(0, min(10, citation_strength))

    return clarity, novelty, citation_strength

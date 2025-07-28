from difflib import SequenceMatcher

def check_plagiarism(text, references):
    """
    Simple plagiarism checker using text similarity.

    Args:
        text (str): The paper's extracted text.
        references (list): A list of reference texts to compare against.

    Returns:
        float: Highest similarity score as a percentage.
    """
    max_similarity = 0.0
    for ref in references:
        similarity = SequenceMatcher(None, text, ref).ratio()
        if similarity > max_similarity:
            max_similarity = similarity

    return max_similarity * 100  # Convert to percentage

"""
Detects whether a prompt is semantically ambiguous even if structurally valid.
"""


def is_ambiguous(prompt: str) -> bool:
    """
    Detects whether a prompt is semantically ambiguous even if structurally valid.
    
    Args:
        prompt: The user's input prompt.
        
    Returns:
        True if the prompt is ambiguous, False otherwise.
    """
    # Convert to lowercase for matching
    lower_prompt = prompt.lower()
    
    # Check word count
    words = lower_prompt.split()
    if len(words) < 3:
        return True
    
    # Vague domain words
    vague_words = [
        "model", "system", "thing", "stuff", "data",
        "process", "method", "technology", "tool"
    ]
    
    # Domain-specific keywords that provide clarity
    domain_keywords = [
        "cnn", "neural", "network", "classification", "regression",
        "database", "python", "algorithm", "model training",
        "machine learning", "deep learning"
    ]
    
    # Check if contains vague words
    has_vague = any(word in lower_prompt for word in vague_words)
    
    # Check if contains domain-specific keywords
    has_domain = any(keyword in lower_prompt for keyword in domain_keywords)
    
    # Ambiguous if has vague words but no domain context
    if has_vague and not has_domain:
        return True
    
    return False


if __name__ == "__main__":
    tests = [
        "Explain models",
        "Explain machine learning models",
        "Tell me about data",
        "Tell me about Python data structures",
        "Compare systems"
    ]
    for t in tests:
        print(t, "→", is_ambiguous(t))

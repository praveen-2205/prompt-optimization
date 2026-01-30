"""
Breaks complex prompts into multiple actionable sub-tasks.
"""

import re


def decompose_prompt(prompt: str) -> list:
    """
    Breaks complex prompts into multiple actionable sub-tasks.
    
    Args:
        prompt: The user's input prompt.
        
    Returns:
        A list of sub-tasks extracted from the prompt.
    """
    # Define connectors to split on
    connectors = ["and", ",", "then", "also", "along with"]
    
    # Build regex pattern for splitting
    # Use word boundaries for text connectors to avoid splitting mid-word
    pattern_parts = []
    for conn in connectors:
        if conn == ",":
            pattern_parts.append(re.escape(conn))
        else:
            pattern_parts.append(r'\b' + re.escape(conn) + r'\b')
    
    pattern = '|'.join(pattern_parts)
    
    # Split the prompt
    parts = re.split(pattern, prompt, flags=re.IGNORECASE)
    
    # Clean each part
    cleaned_parts = []
    for part in parts:
        # Strip spaces
        cleaned = part.strip()
        
        if not cleaned:
            continue
        
        # Remove duplicate words
        words = cleaned.split()
        seen = set()
        unique_words = []
        for word in words:
            lower_word = word.lower()
            if lower_word not in seen:
                seen.add(lower_word)
                unique_words.append(word)
        
        cleaned = ' '.join(unique_words)
        
        if cleaned:
            cleaned_parts.append(cleaned)
    
    # If only one part or no parts, return original prompt
    if len(cleaned_parts) <= 1:
        return [prompt.strip()]
    
    return cleaned_parts


if __name__ == "__main__":
    tests = [
        "Explain CNN and compare with RNN",
        "Summarize this article, then analyze key ideas",
        "Write code and explain the logic",
        "Describe neural networks"
    ]
    for t in tests:
        print(t, "→", decompose_prompt(t))

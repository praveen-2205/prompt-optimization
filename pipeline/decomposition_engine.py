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
    
    # Check for comparison keywords - if present, do NOT split on "and"
    comparison_keywords = ["compare", "difference", "vs", "versus"]
    lower_prompt = prompt.lower()
    is_comparison = any(keyword in lower_prompt for keyword in comparison_keywords)
    
    # Remove "and" from connectors if this is a comparison sentence
    if is_comparison:
        connectors = [c for c in connectors if c != "and"]
    
    # Build regex pattern for splitting
    # Use word boundaries for text connectors to avoid splitting mid-word
    pattern_parts = []
    for conn in connectors:
        if conn == ",":
            pattern_parts.append(re.escape(conn))
        else:
            pattern_parts.append(r'\b' + re.escape(conn) + r'\b')
    
    pattern = '|'.join(pattern_parts)
    
    # Split the prompt (only if we have patterns to split on)
    if pattern:
        parts = re.split(pattern, prompt, flags=re.IGNORECASE)
    else:
        parts = [prompt]
    
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

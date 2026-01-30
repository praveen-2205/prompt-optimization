"""
LLM Reasoner Module

This module decides whether an LLM is needed for semantic understanding
and, if yes, rewrites the prompt semantically.

The hybrid approach uses:
- Rules for structure and control
- LLM for semantic understanding when rule-based logic is insufficient
"""


def needs_llm_assistance(score_data: dict, intents: list, raw_prompt: str) -> bool:
    """
    Determine if LLM assistance is needed for prompt optimization.
    
    Args:
        score_data: Dictionary containing scoring information including 'total_score'.
        intents: List of detected intent strings.
        raw_prompt: The original user input prompt.
        
    Returns:
        True if LLM assistance is needed, False otherwise.
    """
    total_score = score_data.get("total_score", 0)
    
    # Condition 1: Borderline clarity (score between 4 and 6)
    if 4 <= total_score <= 6:
        return True
    
    # Condition 2: More than 3 intents detected
    if len(intents) > 3:
        return True
    
    # Condition 3: Conflicting intents detected
    conflicting_pairs = [
        ("creative", "analysis"),
        ("creative", "coding"),
        ("summarization", "tutorial")
    ]
    for intent1, intent2 in conflicting_pairs:
        if intent1 in intents and intent2 in intents:
            return True
    
    # Condition 4: Long prompt with confusion words
    words = raw_prompt.split()
    confusion_phrases = [
        "confused", "not sure", "help me understand", 
        "i don't get", "explain simply"
    ]
    lower_prompt = raw_prompt.lower()
    
    if len(words) > 40:
        if any(phrase in lower_prompt for phrase in confusion_phrases):
            return True
    
    return False


def llm_rewrite_prompt(raw_prompt: str) -> str:
    """
    Rewrite the prompt using LLM for better semantic understanding.
    
    Args:
        raw_prompt: The original user input prompt.
        
    Returns:
        A semantically rewritten prompt.
    """
    try:
        from pipeline.llm_interface import call_gemini
    except ImportError:
        from llm_interface import call_gemini
    
    rewrite_instruction = (
        "Rewrite the following user request into ONE clear, concise sentence "
        "that preserves the original tasks and does NOT add extra explanation, examples, or structure. "
        "Do NOT expand the request. Do NOT split into multiple parts. "
        "Output only the improved single-sentence request:\n\n"
        + raw_prompt
    )
    
    return call_gemini(rewrite_instruction)


if __name__ == "__main__":
    # Test cases
    test_score_low = {"total_score": 3}
    test_score_borderline = {"total_score": 5}
    test_score_high = {"total_score": 8}
    
    test_intents_few = ["explanation"]
    test_intents_many = ["explanation", "comparison", "coding", "analysis"]
    test_intents_conflicting = ["creative", "analysis"]
    
    print("Borderline score (5):", needs_llm_assistance(test_score_borderline, [], "test"))
    print("High score (8):", needs_llm_assistance(test_score_high, [], "test"))
    print("Many intents (4):", needs_llm_assistance(test_score_high, test_intents_many, "test"))
    print("Conflicting intents:", needs_llm_assistance(test_score_high, test_intents_conflicting, "test"))
    print()
    print("LLM Rewrite:", llm_rewrite_prompt("Explain neural networks"))

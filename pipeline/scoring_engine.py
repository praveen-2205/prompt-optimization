"""
Scores prompts to detect how well-defined they are.

This module evaluates the quality of user prompts based on three criteria:
- Clarity: How clear and actionable the prompt is
- Specificity: How specific and detailed the prompt is
- Structure: How well-formatted and organized the prompt is

Each criterion is scored from 0-5, with a total score out of 15.
"""


def score_prompt(prompt: str) -> dict:
    """
    Score a prompt based on clarity, specificity, and structure.
    
    Args:
        prompt: The user prompt to evaluate.
        
    Returns:
        A dictionary containing individual scores and total score.
    """
    lower_prompt = prompt.lower()
    words = prompt.split()
    word_count = len(words)
    
    # --- Clarity Score (0-5) ---
    clarity = 0
    
    # +2 if prompt length > 5 words
    if word_count > 5:
        clarity += 2
    
    # +2 if contains action verbs
    action_verbs = ["explain", "compare", "build", "analyze", "write"]
    if any(verb in lower_prompt for verb in action_verbs):
        clarity += 2
    
    # +1 if no vague words
    vague_words = ["something", "stuff", "things"]
    if not any(vague in lower_prompt for vague in vague_words):
        clarity += 1
    
    clarity = min(clarity, 5)  # Cap at 5
    
    # --- Specificity Score (0-5) ---
    specificity = 0
    
    # +2 if contains technical words
    technical_words = ["python", "algorithm", "neural", "database", "model"]
    if any(tech in lower_prompt for tech in technical_words):
        specificity += 2
    
    # +2 if contains constraints
    constraint_words = ["step", "example", "code", "table"]
    if any(constraint in lower_prompt for constraint in constraint_words):
        specificity += 2
    
    # +1 if length > 8 words
    if word_count > 8:
        specificity += 1
    
    specificity = min(specificity, 5)  # Cap at 5
    
    # --- Structure Score (0-5) ---
    structure = 0
    
    # +2 if punctuation present
    punctuation_marks = ["?", ".", ":"]
    if any(punct in prompt for punct in punctuation_marks):
        structure += 2
    
    # +2 if includes formatting indicators
    formatting_words = ["list", "table", "bullet", "step"]
    if any(fmt in lower_prompt for fmt in formatting_words):
        structure += 2
    
    # +1 if starts with capital letter
    if prompt and prompt[0].isupper():
        structure += 1
    
    structure = min(structure, 5)  # Cap at 5
    
    # --- Total Score ---
    total_score = clarity + specificity + structure
    
    return {
        "clarity": clarity,
        "specificity": specificity,
        "structure": structure,
        "total_score": total_score
    }


if __name__ == "__main__":
    tests = [
        "tell me something",
        "Explain neural network architecture with example",
        "Compare CNN and RNN in table format",
        "Write python code"
    ]
    for t in tests:
        print(t)
        print(score_prompt(t))

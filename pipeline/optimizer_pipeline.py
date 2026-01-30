"""
This module is the base prompt optimizer. It improves clarity before advanced modules are applied.

The optimizer applies rule-based transformations to raw user prompts to:
- Clean and normalize input text
- Detect user intent using the intent handler
- Apply intent-specific optimization templates
- Wrap general prompts with clear task structure
"""

try:
    from pipeline.intent_handler import detect_intents
    from pipeline.scoring_engine import score_prompt
    from pipeline.ambiguity_detector import is_ambiguous
    from pipeline.decomposition_engine import decompose_prompt
except ImportError:
    from intent_handler import detect_intents
    from scoring_engine import score_prompt
    from ambiguity_detector import is_ambiguous
    from decomposition_engine import decompose_prompt


def _build_instructions_for_intents(intents: list) -> list:
    """
    Build instruction list based on detected intents.
    
    Args:
        intents: List of detected intent strings.
        
    Returns:
        List of instruction strings.
    """
    instructions = []
    
    if "explanation" in intents:
        instructions.append("Explain clearly in structured bullet points.")
    
    if "comparison" in intents:
        instructions.append("Present the comparison in a table covering key differences and similarities.")
    
    if "coding" in intents:
        instructions.append("Provide clean, well-commented code and explain the logic.")
    
    if "analysis" in intents:
        instructions.append("Include analytical insights, pros, cons, and evaluation.")
    
    if "summarization" in intents:
        instructions.append("Provide a concise summary highlighting key ideas.")
    
    if "tutorial" in intents:
        instructions.append("Present the explanation step-by-step like a tutorial.")
    
    # Add creative tone only if task is not technical coding
if "creative" in intents and "coding" not in intents:
    instructions.append("Use engaging and vivid language.")

    
    # If no specific instructions, add a default one
    if not instructions:
        instructions.append("Provide a clear and detailed response.")
    
    return instructions


def optimize_prompt(raw_prompt: str) -> str:
    """
    Optimize a raw user prompt for improved clarity and structure.
    
    Args:
        raw_prompt: The original user input prompt.
        
    Returns:
        An optimized prompt with improved clarity and structure.
    """
    # Step A — Clean the input
    cleaned = raw_prompt.strip()
    cleaned = ' '.join(cleaned.split())  # Remove extra spaces
    
    if not cleaned:
        return ""
    
    # Capitalize first letter
    cleaned = cleaned[0].upper() + cleaned[1:] if len(cleaned) > 1 else cleaned.upper()
    
    # Step B — Score the prompt
    score_data = score_prompt(raw_prompt)
    total_score = score_data["total_score"]
    
    # Step C — Decision logic based on score
    if total_score <= 3:
        return (
            "The request is unclear or too vague. Please provide more details about "
            "what you want. For example, specify the topic, format, or type of output."
        )
    
    # Step D — Ambiguity check (aggressive optimization: applies to all prompts with score > 3)
    if is_ambiguous(raw_prompt):
        return (
            "Your request is too broad or ambiguous. Please clarify the domain or context. "
            "For example, specify whether this relates to technology, business, science, or another field."
        )
    
    # Step E — Decompose prompt into subtasks
    subtasks = decompose_prompt(raw_prompt)
    
    # Step F — Build optimized output for each subtask
    optimized_output = ""
    
    for subtask in subtasks:
        # Detect intents for this subtask
        intents = detect_intents(subtask)
        
        # Build instructions for this subtask
        instructions = _build_instructions_for_intents(intents)
        
        # Format subtask output
        instructions_text = "\n".join(f"- {inst}" for inst in instructions)
        optimized_output += f"Sub-Task: {subtask}\nInstructions:\n{instructions_text}\n\n"
    
    return optimized_output.strip()


if __name__ == "__main__":
    tests = [
        "Write python code to sort a list",           # High quality
        "Explain CNN and compare with RNN",           # Multi-task
        "tell me something",                          # Vague
        "Explain models"                              # Ambiguous
    ]

    for t in tests:
        print("INPUT:", t)
        print("OUTPUT:", optimize_prompt(t))
        print("-" * 50)


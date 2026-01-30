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
    from pipeline.context_handler import needs_context
    from pipeline.llm_reasoner import needs_llm_assistance, llm_rewrite_prompt
    from pipeline.llm_interface import generate_final_answer
except ImportError:
    from intent_handler import detect_intents
    from scoring_engine import score_prompt
    from ambiguity_detector import is_ambiguous
    from decomposition_engine import decompose_prompt
    from context_handler import needs_context
    from llm_reasoner import needs_llm_assistance, llm_rewrite_prompt
    from llm_interface import generate_final_answer


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


def optimize_prompt(raw_prompt: str, previous_context: str = None) -> str:
    """
    Optimize a raw user prompt for improved clarity and structure.
    
    Args:
        raw_prompt: The original user input prompt.
        previous_context: Optional context from previous interactions.
        
    Returns:
        An optimized prompt with improved clarity and structure.
    """
    # STEP 1 — Attach context (MUST be first, before any checks)
    if previous_context and needs_context(raw_prompt):
        raw_prompt = f"Considering the previous context: {previous_context}. Now perform this request: {raw_prompt}"
    
    # STEP 2 — Score the prompt (now with context attached)
    score_data = score_prompt(raw_prompt)
    total_score = score_data["total_score"]
    
    # STEP 3 — If score <= 3, request clarification
    if total_score <= 3:
        return (
            "The request is unclear or too vague. Please provide more details about "
            "what you want. For example, specify the topic, format, or type of output."
        )
    
    # STEP 4 — Ambiguity detection (AFTER context is attached)
    ambiguity_flag = is_ambiguous(raw_prompt)
    if ambiguity_flag:
        return (
            "Your request is too broad or ambiguous. Please clarify the domain or context. "
            "For example, specify whether this relates to technology, business, science, or another field."
        )
    
    # STEP 5 — LLM rewrite decision based on quality
    low_quality = score_data["total_score"] < 6
    is_vague = ambiguity_flag
    
    llm_triggered = False
    if low_quality or is_vague:
        print("[LLM Rewrite Triggered]")
        llm_triggered = True
        raw_prompt = llm_rewrite_prompt(raw_prompt)
    
    # STEP 6 — Decompose prompt into subtasks
    subtasks = decompose_prompt(raw_prompt)
    
    # STEP 7 & 8 — Intent detection and instruction building for each subtask
    optimized_output = ""
    
    if llm_triggered:
        optimized_output += "[LLM Rewrite Triggered]\n\n"
    
    for subtask in subtasks:
        # STEP 7 — Detect intents for this subtask
        intents = detect_intents(subtask)
        
        # STEP 8 — Build instructions for this subtask
        instructions = _build_instructions_for_intents(intents)
        
        # Format subtask output
        instructions_text = "\n".join(f"- {inst}" for inst in instructions)
        optimized_output += f"Sub-Task: {subtask}\nInstructions:\n{instructions_text}\n\n"
    
    # STEP 9 — Debug print: show optimized prompt
    print("----- OPTIMIZED PROMPT -----")
    print(optimized_output)
    print("-" * 40)
    
    return optimized_output


if __name__ == "__main__":
    tests = [
        ("Explain CNN and compare with RNN", None),
        ("I am confused about overfitting and dropout, help me understand simply", None),
        ("Write python code for linear regression and explain", None),
        ("Compare Convolutional Neural Networks (CNN) and Recurrent Neural Networks (RNN) in a table, including their architecture, data type handled, strengths, weaknesses, and common applications.", None)
        ]

    for prompt, ctx in tests:
        print("=" * 60)
        print("ORIGINAL PROMPT:", prompt)
        print("=" * 60)
        result = optimize_prompt(prompt, ctx)
        print("\n----- GEMINI FINAL ANSWER -----")
        print(result)
        print("\n" + "=" * 60 + "\n")


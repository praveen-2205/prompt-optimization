"""
Optimizer Pipeline Module

The main prompt optimization pipeline that runs all analysis modules.
All detection is LLM-powered with no hardcoded rules.

The optimizer ALWAYS outputs an optimized prompt - it never rejects prompts.
When prompts are ambiguous or low quality, it uses LLM to improve them.
"""

import time

try:
    from pipeline.intent_handler import detect_intents_full, detect_intents
    from pipeline.scoring_engine import score_prompt
    from pipeline.ambiguity_detector import detect_ambiguity, is_ambiguous
    from pipeline.decomposition_engine import decompose_prompt_full, decompose_prompt
    from pipeline.context_handler import detect_context_need, needs_context
    from pipeline.llm_interface import llm_rewrite_prompt, generate_final_answer
except ImportError:
    from intent_handler import detect_intents_full, detect_intents
    from scoring_engine import score_prompt
    from ambiguity_detector import detect_ambiguity, is_ambiguous
    from decomposition_engine import decompose_prompt_full, decompose_prompt
    from context_handler import detect_context_need, needs_context
    from llm_interface import llm_rewrite_prompt, generate_final_answer


def optimize_prompt(raw_prompt: str, previous_context: str = None) -> str:
    """
    Optimize a raw user prompt using LLM analysis.
    ALWAYS outputs an optimized prompt - never rejects prompts.
    
    Args:
        raw_prompt: The original user input prompt.
        previous_context: Optional context from previous interactions.
        
    Returns:
        An optimized prompt with improved clarity and structure.
    """
    start_time = time.time()
    
    print("[LLM Analysis Starting...]")
    
    # STEP 1 — Score the prompt
    print("  [1/5] Scoring prompt...")
    score_result = score_prompt(raw_prompt)
    print(f"       Score: {score_result}")
    
    # STEP 2 — Check ambiguity
    print("  [2/5] Checking ambiguity...")
    ambiguity_result = detect_ambiguity(raw_prompt)
    print(f"       Ambiguity: {ambiguity_result}")
    
    # STEP 3 — Check context needs
    print("  [3/5] Checking context needs...")
    context_result = detect_context_need(raw_prompt)
    print(f"       Context: {context_result}")
    
    # STEP 4 — Detect intents
    print("  [4/5] Detecting intents...")
    intent_result = detect_intents_full(raw_prompt)
    print(f"       Intent: {intent_result}")
    
    # STEP 5 — Decompose into subtasks
    print("  [5/5] Decomposing prompt...")
    decomposition_result = decompose_prompt_full(raw_prompt)
    print(f"       Decomposition: {decomposition_result}")
    
    analysis_time = time.time() - start_time
    print(f"[LLM Analysis Complete in {analysis_time:.2f}s]")
    
    # STEP 6 — Attach context if needed
    working_prompt = raw_prompt
    if previous_context and context_result.get("needs_context", False):
        working_prompt = f"Considering the previous context: {previous_context}. Now perform: {raw_prompt}"
    
    # STEP 7 — LLM rewrite if prompt is ambiguous OR low quality score
    # ALWAYS optimize, never reject!
    total_score = score_result.get("total_score", 0)
    is_ambiguous = ambiguity_result.get("is_ambiguous", False)
    
    llm_triggered = False
    if total_score < 10 or is_ambiguous:
        print("[LLM Rewrite Triggered - Improving prompt clarity]")
        llm_triggered = True
        working_prompt = llm_rewrite_prompt(working_prompt)
    
    # STEP 8 — Run intent detection on EACH subtask for specific instructions
    subtasks = decomposition_result.get("subtasks", [working_prompt])
    
    print("[Generating subtask-specific instructions...]")
    subtask_instructions = []
    for i, subtask in enumerate(subtasks, 1):
        print(f"  [Subtask {i}/{len(subtasks)}] Detecting intent for: {subtask[:50]}...")
        subtask_intent = detect_intents_full(subtask)
        subtask_instructions.append({
            "subtask": subtask,
            "primary_intent": subtask_intent.get("primary_intent", "general"),
            "instructions": subtask_intent.get("instructions", ["Provide a clear response."])
        })
    
    # Format output with subtask-instruction mapping
    optimized_output = ""
    
    if llm_triggered:
        optimized_output += "[LLM Rewrite Triggered]\n\n"
    
    # Add subtasks with their specific instructions
    for i, item in enumerate(subtask_instructions, 1):
        optimized_output += f"## Sub-Task {i}: {item['subtask']}\n"
        optimized_output += f"   Intent: {item['primary_intent']}\n"
        optimized_output += "   Instructions:\n"
        for inst in item["instructions"]:
            optimized_output += f"   - {inst}\n"
        optimized_output += "\n"
    
    # Add score info
    optimized_output += f"[Quality Score: {total_score}/15]"
    
    # Debug output
    print("----- OPTIMIZED PROMPT -----")
    print(optimized_output)
    print("-" * 40)
    
    return optimized_output


if __name__ == "__main__":
    tests = [
        ("Explain CNN and compare with RNN", None),
        ("Explain the model", None),
    ]

    for prompt, ctx in tests:
        print("=" * 60)
        print("ORIGINAL PROMPT:", prompt)
        print("=" * 60)
        result = optimize_prompt(prompt, ctx)
        print("\n----- RESULT -----")
        print(result)
        print("\n" + "=" * 60 + "\n")

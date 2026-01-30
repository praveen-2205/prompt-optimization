"""
Decomposition Engine Module

Breaks complex prompts into multiple actionable sub-tasks using LLM analysis.
All decomposition is LLM-powered with no hardcoded rules.
"""

try:
    from pipeline.llm_interface import call_gemini_json, call_gemini_json_async
except ImportError:
    from llm_interface import call_gemini_json, call_gemini_json_async


DECOMPOSITION_PROMPT = '''Break down the following user prompt into actionable sub-tasks.

Rules:
- Only split if there are genuinely distinct tasks
- Keep comparison tasks together (e.g., "compare X and Y" is ONE task, not two)
- Each subtask should be self-contained and actionable
- If the prompt is simple, return it as a single subtask
- Order subtasks logically (dependencies first)

User Prompt: "{prompt}"

Respond in JSON format:
{{
    "subtasks": ["subtask 1", "subtask 2", ...],
    "reasoning": "brief explanation of how you decomposed it"
}}'''


def decompose_prompt(prompt: str) -> list:
    """
    Breaks complex prompts into sub-tasks using LLM.
    
    Args:
        prompt: The user's input prompt.
        
    Returns:
        A list of sub-tasks extracted from the prompt.
    """
    result = decompose_prompt_full(prompt)
    return result.get("subtasks", [prompt])


def decompose_prompt_full(prompt: str) -> dict:
    """
    Full decomposition with detailed analysis.
    
    Args:
        prompt: The user's input prompt.
        
    Returns:
        Dictionary with subtasks and reasoning.
    """
    formatted_prompt = DECOMPOSITION_PROMPT.format(prompt=prompt)
    return call_gemini_json(formatted_prompt)


async def decompose_prompt_async(prompt: str) -> dict:
    """
    Async version of decomposition for parallel processing.
    
    Args:
        prompt: The user's input prompt.
        
    Returns:
        Dictionary with subtasks and reasoning.
    """
    formatted_prompt = DECOMPOSITION_PROMPT.format(prompt=prompt)
    return await call_gemini_json_async(formatted_prompt)


if __name__ == "__main__":
    import asyncio
    
    tests = [
        "Explain CNN and compare with RNN",
        "Summarize this article, then analyze key ideas, and write code to implement it",
        "Write code and explain the logic",
        "Describe neural networks",
        "Compare Python and JavaScript, then create a sample project in both"
    ]
    
    async def run_tests():
        for t in tests:
            result = await decompose_prompt_async(t)
            print(f"'{t}' → {result}")
    
    asyncio.run(run_tests())

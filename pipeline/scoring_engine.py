"""
Scoring Engine Module

Scores prompts to evaluate quality using LLM analysis.
All scoring is LLM-powered with no hardcoded rules.
"""

try:
    from pipeline.llm_interface import call_gemini_json, call_gemini_json_async
except ImportError:
    from llm_interface import call_gemini_json, call_gemini_json_async


SCORING_PROMPT = '''Evaluate the quality of the following user prompt on a scale.

Scoring criteria (0-5 each):
- Clarity: How clear and understandable is the request?
- Specificity: How specific and detailed is the prompt?
- Structure: How well-organized and formatted is the prompt?

User Prompt: "{prompt}"

Respond in JSON format:
{{
    "clarity": 0-5,
    "specificity": 0-5,
    "structure": 0-5,
    "total_score": sum of above (0-15),
    "feedback": "brief feedback on how to improve the prompt"
}}'''


def score_prompt(prompt: str) -> dict:
    """
    Score a prompt based on clarity, specificity, and structure using LLM.
    
    Args:
        prompt: The user prompt to evaluate.
        
    Returns:
        A dictionary containing individual scores and total score.
    """
    formatted_prompt = SCORING_PROMPT.format(prompt=prompt)
    return call_gemini_json(formatted_prompt)


async def score_prompt_async(prompt: str) -> dict:
    """
    Async version of prompt scoring for parallel processing.
    
    Args:
        prompt: The user prompt to evaluate.
        
    Returns:
        A dictionary containing individual scores and total score.
    """
    formatted_prompt = SCORING_PROMPT.format(prompt=prompt)
    return await call_gemini_json_async(formatted_prompt)


if __name__ == "__main__":
    import asyncio
    
    tests = [
        "tell me something",
        "Explain neural network architecture with example",
        "Compare CNN and RNN in table format",
        "Write python code",
        "Create a comprehensive Python tutorial covering data types, control flow, functions, and OOP with examples"
    ]
    
    async def run_tests():
        for t in tests:
            result = await score_prompt_async(t)
            print(f"'{t}'")
            print(f"  Clarity: {result.get('clarity', 'N/A')}")
            print(f"  Specificity: {result.get('specificity', 'N/A')}")
            print(f"  Structure: {result.get('structure', 'N/A')}")
            print(f"  Total: {result.get('total_score', 'N/A')}")
            print(f"  Feedback: {result.get('feedback', 'N/A')}")
            print()
    
    asyncio.run(run_tests())

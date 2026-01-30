"""
Ambiguity Detector Module

Detects whether a prompt is semantically ambiguous using LLM analysis.
All detection is LLM-powered with no hardcoded rules.
"""

try:
    from pipeline.llm_interface import call_gemini_json, call_gemini_json_async
except ImportError:
    from llm_interface import call_gemini_json, call_gemini_json_async


AMBIGUITY_PROMPT = '''Analyze if the following user prompt is ambiguous or too vague.

A prompt is ambiguous if:
- It lacks specific domain context (e.g., "explain models" without specifying what kind)
- It uses vague terms without clarification
- It could have multiple very different interpretations
- It's too short to understand the user's actual intent

User Prompt: "{prompt}"

Respond in JSON format:
{{
    "is_ambiguous": true/false,
    "reason": "brief explanation of why it is or isn't ambiguous",
    "clarification_needed": "what clarification would help (empty string if not ambiguous)"
}}'''


def is_ambiguous(prompt: str) -> bool:
    """
    Detects whether a prompt is semantically ambiguous using LLM.
    
    Args:
        prompt: The user's input prompt.
        
    Returns:
        True if the prompt is ambiguous, False otherwise.
    """
    result = detect_ambiguity(prompt)
    return result.get("is_ambiguous", False)


def detect_ambiguity(prompt: str) -> dict:
    """
    Full ambiguity detection with detailed analysis.
    
    Args:
        prompt: The user's input prompt.
        
    Returns:
        Dictionary with is_ambiguous, reason, and clarification_needed.
    """
    formatted_prompt = AMBIGUITY_PROMPT.format(prompt=prompt)
    return call_gemini_json(formatted_prompt)


async def detect_ambiguity_async(prompt: str) -> dict:
    """
    Async version of ambiguity detection for parallel processing.
    
    Args:
        prompt: The user's input prompt.
        
    Returns:
        Dictionary with is_ambiguous, reason, and clarification_needed.
    """
    formatted_prompt = AMBIGUITY_PROMPT.format(prompt=prompt)
    return await call_gemini_json_async(formatted_prompt)


if __name__ == "__main__":
    import asyncio
    
    tests = [
        "Explain models",
        "Explain machine learning classification models with examples",
        "Tell me about data",
        "Tell me about Python data structures like lists and dictionaries",
        "Compare systems"
    ]
    
    async def run_tests():
        for t in tests:
            result = await detect_ambiguity_async(t)
            print(f"'{t}' → {result}")
    
    asyncio.run(run_tests())

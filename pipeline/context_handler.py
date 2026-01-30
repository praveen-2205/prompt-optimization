"""
Context Handler Module

Detects whether a prompt requires previous conversation context using LLM analysis.
All detection is LLM-powered with no hardcoded rules.
"""

try:
    from pipeline.llm_interface import call_gemini_json, call_gemini_json_async
except ImportError:
    from llm_interface import call_gemini_json, call_gemini_json_async


CONTEXT_PROMPT = '''Analyze if the following user prompt requires previous conversation context to be understood.

A prompt needs context if:
- It uses pronouns referring to something not mentioned (it, this, that, them)
- It references "previous", "above", "earlier", "the last one"
- It's a continuation command (continue, add more, modify, update, fix it)
- It would be incomplete without knowing what came before

User Prompt: "{prompt}"

Respond in JSON format:
{{
    "needs_context": true/false,
    "reason": "brief explanation"
}}'''


def needs_context(prompt: str) -> bool:
    """
    Detects if the prompt needs previous context using LLM.
    
    Args:
        prompt: The user's input prompt.
        
    Returns:
        True if previous context is needed, False otherwise.
    """
    result = detect_context_need(prompt)
    return result.get("needs_context", False)


def detect_context_need(prompt: str) -> dict:
    """
    Full context need detection with detailed analysis.
    
    Args:
        prompt: The user's input prompt.
        
    Returns:
        Dictionary with needs_context and reason.
    """
    formatted_prompt = CONTEXT_PROMPT.format(prompt=prompt)
    return call_gemini_json(formatted_prompt)


async def detect_context_need_async(prompt: str) -> dict:
    """
    Async version of context need detection for parallel processing.
    
    Args:
        prompt: The user's input prompt.
        
    Returns:
        Dictionary with needs_context and reason.
    """
    formatted_prompt = CONTEXT_PROMPT.format(prompt=prompt)
    return await call_gemini_json_async(formatted_prompt)


if __name__ == "__main__":
    import asyncio
    
    tests = [
        "Explain neural networks",
        "Now modify it to use batch normalization",
        "Continue from where we left off",
        "Add more examples to the previous code",
        "What is machine learning?"
    ]
    
    async def run_tests():
        for t in tests:
            result = await detect_context_need_async(t)
            print(f"'{t}' → {result}")
    
    asyncio.run(run_tests())
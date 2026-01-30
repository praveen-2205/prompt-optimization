"""
Intent Handler Module

Detects user intents and generates appropriate instructions using LLM analysis.
All intent detection is LLM-powered with no hardcoded keyword lists.
"""

try:
    from pipeline.llm_interface import call_gemini_json, call_gemini_json_async
except ImportError:
    from llm_interface import call_gemini_json, call_gemini_json_async


INTENT_PROMPT = '''Analyze the following user prompt to detect intents and generate instructions.

Possible intent categories:
- explanation: User wants something explained or described
- comparison: User wants items compared or contrasted
- coding: User wants code written or programming help
- analysis: User wants analytical evaluation with pros/cons
- creative: User wants creative content (stories, poems, etc.)
- tutorial: User wants step-by-step guidance
- summarization: User wants content summarized
- research: User wants information gathered
- problem_solving: User wants help solving a problem
- question: User is asking a question
- instruction: User wants something created or modified

User Prompt: "{prompt}"

Respond in JSON format:
{{
    "intents": ["intent1", "intent2", ...],
    "primary_intent": "the most important intent",
    "instructions": ["specific instruction 1 for optimal response", "instruction 2", ...]
}}

The instructions should tell an AI how to best respond to this prompt.'''


def detect_intent(prompt: str) -> str:
    """
    Detect the primary intent of a user prompt.
    
    Args:
        prompt: The user input prompt to classify.
        
    Returns:
        A string representing the detected primary intent.
    """
    result = detect_intents_full(prompt)
    return result.get("primary_intent", "general")


def detect_intents(prompt: str) -> list:
    """
    Detect all intents for a user prompt.
    
    Args:
        prompt: The user input prompt to classify.
        
    Returns:
        A list of detected intent categories.
    """
    result = detect_intents_full(prompt)
    return result.get("intents", ["general"])


def detect_intents_full(prompt: str) -> dict:
    """
    Full intent detection with instructions.
    
    Args:
        prompt: The user input prompt to classify.
        
    Returns:
        Dictionary with intents, primary_intent, and instructions.
    """
    formatted_prompt = INTENT_PROMPT.format(prompt=prompt)
    return call_gemini_json(formatted_prompt)


async def detect_intents_async(prompt: str) -> dict:
    """
    Async version of intent detection for parallel processing.
    
    Args:
        prompt: The user input prompt to classify.
        
    Returns:
        Dictionary with intents, primary_intent, and instructions.
    """
    formatted_prompt = INTENT_PROMPT.format(prompt=prompt)
    return await call_gemini_json_async(formatted_prompt)


if __name__ == "__main__":
    import asyncio
    
    tests = [
        "Explain CNN",
        "Difference between CNN vs RNN and analyze performance",
        "Summarize this article and explain key ideas",
        "Write a story and describe the main character",
        "Write python code for linear regression and explain how it works"
    ]
    
    async def run_tests():
        for t in tests:
            result = await detect_intents_async(t)
            print(f"'{t}' →")
            print(f"  Intents: {result.get('intents', [])}")
            print(f"  Primary: {result.get('primary_intent', 'N/A')}")
            print(f"  Instructions: {result.get('instructions', [])}")
            print()
    
    asyncio.run(run_tests())

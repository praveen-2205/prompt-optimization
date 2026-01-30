"""
LLM Interface Module

This module provides an interface to call the Gemini LLM API
for semantic prompt analysis and understanding.
Supports both sync and async operations for parallel processing.
"""

import os
import json
import asyncio
import time
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Global model instance for reuse
_model = None

# Semaphore to limit concurrent API requests (prevent rate limiting)
MAX_CONCURRENT_REQUESTS = 3
_semaphore = None


def _get_semaphore():
    """Get or create the async semaphore for rate limiting."""
    global _semaphore
    if _semaphore is None:
        _semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    return _semaphore


def _get_model():
    """Get or create the Gemini model instance."""
    global _model
    if _model is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set in environment variables.")
        genai.configure(api_key=api_key)
        _model = genai.GenerativeModel("gemini-2.0-flash")
    return _model


def call_gemini(prompt: str, max_retries: int = 3) -> str:
    """
    Call the Gemini LLM with the given prompt (synchronous).
    Includes retry logic with exponential backoff for rate limiting.
    
    Args:
        prompt: The prompt to send to the LLM.
        max_retries: Maximum number of retry attempts.
        
    Returns:
        The text response from the LLM.
    """
    model = _get_model()
    
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                wait_time = (2 ** attempt) + 1  # Exponential backoff: 2, 3, 5 seconds
                print(f"[Rate limit hit, waiting {wait_time}s before retry {attempt + 1}/{max_retries}]")
                time.sleep(wait_time)
            else:
                raise e
    
    # Final attempt without catch
    response = model.generate_content(prompt)
    return response.text


async def call_gemini_async(prompt: str) -> str:
    """
    Call the Gemini LLM with the given prompt (asynchronous).
    Uses asyncio to run the sync call in a thread pool for parallelism.
    Uses semaphore to limit concurrent requests and prevent rate limiting.
    
    Args:
        prompt: The prompt to send to the LLM.
        
    Returns:
        The text response from the LLM.
    """
    semaphore = _get_semaphore()
    async with semaphore:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, call_gemini, prompt)


def call_gemini_json(prompt: str) -> dict:
    """
    Call Gemini and parse the response as JSON.
    
    Args:
        prompt: The prompt to send to the LLM (should request JSON output).
        
    Returns:
        Parsed JSON response as a dictionary.
    """
    response = call_gemini(prompt)
    # Clean response - remove markdown code blocks if present
    cleaned = response.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    if cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    return json.loads(cleaned.strip())


async def call_gemini_json_async(prompt: str) -> dict:
    """
    Call Gemini asynchronously and parse the response as JSON.
    
    Args:
        prompt: The prompt to send to the LLM (should request JSON output).
        
    Returns:
        Parsed JSON response as a dictionary.
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, call_gemini_json, prompt)


def llm_rewrite_prompt(raw_prompt: str) -> str:
    """
    Rewrite the prompt using LLM for better semantic understanding.
    
    Args:
        raw_prompt: The original user input prompt.
        
    Returns:
        A semantically rewritten prompt.
    """
    rewrite_instruction = (
        "Rewrite the following user request into ONE clear, concise sentence "
        "that preserves the original tasks and does NOT add extra explanation, examples, or structure. "
        "Do NOT expand the request. Do NOT split into multiple parts. "
        "Output only the improved single-sentence request:\n\n"
        + raw_prompt
    )
    return call_gemini(rewrite_instruction)


def generate_final_answer(prompt: str) -> str:
    """
    Uses Gemini to generate the final response for the optimized prompt.
    
    Args:
        prompt: The optimized prompt to send to the LLM.
        
    Returns:
        The final answer from the LLM.
    """
    return call_gemini(prompt)


if __name__ == "__main__":
    test_prompt = "Explain neural networks simply."
    print("Sync call:", call_gemini(test_prompt)[:100], "...")
    
    # Test async
    async def test_async():
        result = await call_gemini_async(test_prompt)
        print("Async call:", result[:100], "...")
    
    asyncio.run(test_async())

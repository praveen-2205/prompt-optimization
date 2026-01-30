"""
LLM Interface Module

This module provides an interface to call the Gemini LLM API
for semantic prompt rewriting and understanding.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()


def configure_gemini():
    """
    Configure the Gemini API with the API key from environment variables.
    
    Raises:
        ValueError: If GEMINI_API_KEY is not set in environment variables.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set in environment variables.")
    genai.configure(api_key=api_key)


def call_gemini(prompt: str) -> str:
    """
    Call the Gemini LLM with the given prompt.
    
    Args:
        prompt: The prompt to send to the LLM.
        
    Returns:
        The text response from the LLM.
    """
    configure_gemini()
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text


def generate_final_answer(prompt: str) -> str:
    """
    Uses Gemini to generate the final response for the optimized prompt.
    
    Args:
        prompt: The optimized prompt to send to the LLM.
        
    Returns:
        The final answer from the LLM.
    """
    configure_gemini()
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text


if __name__ == "__main__":
    test_prompt = "Explain neural networks simply."
    print(call_gemini(test_prompt))


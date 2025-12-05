"""Ollama inference engine - automatic GPU acceleration."""
import logging
from typing import AsyncGenerator
import httpx

logger = logging.getLogger(__name__)

OLLAMA_BASE_URL = "http://localhost:11434"


async def check_ollama_available() -> bool:
    """Check if Ollama is running and available."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
            return response.status_code == 200
    except Exception as e:
        logger.debug(f"Ollama not available: {e}")
        return False


async def list_ollama_models() -> list[dict]:
    """List all available Ollama models."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
            if response.status_code == 200:
                data = response.json()
                return data.get("models", [])
    except Exception as e:
        logger.error(f"Failed to list Ollama models: {e}")
    return []


async def generate_streaming_ollama(
    model_name: str,
    messages: list[dict[str, str]],
    temperature: float = 0.7,
    max_tokens: int = 512,
    top_p: float = 0.9,
) -> AsyncGenerator[str, None]:
    """
    Generate streaming chat completions using Ollama.
    
    Args:
        model_name: Ollama model name (e.g., "llama3.1:8b")
        messages: Chat messages in OpenAI format
        temperature: Sampling temperature
        max_tokens: Maximum tokens to generate
        top_p: Nucleus sampling parameter
    
    Yields:
        Generated text tokens
    """
    logger.info(f"Generating response with Ollama model: {model_name}")
    
    payload = {
        "model": model_name,
        "messages": messages,
        "stream": True,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
            "top_p": top_p,
        }
    }
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream(
                "POST",
                f"{OLLAMA_BASE_URL}/api/chat",
                json=payload,
            ) as response:
                if response.status_code != 200:
                    error_text = await response.aread()
                    logger.error(f"Ollama error: {error_text}")
                    raise RuntimeError(f"Ollama request failed: {response.status_code}")
                
                async for line in response.aiter_lines():
                    if line.strip():
                        try:
                            import json
                            chunk = json.loads(line)
                            
                            # Check if this is the final message
                            if chunk.get("done", False):
                                logger.info(f"Ollama generation complete")
                                break
                            
                            # Extract content from message
                            message = chunk.get("message", {})
                            content = message.get("content", "")
                            
                            if content:
                                yield content
                                
                        except json.JSONDecodeError as e:
                            logger.error(f"Failed to parse Ollama response: {e}")
                            continue
                            
    except httpx.TimeoutException:
        logger.error("Ollama request timed out")
        raise RuntimeError("Ollama request timed out")
    except Exception as e:
        logger.error(f"Ollama generation error: {e}")
        raise

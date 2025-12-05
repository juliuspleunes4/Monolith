"""LLM inference placeholder - requires llama-cpp-python installation."""
import os
from pathlib import Path
from typing import Optional, AsyncGenerator
import logging
import asyncio

logger = logging.getLogger(__name__)

# Get models directory
MODELS_DIR = Path(os.getenv("MODELS_DIR", "../models"))

# Cache loaded models (placeholder: dict instead of Llama objects)
_loaded_models: dict[str, dict] = {}


def get_model_path(model_id: str) -> Path:
    """Get the full path to a model file."""
    return MODELS_DIR / model_id


def load_model(model_id: str, n_ctx: int = 2048, n_gpu_layers: int = 0) -> dict:
    """
    Placeholder for model loading.
    TODO: Install llama-cpp-python with Visual Studio C++ Build Tools to enable actual inference.
    
    Args:
        model_id: Model ID in format "category/filename.gguf"
        n_ctx: Context window size
        n_gpu_layers: Number of layers to offload to GPU (0 for CPU only)
    
    Returns:
        Placeholder model dict
    """
    if model_id in _loaded_models:
        logger.info(f"Model {model_id} already loaded (placeholder)")
        return _loaded_models[model_id]
    
    model_path = get_model_path(model_id)
    
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    
    logger.warning(f"Using placeholder for model {model_id} - llama-cpp-python not installed")
    logger.info(f"Model file exists at: {model_path}")
    
    # Store placeholder
    _loaded_models[model_id] = {"id": model_id, "path": str(model_path)}
    return _loaded_models[model_id]


def unload_model(model_id: str) -> bool:
    """
    Unload a model from memory.
    
    Args:
        model_id: Model ID to unload
    
    Returns:
        True if model was unloaded, False if it wasn't loaded
    """
    if model_id in _loaded_models:
        del _loaded_models[model_id]
        logger.info(f"Unloaded model {model_id}")
        return True
    return False


async def generate_streaming(
    model_id: str,
    messages: list[dict[str, str]],
    temperature: float = 0.7,
    max_tokens: int = 512,
    top_p: float = 0.9,
) -> AsyncGenerator[str, None]:
    """
    Generate streaming chat completions (placeholder implementation).
    TODO: Install llama-cpp-python to enable actual LLM inference.
    
    Args:
        model_id: Model ID to use
        messages: Chat messages in format [{"role": "user", "content": "..."}]
        temperature: Sampling temperature (0-2)
        max_tokens: Maximum tokens to generate
        top_p: Nucleus sampling parameter
    
    Yields:
        Generated tokens as they're produced
    """
    try:
        # Load model (placeholder)
        model = load_model(model_id)
        
        # Create prompt from messages
        prompt = format_chat_prompt(messages)
        
        logger.warning(f"Using placeholder response - llama-cpp-python not installed")
        logger.info(f"Would generate response for model {model_id}")
        logger.debug(f"Prompt: {prompt[:100]}...")
        
        # Placeholder response with streaming simulation
        user_message = messages[-1].get('content', '') if messages else ''
        placeholder_response = f"I'm a placeholder response from {model_id}. To enable actual LLM inference, please install llama-cpp-python with Visual Studio C++ Build Tools. Your message was: {user_message}"
        
        # Simulate streaming by yielding word by word
        words = placeholder_response.split()
        for word in words:
            yield word + " "
            await asyncio.sleep(0.05)  # Simulate generation delay
                    
    except Exception as e:
        logger.error(f"Error during generation: {e}")
        raise


def format_chat_prompt(messages: list[dict[str, str]]) -> str:
    """
    Format chat messages into a single prompt string.
    
    Args:
        messages: List of message dicts with 'role' and 'content'
    
    Returns:
        Formatted prompt string
    """
    prompt_parts = []
    
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        
        if role == "system":
            prompt_parts.append(f"System: {content}\n\n")
        elif role == "user":
            prompt_parts.append(f"User: {content}\n\n")
        elif role == "assistant":
            prompt_parts.append(f"Assistant: {content}\n\n")
    
    # Add final Assistant: prefix for generation
    prompt_parts.append("Assistant: ")
    
    return "".join(prompt_parts)


def get_loaded_models() -> list[str]:
    """Get list of currently loaded model IDs."""
    return list(_loaded_models.keys())

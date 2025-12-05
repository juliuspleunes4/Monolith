"""LLM inference with llama-cpp-python - GPU with CPU fallback."""
import os
from pathlib import Path
from typing import AsyncGenerator
import logging
import asyncio

try:
    from llama_cpp import Llama
    LLAMA_CPP_AVAILABLE = True
    
    # Try to detect CUDA availability
    try:
        import llama_cpp
        if hasattr(llama_cpp, '__version__'):
            logger_init = logging.getLogger(__name__)
            logger_init.info(f"llama-cpp-python version: {llama_cpp.__version__}")
    except Exception as e:
        pass
        
except ImportError:
    LLAMA_CPP_AVAILABLE = False

logger = logging.getLogger(__name__)

# Get models directory
MODELS_DIR = Path(os.getenv("MODELS_DIR", "../models"))

# Cache loaded models
_loaded_models: dict[str, "Llama"] = {}


def get_model_path(model_id: str) -> Path:
    """Get the full path to a model file."""
    return MODELS_DIR / model_id


def load_model(model_id: str, n_ctx: int = 4096, n_gpu_layers: int = -1) -> "Llama":
    """
    Load a GGUF model with GPU acceleration (fallback to CPU if GPU unavailable).
    
    Args:
        model_id: Model ID in format "category/filename.gguf"
        n_ctx: Context window size (default 4096)
        n_gpu_layers: Number of layers to offload to GPU (-1 = all layers, 0 = CPU only)
    
    Returns:
        Loaded Llama model instance
    """
    if not LLAMA_CPP_AVAILABLE:
        raise RuntimeError("llama-cpp-python is not installed. Cannot load model.")
    
    if model_id in _loaded_models:
        logger.info(f"Model {model_id} already loaded")
        return _loaded_models[model_id]
    
    model_path = get_model_path(model_id)
    
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    
    logger.info(f"Loading model {model_id} from {model_path}")
    logger.info(f"Context size: {n_ctx}, GPU layers: {n_gpu_layers}")
    
    try:
        # Try loading with GPU support first (n_gpu_layers=-1 uses all available GPU)
        model = Llama(
            model_path=str(model_path),
            n_ctx=n_ctx,
            n_gpu_layers=n_gpu_layers,
            verbose=True,  # Show GPU info in logs
        )
        logger.info(f"Model {model_id} loaded successfully with GPU layers: {n_gpu_layers}")
    except Exception as gpu_error:
        logger.warning(f"Failed to load model with GPU: {gpu_error}")
        logger.info(f"Falling back to CPU-only mode")
        try:
            # Fallback to CPU only
            model = Llama(
                model_path=str(model_path),
                n_ctx=n_ctx,
                n_gpu_layers=0,  # CPU only
                verbose=True,
            )
            logger.info(f"Model {model_id} loaded successfully on CPU")
        except Exception as cpu_error:
            logger.error(f"Failed to load model on CPU: {cpu_error}")
            raise
    
    _loaded_models[model_id] = model
    return model


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
    Generate streaming chat completions using llama-cpp-python.
    
    Args:
        model_id: Model ID to use
        messages: Chat messages in format [{"role": "user", "content": "..."}]
        temperature: Sampling temperature (0-2)
        max_tokens: Maximum tokens to generate
        top_p: Nucleus sampling parameter
    
    Yields:
        Generated tokens as they're produced
    """
    if not LLAMA_CPP_AVAILABLE:
        error_msg = "llama-cpp-python is not installed. Cannot generate responses."
        logger.error(error_msg)
        yield error_msg
        return
    
    try:
        # Load model (with GPU support, fallback to CPU)
        model = load_model(model_id)
        
        logger.info(f"Generating response for model {model_id}")
        logger.debug(f"Temperature: {temperature}, Max tokens: {max_tokens}, Top-p: {top_p}")
        
        # Use create_chat_completion which handles the chat template automatically
        stream = model.create_chat_completion(
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            stream=True,
        )
        
        # Yield tokens as they're generated
        for output in stream:
            if "choices" in output and len(output["choices"]) > 0:
                choice = output["choices"][0]
                # For chat completion, use 'delta' -> 'content'
                if "delta" in choice and "content" in choice["delta"]:
                    token = choice["delta"]["content"]
                    yield token
                    await asyncio.sleep(0)  # Allow other coroutines to run
                    
    except Exception as e:
        logger.error(f"Error during generation: {e}")
        error_msg = f"Error: {str(e)}"
        yield error_msg
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

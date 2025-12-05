"""Models router for managing LLM models."""
from fastapi import APIRouter
from pathlib import Path
import os
from app.llm.ollama_inference import list_ollama_models, check_ollama_available

router = APIRouter()

# Get models directory from environment or use default
# Backend runs from backend/ folder, so go up one level to find models/
MODELS_DIR = Path(os.getenv("MODELS_DIR", "../models"))


def scan_models():
    """Scan the models directory for .gguf files organized by size category."""
    models = []
    categories = ["small", "medium", "large"]
    
    for category in categories:
        category_path = MODELS_DIR / category
        if not category_path.exists():
            continue
            
        # Find all .gguf files in this category
        for model_file in category_path.glob("*.gguf"):
            file_size = model_file.stat().st_size
            models.append({
                "id": f"{category}/{model_file.name}",
                "name": model_file.stem,  # filename without extension
                "category": category,
                "filename": model_file.name,
                "size": file_size,
                "size_mb": round(file_size / (1024 * 1024), 2),
                "path": str(model_file),
                "backend": "llama-cpp",
                "loaded": False
            })
    
    return models


async def scan_ollama_models():
    """Scan Ollama for available models."""
    models = []
    
    if not await check_ollama_available():
        return models
    
    ollama_models = await list_ollama_models()
    
    for model in ollama_models:
        model_name = model.get("name", "")
        size_bytes = model.get("size", 0)
        
        models.append({
            "id": f"ollama:{model_name}",
            "name": model_name,
            "category": "ollama",
            "filename": model_name,
            "size": size_bytes,
            "size_mb": round(size_bytes / (1024 * 1024), 2),
            "backend": "ollama",
            "loaded": True  # Ollama models are always "loaded"
        })
    
    return models


@router.get("/models")
async def list_models():
    """
    List all available LLM models from both local .gguf files and Ollama.
    """
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        # Get local .gguf models
        local_models = scan_models()
        logger.info(f"Found {len(local_models)} local .gguf models")
        
        # Get Ollama models
        ollama_models = await scan_ollama_models()
        logger.info(f"Found {len(ollama_models)} Ollama models")
        
        # Combine both
        all_models = local_models + ollama_models
        logger.info(f"Returning {len(all_models)} total models")
        
        return {"models": all_models}
    except Exception as e:
        logger.error(f"Error listing models: {e}", exc_info=True)
        return {"models": [], "error": str(e)}


@router.post("/models/{model_id}/load")
async def load_model(model_id: str):
    """
    Load a specific model into memory.
    
    TODO: Implement model loading with:
    - Validate model_id exists
    - Load model using LLM engine
    - Return loading status
    - Handle errors (OOM, invalid model)
    """
    return {"error": {"code": "NOT_IMPLEMENTED", "message": "Model loading not yet implemented"}}


@router.post("/models/{model_id}/unload")
async def unload_model(model_id: str):
    """
    Unload a model from memory.
    
    TODO: Implement model unloading with:
    - Validate model_id is loaded
    - Free model memory
    - Return status
    """
    return {"error": {"code": "NOT_IMPLEMENTED", "message": "Model unloading not yet implemented"}}

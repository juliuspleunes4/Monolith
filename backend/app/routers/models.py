"""Models router for managing LLM models."""
from fastapi import APIRouter
from pathlib import Path
import os

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
                "loaded": False  # TODO: track loaded models
            })
    
    return models


@router.get("/models")
async def list_models():
    """
    List all available LLM models organized by size category.
    
    Scans models/small, models/medium, and models/large directories
    for .gguf files and returns them categorized.
    """
    try:
        models = scan_models()
        return {"models": models}
    except Exception as e:
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

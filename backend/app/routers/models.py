"""Models router for managing LLM models."""
from fastapi import APIRouter

router = APIRouter()


@router.get("/models")
async def list_models():
    """
    List all available LLM models.
    
    TODO: Implement models listing with:
    - Scan MODELS_DIR for .gguf files
    - Return model metadata (name, size, loaded status)
    - Handle missing models directory
    """
    return {"models": []}


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

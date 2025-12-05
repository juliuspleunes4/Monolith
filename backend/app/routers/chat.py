"""Chat router for handling LLM conversations."""
from fastapi import APIRouter

router = APIRouter()


@router.post("/chat")
async def chat():
    """
    Stream chat completions from an LLM model.
    
    TODO: Implement chat endpoint with:
    - Request validation (model, messages, parameters)
    - Model loading/selection
    - Token streaming via SSE
    - Error handling
    """
    return {"error": {"code": "NOT_IMPLEMENTED", "message": "Chat endpoint not yet implemented"}}

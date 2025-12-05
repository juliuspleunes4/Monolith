"""Chat router for handling LLM conversations."""
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Optional
import logging
import json
from app.llm.inference import generate_streaming
from app.llm.ollama_inference import generate_streaming_ollama, check_ollama_available

logger = logging.getLogger(__name__)

router = APIRouter()


class ChatMessage(BaseModel):
    """Chat message model."""
    role: str = Field(..., description="Message role: system, user, or assistant")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    """Chat completion request model."""
    model: str = Field(..., description="Model ID to use for generation")
    messages: list[ChatMessage] = Field(..., description="Conversation messages")
    temperature: Optional[float] = Field(0.7, ge=0, le=2, description="Sampling temperature")
    max_tokens: Optional[int] = Field(512, ge=1, le=4096, description="Maximum tokens to generate")
    top_p: Optional[float] = Field(0.9, ge=0, le=1, description="Nucleus sampling parameter")


@router.post("/chat")
async def chat(request: ChatRequest):
    """
    Stream chat completions from an LLM model using Server-Sent Events.
    
    Args:
        request: Chat request with model, messages, and generation parameters
    
    Returns:
        StreamingResponse with SSE format
    """
    logger.info(f"Chat request for model: {request.model}")
    
    # Convert Pydantic models to dicts
    messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
    
    async def event_stream():
        """Generate SSE events."""
        try:
            # Detect if this is an Ollama model
            is_ollama = request.model.startswith("ollama:")
            
            if is_ollama:
                # Extract Ollama model name (remove "ollama:" prefix)
                model_name = request.model.replace("ollama:", "")
                
                # Check if Ollama is available
                if not await check_ollama_available():
                    error_data = json.dumps({"error": "Ollama is not running. Please start Ollama."})
                    yield f"data: {error_data}\n\n"
                    return
                
                # Use Ollama inference
                async for token in generate_streaming_ollama(
                    model_name=model_name,
                    messages=messages,
                    temperature=request.temperature,
                    max_tokens=request.max_tokens,
                    top_p=request.top_p,
                ):
                    data = json.dumps({"token": token})
                    logger.debug(f"Yielding token: {token}")
                    yield f"data: {data}\n\n"
            else:
                # Use llama-cpp-python inference
                async for token in generate_streaming(
                    model_id=request.model,
                    messages=messages,
                    temperature=request.temperature,
                    max_tokens=request.max_tokens,
                    top_p=request.top_p,
                ):
                    data = json.dumps({"token": token})
                    yield f"data: {data}\n\n"
            
            # Send completion signal
            yield f"data: {json.dumps({'done': True})}\n\n"
            
        except FileNotFoundError as e:
            error_data = json.dumps({"error": str(e)})
            yield f"data: {error_data}\n\n"
            logger.error(f"Model not found: {e}")
        except Exception as e:
            error_data = json.dumps({"error": f"Generation failed: {str(e)}"})
            yield f"data: {error_data}\n\n"
            logger.error(f"Error during chat generation: {e}", exc_info=True)
    
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )

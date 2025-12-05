"""Conversations router for managing chat history."""
from fastapi import APIRouter

router = APIRouter()


@router.get("/conversations")
async def list_conversations():
    """
    List all saved conversations.
    
    TODO: Implement conversation listing with:
    - Query SQLite database
    - Return conversation metadata (id, title, created_at, updated_at)
    - Pagination support
    """
    return {"conversations": []}


@router.post("/conversations")
async def create_conversation():
    """
    Create a new conversation.
    
    TODO: Implement conversation creation with:
    - Generate unique ID
    - Store in database
    - Return conversation object
    """
    return {"error": {"code": "NOT_IMPLEMENTED", "message": "Conversation creation not yet implemented"}}


@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """
    Get a specific conversation with full message history.
    
    TODO: Implement conversation retrieval with:
    - Query database by ID
    - Load all messages
    - Handle not found
    """
    return {"error": {"code": "NOT_IMPLEMENTED", "message": "Conversation retrieval not yet implemented"}}


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """
    Delete a conversation.
    
    TODO: Implement conversation deletion with:
    - Validate conversation exists
    - Delete from database
    - Return success status
    """
    return {"error": {"code": "NOT_IMPLEMENTED", "message": "Conversation deletion not yet implemented"}}

# Monolith API Documentation

## Overview

Monolith provides a REST API for interacting with local LLM models. All endpoints are versioned under `/api/v1/`.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

No authentication required - fully local operation.

## Endpoints

### Chat

#### POST /api/v1/chat
Stream chat completions from an LLM model.

**Request Body:**
```json
{
  "model": "string",
  "messages": [
    {
      "role": "user|assistant|system",
      "content": "string"
    }
  ],
  "temperature": 0.7,
  "max_tokens": 2048,
  "stream": true
}
```

**Response (SSE Stream):**
```
data: {"token": "Hello", "done": false}
data: {"token": " world", "done": false}
data: {"token": "", "done": true}
```

### Models

#### GET /api/v1/models
List all available LLM models.

**Response:**
```json
{
  "models": [
    {
      "id": "string",
      "name": "string",
      "size": "string",
      "loaded": boolean
    }
  ]
}
```

#### POST /api/v1/models/{model_id}/load
Load a specific model into memory.

#### POST /api/v1/models/{model_id}/unload
Unload a model from memory.

### Conversations

#### GET /api/v1/conversations
List all saved conversations.

#### POST /api/v1/conversations
Create a new conversation.

#### GET /api/v1/conversations/{conversation_id}
Get a specific conversation with full message history.

#### DELETE /api/v1/conversations/{conversation_id}
Delete a conversation.

## Error Responses

All errors follow this format:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {}
  }
}
```

## Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `404` - Not Found
- `500` - Internal Server Error
- `503` - Service Unavailable (model not loaded)

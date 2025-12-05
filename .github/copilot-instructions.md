# Monolith - Copilot Instructions

## Project Overview

Monolith is a fully local, Docker-based application that enables users to chat with multiple Large Language Models (LLMs) through a unified web interface. The application is designed to run entirely offline with bundled LLM models.

## Architecture

### Components
- **Backend**: Python FastAPI server handling LLM inference and API endpoints
- **Frontend**: Modern web UI (React/Vue) for chat interface
- **LLM Engine**: Integration with local inference engines (llama.cpp, Ollama, or similar)
- **Docker**: Multi-container setup with models bundled in the image

### Technology Stack
- **Backend**: Python 3.11+, FastAPI, uvicorn
- **LLM Inference**: llama.cpp or Ollama
- **Frontend**: React/TypeScript or Vue.js
- **Database**: SQLite for chat history (local persistent volume)
- **Docker**: Multi-stage builds, docker-compose for orchestration

## Project Structure
```
Monolith/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── models/              # Data models
│   │   ├── routers/             # API endpoints
│   │   ├── services/            # Business logic
│   │   └── llm/                 # LLM integration
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── Dockerfile
├── models/                       # Directory for LLM model files
├── docker-compose.yml
├── docs/
│   ├── CHANGELOG.md
│   └── API.md
└── README.md
```

## Development Guidelines

### General Principles
1. **No Mock Data**: Use clearly marked TODO placeholders instead of fake data
2. **Type Safety**: Use TypeScript for frontend, type hints for Python
3. **Error Handling**: Comprehensive error handling with meaningful messages
4. **Logging**: Structured logging for debugging and monitoring
5. **Documentation**: Document all public APIs and complex logic
6. **Security**: No external network calls, all processing local

### Backend Standards
- Use FastAPI with async/await for all endpoints
- Pydantic models for request/response validation
- Dependency injection for services
- Environment variables for configuration
- Proper HTTP status codes
- CORS configuration for frontend communication

### Frontend Standards
- Component-based architecture
- Responsive design (mobile-friendly)
- WebSocket or SSE for streaming responses
- Error boundaries and loading states
- Accessible UI (WCAG 2.1 AA)

### Design Guidelines
- **Style**: Clean and minimal aesthetic - no rainbow gradients or flashy effects
- **Inspiration**: Follow established chatbot UI patterns (ChatGPT, Claude, Grok)
- **Icons**: Use icons throughout the interface where appropriate (model selector, settings, new chat, etc.)
- **Color Scheme**: Neutral, professional palette with subtle accents
- **Typography**: Clear, readable fonts with proper hierarchy
- **Layout**: Sidebar for conversations, main chat area, clean message bubbles
- **Dark Mode**: Support both light and dark themes

### LLM Integration
- Support for multiple models simultaneously
- Streaming token generation
- Temperature, top-p, max_tokens controls
- Context window management
- Model switching without restart

### Docker Best Practices
- Multi-stage builds to minimize image size
- Health checks for all services
- Volume mounts for persistence (chat history, user config)
- Resource limits (CPU/memory)
- Non-root user execution
- Layer caching optimization

### API Design
- RESTful endpoints for CRUD operations
- WebSocket/SSE for chat streaming
- Versioned API (`/api/v1/`)
- Consistent error response format
- Rate limiting considerations

### Testing
- Unit tests for business logic
- Integration tests for API endpoints
- E2E tests for critical user flows
- Test coverage > 80%

### Git Workflow
- All changes documented in `docs/CHANGELOG.md`
- Meaningful commit messages
- Feature branches for new functionality
- No summary documents after implementations

## Key Features to Implement

1. **Chat Interface**
   - Multi-turn conversations
   - Message history
   - Code syntax highlighting
   - Markdown rendering
   - Copy/paste functionality

2. **Model Management**
   - List available models
   - Switch between models
   - Display model info (size, capabilities)
   - Model loading status

3. **Conversation Management**
   - New conversation
   - Save/load conversations
   - Delete conversations
   - Export conversations

4. **Settings**
   - Model parameters (temperature, etc.)
   - UI preferences
   - System prompts
   - Context length limits

## Configuration

### Environment Variables
- `MODELS_DIR`: Directory containing LLM models
- `DATA_DIR`: Directory for persistent data
- `LOG_LEVEL`: Logging level (INFO, DEBUG, etc.)
- `MAX_CONCURRENT_REQUESTS`: Request limit
- `FRONTEND_URL`: Frontend origin for CORS

## Performance Considerations
- Lazy loading of models
- Request queuing for concurrent chats
- Token streaming for responsive UI
- Model unloading for memory management
- Efficient context caching

## Security
- No external API calls
- Input sanitization
- SQL injection prevention (parameterized queries)
- XSS prevention in UI
- Content Security Policy headers

## Common Patterns

### Error Response Format
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {}
  }
}
```

### Streaming Response
- Use Server-Sent Events (SSE) or WebSocket
- Send tokens as they're generated
- Include metadata (model, timestamp)

## TODO Placeholder Format
Use clear, actionable TODOs:
```python
# TODO: Implement actual model loading logic
# TODO: Add authentication middleware
# TODO: Optimize prompt caching
```

## Step-by-Step Development Approach
1. Set up project structure and Docker configuration
2. Implement backend API skeleton
3. Add LLM integration layer
4. Create frontend UI components
5. Implement chat functionality
6. Add conversation persistence
7. Implement model management
8. Add settings and configuration
9. Optimize performance
10. Documentation and deployment guide

## Changelog Management
Every change must be documented in `docs/CHANGELOG.md` with:
- Date
- Category (Added, Changed, Fixed, Removed)
- Description of change

## No Summary Documents
Do not create markdown files explaining implementations. Code should be self-documenting with comments. User documentation goes in README.md only.
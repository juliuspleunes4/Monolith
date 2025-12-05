# Changelog

All notable changes to Monolith will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.0.0] - 2025-12-05

### 🎉 Initial Release

**Monolith v1.0.0** - A fully local, GPU-accelerated LLM chat application with one-command Docker deployment!

### Added

#### 🐳 Docker & Deployment
- Docker Compose orchestration with GPU support via NVIDIA Container Toolkit
- Pre-built Docker images published to Docker Hub (juliuspleunes4/monolith-backend, juliuspleunes4/monolith-frontend)
- Automatic `deepseek-r1:8b` model download on first run via ollama-init service
- GitHub Actions workflow for automated Docker image building and publishing on releases
- `docker-compose.yml` - Production deployment with pre-built images (5-10 min setup)
- `docker-compose.dev.yml` - Development deployment with live code reload
- `docker-compose.cpu.yml` - CPU-only mode for systems without GPU
- Persistent Docker volumes for chat history and Ollama models
- Health checks for all services (backend, frontend, ollama)
- Multi-platform support (linux/amd64, linux/arm64)

#### 🚀 Backend (FastAPI)
- FastAPI application with async/await for all endpoints
- Dual-backend architecture: Ollama (GPU) + llama-cpp-python (CPU fallback)
- Ollama integration with automatic GPU detection and offloading
- Real-time streaming chat completions via Server-Sent Events (SSE)
- Dynamic model discovery from Ollama and local .gguf files
- Model management endpoints (list, load, unload)
- Conversation persistence with SQLite (TODO)
- Health check endpoint (`/health`)
- CORS configuration for frontend communication
- Environment-based configuration (LOG_LEVEL, MODELS_DIR, OLLAMA_HOST)
- Multi-stage Docker build with security best practices
- Non-root user execution in containers

#### 🎨 Frontend (React + TypeScript)
- Modern React 18 with TypeScript and Vite build system
- Clean, minimal UI inspired by ChatGPT/Claude/Grok
- Real-time message streaming with typing indicators
- Model selector with categorization (Ollama ⚡, Small/Medium/Large)
- Collapsible sidebar (64px collapsed, full width on hover)
- Conversation management (new chat, history, delete)
- Empty state with "Hello, how can I help you?" greeting
- Clickable suggestion prompts for quick starts
- Dark/light theme support with CSS variables
- Message bubbles with avatars and timestamps
- Auto-resizing textarea with keyboard shortcuts (Enter to send, Shift+Enter for newline)
- Code syntax highlighting with copy button
- Markdown rendering in messages
- LocalStorage-based conversation persistence
- Responsive design optimized for desktop and mobile
- Nginx production serving with gzip compression and security headers

#### 📚 Documentation
- Comprehensive README with Docker Quick Start, manual setup, and troubleshooting
- `docs/DOCKER.md` - Complete Docker deployment guide with advanced configurations
- `docs/API.md` - REST API reference (placeholder)
- `docs/CHANGELOG.md` - Version history and release notes
- `.github/copilot-instructions.md` - Development guidelines and project architecture
- `.env.example` - Environment variable template
- Model management commands and popular model recommendations

#### 🛠️ Development Tools
- Project structure with clear separation of concerns
- TypeScript interfaces for type safety
- Python type hints throughout backend
- `.dockerignore` files for optimized image builds
- `.gitignore` for Python, Node, Docker artifacts
- Logging with configurable levels
- Error handling with meaningful messages

### Features

- **One-Command Deployment**: `docker compose up` starts everything with GPU acceleration
- **GPU-Accelerated Inference**: 20-30+ tokens/second with NVIDIA GPU support
- **Pre-installed Model**: deepseek-r1:8b (~5GB) automatically downloaded
- **Fully Offline**: No external API calls, all processing local
- **Multiple Model Support**: Easy switching between Ollama models and local .gguf files
- **Conversation Persistence**: Chat history survives container restarts
- **Production Ready**: Health checks, auto-restart, volume management included

### Technical Details

- **Backend**: Python 3.11+, FastAPI 0.115.0, uvicorn, httpx, llama-cpp-python
- **Frontend**: React 18.3.1, TypeScript 5.6.2, Vite
- **LLM Engine**: Ollama (latest) with automatic GPU detection
- **Database**: LocalStorage (frontend), SQLite planned (backend)
- **Containerization**: Docker Compose with multi-stage builds
- **CI/CD**: GitHub Actions for automated image publishing

### Performance

- **GPU Mode**: 20-30+ tokens/second with NVIDIA GPU
- **CPU Mode**: 0.5-2 tokens/second (fallback)
- **Setup Time**: 10-15 minutes first run (5-10 min with pre-built images)
- **Container Startup**: ~30 seconds after images are downloaded

### Security

- Non-root user execution in all containers
- Content Security Policy headers
- Input sanitization and validation
- No external network calls
- XSS and injection protection

## [Unreleased]

### Future Enhancements
- Backend SQLite database for conversation persistence
- Export conversations to markdown/JSON
- User-configurable system prompts
- Model performance monitoring UI
- Additional Ollama model templates
- Multi-language support

# Monolith v1.0.0 - Initial Release 🎉

**A fully local, GPU-accelerated LLM chat application with one-command Docker deployment**

> Deploy your own ChatGPT-style interface in 10 minutes. No cloud, no API keys, no tracking.

---

## 🚀 Quick Start

```bash
git clone https://github.com/juliuspleunes4/Monolith.git
cd Monolith
docker compose up
```

Open http://localhost:3000 and start chatting with `deepseek-r1:8b`!

---

## ✨ What's New in v1.0.0

### 🐳 One-Command Docker Deployment
- **Pre-built images** on Docker Hub - no build time needed!
- **Automatic model download** - `deepseek-r1:8b` (~5GB) installed on first run
- **GPU acceleration** - NVIDIA GPU support out of the box
- **5-10 minute setup** - from clone to chat in minutes

### 🚀 Performance
- **20-30+ tokens/second** with GPU acceleration
- **Real-time streaming** - see responses as they're generated
- **Dual backends** - Ollama (GPU) + llama-cpp-python (CPU fallback)

### 🎨 Modern UI
- Clean, minimal interface inspired by ChatGPT/Claude
- Collapsible sidebar with conversation history
- Dark/light theme support
- Code syntax highlighting with copy button
- Markdown rendering in messages

### 🔌 Fully Offline
- No external API calls
- All processing happens locally
- Your data never leaves your machine
- Works without internet after initial setup

---

## 📦 What's Included

### Pre-Built Docker Images
- `juliuspleunes4/monolith-backend:1.0.0` - FastAPI backend
- `juliuspleunes4/monolith-frontend:1.0.0` - React UI

### Pre-Installed Model
- `deepseek-r1:8b` - Excellent reasoning model (~5GB)

### Full Stack
- **Backend**: FastAPI + Ollama integration
- **Frontend**: React + TypeScript + Vite
- **LLM Engine**: Ollama with automatic GPU support
- **Deployment**: Docker Compose with health checks

---

## 🎯 System Requirements

### Minimum (CPU Mode)
- Docker with Docker Compose
- 4 CPU cores, 8GB RAM
- 15GB disk space

### Recommended (GPU Mode)
- NVIDIA GPU with 8GB+ VRAM
- NVIDIA Container Toolkit
- 8+ CPU cores, 16GB+ RAM
- 50GB+ disk space

---

## 📚 Documentation

- [Quick Start Guide](README.md#-quick-start-docker---recommended)
- [Docker Deployment Guide](docs/DOCKER.md)
- [Manual Setup](README.md#-manual-setup-without-docker)
- [Full Changelog](docs/CHANGELOG.md)

---

## 🐛 Known Issues

- Conversation persistence uses localStorage (SQLite planned for v1.1)
- Some model architectures not yet supported by llama-cpp-python

---

## 🙏 Acknowledgments

Built with:
- [Ollama](https://ollama.com) - Simplified LLM inference
- [FastAPI](https://fastapi.tiangolo.com) - Modern Python web framework
- [React](https://reactjs.org) - UI library
- [Docker](https://www.docker.com) - Containerization

---

## 🔄 Upgrading from Pre-Release

If you've been testing development versions:

```bash
# Pull latest code
git pull origin main

# Pull new images
docker compose pull

# Restart with new version
docker compose down
docker compose up
```

---

## 💬 Feedback & Support

- 🐛 [Report Issues](https://github.com/juliuspleunes4/Monolith/issues)
- 💡 [Feature Requests](https://github.com/juliuspleunes4/Monolith/discussions)
- ⭐ Star the repo if this helped you!

---

## 📝 Full Release Notes

See [CHANGELOG.md](docs/CHANGELOG.md) for complete details.

---

**Built with ❤️ for the local LLM community**

*Run AI locally. Keep your data private. Stay in control.*

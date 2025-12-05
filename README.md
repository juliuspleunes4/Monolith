<div align="center">

# 🗿 Monolith

**A fully local, GPU-accelerated LLM chat application with one-command Docker deployment**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE.md)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.3.1-61dafb.svg)](https://reactjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.6.2-3178c6.svg)](https://www.typescriptlang.org)
[![Ollama](https://img.shields.io/badge/Ollama-Latest-000000.svg)](https://ollama.com)

*Chat with multiple LLMs locally with automatic GPU acceleration. No cloud, no API keys, no tracking. Deploy in seconds with Docker.*

[Features](#-features) • [Quick Start](#-quick-start-docker---recommended) • [Manual Setup](#-manual-setup-without-docker) • [Docker Guide](docs/DOCKER.md) • [Development](#-development)

![Monolith Screenshot](https://via.placeholder.com/800x450/1a1a1a/5170ff?text=Monolith+Chat+Interface)

</div>

---

## ✨ Features

- 🐳 **One-Command Deployment** - `docker compose up` and you're running with GPU acceleration
- 🚀 **GPU-Accelerated Inference** - Automatic NVIDIA GPU detection and offloading via Ollama
- 📦 **Pre-installed Model** - Includes `deepseek-r1:8b` automatically downloaded on first run
- 💬 **Real-time Streaming** - Server-Sent Events for responsive token generation (20-30+ tokens/sec)
- 🔄 **Multiple Backends** - Support for both Ollama (GPU) and llama-cpp-python (CPU)
- 🎨 **Modern UI** - Clean, responsive interface with markdown rendering and syntax highlighting
- 💾 **Conversation Persistence** - Persistent chat history across container restarts
- 🔌 **Fully Offline** - No external API calls, all processing happens locally
- 🎯 **Model Management** - Easy switching between multiple LLM models
- 🌓 **Dark Mode Ready** - Professional color scheme optimized for extended use
- ⚡ **Production Ready** - Health checks, auto-restart, volume management included

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Docker Compose                           │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────────────┐│
│  │   Frontend   │   │   Backend    │   │   Ollama + GPU       ││
│  │   (nginx)    │◄─►│   (FastAPI)  │◄─►│   deepseek-r1:8b     ││
│  │   Port 3000  │   │   Port 8000  │   │   Port 11434         ││
│  └──────────────┘   └──────────────┘   └──────────────────────┘│
│         │                   │                      │             │
│         │                   │                      ▼             │
│         │                   │              ┌──────────────┐      │
│         │                   │              │ NVIDIA GPU   │      │
│         │                   │              │ CUDA Runtime │      │
│         │                   ▼              └──────────────┘      │
│         │           ┌──────────────┐                             │
│         │           │  Persistent  │                             │
│         │           │   Volumes    │                             │
│         └───────────┤ • Chat Data  │                             │
│                     │ • Models     │                             │
│                     └──────────────┘                             │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start (Docker - Recommended)

### Prerequisites

- **Docker** with Docker Compose
- **NVIDIA GPU** with [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) (for GPU acceleration)
  - Or CPU-only mode (slower but works without GPU)

### One-Command Setup

```bash
# Clone the repository
git clone https://github.com/juliuspleunes4/Monolith.git
cd Monolith

# Start everything (includes automatic deepseek-r1:8b download)
docker compose up

# Open browser to http://localhost:3000
```

**That's it!** The first run will:
1. ✅ Build frontend and backend containers (~2-5 minutes)
2. ✅ Start Ollama with GPU support
3. ✅ Automatically download `deepseek-r1:8b` model (~5GB, 5-10 minutes)
4. ✅ Launch the UI at http://localhost:3000

**Total setup time:** 10-15 minutes on first run, then instant afterwards!

### GPU Support

**Linux (NVIDIA):**
```bash
# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

**Windows/Mac:**
- Docker Desktop includes GPU support automatically
- Ensure GPU drivers are up to date

### CPU-Only Mode

If you don't have a GPU or NVIDIA Container Toolkit:

```bash
# Use the CPU-only compose file
docker compose -f docker-compose.cpu.yml up
```

⚠️ **Note:** CPU inference is significantly slower (~0.5-2 tokens/sec vs 20-30+ on GPU)

### Docker Commands Reference

```bash
# Start in background
docker compose up -d

# View logs
docker compose logs -f

# Stop all services
docker compose down

# Stop and remove volumes (fresh start)
docker compose down -v

# Add more Ollama models
docker exec -it monolith-ollama ollama pull llama3.2:3b

# Rebuild after code changes
docker compose up --build
```

---

## 🛠️ Manual Setup (Without Docker)

### Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **Ollama** (for GPU acceleration)
- **NVIDIA GPU** (recommended) or CPU fallback

### 1. Install Ollama

Download and install Ollama from [ollama.com](https://ollama.com):

**Windows:**
```powershell
# Download installer from https://ollama.com/download/windows
# Or use winget:
winget install Ollama.Ollama
```

**macOS:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Pull an LLM Model

```bash
# Start Ollama service (usually automatic)
ollama serve

# Pull Llama 3.1 8B (recommended, ~5GB)
ollama pull llama3.1:8b

# Or try other models:
ollama pull llama3.2:3b      # Smaller, faster (1.3GB)
ollama pull mistral:7b       # Great general model (4.1GB)
ollama pull qwen2.5:7b       # Excellent for coding (4.7GB)
```

### 3. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/juliuspleunes4/Monolith.git
cd Monolith

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install

# Start both servers
cd ../backend
python -m uvicorn app.main:app --reload --port 8000

# In another terminal
cd frontend
npm run dev
```

### 4. Open and Chat

Open your browser to **http://localhost:3001** and start chatting! 🎉

## 📦 Installation

### Backend Setup

The backend is built with FastAPI and supports multiple LLM inference engines.

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the backend
python -m uvicorn app.main:app --reload --port 8000
```

**Backend runs on:** `http://localhost:8000`

### Frontend Setup

The frontend is built with React and TypeScript using Vite.

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Frontend runs on:** `http://localhost:3001`

### Optional: Local .GGUF Models

To use local .gguf model files (CPU inference):

1. Create model directories:
```bash
mkdir -p models/{small,medium,large}
```

2. Download models from [Hugging Face](https://huggingface.co/models?library=gguf):
```bash
# Example: Download gemma-3-1b-it
cd models/small
wget https://huggingface.co/user/model/resolve/main/model.gguf
```

3. Restart the backend - models will appear automatically!

## 🎯 Usage

### Selecting Models

Click the **Model** selector in the top-right corner to choose from:

- **OLLAMA** category (⚡ GPU-accelerated)
  - Automatic GPU offloading
  - 20-30+ tokens/second
  - Recommended for best performance

- **SMALL/MEDIUM/LARGE** categories (CPU)
  - Local .gguf files
  - Fallback option
  - No GPU required

### Managing Ollama Models

**With Docker:**
```bash
# List installed models
docker exec -it monolith-ollama ollama list

# Pull new models
docker exec -it monolith-ollama ollama pull <model-name>

# Remove models
docker exec -it monolith-ollama ollama rm <model-name>

# Show model information
docker exec -it monolith-ollama ollama show <model-name>
```

**Without Docker:**
```bash
# List installed models
ollama list

# Pull new models
ollama pull <model-name>

# Remove models
ollama rm <model-name>
```

Popular models to try:
- `deepseek-r1:8b` - Excellent reasoning (pre-installed with Docker)
- `llama3.1:8b` - Latest Llama, great all-rounder
- `llama3.2:3b` - Smaller, faster variant
- `mistral:7b` - Strong general performance
- `qwen2.5:7b` - Top-tier coding model
- `gemma3:7b` - Google's efficient model

### Conversation Management

- **New Chat**: Click the "+" button to start fresh
- **History**: Previous conversations saved in sidebar
- **Persistence**: Conversations stored in browser localStorage

### Code Blocks

Code in responses is automatically syntax-highlighted with:
- Language detection
- Copy button
- Line numbers
- Professional dark theme

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `backend` directory:

```env
# Model directories
MODELS_DIR=../models

# Ollama configuration
OLLAMA_BASE_URL=http://localhost:11434

# Logging
LOG_LEVEL=INFO
```

### Model Parameters

Adjust generation parameters in the chat interface:
- **Temperature**: 0.0 (focused) to 2.0 (creative)
- **Max Tokens**: Maximum response length
- **Top P**: Nucleus sampling threshold

## 🛠️ Development

### Project Structure

```
monolith/
├── backend/
│   ├── app/
│   │   ├── llm/
│   │   │   ├── inference.py          # llama-cpp-python inference
│   │   │   └── ollama_inference.py   # Ollama integration
│   │   ├── routers/
│   │   │   ├── chat.py               # Chat endpoints
│   │   │   ├── conversations.py      # Conversation management
│   │   │   └── models.py             # Model listing/management
│   │   └── main.py                   # FastAPI application
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInterface.tsx     # Main chat UI
│   │   │   ├── ModelSelector.tsx     # Model picker
│   │   │   └── Sidebar.tsx           # Conversation history
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
├── models/                            # Local .gguf models (optional)
│   ├── small/
│   ├── medium/
│   └── large/
└── README.md
```

### API Endpoints

**GET** `/api/v1/models`
- List all available models (Ollama + local)

**POST** `/api/v1/chat`
- Stream chat completions
- Body: `{ model, messages, temperature, max_tokens, top_p }`

**GET** `/api/v1/conversations`
- List all conversations

**POST** `/api/v1/conversations`
- Create new conversation

### Adding Custom Backends

Implement the inference interface in `app/llm/`:

```python
async def generate_streaming(
    model_id: str,
    messages: list[dict[str, str]],
    temperature: float = 0.7,
    max_tokens: int = 512,
    top_p: float = 0.9,
) -> AsyncGenerator[str, None]:
    # Your implementation
    yield token
```

## 🐛 Troubleshooting

### Docker Issues

**Container won't start:**
```bash
# Check logs
docker compose logs

# Rebuild from scratch
docker compose down -v
docker compose up --build
```

**GPU not detected:**
```bash
# Verify NVIDIA Container Toolkit
docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi

# Check docker daemon.json has nvidia runtime
cat /etc/docker/daemon.json
```

**Model download fails:**
```bash
# Manually pull model
docker exec -it monolith-ollama ollama pull deepseek-r1:8b
```

See [docs/DOCKER.md](docs/DOCKER.md) for comprehensive Docker troubleshooting.

### Ollama Not Detected (Manual Setup)

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama service
# Windows: Restart from system tray
# macOS/Linux: 
systemctl restart ollama
```

### GPU Not Being Used

```bash
# Verify GPU is available
nvidia-smi  # For NVIDIA
# Ollama automatically uses GPU if available

# Check Ollama logs
ollama logs
```

### Backend Connection Issues

- Ensure backend is running on port 8000
- Check CORS settings in `app/main.py`
- Verify firewall isn't blocking localhost connections

### Slow Performance

- Use **Ollama models** for GPU acceleration
- Reduce `max_tokens` for faster responses
- Try smaller models (llama3.2:3b instead of llama3.1:8b)
- Close other GPU-intensive applications

## 📝 License

MIT License - see [LICENSE.md](LICENSE.md) for details

## 📚 Documentation

- **[Docker Deployment Guide](docs/DOCKER.md)** - Comprehensive Docker setup and troubleshooting
- **[API Documentation](docs/API.md)** - REST API reference (coming soon)
- **[Changelog](docs/CHANGELOG.md)** - Version history and updates

## 🙏 Acknowledgments

- [Ollama](https://ollama.com) - Simplified LLM inference with automatic GPU support
- [FastAPI](https://fastapi.tiangolo.com) - Modern Python web framework
- [React](https://reactjs.org) - UI library
- [Docker](https://www.docker.com) - Containerization platform
- [llama.cpp](https://github.com/ggerganov/llama.cpp) - LLM inference engine
- [Hugging Face](https://huggingface.co) - Model repository

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⭐ Show Your Support

Give a ⭐ if this project helped you! It helps others discover Monolith.

## 📧 Contact

Questions? Open an [issue](https://github.com/juliuspleunes4/Monolith/issues) or start a [discussion](https://github.com/juliuspleunes4/Monolith/discussions)!

---

<div align="center">

**Built with ❤️ for the local LLM community**

*Run AI locally. Keep your data private. Stay in control.*

[⬆ Back to Top](#-monolith)

</div>

<div align="center">

# 🗿 Monolith

**A fully local, GPU-accelerated LLM chat application**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE.md)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.3.1-61dafb.svg)](https://reactjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.6.2-3178c6.svg)](https://www.typescriptlang.org)
[![Ollama](https://img.shields.io/badge/Ollama-0.13.1-000000.svg)](https://ollama.com)

*Chat with multiple LLMs locally with automatic GPU acceleration. No cloud, no API keys, no tracking.*

[Features](#-features) • [Quick Start](#-quick-start) • [Installation](#-installation) • [Usage](#-usage) • [Models](#-models) • [Development](#-development)

![Monolith Screenshot](https://via.placeholder.com/800x450/1a1a1a/5170ff?text=Monolith+Chat+Interface)

</div>

---

## ✨ Features

- 🚀 **GPU-Accelerated Inference** - Automatic GPU detection and offloading via Ollama
- 💬 **Real-time Streaming** - Server-Sent Events for responsive token generation
- 🔄 **Multiple Backends** - Support for both Ollama (GPU) and llama-cpp-python (CPU)
- 🎨 **Modern UI** - Clean, responsive interface with markdown rendering and syntax highlighting
- 💾 **Conversation Persistence** - LocalStorage-based chat history
- 🔌 **Fully Offline** - No external API calls, all processing happens locally
- 🎯 **Model Management** - Easy switching between multiple LLM models
- 🌓 **Dark Mode Ready** - Professional color scheme optimized for extended use

## 🏗️ Architecture

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│  React Frontend │ ◄──► │  FastAPI Backend │ ◄──► │  Ollama Engine  │
│   (Port 3001)   │      │   (Port 8000)    │      │  (Port 11434)   │
└─────────────────┘      └──────────────────┘      └─────────────────┘
        │                         │                          │
        │                         │                          ▼
        │                         │                  ┌──────────────┐
        │                         │                  │ GPU Inference│
        │                         │                  │ (CUDA/Metal) │
        │                         ▼                  └──────────────┘
        │                 ┌──────────────┐
        │                 │  Local .gguf │
        │                 │   CPU Models │
        └─────────────────┴──────────────┘
```

## 🚀 Quick Start

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
git clone https://github.com/yourusername/monolith.git
cd monolith

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

```bash
# List installed models
ollama list

# Pull new models
ollama pull <model-name>

# Remove models
ollama rm <model-name>

# Show model information
ollama show <model-name>
```

Popular models to try:
- `llama3.1:8b` - Latest Llama, great all-rounder
- `llama3.2:3b` - Smaller, faster variant
- `deepseek-r1:8b` - Excellent reasoning capabilities
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

### Ollama Not Detected

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

## 🙏 Acknowledgments

- [Ollama](https://ollama.com) - Simplified LLM inference
- [FastAPI](https://fastapi.tiangolo.com) - Modern Python web framework
- [React](https://reactjs.org) - UI library
- [llama.cpp](https://github.com/ggerganov/llama.cpp) - LLM inference engine
- [Hugging Face](https://huggingface.co) - Model repository

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

Questions? Open an issue or reach out!

---

<div align="center">

**Built with ❤️ for the local LLM community**

[⬆ Back to Top](#-monolith)

</div>

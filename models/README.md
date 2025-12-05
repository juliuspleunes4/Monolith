# LLM Models Directory

Place your local GGUF model files in the appropriate size subdirectories. Models will be automatically detected and categorized by Monolith.

## 📁 Directory Structure

```
models/
├── small/       # Models < 5GB
├── medium/      # Models 5-10GB
├── large/       # Models > 10GB
└── README.md    # This file
```

**Important:** Place each model file in its corresponding size folder for proper categorization in the UI.

## 🚀 Primary Recommendation: Use Ollama

For the best experience, **use Ollama models** instead of local .gguf files:
- ✅ Automatic GPU acceleration
- ✅ 20-30+ tokens/second performance
- ✅ Easy model management with `ollama pull <model>`
- ✅ No manual file downloads needed

Ollama models appear in the **OLLAMA** category in the model selector.

## 📥 Local GGUF Models (Optional)

If you want to use local .gguf files (CPU fallback), download them from [Hugging Face](https://huggingface.co/models?library=gguf) and place in the correct folder:

### Small Models (< 5GB) → `models/small/`
- Llama 3.2 3B
- Phi-3 Mini  
- TinyLlama 1.1B
- Gemma 2B

### Medium Models (5-10GB) → `models/medium/`
- Llama 3.2 8B
- Mistral 7B
- Gemma 7B
- Qwen 7B

### Large Models (> 10GB) → `models/large/`
- Llama 3.1 70B
- Mixtral 8x7B
- Llama 3 70B

## 🔄 How to Add Models

### Option 1: Ollama (Recommended)
```bash
# With Docker
docker exec -it monolith-ollama ollama pull llama3.2:3b

# Without Docker
ollama pull llama3.2:3b
```

### Option 2: Local GGUF Files
```bash
# Example: Add a small model
cd models/small
wget https://huggingface.co/...your-model.gguf

# Example: Add a medium model
cd models/medium
wget https://huggingface.co/...your-model.gguf

# Restart backend to detect new models
docker compose restart backend
```

## 📊 Model Categories in UI

Models will appear in the model selector based on their location:
- **OLLAMA** ⚡ - Ollama models (GPU-accelerated)
- **SMALL** - Models in `models/small/` folder
- **MEDIUM** - Models in `models/medium/` folder
- **LARGE** - Models in `models/large/` folder

## ⚠️ Notes

- Local .gguf models use **CPU inference only** (slower performance)
- Ollama models automatically use **GPU acceleration** when available
- Models are detected on backend startup
- Restart the backend after adding new .gguf files

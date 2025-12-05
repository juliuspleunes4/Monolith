# LLM Models Directory

Place your LLM model files in this directory. Supported formats:
- GGUF (llama.cpp compatible)
- GGML (legacy)

## Recommended Models

### Small Models (< 5GB)
- Llama 3.2 3B
- Phi-3 Mini
- TinyLlama 1.1B

### Medium Models (5-10GB)
- Llama 3.2 8B
- Mistral 7B
- Gemma 7B

### Large Models (> 10GB)
- Llama 3.1 70B
- Mixtral 8x7B

## Directory Structure

```
models/
├── model-name-1.gguf
├── model-name-2.gguf
└── README.md (this file)
```

Models will be automatically detected and loaded by Monolith on startup.

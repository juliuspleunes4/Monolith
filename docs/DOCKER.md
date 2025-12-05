# 🐳 Docker Deployment Guide

This guide covers deploying Monolith using Docker with automatic model installation.

## 🚀 Quick Start

### 1. Prerequisites

- Docker 20.10+ with Docker Compose
- For GPU support: [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
- 10GB free disk space (for model downloads)

### 2. Launch

```bash
# GPU mode (recommended)
docker compose up

# CPU mode (no GPU required)
docker compose -f docker-compose.cpu.yml up

# Background mode
docker compose up -d
```

### 3. Access

Open **http://localhost:3000** in your browser 🎉

The first run will:
- ✅ Build containers (~2-5 minutes)
- ✅ Pull `deepseek-r1:8b` model (~5GB, 5-10 minutes)
- ✅ Start all services automatically

---

## 📋 What Gets Deployed

| Service | Port | Description |
|---------|------|-------------|
| **frontend** | 3000 | React UI with nginx |
| **backend** | 8000 | FastAPI server |
| **ollama** | 11434 | LLM inference engine |

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Backend
LOG_LEVEL=INFO
MODELS_DIR=/app/models
DATA_DIR=/app/data

# Ollama
OLLAMA_HOST=http://ollama:11434

# Frontend
FRONTEND_URL=http://localhost:3000
```

### GPU Memory Limits

Edit `docker-compose.yml` to limit GPU usage:

```yaml
services:
  ollama:
    deploy:
      resources:
        limits:
          memory: 8G
        reservations:
          devices:
            - driver: nvidia
              count: 1  # Use only 1 GPU
              capabilities: [gpu]
```

---

## 📦 Adding More Models

### Via Docker Exec

```bash
# Add smaller model
docker exec -it monolith-ollama ollama pull llama3.2:1b

# Add coding model
docker exec -it monolith-ollama ollama pull qwen2.5-coder:7b

# List installed models
docker exec -it monolith-ollama ollama list
```

### Via Compose Override

Create `docker-compose.override.yml`:

```yaml
services:
  ollama-init:
    command:
      - |
        echo "Installing multiple models..."
        ollama pull deepseek-r1:8b
        ollama pull llama3.2:3b
        ollama pull mistral:7b
        echo "✓ All models ready!"
```

Then run: `docker compose up`

---

## 🔄 Common Operations

### View Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f ollama

# Last 100 lines
docker compose logs --tail=100
```

### Restart Services

```bash
# Restart all
docker compose restart

# Restart specific service
docker compose restart backend
```

### Update After Code Changes

```bash
# Rebuild and restart
docker compose up --build

# Rebuild specific service
docker compose up --build backend
```

### Clean Slate

```bash
# Stop and remove containers
docker compose down

# Remove volumes too (deletes data!)
docker compose down -v

# Remove images
docker compose down --rmi all
```

---

## 🐛 Troubleshooting

### GPU Not Detected

**Check NVIDIA drivers:**
```bash
nvidia-smi
```

**Verify Container Toolkit:**
```bash
docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi
```

**Ensure Docker daemon config** (`/etc/docker/daemon.json`):
```json
{
  "runtimes": {
    "nvidia": {
      "path": "nvidia-container-runtime",
      "runtimeArgs": []
    }
  }
}
```

Then: `sudo systemctl restart docker`

### Model Download Fails

```bash
# Check Ollama logs
docker compose logs ollama-init

# Manually pull
docker exec -it monolith-ollama ollama pull deepseek-r1:8b
```

### Port Already in Use

Change ports in `docker-compose.yml`:
```yaml
services:
  frontend:
    ports:
      - "3001:3000"  # Changed from 3000:3000
  backend:
    ports:
      - "8001:8000"  # Changed from 8000:8000
```

### Out of Memory

Reduce model concurrency in backend:
```yaml
services:
  backend:
    environment:
      - MAX_CONCURRENT_REQUESTS=1
```

Or use a smaller model:
```bash
docker exec -it monolith-ollama ollama pull llama3.2:1b
```

---

## 📊 Resource Requirements

### Minimum

- **CPU:** 4 cores
- **RAM:** 8GB
- **Disk:** 15GB
- **GPU:** None (CPU mode)

### Recommended

- **CPU:** 8+ cores
- **RAM:** 16GB+
- **Disk:** 50GB+ (for multiple models)
- **GPU:** NVIDIA with 8GB+ VRAM

### Model Sizes

| Model | Size | VRAM | Speed (GPU) |
|-------|------|------|-------------|
| llama3.2:1b | 1.3GB | 2GB | 50+ tok/s |
| llama3.2:3b | 2.0GB | 4GB | 40+ tok/s |
| llama3.1:8b | 4.9GB | 6GB | 30+ tok/s |
| deepseek-r1:8b | 5.2GB | 6GB | 20+ tok/s |
| mistral:7b | 4.1GB | 6GB | 35+ tok/s |

---

## 🔒 Production Deployment

### Using Traefik (Reverse Proxy)

```yaml
services:
  frontend:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.monolith.rule=Host(`chat.yourdomain.com`)"
      - "traefik.http.routers.monolith.entrypoints=websecure"
      - "traefik.http.routers.monolith.tls.certresolver=letsencrypt"
```

### Health Monitoring

All services include health checks:
```bash
# Check status
docker compose ps

# Healthy output shows:
# NAME                STATE    HEALTH
# monolith-backend    Up       healthy
# monolith-frontend   Up       healthy
# monolith-ollama     Up       healthy
```

### Persistent Data

Data is stored in Docker volumes:
- `monolith-ollama-data`: Downloaded models
- `monolith-backend-data`: Chat history, settings

**Backup:**
```bash
docker run --rm -v monolith-backend-data:/data -v $(pwd):/backup \
  alpine tar czf /backup/monolith-backup-$(date +%Y%m%d).tar.gz /data
```

**Restore:**
```bash
docker run --rm -v monolith-backend-data:/data -v $(pwd):/backup \
  alpine tar xzf /backup/monolith-backup-20250101.tar.gz -C /
```

---

## 🌐 Remote Access

### Via SSH Tunnel

```bash
# On your local machine
ssh -L 3000:localhost:3000 user@remote-server

# Then access http://localhost:3000
```

### Via Tailscale (Recommended)

1. Install Tailscale on server and client
2. Access via: `http://[tailscale-ip]:3000`

### Via Cloudflare Tunnel

```bash
cloudflared tunnel --url http://localhost:3000
```

---

## 📚 Additional Resources

- [Docker Compose Docs](https://docs.docker.com/compose/)
- [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-container-toolkit)
- [Ollama Docker Hub](https://hub.docker.com/r/ollama/ollama)
- [FastAPI Docker Deployment](https://fastapi.tiangolo.com/deployment/docker/)

# Release Notes v1.0.1

## 🐛 Bug Fix Release

**Release Date:** December 5, 2025

This is a critical bug fix release that resolves Docker deployment issues discovered in v1.0.0.

---

## What's Fixed

### Docker Health Check Issue
- **Problem**: Ollama container health checks were failing with "curl: executable file not found" error
- **Solution**: Changed health check from `curl -f http://localhost:11434/api/tags` to `ollama list` command
- **Impact**: Ollama containers now properly report healthy status, allowing dependent services to start

### Backend Permission Errors
- **Problem**: Backend container failed with "Permission denied" error when trying to execute uvicorn
- **Solution**: Fixed Dockerfile to copy Python dependencies to non-root user's home directory (`/home/monolith/.local`) instead of `/root/.local`
- **Impact**: Backend now starts successfully and passes health checks

### Comprehensive Fix Coverage
- Applied fixes to all Docker Compose variants:
  - `docker-compose.yml` (production with pre-built images)
  - `docker-compose.dev.yml` (development with local builds)
  - `docker-compose.cpu.yml` (CPU-only mode)

---

## 🚀 Quick Start

### For New Users

```bash
# Clone the repository
git clone https://github.com/juliuspleunes4/Monolith.git
cd Monolith

# Checkout v1.0.1
git checkout v1.0.1

# Start everything (make sure Docker Desktop is running!)
docker compose up -d
```

Open http://localhost:3000 and start chatting!

### For Existing v1.0.0 Users

```bash
# Pull the fixed images
docker compose pull

# Restart with new version
docker compose down
docker compose up -d
```

---

## 📝 Technical Details

**Changed Files:**
- `backend/Dockerfile` - Fixed Python dependency path and ownership
- `docker-compose.yml` - Updated Ollama health check command
- `docker-compose.dev.yml` - Updated Ollama health check command
- `docker-compose.cpu.yml` - Updated Ollama health check command
- `docs/CHANGELOG.md` - Documented changes

**Docker Images:**
- `juliuspleunes4/monolith-backend:1.0.1`
- `juliuspleunes4/monolith-backend:1.0`
- `juliuspleunes4/monolith-backend:latest`
- `juliuspleunes4/monolith-frontend:1.0.1` (unchanged, re-tagged)
- `juliuspleunes4/monolith-frontend:1.0`
- `juliuspleunes4/monolith-frontend:latest`

**Platforms Supported:**
- linux/amd64
- linux/arm64

---

## ⚠️ Known Issues

None reported for v1.0.1.

---

## 📚 Documentation

- [Docker Deployment Guide](../docs/DOCKER.md)
- [Changelog](../docs/CHANGELOG.md)
- [Release Checklist](RELEASE_CHECKLIST.md)
- [README](../README.md)

---

## 🙏 Thank You

Thanks to early adopters who tested v1.0.0 and helped identify these issues quickly!

---

**Full Changelog**: https://github.com/juliuspleunes4/Monolith/compare/v1.0.0...v1.0.1

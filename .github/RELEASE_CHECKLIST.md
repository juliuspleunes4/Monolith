# Release Checklist for v1.0.0

Follow these steps to publish the v1.0.0 release.

## 📋 Prerequisites

### 1. Docker Hub Account Setup
1. Create account at https://hub.docker.com
2. Create two repositories:
   - `monolith-backend` (public)
   - `monolith-frontend` (public)
3. Generate access token:
   - Go to Account Settings → Security → Access Tokens
   - Create new token with Read & Write permissions
   - Save the token securely

### 2. GitHub Secrets Configuration
Add these secrets to your repository (Settings → Secrets and variables → Actions):
- `DOCKERHUB_USERNAME` - Your Docker Hub username
- `DOCKERHUB_TOKEN` - The access token from step 1

---

## 🚀 Release Steps

### Step 1: Update Version and Documentation

**Before creating any tags, ensure all version references are updated:**

1. **Update `docs/CHANGELOG.md`**
   - Add new version section (e.g., `## [1.1.0] - 2025-12-XX`)
   - List all changes under appropriate categories:
     - Added
     - Changed
     - Fixed
     - Removed
   - Move items from `[Unreleased]` section if applicable

2. **Verify version numbers are consistent across:**
   - `docs/CHANGELOG.md` - Version header and release date
   - `.github/RELEASE_NOTES_vX.X.X.md` - Create new file if needed
   - `README.md` - Update any version-specific references
   - `backend/app/__init__.py` or `package.json` - If versioned

3. **Commit all documentation updates:**
   ```bash
   git add docs/CHANGELOG.md .github/RELEASE_NOTES_*.md README.md
   git commit -m "docs: prepare for vX.X.X release"
   git push origin main
   ```

### Step 2: Verify Everything Works Locally

```bash
# Test with pre-built image paths
docker compose -f docker-compose.yml config

# Test build manually
cd backend && docker build -t test-backend .
cd ../frontend && docker build -t test-frontend .
```

### Step 3: Create Git Tag and Trigger GitHub Actions

```bash
# Ensure you're on main branch with latest changes
git checkout main
git pull origin main

# Create annotated tag (use the version number you documented in Step 1)
git tag -a v1.0.0 -m "Release v1.0.0 - Initial public release with Docker Hub support"

# Push tag to GitHub - THIS AUTOMATICALLY TRIGGERS GITHUB ACTIONS
git push origin v1.0.0
```

**⚡ Pushing the tag automatically triggers the GitHub Actions workflow** which will:

### Step 4: GitHub Actions Automatically Builds and Publishes
1. ✅ Build backend and frontend images for linux/amd64 and linux/arm64
2. ✅ Tag with semantic versions (1.0.0, 1.0, 1, latest)
3. ✅ Push to Docker Hub repositories
4. ✅ Create build summary

**Monitor progress at:** https://github.com/juliuspleunes4/Monolith/actions

Wait for the workflow to complete (typically 5-10 minutes). Ensure all jobs show green checkmarks.

### Step 5: Create GitHub Release

Once GitHub Actions completes successfully:

1. Go to https://github.com/juliuspleunes4/Monolith/releases/new
2. Select tag: `v1.0.0` (the tag you created in Step 3)
3. Release title: `v1.0.0 - Initial Release 🎉`
4. Copy content from `.github/RELEASE_NOTES_v1.0.0.md` (or the version-specific file you created in Step 1)
5. Check "Set as the latest release"
6. Click "Publish release"

### Step 6: Verify Deployment

```bash
# Test pulling images
docker pull juliuspleunes4/monolith-backend:1.0.0
docker pull juliuspleunes4/monolith-frontend:1.0.0

# Test full deployment
git clone https://github.com/juliuspleunes4/Monolith.git test-deploy
cd test-deploy
git checkout v1.0.0
docker compose pull
docker compose up
```

Should be running at http://localhost:3000 in 5-10 minutes!

---

## 📝 Post-Release Tasks

### Update Docker Hub Descriptions

**Backend Repository** (https://hub.docker.com/r/juliuspleunes4/monolith-backend):
```markdown
# Monolith Backend

FastAPI backend for Monolith - a fully local, GPU-accelerated LLM chat application.

## Features
- Dual backend support: Ollama (GPU) + llama-cpp-python (CPU)
- Real-time streaming via SSE
- Automatic model discovery
- Health checks included

## Usage
```bash
docker compose up
```

Part of [Monolith](https://github.com/juliuspleunes4/Monolith) - full deployment instructions in repo.
```

**Frontend Repository** (https://hub.docker.com/r/juliuspleunes4/monolith-frontend):
```markdown
# Monolith Frontend

React + TypeScript frontend for Monolith - a fully local, GPU-accelerated LLM chat application.

## Features
- Clean ChatGPT-style interface
- Real-time message streaming
- Dark/light theme support
- Code syntax highlighting
- Nginx production serving

## Usage
```bash
docker compose up
```

Part of [Monolith](https://github.com/juliuspleunes4/Monolith) - full deployment instructions in repo.
```

### Announce Release
- [ ] Update main README badges if needed
- [ ] Share on relevant communities (optional)
- [ ] Monitor issues for user feedback

---

## 🔄 For Future Releases

When releasing v1.1.0, v1.2.0, etc.:

1. Update `docs/CHANGELOG.md` with new version
2. Create tag: `git tag -a v1.1.0 -m "Release v1.1.0 - Description"`
3. Push tag: `git push origin v1.1.0`
4. GitHub Actions builds and pushes automatically
5. Create GitHub release with notes
6. Images tagged as:
   - `1.1.0` (specific version)
   - `1.1` (minor version)
   - `1` (major version)
   - `latest` (if main branch)

---

## 🐛 Troubleshooting

**GitHub Actions fails to push:**
- Verify Docker Hub token hasn't expired
- Check `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets
- Ensure repositories exist on Docker Hub

**Images won't pull:**
- Ensure repositories are public on Docker Hub
- Wait 2-3 minutes after Actions complete for images to be available
- Check Docker Hub for image tags

**Build fails:**
- Test local build: `docker build -t test ./backend`
- Check Dockerfile syntax
- Verify all required files are not in .dockerignore

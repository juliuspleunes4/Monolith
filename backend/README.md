# Monolith Backend

FastAPI backend for the Monolith local LLM chat application.

## Prerequisites

- Python 3.11 or later
- pip (Python package manager)

### Installing Python on Windows

1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **Important:** Check "Add Python to PATH" during installation
4. Verify installation by opening PowerShell and running:
   ```powershell
   python --version
   ```

## Setup

### Manual Setup

1. Create virtual environment:
   ```powershell
   python -m venv venv
   ```

2. Activate virtual environment:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

## Running the Server

### Manual Start

1. Activate the virtual environment (if not already activated):
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

2. Start the server:
   ```powershell
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

The API will be available at:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## API Endpoints

### Models
- `GET /api/v1/models` - List all available models
- `POST /api/v1/models/{model_id}/load` - Load a model
- `POST /api/v1/models/{model_id}/unload` - Unload a model

### Chat
- `POST /api/v1/chat` - Send a chat message
- `POST /api/v1/chat/stream` - Stream chat responses

### Conversations
- `GET /api/v1/conversations` - List all conversations
- `GET /api/v1/conversations/{id}` - Get a specific conversation
- `POST /api/v1/conversations` - Create a new conversation
- `PUT /api/v1/conversations/{id}` - Update a conversation
- `DELETE /api/v1/conversations/{id}` - Delete a conversation

## Environment Variables

Create a `.env` file in the backend directory:

```env
LOG_LEVEL=INFO
MODELS_DIR=../models
DATA_DIR=../data
FRONTEND_URL=http://localhost:3001
```

## Development

The server runs in reload mode by default, so code changes will automatically restart the server.

## Troubleshooting

### Virtual environment activation fails
If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Python not found
Make sure Python is in your PATH. You can verify by running:
```powershell
python --version
```

If not found, reinstall Python and check "Add Python to PATH".

### Port already in use
If port 8000 is already in use, you can change it:
```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

Don't forget to update the frontend API URL accordingly.

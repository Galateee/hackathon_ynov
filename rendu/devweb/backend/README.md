# 🚀 TechCorp AI Chat - Backend API

Flask API with multi-mode inference support: Local, Ollama, or Triton.

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- For GPU support: CUDA 11.8+ (optional but recommended)

## Installation

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Edit `.env` file to choose inference mode:

### Mode 1: LOCAL (Default) 🖥️
Load Phi-3.5 directly on your machine. Best for immediate testing!

```env
INFERENCE_MODE=local
BASE_MODEL_NAME=microsoft/Phi-3-mini-4k-instruct
MODEL_PATH=../../models/phi3_financial
BACKEND_PORT=5000
```

**Pros:**
- No external server needed
- Immediate testing available
- Works offline
- Can use GPU/CPU auto-detection

**Cons:**
- First run ~1-2 min to load model
- Requires torch + transformers (~5GB)
- Slower on CPU

### Mode 2: OLLAMA 🐪
Use Ollama inference server (once INFRA team deploys it)

```env
INFERENCE_MODE=ollama
INFERENCE_SERVER=http://localhost:11434
MODEL_NAME=phi3.5-financial
```

**Pros:**
- Simple, lightweight setup
- Recommended for production
- Fast inference

**Cons:**
- Requires separate Ollama server running

### Mode 3: TRITON 🔷
Use Triton Inference Server (advanced option)

```env
INFERENCE_MODE=triton
INFERENCE_SERVER=http://localhost:8000
MODEL_NAME=phi35_financial
```

**Pros:**
- Scalable, high-performance
- Enterprise-grade

**Cons:**
- More complex setup
- Requires separate Triton server

## Running the Server

```bash
python app.py
```

The API will start at `http://localhost:5000`

First run in LOCAL mode may take 1-2 minutes as it downloads and loads the model.

## API Endpoints

### Check Server Status
```bash
GET /api/status
# Response:
# {
#   "connected": true,
#   "mode": "local",
#   "status": "✅ Connected",
#   "backend": "🖥️ Local Model"
# }
```

### Send Chat Message
```bash
POST /api/chat
# Body: {"message": "What is compound interest?"}
# Response: {"reply": "...", "history": [...], "status": "connected"}
```

### Get Full History
```bash
GET /api/history
```

### Clear History
```bash
DELETE /api/history
```

### Health Check
```bash
GET /api/health
```

## Switching Between Modes

1. **Stop the server** (Ctrl+C)
2. **Edit `.env`** and change `INFERENCE_MODE`
3. **Restart** with `python app.py`

That's it! The backend auto-initializes the chosen mode.

## Troubleshooting

### Local Mode Issues

**"CUDA out of memory"**
- Switch to CPU: Uses bitsandbytes 4-bit quantization automatically
- Or reduce max_tokens in app.py (line ~145)

**"Model download very slow"**
- First run downloads ~3GB from HuggingFace
- Check internet connection
- Can take 5-10 minutes depending on speed

**"RuntimeError: Expected all tensors to be on the same device"**
- GPU/CPU mismatch - usually auto-detected
- Ensure torch & CUDA are installed: `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`

### Ollama Mode Issues

**"Connection refused"**
- Check if Ollama is running: `ollama serve`
- Verify URL in .env: `http://localhost:11434`

**"Model not found"**
- Pull model: `ollama pull phi3.5-financial`
- Check available: `ollama list`

### Triton Mode Issues

**"Connection refused"**
- Check if Triton server is running on port 8000
- Verify model is deployed in Triton

**"Invalid model name"**
- Ensure model name matches Triton deployment

## Performance Tips

**LOCAL mode:**
- First load: ~30-60s (model initialization)
- First response: ~5-10s (usually)
- Subsequent responses: ~2-5s (faster)
- GPU: ~2-3s per response
- CPU: ~10-30s per response

**OLLAMA mode:**
- ~1-5s per response (optimized)

**TRITON mode:**
- ~1-3s per response (production-grade)

## Important Notes

- Conversation history stored in-memory only (resets on restart)
- For production: use database (PostgreSQL/MongoDB)
- API timeout: 30 seconds per request
- Supports concurrent requests via Flask's threading

## Next Steps

1. ✅ Install dependencies
2. ✅ Configure `.env` (default is LOCAL mode)
3. ✅ Run `python app.py`
4. ✅ Frontend connects to http://localhost:5000
5. ✅ When INFRA deploys Ollama, switch modes in `.env`


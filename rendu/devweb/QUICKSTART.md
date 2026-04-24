# 🚀 Quick Launch Guide

## ⚡ 5-Minute Setup

### 1. Backend (Terminal 1)
```bash
cd backend
pip install -r requirements.txt
python app.py
```
✅ Backend running on http://localhost:5000

**First run takes 1-2 minutes** (downloads model ~3GB)

### 2. Frontend (Terminal 2)
```bash
cd frontend
npm install
npm start
```
✅ Frontend running on http://localhost:3000

### 3. Open Browser
Go to: **http://localhost:3000**

## ⚠️ Key Points

✓ **Backend supports 3 modes** (auto-configured):

| Mode | Setup | Best For |
|------|-------|----------|
| **LOCAL** (default 🖥️) | Works now! | Immediate testing (no INFRA needed) |
| **OLLAMA** 🐪 | When INFRA deploys | Production ready |
| **TRITON** 🔷 | When INFRA deploys | Enterprise deployment |

✓ **Switch modes anytime:**
- Edit `backend/.env` → change `INFERENCE_MODE`
- Restart backend
- Done!

## 🧪 Test It

1. Check backend: `curl http://localhost:5000/api/status`
2. In app, look for 🟢 Connected indicator
3. Ask: "What is compound interest?"
4. Should get instant response from **local model** 🎉

## 📊 Performance

| Mode | First Response | Subsequent |
|------|---|---|
| LOCAL (GPU) | ~5-10s | ~2-3s |
| LOCAL (CPU) | ~15-30s | ~10-20s |
| OLLAMA | ~2-5s | ~1-3s |
| TRITON | ~1-3s | ~1-2s |

**LOCAL mode works RIGHT NOW even without INFRA!**

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 5000 busy | Change `BACKEND_PORT` in `.env` |
| npm install fails | Try: `npm cache clean --force` |
| React won't start | Try: `rm -rf node_modules && npm install` |
| Model download slow | First run is ~5-10 min (3GB download) |
| GPU out of memory | Backend auto-switches to 4-bit quantization |

## 🚀 Next: Switch to Production Mode

When **INFRA** deploys Ollama/Triton:

1. Update `backend/.env`:
   ```env
   INFERENCE_MODE=ollama  # or triton
   INFERENCE_SERVER=http://your-server:port
   ```
2. Restart backend
3. Immediate switch ✅

---

**You're ready to go! Backend works NOW with local model.** 💪


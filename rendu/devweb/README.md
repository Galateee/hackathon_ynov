# 💻 TechCorp AI Chat - Full Stack Application

**Production-ready chat interface** for the Phi-3.5-Financial model deployed on Ollama/Triton.

## 🏗️ Architecture

```
TechCorp AI Chat
├── Frontend (React)
│   └── http://localhost:3000
├── Backend (Flask API)
│   └── http://localhost:5000
└── Inference Server (Ollama/Triton)
    └── http://localhost:11434 or :8000
```

## 🚀 Quick Start

### Step 1: Backend Setup

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with server details from your INFRA team
python app.py
```

Backend runs on: **http://localhost:5000**

### Step 2: Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend opens at: **http://localhost:3000**

### Step 3: Verify Connection

1. Open http://localhost:3000 in your browser
2. Check the status indicator (should be 🟢 Connected)
3. Ask a question: "What is finance?"

## 📋 System Requirements

### Backend
- Python 3.8+
- pip
- ~50MB disk space

### Frontend
- Node.js 14+
- npm
- Modern web browser

### Inference Server (handled by INFRA team)
- Ollama (localhost:11434) OR
- Triton (localhost:8000)
- Phi-3.5-Financial model deployed

## 🔧 Configuration

### Backend (.env file)

```env
# Inference server choice
INFERENCE_SERVER=http://localhost:11434    # Ollama
# INFERENCE_SERVER=http://localhost:8000   # Triton

# Model configuration
MODEL_NAME=phi3.5-financial

# Backend settings
BACKEND_PORT=5000
DEBUG=True
```

### Frontend (environment variables)

```bash
REACT_APP_API_URL=http://localhost:5000  # Backend URL
```

## 📊 Project Structure

```
rendu/devweb/
├── backend/
│   ├── app.py              # Flask API server
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example        # Config template
│   └── README.md
├── frontend/
│   ├── package.json        # NPM dependencies
│   ├── public/
│   │   ├── index.html
│   │   └── manifest.json
│   ├── src/
│   │   ├── App.js          # Main chat component
│   │   ├── App.css         # Styling
│   │   ├── index.js        # React entry
│   │   └── index.css       # Global styles
│   ├── README.md
│   └── .gitignore
└── README.md
```

## 🎯 Features

✅ **Real-time Chat**
- Send/receive messages instantly
- Full conversation history
- Message timestamps

✅ **Server Health Monitoring**
- Live connection status
- Auto-reconnection checks
- Visual indicators

✅ **User Experience**
- Responsive design (mobile-friendly)
- Loading animations
- Error handling
- Clear history function

## 🔌 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/status` | Check server connection |
| POST | `/api/chat` | Send message & get response |
| GET | `/api/history` | Get conversation history |
| DELETE | `/api/history` | Clear conversation |
| GET | `/api/health` | Health check |

## 🚀 Deployment

### Local Development (7h Challenge)
Already configured for localhost. Just run both servers.

### Production
- Backend: Deploy Flask to production server
- Frontend: Run `npm build` and serve static files
- Use environment variables for configuration

## 🐛 Troubleshooting

### Backend Issues

**"Address already in use"**
```bash
# Kill process on port 5000
# Windows: taskkill /PID <PID> /F
# macOS/Linux: kill -9 $(lsof -t -i:5000)
```

**"Connection refused"**
- Check if inference server is running
- Verify correct URL in .env

**"Model not found"**
- Ask INFRA team for exact model name
- Update MODEL_NAME in .env

### Frontend Issues

**"Cannot connect to API"**
- Check if backend is running on port 5000
- Verify CORS is enabled
- Check browser console (F12)

**"Blank page"**
- Check browser console for errors
- Ensure Node.js is installed
- Try: `rm -rf node_modules && npm install`

## 👥 Team Coordination

**Key Points:**
- **INFRA Team** deploys Ollama/Triton with Phi-3.5-Financial
  - Give you: Server URL + Model name
- **DEV WEB** (You) creates web interface
  - Configure backend .env with their details
  - Test integration
- **IA/DATA/CYBER** Teams: validate model quality

## 📝 Notes

- Conversation history is stored in-memory (resets on restart)
- For production, use database (PostgreSQL/MongoDB)
- API timeout: 30 seconds (adjust in app.py if needed)
- Frontend requires modern browser (Chrome, Firefox, Safari, Edge)

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [Ollama API Docs](https://github.com/jmorganca/ollama/blob/main/docs/api.md)
- [Triton Inference Server](https://github.com/triton-inference-server/tutorials)

---

**Ready to launch TechCorp's AI! 🚀**

# 🎨 TechCorp AI Chat - Frontend

React-based web interface for the TechCorp AI Chat application.

## Prerequisites

- Node.js 14+ and npm
- Backend API running (see ../backend/README.md)

## Installation

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

## Running the Application

```bash
npm start
```

The application will open at `http://localhost:3000`

## Build for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` directory.

## Configuration

The frontend automatically connects to the backend at `http://localhost:5000`

To change this, set the `REACT_APP_API_URL` environment variable:

```bash
# Windows
set REACT_APP_API_URL=http://your-backend-url:5000
npm start

# macOS/Linux
REACT_APP_API_URL=http://your-backend-url:5000 npm start
```

## Features

✨ **Real-time Chat Interface**
- Send messages and receive responses from the AI model
- View full conversation history
- Auto-scroll to latest messages

🟢 **Connection Status**
- Real-time indicator showing connection to inference server
- Visual feedback when server is disconnected
- Automatic status checks every 5 seconds

🎯 **User-Friendly**
- Clean, modern UI with gradient background
- Responsive design (works on mobile)
- Loading indicators while waiting for responses
- Clear/reset conversation history button

## File Structure

```
frontend/
├── public/           # Static files
│   ├── index.html
│   └── manifest.json
├── src/
│   ├── App.js       # Main chat component
│   ├── App.css      # Chat styling
│   ├── index.js     # React entry point
│   └── index.css    # Global styles
├── package.json
└── README.md
```

## Troubleshooting

- **Blank page**: Check browser console (F12) for errors
- **"Cannot connect to API"**: Ensure backend is running on port 5000
- **No response from model**: Check backend status endpoint
- **Styling issues**: Clear browser cache (Ctrl+Shift+Delete)

## Available Scripts

- `npm start` - Start development server
- `npm build` - Create production build
- `npm test` - Run tests
- `npm eject` - Eject from Create React App (irreversible)

# DEV WEB - React/Node.js

Interface de chat web en React avec backend Node.js (Express) connecte a Ollama.

## Fonctionnalites

- Chat temps reel avec historique de conversation
- Etat de connexion au serveur (connecte / deconnecte)
- Parametres d inference ajustables (temperature, top-p, max tokens)
- Lancement en une commande depuis ce dossier

## Architecture

- frontend/: React + Vite (http://localhost:5173)
- backend/: Node.js + Express (http://localhost:3001)
- Ollama cible: (http://13.222.248.247:11434)

## Lancement (une commande)

```powershell
./run.ps1
```

## Alternative manuelle

```powershell
npm install
npm run install:all
npm run dev
```

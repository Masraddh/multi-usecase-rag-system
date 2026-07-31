# RAG AI Assistant Suite Documentation

## Architecture
Combines sliding-window chunking, TF-IDF vector search, FastAPI backend, and Next.js frontend.

## Installation
```bash
pip install -r requirements.txt
npm install --prefix frontend
```

## Execution
Start backend: `uvicorn backend.main:app --port 8000`
Start frontend: `npm run dev --prefix frontend`

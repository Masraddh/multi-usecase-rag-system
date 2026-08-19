@echo off
title RAG AI Assistant Suite Launcher
echo ==================================================================
echo   LAUNCHING RAG AI ASSISTANT SUITE FULL STACK PLATFORM
echo ==================================================================
echo.
echo 1. Starting FastAPI Python Backend API Server (http://localhost:8000)...
start "RAG Backend Server (Port 8000)" cmd /k "python -m uvicorn backend.main:app --port 8000 --reload"

echo 2. Starting Next.js Frontend Development Server (http://localhost:3000)...
start "RAG Frontend Server (Port 3000)" cmd /k "cd frontend && npm run dev"

echo 3. Opening Web Browser...
timeout /t 3 >nul
start http://localhost:3000

echo.
echo Full Stack Application Services Launched Successfully!
pause

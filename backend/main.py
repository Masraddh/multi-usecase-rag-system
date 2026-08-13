import os
import sys
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Ensure backend directory is in python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

try:
    from backend.api.routes import router as api_router
except ModuleNotFoundError:
    from api.routes import router as api_router


app = FastAPI(
    title="🧠 RAG AI Assistant Suite API",
    description="Enterprise-Grade Multi-Use Case Retrieval-Augmented Generation Platform API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for Next.js frontend and Vercel deployments
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "title": "🧠 RAG AI Assistant Suite API",
        "status": "online",
        "docs": "/docs",
        "health": "/api/v1/health",
        "assistants": "/api/v1/assistants"
    }


@app.exception_handler(Exception)
def global_exception_handler(request: Request, exc: Exception):
    """Ensure internal errors never expose Python tracebacks to the client."""
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred. Please try again or check settings."}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

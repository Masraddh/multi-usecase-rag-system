import os
import io
import traceback
from typing import List
from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form

from models.schemas import (
    AssistantInfo,
    ChatRequest,
    ChatResponse,
    RetrieveRequest,
    RetrieveResponse,
    RetrievedChunk,
    SystemStats,
    SettingsUpdate,
    HealthResponse
)
from use_cases.registry import get_registry
from engine.document_loaders import extract_text

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check():
    registry = get_registry()
    has_key = bool(os.getenv("ANTHROPIC_API_KEY"))
    return HealthResponse(
        status="online",
        version="1.0.0",
        assistants_loaded=len(registry.assistants),
        api_key_configured=has_key
    )


@router.get("/assistants", response_model=List[AssistantInfo], tags=["Assistants"])
def list_assistants():
    """List metadata for all 5 registered RAG AI Assistants."""
    registry = get_registry()
    return registry.list_assistants()


@router.get("/assistants/{assistant_id}", response_model=AssistantInfo, tags=["Assistants"])
def get_assistant_detail(assistant_id: str):
    """Retrieve configuration and status of a specific AI Assistant."""
    registry = get_registry()
    data = registry.get_assistant(assistant_id)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Assistant '{assistant_id}' not found. Valid options: {list(registry.assistants.keys())}"
        )
    return data["info"]


async def _process_upload(assistant_id: str, file: UploadFile):
    registry = get_registry()
    ast = registry.get_assistant(assistant_id)
    if not ast:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Assistant '{assistant_id}' not found."
        )

    contents = await file.read()
    filename = file.filename or "uploaded_document.pdf"

    # Document Reader Extraction & Validation
    try:
        doc_text, num_pages, num_words, num_chars = DocumentReader.extract_text(contents, filename=filename)
    except ValueError as ve:
        tb = traceback.format_exc()
        print(f"[DOCUMENT READER VALUE ERROR]:\n{tb}", flush=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        tb = traceback.format_exc()
        print(f"[DOCUMENT UPLOAD UNHANDLED EXCEPTION]:\n{tb}", flush=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to read this document ({type(e).__name__}: {str(e)}). Please upload a valid PDF, DOCX, TXT or Markdown file."
        )

    # Index into RAG engine & update registry metadata
    result = registry.update_assistant_dataset(
        assistant_id=assistant_id,
        new_text=doc_text,
        filename=filename,
        num_pages=num_pages,
        num_words=num_words,
        num_chars=num_chars
    )

    return {
        "message": f"Successfully parsed and indexed '{filename}'!",
        "filename": filename,
        "num_pages": result["num_pages"],
        "num_words": result["num_words"],
        "num_chars": result["num_chars"],
        "num_chunks": result["num_chunks"],
        "vocab_size": result.get("vocab_size", 0),
        "matrix_shape": result.get("matrix_shape", "(0, 0)"),
        "first_chunk_preview": result.get("first_chunk_preview", ""),
        "active_source": result["active_source"],
        "index_status": result["index_status"],
        "retrieval_ready": result["retrieval_ready"],
        "assistant_id": assistant_id
    }


@router.post("/assistants/{assistant_id}/upload", tags=["Assistants"])
async def upload_document_for_assistant(assistant_id: str, file: UploadFile = File(...)):
    """Upload a document for a specific assistant by ID in path."""
    return await _process_upload(assistant_id, file)


@router.post("/upload", tags=["Document Upload"])
async def upload_document(assistant_id: str = Form(...), file: UploadFile = File(...)):
    """Upload a document for an assistant specified in form data."""
    return await _process_upload(assistant_id, file)


@router.post("/assistants/{assistant_id}/reset", tags=["Assistants"])
def reset_document_for_assistant(assistant_id: str):
    """
    Reset an assistant's active dataset back to its original default dataset.
    """
    registry = get_registry()
    ast = registry.get_assistant(assistant_id)
    if not ast:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Assistant '{assistant_id}' not found."
        )

    result = registry.reset_assistant_dataset(assistant_id)
    return {
        "message": f"Successfully reset '{assistant_id}' back to default dataset '{result['filename']}'.",
        "filename": result["filename"],
        "num_pages": result["num_pages"],
        "num_words": result["num_words"],
        "num_chunks": result["num_chunks"],
        "active_source": result["active_source"],
        "assistant_id": assistant_id
    }


@router.post("/chat", response_model=ChatResponse, tags=["RAG Execution"])
def chat_with_assistant(req: ChatRequest):
    """
    Process user query through selected assistant RAG engine.
    Executes TF-IDF vector retrieval and LLM completion with strict grounding.
    """
    if not req.query or not req.query.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query prompt cannot be empty."
        )

    registry = get_registry()
    data = registry.get_assistant(req.assistant_id)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Assistant '{req.assistant_id}' not found."
        )

    engine = data["engine"]

    # Update parameters if custom overrides provided in request
    engine.update_params(
        max_words=req.max_words,
        overlap=req.overlap,
        top_k=req.top_k,
        api_key=req.api_key
    )

    try:
        detailed = engine.ask_detailed(req.query.strip())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing RAG query: {str(e)}"
        )

    registry.record_query(
        assistant_id=req.assistant_id,
        query=req.query,
        latency=detailed["latency_ms"],
        score=detailed["max_similarity_score"]
    )

    retrieved_models = [RetrievedChunk(**chunk) for chunk in detailed["retrieved_chunks"]]

    return ChatResponse(
        assistant_id=req.assistant_id,
        query=req.query,
        answer=detailed["answer"],
        citations=detailed["citations"],
        retrieved_chunks=retrieved_models,
        max_similarity_score=detailed["max_similarity_score"],
        latency_ms=detailed["latency_ms"]
    )


@router.post("/retrieve", response_model=RetrieveResponse, tags=["RAG Vector Search"])
def preview_retrieval(req: RetrieveRequest):
    """
    Perform TF-IDF Cosine Similarity vector retrieval without calling the LLM.
    """
    registry = get_registry()
    data = registry.get_assistant(req.assistant_id)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Assistant '{req.assistant_id}' not found."
        )

    engine = data["engine"]
    raw_results = engine.retrieve(req.query, top_k=req.top_k)

    chunks = []
    for idx, score, text in raw_results:
        chunks.append(RetrievedChunk(
            chunk_index=idx,
            similarity_score=round(score, 4),
            confidence_percent=round(score * 100, 1),
            text=text,
            keywords=[]
        ))

    return RetrieveResponse(
        assistant_id=req.assistant_id,
        query=req.query,
        chunks=chunks
    )


@router.get("/stats", response_model=SystemStats, tags=["Analytics"])
def get_system_stats():
    """Retrieve platform analytics metrics across all registered assistants."""
    registry = get_registry()
    return registry.get_stats()


@router.post("/settings", tags=["Configuration"])
def update_settings(settings: SettingsUpdate):
    """Update environment variables and global defaults at runtime."""
    if settings.api_key:
        os.environ["ANTHROPIC_API_KEY"] = settings.api_key
        registry = get_registry()
        for ast in registry.assistants.values():
            ast["engine"].update_params(api_key=settings.api_key)

    return {"message": "Settings updated successfully.", "api_key_set": bool(os.getenv("ANTHROPIC_API_KEY"))}

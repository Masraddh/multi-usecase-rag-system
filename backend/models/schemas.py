from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class AssistantInfo(BaseModel):
    id: str = Field(..., description="Unique assistant identifier")
    name: str = Field(..., description="Display name of assistant")
    icon: str = Field(..., description="Lucide icon name or emoji")
    persona: str = Field(..., description="Role and instructions persona")
    description: str = Field(..., description="Short explanation of assistant purpose")
    max_words: int = Field(..., description="Current chunk max words parameter")
    overlap: int = Field(..., description="Current chunk word overlap parameter")
    top_k: int = Field(..., description="Current top K retrieval parameter")
    total_docs: int = Field(1, description="Number of indexed documents")
    total_chunks: int = Field(..., description="Number of generated text chunks")
    active_source: str = Field("default", description="'default' or 'uploaded'")
    filename: str = Field("default_dataset.txt", description="Active document filename")
    num_pages: int = Field(1, description="Active document page count")
    num_words: int = Field(0, description="Active document total word count")
    num_chars: int = Field(0, description="Active document total character count")
    vocab_size: int = Field(0, description="TF-IDF vocabulary size")
    matrix_shape: str = Field("(0, 0)", description="TF-IDF matrix shape string")
    first_chunk_preview: str = Field("", description="Preview text of the first chunk")
    index_status: str = Field("✅ Successfully Indexed", description="Index status text indicator")
    retrieval_ready: bool = Field(True, description="Whether TF-IDF retrieval index is ready")
    is_custom: bool = Field(False, description="Whether active document is a custom upload")
    documents: List[str] = Field(default_factory=list, description="List of active knowledge base filenames")
    build_time_ms: float = Field(0.0, description="Knowledge base index build duration in milliseconds")
    sample_queries: List[str] = Field(default_factory=list, description="Pre-loaded sample user queries")


class RetrievedChunk(BaseModel):
    chunk_index: int = Field(..., description="1-based source chunk index")
    similarity_score: float = Field(..., description="Cosine similarity score (0.0 to 1.0)")
    confidence_percent: float = Field(..., description="Confidence percentage")
    text: str = Field(..., description="Retrieved chunk text content")
    keywords: List[str] = Field(default_factory=list, description="Highlighted query matching terms")


class ChatRequest(BaseModel):
    assistant_id: str = Field(..., description="Target AI assistant ID")
    query: str = Field(..., description="User prompt query")
    max_words: Optional[int] = Field(None, description="Optional override chunk size")
    overlap: Optional[int] = Field(None, description="Optional override chunk overlap")
    top_k: Optional[int] = Field(None, description="Optional override top_k parameter")
    grounded_mode: Optional[bool] = Field(True, description="Strict Grounded RAG mode if True, Open General Knowledge LLM mode if False")
    api_key: Optional[str] = Field(None, description="Optional per-session Anthropic API Key override")


class ChatResponse(BaseModel):
    assistant_id: str
    query: str
    answer: str
    citations: List[str]
    retrieved_chunks: List[RetrievedChunk]
    max_similarity_score: float
    latency_ms: float


class RetrieveRequest(BaseModel):
    assistant_id: str
    query: str
    top_k: Optional[int] = None


class RetrieveResponse(BaseModel):
    assistant_id: str
    query: str
    chunks: List[RetrievedChunk]


class SystemStats(BaseModel):
    total_documents: int
    total_chunks: int
    avg_retrieval_score: float
    current_model: str
    avg_response_time_ms: float
    total_queries: int
    assistant_breakdown: List[Dict[str, Any]]


class SettingsUpdate(BaseModel):
    api_key: Optional[str] = None
    model: Optional[str] = None
    default_max_words: Optional[int] = None
    default_overlap: Optional[int] = None
    default_top_k: Optional[int] = None


class HealthResponse(BaseModel):
    status: str
    version: str
    assistants_loaded: int
    api_key_configured: bool

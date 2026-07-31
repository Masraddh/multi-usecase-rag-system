# 🧠 RAG AI Assistant Suite - FastAPI Backend

High-performance, production-ready FastAPI backend for the **RAG AI Assistant Suite**. Reuses a modular `RAGEngine` combining sliding-window word chunking, TF-IDF vectorization, Cosine Similarity search, and Anthropic Claude Sonnet integration.

## 🚀 Features

- **5 AI Assistants**:
  - 🎤 Interview Preparation Coach
  - 🎓 Campus FAQ Helpdesk
  - 📚 Exam Study Buddy (fine-tuned chunking: 50 words / 12 overlap)
  - 🛒 Ecommerce Customer Support (Voyager Pro Backpack)
  - 💻 Code & API Documentation Expert (`RAGEngine`)
- **Strict Grounding Enforcement**:
  - Answers strictly using retrieved document context.
  - Guarantees `I don't have that information.` for out-of-scope queries.
  - Automatic `[Source X]` citations.
- **Self-Documenting OpenAPI**: Interactive Swagger UI at `/docs`.
- **Production Performance**: TF-IDF matrices and vectorizers cached to prevent recomputation.

## 🛠 Quickstart

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set environment variables (Optional, offline fallback included)
export ANTHROPIC_API_KEY="your_api_key"

# 3. Start server
python main.py
```

Server runs on `http://localhost:8000`. Interactive docs: `http://localhost:8000/docs`.

## 🧪 Testing

```bash
pytest tests/ -v
```

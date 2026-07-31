# 🧠 RAG AI Assistant Suite – Enterprise Retrieval-Augmented Generation Platform

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Next.js 15](https://img.shields.io/badge/Frontend-Next.js%2015-black)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688)
![Anthropic Claude](https://img.shields.io/badge/LLM-Anthropic%20Claude%203.7%20Sonnet-violet)
![scikit-learn](https://img.shields.io/badge/Vector%20Search-TF--IDF%20%2B%20Cosine%20Similarity-orange)

An enterprise-grade, multi-use case Retrieval-Augmented Generation (RAG) platform hosting **five independent specialized AI Assistants** powered by a single, modular Python `RAGEngine`.

---

## 🌟 Executive Overview

The **RAG AI Assistant Suite** is designed to solve knowledge boundary and hallucination problems in domain-specific AI systems. By combining word-level sliding window chunking (`max_words`, `overlap`), TF-IDF vectorization with cached matrices, Cosine Similarity matching, and strict prompt grounding via Anthropic Claude Sonnet, the platform provides zero-hallucination answers with explicit source citations.

---

## 🤖 The 5 AI Assistants

| Assistant | Persona | Dataset Covered | Tuned Chunk Parameters |
| :--- | :--- | :--- | :--- |
| **🎤 1. Interview Prep Coach** | Professional Interview Coach | Candidate Resume, React Native, Power BI, SQL, RAG projects | `max_words: 80`, `overlap: 15`, `top_k: 2` |
| **🎓 2. Campus FAQ Helpdesk** | Friendly Student Helpdesk | Hostel curfew, Library borrowing rules, Fee penalties, Internal Exams | `max_words: 90`, `overlap: 20`, `top_k: 3` |
| **📚 3. Exam Study Buddy** | Patient OS Teacher | CPU Scheduling (FCFS, SJF, Round Robin, Convoy Effect) | `max_words: 50`, `overlap: 12`, `top_k: 3` |
| **🛒 4. Ecommerce Support Agent** | Customer Support Agent | Voyager Pro 30L Backpack specs, 15-day return policy, Warranty | `max_words: 80`, `overlap: 15`, `top_k: 2` |
| **💻 5. Code Documentation Expert** | Technical Documentation Expert | `RAGEngine` API documentation (`chunk_text`, `retrieve`, `ask`) | `max_words: 80`, `overlap: 20`, `top_k: 3` |

---

## 🏗 System Architecture Diagram

```mermaid
flowchart TD
    User([User Prompt Query]) --> UI[Next.js 15 App Router Frontend]
    UI --> API[FastAPI Backend /api/v1/chat]
    API --> Reg[Assistant Registry]
    Reg --> Engine[RAGEngine Instance]
    
    subgraph Vector Retrieval Engine
        Engine --> Chunk[Sliding Window Word Chunking max_words, overlap]
        Chunk --> TFIDF[TfidfVectorizer scikit-learn]
        TFIDF --> Cosine[Cosine Similarity Matrix Calculation]
        Cosine --> TopK[Top-K Highest Relevance Chunks Filter]
    end
    
    TopK --> Grounding[Strict Grounding System Prompt]
    Grounding --> Anthropic[Anthropic Claude 3.7 Sonnet API]
    Anthropic --> Citation[Source Citations [Source 1], [Source 2] Synthesis]
    
    Citation --> Response[JSON ChatResponse with Latency & Scores]
    Response --> UI
```

---

## 📂 Repository Folder Structure

```
RAG_AI_Assistant_Suite/
├── backend/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py          # REST Endpoints (/health, /assistants, /chat, /retrieve, /stats)
│   ├── data/
│   │   ├── interview_prep.txt # Interview dataset
│   │   ├── campus_faq.txt     # Campus policies dataset
│   │   ├── study_buddy.txt    # Operating Systems CPU scheduling dataset
│   │   ├── ecommerce.txt      # Backpack product dataset
│   │   └── code_docs.txt      # RAGEngine API documentation dataset
│   ├── engine/
│   │   ├── __init__.py
│   │   └── rag_engine.py      # Core modular RAGEngine class
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py         # Pydantic v2 schemas
│   ├── use_cases/
│   │   ├── __init__.py
│   │   └── registry.py        # Singleton registry for 5 assistants
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_engine.py     # Unit tests for chunking, retrieval & grounding
│   │   └── test_api.py        # FastAPI integration test suite
│   ├── main.py                # FastAPI entry point & CORS configuration
│   ├── requirements.txt       # Python dependencies
│   └── README.md
├── frontend/
│   ├── app/
│   │   ├── layout.tsx         # Root layout with navbar & footer
│   │   ├── page.tsx           # Hero landing page & features
│   │   ├── chat/page.tsx      # ChatGPT/Perplexity AI Studio Workspace
│   │   ├── dashboard/page.tsx # System metrics analytics dashboard
│   │   ├── settings/page.tsx  # API Key & hyperparameter tuner
│   │   └── about/page.tsx     # Technical architecture docs
│   ├── components/
│   │   ├── Navbar.tsx         # Navigation bar with dark/light mode
│   │   ├── Footer.tsx         # Footer links & status
│   │   ├── Sidebar.tsx        # Assistant selector & RAG sliders
│   │   ├── MessageItem.tsx    # Message bubble with citation badges
│   │   ├── RetrievalPanel.tsx # Vector search inspector drawer
│   │   └── StatsCard.tsx      # Metric widget
│   ├── services/
│   │   └── api.ts             # API client wrapper
│   ├── styles/
│   │   └── globals.css        # Glassmorphism & HSL design tokens
│   ├── package.json
│   ├── next.config.js
│   ├── tsconfig.json
│   └── tailwind.config.js
├── vercel.json                # Vercel frontend deployment manifest
├── render.yaml                # Render backend web service definition
└── README.md
```

---

## ⚡ Quickstart & Local Setup

### Prerequisites
- Python 3.10+
- Node.js 18+ & npm

### 1. Backend Setup (FastAPI)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Set your Anthropic API Key
export ANTHROPIC_API_KEY="sk-ant-api03-..."

# Run backend server
python main.py
```
FastAPI server starts on `http://localhost:8000`. Interactive Swagger UI available at `http://localhost:8000/docs`.

### 2. Frontend Setup (Next.js 15)

```bash
# Navigate to frontend
cd frontend

# Install packages
npm install

# Start Next.js development server
npm run dev
```
Web application opens at `http://localhost:3000`.

---

## 🧪 Automated Testing

The backend includes a comprehensive `pytest` test suite:

```bash
pytest backend/tests/ -v
```

Tests verify:
- Word sliding window chunking with overlap boundaries
- TF-IDF Cosine Similarity vector ranking
- Strict grounding fallback (`I don't have that information.`)
- `[Source X]` citation tag formatting
- OpenAPI endpoints (`/health`, `/assistants`, `/chat`, `/retrieve`, `/stats`)

---

## 🚀 Deployment Instructions

### Frontend Deployment (Vercel)

1. Import the repository into your Vercel Dashboard.
2. Set **Root Directory** to `frontend`.
3. Set **Build Command** to `npm run build`.
4. Add Environment Variable:
   - `NEXT_PUBLIC_API_URL`: `https://your-render-backend.onrender.com/api/v1`
5. Click **Deploy**.

### Backend Deployment (Render)

1. Create a new **Web Service** on Render connected to this GitHub repo.
2. Select **Python 3** environment.
3. Set **Build Command**: `pip install -r backend/requirements.txt`.
4. Set **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port 10000`.
5. Add Environment Variables:
   - `ANTHROPIC_API_KEY`: `your_anthropic_api_key`
6. Click **Create Web Service**.

---

## 📌 Technical Interview Q&A

### Q1: How does the sliding window chunking algorithm preserve context?
**Answer**: Words are split sequentially up to `max_words`. By setting `overlap > 0`, consecutive chunks share trailing/leading words (e.g. 15 shared words). This prevents key phrases, entity names, or complex concepts from being cut in half at chunk boundaries.

### Q2: Why use TF-IDF with Cosine Similarity over heavy vector databases for domain datasets?
**Answer**: For targeted SaaS datasets (e.g. candidate resumes, campus handbooks, product manuals), TF-IDF vectorization executes in sub-millisecond speeds without external database latency, zero operational cost, and deterministic exact-term matching. The vectorizer matrix is cached upon engine instantiation to prevent recomputation.

### Q3: How is zero-hallucination guaranteed?
**Answer**: System prompts explicitly dictate that the LLM must rely *strictly* on retrieved text chunks. If top Cosine Similarity scores fall below threshold or context is absent, the engine bypasses extrapolation and outputs: `"I don't have that information."`

---

## 📝 License
This project is open-source and available under the [MIT License](LICENSE).

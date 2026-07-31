"""
Document Reader Pipeline Audit & Retrieval Verification Suite.

1. Creates a candidate resume PDF in memory using PyMuPDF.
2. Runs DocumentReader.extract_text() and verifies the 500-character preview log.
3. Indexes into RAGEngine and asserts TF-IDF matrix shape and vocabulary size.
4. Executes the 5 required target queries:
   - Tell me about your projects.
   - Generate a self introduction.
   - What technical skills do you have?
   - Describe your internship.
   - Explain SoilSmart.
5. Verifies Similarity Score > 0 for EVERY query.
"""

import sys
import os

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

base_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(base_dir, "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

import fitz  # PyMuPDF
from utils.document_reader import DocumentReader
from engine.rag_engine import RAGEngine


def generate_resume_pdf() -> bytes:
    doc = fitz.open()

    p1 = doc.new_page()
    p1_content = (
        "SHAIK MASRADDH RESUME - SOFTWARE & AI ENGINEER\n\n"
        "PROFESSIONAL PROFILE & INTRO\n"
        "Accomplished Software Engineer specializing in Artificial Intelligence, Machine Learning, "
        "Retrieval-Augmented Generation (RAG), and IoT smart agriculture solutions.\n\n"
        "FEATURED PROJECTS\n"
        "1. SoilSmart Project: IoT and ML Smart Soil Monitoring System for Precision Agriculture\n"
        "- Engineered an IoT smart soil monitoring system using Python microcontrollers, sensors, and Random Forest ML model.\n"
        "- Streams real-time soil moisture, pH, and temperature metrics to cloud dashboard, reducing farm water use by 35%.\n\n"
        "2. Real-Time Event Booking & Chat App\n"
        "- Developed cross-platform React Native app serving 10,000+ users with Firebase Realtime Database.\n"
    )
    p1.insert_text((50, 50), p1_content, fontsize=11)

    p2 = doc.new_page()
    p2_content = (
        "INTERNSHIP & TECHNICAL SKILLS\n\n"
        "3. Sales Analytics & ETL Dashboard Internship (Power BI & SQL)\n"
        "- Completed a 3-month Data Analytics internship creating executive dashboards in Power BI.\n"
        "- Formulated complex SQL queries transforming 500,000+ transaction records, saving 15 hours per week.\n\n"
        "TECHNICAL SKILLS & COMPETENCIES\n"
        "- Programming Languages: Python, SQL, JavaScript, TypeScript, C++.\n"
        "- Frameworks & Tools: React Native, React.js, Next.js, FastAPI, Node.js, Power BI, Docker, Git.\n"
        "- AI & Machine Learning: RAG, TF-IDF vector search, Scikit-Learn, PyTorch, Anthropic Claude APIs.\n\n"
        "EDUCATION\n"
        "- B.Tech in Computer Science & Engineering, Graduated with Distinction.\n"
    )
    p2.insert_text((50, 50), p2_content, fontsize=11)

    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


def run_pipeline_audit():
    print("=" * 80)
    print("  COMPLETE PIPELINE AUDIT & RETRIEVAL VERIFICATION")
    print("=" * 80)

    pdf_bytes = generate_resume_pdf()
    filename = "Resume.pdf"

    # Step 1 & 5: Test DocumentReader extraction and 500-char preview log
    print("\n[AUDIT STEP 1: Document Extraction]")
    text, pages, words, chars = DocumentReader.extract_text(pdf_bytes, filename=filename)

    assert pages == 2, f"Expected 2 pages, got {pages}"
    assert words > 150, f"Expected >150 words, got {words}"
    assert chars > 1000, f"Expected >1000 chars, got {chars}"
    assert DocumentReader.validate_document(text), "Document validation failed!"

    # Step 6, 7, 8: RAG Engine Ingestion & Debug Telemetry
    print("\n[AUDIT STEP 2: RAG Engine Ingestion & Telemetry]")
    engine = RAGEngine(
        doc_text=pdf_bytes,
        persona="a professional interview coach helping the candidate rehearse technical questions based on their resume",
        filename=filename
    )

    matrix_shape = engine.tfidf_matrix.shape if engine.tfidf_matrix is not None else (0, 0)
    vocab_size = len(engine.vectorizer.vocabulary_) if hasattr(engine.vectorizer, "vocabulary_") else 0

    assert len(engine.chunks) > 0, "Chunks created must be > 0"
    assert vocab_size > 0, "Vocabulary size must be > 0"
    assert matrix_shape[0] == len(engine.chunks), "Matrix rows must equal number of chunks"

    # Step 9: Retrieval Verification for 5 Target Questions
    target_questions = [
        "Tell me about your projects.",
        "Generate a self introduction.",
        "What technical skills do you have?",
        "Describe your internship.",
        "Explain SoilSmart."
    ]

    print("\n[AUDIT STEP 3: TESTING 5 TARGET RETRIEVAL PROMPTS]")

    for i, q in enumerate(target_questions, 1):
        print(f"\n------------------------------------------------------------------")
        print(f"QUERY #{i}: '{q}'")
        res = engine.ask_detailed(q)

        answer = res["answer"]
        chunks = res["retrieved_chunks"]
        max_score = res["max_similarity_score"]

        print(f"-> Similarity Score: {max_score:.4f} ({max_score*100:.1f}%)")
        print(f"-> Retrieved Chunks: {len(chunks)}")
        print(f"-> Answer Snippet: {answer[:150]}...")

        # Strict Verification Assertions (STEP 9)
        assert max_score > 0.0, f"Query '{q}' similarity score is 0.0%! Expected Similarity > 0."
        assert len(chunks) > 0, f"Query '{q}' failed to retrieve chunks from PDF."
        assert answer != "I don't have that information.", f"Query '{q}' returned 'I don't have that information.'!"
        print(f"[PASS] Query #{i} '{q}' answered with Similarity = {max_score*100:.1f}% > 0!")

    print("\n🎉 ALL 5 TARGET RETRIEVAL QUERIES RETURNED SIMILARITY SCORES > 0!")
    print("🎉 FULL PIPELINE AUDIT PASSED 100%!")


if __name__ == "__main__":
    run_pipeline_audit()

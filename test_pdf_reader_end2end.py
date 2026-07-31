"""
End-to-End Automated Test Suite for DocumentReader & PDF Ingestion.

1. Generates a realistic multi-page candidate resume PDF in memory.
2. Invokes DocumentReader.extract_text() to verify text extraction, cleaning, and validation.
3. Initializes RAGEngine directly from PDF bytes.
4. Verifies TF-IDF matrix generation, vocabulary size, matrix shape, and debug telemetry.
5. Executes the 5 required target prompts:
   - Generate a self introduction
   - Explain my projects
   - Tell me about my internship
   - What are my technical skills?
   - Describe my SoilSmart project.
6. Asserts that EVERY question returns grounded, non-zero similarity content from the PDF.
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


def generate_test_resume_pdf() -> bytes:
    """
    Generates a 2-page candidate resume PDF with PyMuPDF.
    """
    doc = fitz.open()

    # Page 1: Header, Intro, SoilSmart & Event Booking Projects
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

    # Page 2: Internship, Technical Skills, Education
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


def test_pdf_reader_end2end():
    print("=" * 80)
    print("  VERIFICATION TEST: DOCUMENT READER & FILE-BASED RAG PIPELINE")
    print("=" * 80)

    pdf_bytes = generate_test_resume_pdf()
    filename = "Resume.pdf"

    # 1. Test DocumentReader.extract_text()
    print("\n[STEP 1: DocumentReader.extract_text() Extraction]")
    text, pages, words, chars = DocumentReader.extract_text(pdf_bytes, filename=filename)
    
    print(f"-> Extracted Document Name: {filename}")
    print(f"-> Pages Read: {pages}")
    print(f"-> Characters Extracted: {chars}")
    print(f"-> Words Extracted: {words}")
    print(f"-> Document Validation: {'✅ VALID' if DocumentReader.validate_document(text) else '❌ INVALID'}")

    assert pages == 2, f"Expected 2 pages, got {pages}"
    assert words > 150, f"Expected >150 words, got {words}"
    assert chars > 1000, f"Expected >1000 chars, got {chars}"
    assert "SoilSmart" in text, "Text must contain SoilSmart project"

    # 2. Test RAGEngine Direct Initialization from PDF Bytes
    print("\n[STEP 2: RAGEngine Ingestion & Vector Indexing]")
    engine = RAGEngine(
        doc_text=pdf_bytes,
        persona="a professional interview coach helping the candidate rehearse technical questions based on their resume",
        max_words=80,
        overlap=15,
        top_k=3,
        filename=filename
    )

    matrix_shape = engine.tfidf_matrix.shape if engine.tfidf_matrix is not None else (0, 0)
    vocab_size = len(engine.vectorizer.vocabulary_) if hasattr(engine.vectorizer, "vocabulary_") else 0

    print(f"-> Chunks Created: {len(engine.chunks)}")
    print(f"-> Vocabulary Size: {vocab_size}")
    print(f"-> TF-IDF Matrix Shape: {matrix_shape}")
    print(f"-> Index Status: ✅ Successfully Indexed")
    print(f"-> Retrieval Status: ✅ Retrieval Ready")

    assert len(engine.chunks) > 0, "Chunks created must be > 0"
    assert vocab_size > 0, "Vocabulary size must be > 0"
    assert matrix_shape[0] == len(engine.chunks), "Matrix rows must equal number of chunks"

    # 3. Test 5 Required Question Prompts
    target_prompts = [
        "Generate a self introduction",
        "Explain my projects",
        "Tell me about my internship",
        "What are my technical skills?",
        "Describe my SoilSmart project."
    ]

    print("\n[STEP 3: TESTING 5 TARGET QUESTION PROMPTS ON PDF KNOWLEDGE BASE]")

    for i, q in enumerate(target_prompts, 1):
        print(f"\n------------------------------------------------------------------")
        print(f"PROMPT #{i}: '{q}'")
        res = engine.ask_detailed(q)
        
        answer = res["answer"]
        chunks = res["retrieved_chunks"]
        max_score = res["max_similarity_score"]

        print(f"-> Similarity Score: {max_score:.4f} ({max_score*100:.1f}%)")
        print(f"-> Retrieved Chunks Count: {len(chunks)}")
        print(f"-> Answer Snippet:\n{answer[:180]}...")

        # Strict Verification Assertions
        assert answer != "I don't have that information.", f"Query '{q}' returned 'I don't have that information.'! PDF ingestion incomplete."
        assert max_score > 0.0, f"Query '{q}' similarity score MUST be > 0.0%"
        assert len(chunks) > 0, f"Query '{q}' MUST retrieve context chunks from PDF."
        print(f"[PASS] Prompt #{i} '{q}' answered successfully from PDF!")

    # 4. Out of Domain Query Test
    irr_query = "What is Quantum Computing superposition?"
    print(f"\n------------------------------------------------------------------")
    print(f"IRRELEVANT QUERY TEST: '{irr_query}'")
    res_irr = engine.ask_detailed(irr_query)
    assert res_irr["answer"] == "I don't have that information.", "Out-of-domain query MUST return 'I don't have that information.'"
    print(f"[PASS] Out-of-domain query correctly rejected!")

    print("\n🎉 ALL DOCUMENT READER & PDF QUESTION ANSWERING VERIFICATION TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    test_pdf_reader_end2end()

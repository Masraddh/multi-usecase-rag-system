"""
Automated Verification Suite for Document Extraction & Ingestion Pipeline.

Generates a realistic candidate resume PDF in memory using PyMuPDF (fitz).
Tests the complete document ingestion pipeline:
- load_pdf() with PyMuPDF -> pdfplumber -> pypdf fallback chain
- extract_text() & clean_text()
- chunk_document() & build_vector_index()
- reload_index() & debug validation stats output

Executes and asserts response for the 5 required queries:
1. Tell me about your projects.
2. Generate a self introduction.
3. What technical skills do you have?
4. Describe your internship.
5. Explain your SoilSmart project.
"""

import sys
import os
import io

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

base_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(base_dir, "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

import fitz  # PyMuPDF
from engine.document_loaders import extract_text, load_pdf, clean_text
from engine.rag_engine import RAGEngine
from use_cases.registry import get_registry


def create_sample_resume_pdf_bytes() -> bytes:
    """
    Creates a multi-page PDF document in bytes containing rich candidate resume details.
    """
    doc = fitz.open()

    # Page 1: Header, Profile & SoilSmart Project
    page1 = doc.new_page()
    text_p1 = (
        "SHAIK MASRADDH - AI & SOFTWARE ENGINEER RESUME\n\n"
        "PROFESSIONAL PROFILE SUMMARY\n"
        "Experienced Software Engineer specializing in Artificial Intelligence, Retrieval-Augmented Generation (RAG) "
        "systems, full-stack web applications, and Internet of Things (IoT) precision agriculture solutions.\n\n"
        "KEY FEATURED PROJECTS\n\n"
        "Project 1: SoilSmart - Smart Soil Monitoring System (IoT & Machine Learning)\n"
        "- Engineered an IoT and ML-driven smart soil monitoring system for precision agriculture using Python, microcontrollers, and Random Forest classifier.\n"
        "- Integrated real-time soil moisture, pH, and temperature sensors streaming data via MQTT protocol to an automated analytics dashboard.\n"
        "- Improved crop yield recommendations by 28% and reduced water consumption by 35% across test agricultural farms.\n\n"
        "Project 2: Real-Time Event Booking & Live Chat App (React Native & Firebase)\n"
        "- Developed a cross-platform mobile application using React Native, WebSockets, and Firebase Realtime Database.\n"
        "- Handled real-time data streaming for live seat selection and instant push notifications, serving over 10,000 active users.\n"
        "- Optimized app rendering performance by reducing re-renders by 35% using React Hooks and custom memoization.\n"
    )
    page1.insert_text((50, 50), text_p1, fontsize=11)

    # Page 2: Internship, Technical Skills & Education
    page2 = doc.new_page()
    text_p2 = (
        "PROFESSIONAL INTERNSHIP & TECHNICAL SKILLS\n\n"
        "Project 3: Sales Analytics & ETL Dashboard Internship (Power BI & SQL)\n"
        "- Completed a 3-month Data Analytics internship building interactive executive dashboards in Power BI.\n"
        "- Wrote complex SQL queries and stored procedures to transform 500,000+ customer transaction records.\n"
        "- Automated weekly data refresh workflows, reducing manual report preparation time by 15 hours per week.\n\n"
        "TECHNICAL SKILLS & COMPETENCIES\n"
        "- Programming Languages: Python, SQL, JavaScript, TypeScript, C++.\n"
        "- Frameworks & Tools: React Native, React.js, Next.js, FastAPI, Node.js, Power BI, Docker, Git, MQTT.\n"
        "- AI & Machine Learning: Retrieval-Augmented Generation (RAG), TF-IDF vector search, Scikit-Learn, Anthropic Claude APIs, PyTorch.\n\n"
        "EDUCATION\n"
        "- Bachelor of Technology in Computer Science & Engineering (B.Tech CSE), Graduated with Distinction.\n"
    )
    page2.insert_text((50, 50), text_p2, fontsize=11)

    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


def test_pdf_extraction_and_rag_pipeline():
    print("=" * 80)
    print("  VERIFICATION TEST: COMPLETE PDF EXTRACTION & INGESTION PIPELINE")
    print("=" * 80)

    pdf_bytes = create_sample_resume_pdf_bytes()
    filename = "Shaik_Masraddh_Resume.pdf"

    # Step 1: Execute extract_text router
    cleaned_text, pages, words, chars = extract_text(filename, pdf_bytes)

    print("\n[STEP 1: PDF EXTRACTION TELEMETRY]")
    print(f"- File Name: {filename}")
    print(f"- Pages Read: {pages}")
    print(f"- Words Extracted: {words}")
    print(f"- Characters Extracted: {chars}")
    print(f"- Index Status: ✅ Successfully Extracted")

    assert pages == 2, f"Expected 2 pages, got {pages}"
    assert words > 200, f"Expected >200 words, got {words}"
    assert chars > 1000, f"Expected >1000 chars, got {chars}"
    assert "SoilSmart" in cleaned_text, "Extracted text must contain SoilSmart project"

    # Step 2: Index PDF into RAGEngine & Reload Index
    engine = RAGEngine(
        doc_text=cleaned_text,
        persona="a professional interview coach helping the candidate rehearse technical questions based on their resume",
        max_words=80,
        overlap=20,
        top_k=3
    )

    reload_stats = engine.reload_index(cleaned_text)
    assert reload_stats["num_chunks"] > 0, "Chunks generated must be > 0"
    assert reload_stats["vocab_size"] > 0, "TF-IDF Vocabulary size must be > 0"

    # Step 3: Test 5 Required Target Queries
    target_queries = [
        ("Tell me about your projects.", ["SoilSmart", "React Native", "Power BI", "Event Booking", "Project"]),
        ("Generate a self introduction.", ["Shaik", "Engineer", "Artificial Intelligence", "software", "profile"]),
        ("What technical skills do you have?", ["Python", "SQL", "JavaScript", "React", "Docker", "RAG"]),
        ("Describe your internship.", ["Sales Analytics", "ETL", "Power BI", "SQL", "internship"]),
        ("Explain your SoilSmart project.", ["SoilSmart", "soil monitoring", "precision agriculture", "IoT", "Random Forest"])
    ]

    print("\n[STEP 2: TESTING 5 TARGET QUESTION-ANSWERING PROMPTS ON PDF DATASET]")

    for idx, (query, expected_keywords) in enumerate(target_queries, 1):
        print(f"\n------------------------------------------------------------------")
        print(f"QUERY #{idx}: '{query}'")
        res = engine.ask_detailed(query)

        answer = res["answer"]
        chunks = res["retrieved_chunks"]
        max_score = res["max_similarity_score"]

        print(f"-> Similarity Score: {max_score:.4f} ({max_score*100:.1f}%)")
        print(f"-> Retrieved Chunks: {len(chunks)}")
        print(f"-> Response Snippet:\n{answer[:180]}...")

        # Assertions
        assert answer != "I don't have that information.", f"Query '{query}' should NOT return 'I don't have that information.'"
        assert max_score > 0.0, f"Query '{query}' MUST return non-zero similarity score."
        assert len(chunks) > 0, f"Query '{query}' MUST retrieve context chunks."
        assert any(k.lower() in answer.lower() for k in expected_keywords), \
            f"Answer for '{query}' should contain one of expected keywords: {expected_keywords}"

        print(f"[PASS] Query #{idx} '{query}' succeeded with grounded response!")

    # Step 4: Verify Out-of-Domain Rejection
    out_of_domain = "What is Quantum Computing superposition?"
    print(f"\n------------------------------------------------------------------")
    print(f"OUT-OF-DOMAIN QUERY: '{out_of_domain}'")
    res_irr = engine.ask_detailed(out_of_domain)
    assert res_irr["answer"] == "I don't have that information.", "Out-of-domain query MUST return 'I don't have that information.'"
    print(f"[PASS] Out-of-domain query correctly rejected!")

    print("\n🎉 ALL PDF PIPELINE & QUESTION ANSWERING VERIFICATION TESTS PASSED!")


if __name__ == "__main__":
    test_pdf_extraction_and_rag_pipeline()

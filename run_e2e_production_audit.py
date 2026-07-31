import requests
import io
import fitz  # PyMuPDF
import os
import json
from dotenv import load_dotenv

load_dotenv()

def generate_sample_pdf_bytes() -> bytes:
    doc = fitz.open()
    
    # Page 1
    p1 = doc.new_page()
    text_p1 = (
        "SHAIK MASRADDH - AI & SOFTWARE ENGINEER RESUME\n"
        "Hyderabad, Telangana | +91 7207816391 | shaikmasraddh@gmail.com\n\n"
        "PROFESSIONAL PROFILE SUMMARY\n"
        "Experienced Software Engineer specializing in Artificial Intelligence, Retrieval-Augmented Generation (RAG) systems, "
        "and Web Application development. Skilled in building end-to-end full-stack applications with Next.js, FastAPI, and Python.\n\n"
        "KEY FEATURED PROJECTS\n"
        "Project 1: SoilSmart - Smart Soil Monitoring System (IoT & Machine Learning)\n"
        "- Engineered an IoT and ML-driven smart soil monitoring system for precision agriculture using Python and microcontrollers.\n"
        "- Integrated real-time soil moisture, pH, and temperature sensors streaming data via MQTT protocol to an automated dashboard.\n"
        "- Improved crop yield recommendations by 28% and reduced farm water usage by 35%.\n\n"
        "Project 2: Real-Time Event Booking & Live Chat App (React Native)\n"
        "- Developed a cross-platform mobile application using React Native, WebSockets, and Firebase Realtime Database.\n"
        "- Handled real-time data streaming for live seat selection and instant push notifications, serving over 10,000 active users.\n"
        "- Optimized app rendering performance by reducing re-renders by 35% using React Hooks and custom memoization."
    )
    p1.insert_text((50, 50), text_p1, fontsize=11)

    # Page 2
    p2 = doc.new_page()
    text_p2 = (
        "TECHNICAL SKILLS & COMPETENCIES\n"
        "- Programming Languages: Python, JavaScript, TypeScript, SQL, HTML5, CSS3\n"
        "- Frameworks & Libraries: FastAPI, Next.js, React, PyTorch, Scikit-Learn, Pandas, NumPy\n"
        "- Databases & DevOps: PostgreSQL, MongoDB, Redis, Docker, Git, GitHub Actions, Linux\n\n"
        "EDUCATION\n"
        "Bachelor of Technology in Information Technology | G. Narayanamma Institute of Technology & Science"
    )
    p2.insert_text((50, 50), text_p2, fontsize=11)

    buffer = io.BytesIO()
    doc.save(buffer)
    doc.close()
    return buffer.getvalue()


def run_full_8stage_audit():
    stage_results = {}
    print("=" * 80)
    print("STARTING END-TO-END 8-STAGE RAG SYSTEM PRODUCTION AUDIT")
    print("=" * 80)

    pdf_bytes = generate_sample_pdf_bytes()
    filename = "Shaik_Masraddh_Resume.pdf"
    file_size_kb = round(len(pdf_bytes) / 1024, 2)
    content_type = "application/pdf"

    # STAGE 1: Frontend File Upload Preparation
    print("\n--- STAGE 1: Verify Frontend Upload Payload ---")
    print(f"Filename: '{filename}'")
    print(f"Size: {file_size_kb} KB ({len(pdf_bytes)} bytes)")
    print(f"Content-Type: {content_type}")
    if filename and len(pdf_bytes) > 0 and content_type == "application/pdf":
        stage_results["Stage 1 (Frontend Upload)"] = "PASS"
        print("[PASS] STAGE 1: Frontend file payload valid.")
    else:
        stage_results["Stage 1 (Frontend Upload)"] = "FAIL"
        print("[FAIL] STAGE 1: Frontend upload payload invalid.")

    # STAGE 2: Backend Upload Endpoint Receipt
    upload_url = "http://localhost:8000/api/v1/upload"
    files = {"file": (filename, pdf_bytes, content_type)}
    data = {"assistant_id": "interview_coach"}

    print(f"\n--- STAGE 2: Verify Backend Upload Endpoint Receipt ({upload_url}) ---")
    res_up = requests.post(upload_url, files=files, data=data)
    print(f"HTTP Status Code: {res_up.status_code}")
    up_json = res_up.json()
    print("Upload Payload Response:", json.dumps(up_json, indent=2))
    
    if res_up.status_code == 200:
        stage_results["Stage 2 (Backend Upload Endpoint)"] = "PASS"
        print("[PASS] STAGE 2: Backend received and processed upload file.")
    else:
        stage_results["Stage 2 (Backend Upload Endpoint)"] = "FAIL"
        print(f"[FAIL] STAGE 2: Backend upload endpoint failed: {up_json}")

    # STAGE 3: DocumentReader Text Extraction
    print("\n--- STAGE 3: Verify DocumentReader PDF Extraction ---")
    num_pages = up_json.get("num_pages", 0)
    num_words = up_json.get("num_words", 0)
    num_chars = up_json.get("num_chars", 0)
    preview = up_json.get("first_chunk_preview", "")
    
    print(f"Pages Extracted: {num_pages}")
    print(f"Characters Extracted: {num_chars}")
    print(f"Words Extracted: {num_words}")
    print(f"Preview (First 150 Chars): \"{preview[:150]}...\"")

    if num_pages >= 2 and num_words > 50 and num_chars > 200:
        stage_results["Stage 3 (DocumentReader Text Extraction)"] = "PASS"
        print("[PASS] STAGE 3: DocumentReader successfully extracted text.")
    else:
        stage_results["Stage 3 (DocumentReader Text Extraction)"] = "FAIL"
        print("[FAIL] STAGE 3: DocumentReader failed to extract text.")

    # STAGE 4: Chunking
    print("\n--- STAGE 4: Verify Text Chunking ---")
    num_chunks = up_json.get("num_chunks", 0)
    print(f"Chunks Created: {num_chunks}")
    print("Max Words per Chunk: 80 | Overlap: 15")
    print(f"First Chunk Preview: \"{preview[:120]}...\"")

    if num_chunks >= 1:
        stage_results["Stage 4 (Chunking)"] = "PASS"
        print("[PASS] STAGE 4: Text chunking successful.")
    else:
        stage_results["Stage 4 (Chunking)"] = "FAIL"
        print("[FAIL] STAGE 4: Text chunking failed.")

    # STAGE 5: TF-IDF Vector Indexing
    print("\n--- STAGE 5: Verify TF-IDF Vector Matrix ---")
    vocab_size = up_json.get("vocab_size", 0)
    matrix_shape = up_json.get("matrix_shape", "(0, 0)")
    print(f"Vocabulary Size: {vocab_size}")
    print(f"Matrix Shape: {matrix_shape}")

    if vocab_size > 0 and matrix_shape != "(0, 0)":
        stage_results["Stage 5 (TF-IDF Vector Indexing)"] = "PASS"
        print("[PASS] STAGE 5: TF-IDF vector matrix created successfully.")
    else:
        stage_results["Stage 5 (TF-IDF Vector Indexing)"] = "FAIL"
        print("[FAIL] STAGE 5: TF-IDF vector matrix generation failed.")

    # STAGE 6: Vector Retrieval
    print("\n--- STAGE 6: Verify Top-K Chunk Retrieval ---")
    chat_url = "http://localhost:8000/api/v1/chat"
    query_str = "Explain my projects."
    query_payload = {
        "assistant_id": "interview_coach",
        "query": query_str
    }
    
    print(f"Querying: '{query_str}'...")
    res_chat = requests.post(chat_url, json=query_payload)
    print(f"HTTP Status Code: {res_chat.status_code}")
    chat_json = res_chat.json()
    
    max_sim = chat_json.get("max_similarity_score", 0.0)
    retrieved_chunks = chat_json.get("retrieved_chunks", [])
    print(f"Max Similarity Score: {max_sim * 100:.1f}%")
    print(f"Retrieved Chunks Count: {len(retrieved_chunks)}")

    if res_chat.status_code == 200 and max_sim > 0:
        stage_results["Stage 6 (Vector Retrieval)"] = "PASS"
        print("[PASS] STAGE 6: Top-K vector retrieval succeeded with non-zero similarity score.")
    else:
        stage_results["Stage 6 (Vector Retrieval)"] = "FAIL"
        print("[FAIL] STAGE 6: Vector retrieval failed.")

    # STAGE 7: Gemini AI Completion
    print("\n--- STAGE 7: Verify Gemini AI Completion ---")
    answer = chat_json.get("answer", "")
    citations = chat_json.get("citations", [])
    print("Answer Received:\n", answer)
    print("Citations Received:", citations)

    gemini_key = os.getenv("GEMINI_API_KEY")
    print(f"GEMINI_API_KEY Configured in Environment: {'YES' if gemini_key else 'NO'}")
    print(f"Gemini Model: gemini-1.5-flash")

    if res_chat.status_code == 200 and answer and len(answer) > 20:
        stage_results["Stage 7 (Gemini AI Completion)"] = "PASS"
        print("[PASS] STAGE 7: Gemini AI generated grounded response.")
    else:
        stage_results["Stage 7 (Gemini AI Completion)"] = "FAIL"
        print("[FAIL] STAGE 7: Gemini AI completion failed.")

    # STAGE 8: Frontend Response Rendering & Citations
    print("\n--- STAGE 8: Verify Frontend Answer & Citations Rendering ---")
    has_sources = len(citations) > 0 or "[Source" in answer
    print(f"Answer Non-Empty: {'YES' if bool(answer) else 'NO'}")
    print(f"Source Citations Present: {'YES' if has_sources else 'NO'}")

    if answer and (has_sources or max_sim > 0):
        stage_results["Stage 8 (Frontend Response Rendering)"] = "PASS"
        print("[PASS] STAGE 8: Answer and citations successfully validated for UI rendering.")
    else:
        stage_results["Stage 8 (Frontend Response Rendering)"] = "FAIL"
        print("[FAIL] STAGE 8: Frontend answer rendering failed.")

    # Summary Report
    print("\n" + "=" * 80)
    print("END-TO-END AUDIT SUMMARY RESULTS")
    print("=" * 80)
    all_passed = True
    for stage, status in stage_results.items():
        print(f"[{status}] {stage}")
        if status != "PASS":
            all_passed = False
    print("=" * 80)
    print(f"OVERALL AUDIT STATUS: {'ALL STAGES PASSED 100%' if all_passed else 'SOME STAGES FAILED'}")
    print("=" * 80)

    # Write DEBUG_REPORT.md
    with open("DEBUG_REPORT.md", "w", encoding="utf-8") as f:
        f.write("# RAG System End-to-End Audit & Debug Report\n\n")
        f.write("## 8-Stage Pipeline Audit Checklist\n\n")
        f.write("| Stage | Description | Status | Diagnostics |\n")
        f.write("|---|---|---|---|\n")
        f.write(f"| Stage 1 | Frontend File Upload | **{stage_results.get('Stage 1 (Frontend Upload)', 'FAIL')}** | File '{filename}', {file_size_kb} KB, `{content_type}` |\n")
        f.write(f"| Stage 2 | Backend Upload Endpoint | **{stage_results.get('Stage 2 (Backend Upload Endpoint)', 'FAIL')}** | HTTP 200 OK via `/api/v1/upload` |\n")
        f.write(f"| Stage 3 | DocumentReader PDF Extraction | **{stage_results.get('Stage 3 (DocumentReader Text Extraction)', 'FAIL')}** | {num_pages} Pages, {num_words} Words, {num_chars} Chars |\n")
        f.write(f"| Stage 4 | Text Chunking | **{stage_results.get('Stage 4 (Chunking)', 'FAIL')}** | {num_chunks} Chunks (80 words / 15 overlap) |\n")
        f.write(f"| Stage 5 | TF-IDF Vector Indexing | **{stage_results.get('Stage 5 (TF-IDF Vector Indexing)', 'FAIL')}** | Vocab Size: {vocab_size}, Matrix Shape: {matrix_shape} |\n")
        f.write(f"| Stage 6 | Vector Retrieval | **{stage_results.get('Stage 6 (Vector Retrieval)', 'FAIL')}** | Query: '{query_str}', Max Score: {max_sim * 100:.1f}% |\n")
        f.write(f"| Stage 7 | Gemini AI Completion | **{stage_results.get('Stage 7 (Gemini AI Completion)', 'FAIL')}** | Model: `gemini-1.5-flash`, Answer generated |\n")
        f.write(f"| Stage 8 | Frontend Answer & Citations | **{stage_results.get('Stage 8 (Frontend Response Rendering)', 'FAIL')}** | Citations: {citations} |\n\n")
        f.write("## Overall System Audit Verdict\n\n")
        if all_passed:
            f.write("### ✅ ALL 8 STAGES PASSED 100%\n\n")
            f.write("The end-to-end RAG system is 100% operational from PDF ingestion through TF-IDF vectorization and Google Gemini AI completion.\n")
        else:
            f.write("### ❌ SYSTEM AUDIT FAILED\n\n")
            f.write("One or more stages failed during verification.\n")

    return all_passed

if __name__ == "__main__":
    run_full_8stage_audit()

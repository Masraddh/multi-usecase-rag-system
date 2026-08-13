import requests
import io
import fitz  # PyMuPDF

def create_sample_pdf_bytes() -> bytes:
    """Creates a sample multi-page PDF document using PyMuPDF."""
    doc = fitz.open()
    
    # Page 1: Header, Summary, Projects
    page1 = doc.new_page()
    text_page1 = (
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
    page1.insert_text((50, 50), text_page1, fontsize=11)

    # Page 2: Skills & Education
    page2 = doc.new_page()
    text_page2 = (
        "TECHNICAL SKILLS & COMPETENCIES\n"
        "- Programming Languages: Python, JavaScript, TypeScript, SQL, HTML5, CSS3\n"
        "- Frameworks & Libraries: FastAPI, Next.js, React, PyTorch, Scikit-Learn, Pandas, NumPy\n"
        "- Databases & DevOps: PostgreSQL, MongoDB, Redis, Docker, Git, GitHub Actions, Linux\n\n"
        "EDUCATION\n"
        "Bachelor of Technology in Information Technology | G. Narayanamma Institute of Technology & Science"
    )
    page2.insert_text((50, 50), text_page2, fontsize=11)

    buffer = io.BytesIO()
    doc.save(buffer)
    doc.close()
    return buffer.getvalue()


def test_pdf_ingestion_pipeline():
    print("=" * 80)
    print("STEP 1: Generating sample PDF bytes with PyMuPDF...")
    pdf_bytes = create_sample_pdf_bytes()
    filename = "Shaik_Masraddh_Resume.pdf"
    print(f"Generated PDF File: '{filename}', Size: {round(len(pdf_bytes)/1024, 2)} KB")
    print("=" * 80)

    # Step 2: Upload to backend
    upload_url = "http://localhost:8000/api/v1/upload"
    files = {"file": (filename, pdf_bytes, "application/pdf")}
    data = {"assistant_id": "interview_coach"}

    print(f"\nSTEP 2: Uploading '{filename}' to {upload_url}...")
    res = requests.post(upload_url, files=files, data=data)
    print("Upload Status Code:", res.status_code)
    upload_json = res.json()
    print("Upload Response Payload:\n", upload_json)
    
    assert res.status_code == 200, f"Upload failed with status {res.status_code}: {upload_json}"
    assert upload_json.get("num_pages", 0) >= 2, "Failed to read 2 pages from PDF"
    assert upload_json.get("num_words", 0) > 50, "Extracted word count is too low"
    assert upload_json.get("num_chunks", 0) >= 1, "No vector chunks generated"
    print("\n✓ STEP 2 PASSED: PDF Uploaded, Page-by-Page Extracted, and Indexed!")

    # Step 3: Query active PDF index
    chat_url = "http://localhost:8000/api/v1/chat"
    query_payload = {
        "assistant_id": "interview_coach",
        "query": "tell me about projects?"
    }

    print(f"\nSTEP 3: Sending query 'tell me about projects?' to {chat_url}...")
    res_chat = requests.post(chat_url, json=query_payload)
    print("Chat Status Code:", res_chat.status_code)
    chat_json = res_chat.json()
    print("\nChat Answer:\n", chat_json.get("answer"))
    print("\nMax Similarity Score:", chat_json.get("max_similarity_score"))
    print("Citations:", chat_json.get("citations"))

    assert res_chat.status_code == 200, f"Chat query failed with status {res_chat.status_code}"
    assert chat_json.get("answer"), "Returned answer is empty"
    print("\n✓ STEP 3 PASSED: Query Successfully Answered from Uploaded PDF Knowledge Base!")
    print("=" * 80)

if __name__ == "__main__":
    test_pdf_ingestion_pipeline()

import requests
import io
import fitz

def create_checkbox_pdf() -> bytes:
    doc = fitz.open()
    page = doc.new_page()
    content = (
        "STUDENT AUDIT & CHECKLIST WORKBOOK\n\n"
        "☐ Section 1: Introduction Completed\n"
        "☐ Section 2: SoilSmart IoT Agriculture System & ML Models\n"
        "☐ Section 3: React Native Live Chat & Event Booking App\n"
        "☐ Section 4: Operating Systems CPU Scheduling Algorithms (FCFS, SJF, Round Robin)\n\n"
        "Instructions: Mark all checkboxes after completing practice exercises."
    )
    page.insert_text((50, 50), content, fontsize=11)
    buffer = io.BytesIO()
    doc.save(buffer)
    doc.close()
    return buffer.getvalue()

def test_checkbox_pdf_query():
    pdf_bytes = create_checkbox_pdf()
    filename = "Checklist_Workbook.pdf"
    
    upload_url = "http://localhost:8000/api/v1/upload"
    files = {"file": (filename, pdf_bytes, "application/pdf")}
    data = {"assistant_id": "study_buddy"}
    
    print(f"1. Uploading PDF with checkboxes ({filename})...")
    res_up = requests.post(upload_url, files=files, data=data)
    print("Upload Status Code:", res_up.status_code)
    print("Upload Payload:", res_up.json())
    
    chat_url = "http://localhost:8000/api/v1/chat"
    query_payload = {
        "assistant_id": "study_buddy",
        "query": "explain the checklist sections"
    }
    
    print("\n2. Querying document with checkboxes...")
    res_chat = requests.post(chat_url, json=query_payload)
    print("Chat Status Code:", res_chat.status_code)
    chat_json = res_chat.json()
    print("Answer:\n", chat_json.get("answer"))
    print("Max Similarity Score:", chat_json.get("max_similarity_score"))

if __name__ == "__main__":
    test_checkbox_pdf_query()

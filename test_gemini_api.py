import requests
import io
import fitz

def create_sample_pdf() -> bytes:
    doc = fitz.open()
    page = doc.new_page()
    content = (
        "OPERATING SYSTEMS STUDY GUIDE\n\n"
        "1. FCFS SCHEDULING:\n"
        "First-Come, First-Served scheduling allocates CPU to processes in order of arrival.\n"
        "It is non-preemptive and causes the convoy effect where short processes wait for long ones.\n\n"
        "2. SJF SCHEDULING:\n"
        "Shortest Job First scheduling selects process with shortest burst time.\n"
        "SJF is provably optimal giving minimal average waiting time."
    )
    page.insert_text((50, 50), content, fontsize=11)
    buffer = io.BytesIO()
    doc.save(buffer)
    doc.close()
    return buffer.getvalue()

def test_gemini_full_flow():
    pdf_bytes = create_sample_pdf()
    filename = "OS_Guide.pdf"
    
    upload_url = "http://localhost:8000/api/v1/upload"
    files = {"file": (filename, pdf_bytes, "application/pdf")}
    data = {"assistant_id": "study_buddy"}
    
    print(f"1. Uploading '{filename}' to {upload_url}...")
    res_up = requests.post(upload_url, files=files, data=data)
    print("Upload Status Code:", res_up.status_code)
    print("Upload Payload:", res_up.json())
    
    chat_url = "http://localhost:8000/api/v1/chat"
    query_payload = {
        "assistant_id": "study_buddy",
        "query": "Explain FCFS and SJF scheduling"
    }
    
    print("\n2. Querying 'Explain FCFS and SJF scheduling'...")
    res_chat = requests.post(chat_url, json=query_payload)
    print("Chat Status Code:", res_chat.status_code)
    chat_json = res_chat.json()
    print("\nGemini AI Response:\n", chat_json.get("answer"))
    print("\nMax Similarity Score:", chat_json.get("max_similarity_score"))

if __name__ == "__main__":
    test_gemini_full_flow()

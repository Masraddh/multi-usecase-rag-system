import requests
import io
import fitz  # PyMuPDF

def create_operating_systems_pdf() -> bytes:
    doc = fitz.open()
    
    page = doc.new_page()
    content = (
        "OPERATING SYSTEMS EXAM STUDY GUIDE - CPU SCHEDULING ALGORITHMS\n\n"
        "1. FIRST-COME, FIRST-SERVED (FCFS) SCHEDULING:\n"
        "- Non-preemptive scheduling algorithm where process that requests CPU first is allocated CPU first.\n"
        "- Convoy Effect: Short processes wait behind a long process, drastically increasing average waiting time.\n\n"
        "2. SHORTEST-JOB-FIRST (SJF) SCHEDULING:\n"
        "- Associates with each process the length of its next CPU burst.\n"
        "- SJF is provably optimal because it gives the minimum average waiting time for a given set of processes.\n\n"
        "3. ROUND ROBIN (RR) SCHEDULING:\n"
        "- Designed for time-sharing systems. Small unit of time (time quantum / time slice, usually 10-100 ms) is defined.\n"
        "- Context switching overhead: If time quantum is too small, frequent context switching slows down system execution."
    )
    page.insert_text((50, 50), content, fontsize=11)
    
    buffer = io.BytesIO()
    doc.save(buffer)
    doc.close()
    return buffer.getvalue()

def test_exam_study_buddy_pdf():
    pdf_bytes = create_operating_systems_pdf()
    filename = "OS_Scheduling_Notes.pdf"
    
    upload_url = "http://localhost:8000/api/v1/upload"
    files = {"file": (filename, pdf_bytes, "application/pdf")}
    data = {"assistant_id": "study_buddy"}
    
    print(f"1. Uploading '{filename}' for Assistant 'study_buddy' to {upload_url}...")
    res = requests.post(upload_url, files=files, data=data)
    print("Upload Status Code:", res.status_code)
    upload_json = res.json()
    print("Upload Response Payload:\n", upload_json)
    
    assert res.status_code == 200, f"Upload failed with status {res.status_code}: {upload_json}"
    
    # Query Exam Study Buddy
    chat_url = "http://localhost:8000/api/v1/chat"
    query_payload = {
        "assistant_id": "study_buddy",
        "query": "Which scheduling algorithm causes the convoy effect and why?"
    }
    
    print("\n2. Querying 'Which scheduling algorithm causes the convoy effect and why?'...")
    res_chat = requests.post(chat_url, json=query_payload)
    print("Chat Status Code:", res_chat.status_code)
    chat_json = res_chat.json()
    print("Chat Answer:\n", chat_json.get("answer"))
    print("Max Similarity Score:", chat_json.get("max_similarity_score"))

if __name__ == "__main__":
    test_exam_study_buddy_pdf()

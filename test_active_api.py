import requests
import json

def test_active_backend():
    url = "http://localhost:8000/api/v1/chat"
    payload = {
        "assistant_id": "interview_coach",
        "query": "tell me about projects?"
    }
    
    print("Testing active FastAPI backend at http://localhost:8000/api/v1/chat ...")
    response = requests.post(url, json=payload)
    print("Status Code:", response.status_code)
    data = response.json()
    print("Answer:\n", data.get("answer"))
    print("Citations:", data.get("citations"))
    print("Max Similarity Score:", data.get("max_similarity_score"))

if __name__ == "__main__":
    test_active_backend()

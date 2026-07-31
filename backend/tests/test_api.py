import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["assistants_loaded"] == 5


def test_list_assistants():
    response = client.get("/api/v1/assistants")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    ids = [ast["id"] for ast in data]
    assert "interview_coach" in ids
    assert "campus_faq" in ids
    assert "study_buddy" in ids
    assert "ecommerce_support" in ids
    assert "code_docs" in ids


def test_get_assistant_detail():
    response = client.get("/api/v1/assistants/interview_coach")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Interview Preparation Coach"


def test_chat_endpoint_grounded():
    payload = {
        "assistant_id": "campus_faq",
        "query": "How many books can I borrow from the library?"
    }
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert len(data["retrieved_chunks"]) > 0
    assert data["max_similarity_score"] > 0.0


def test_chat_endpoint_ungrounded():
    payload = {
        "assistant_id": "campus_faq",
        "query": "What is the capital of France?"
    }
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "I don't have that information."


def test_retrieve_preview_endpoint():
    payload = {
        "assistant_id": "study_buddy",
        "query": "convoy effect"
    }
    response = client.post("/api/v1/retrieve", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["chunks"]) > 0
    assert "FCFS" in data["chunks"][0]["text"] or "Convoy" in data["chunks"][0]["text"]


def test_system_stats():
    response = client.get("/api/v1/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total_documents"] == 5
    assert data["total_chunks"] > 5

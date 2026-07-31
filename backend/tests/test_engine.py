import sys
import os
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.rag_engine import RAGEngine


def test_chunking_sliding_window():
    text = "Word1 Word2 Word3 Word4 Word5 Word6 Word7 Word8 Word9 Word10"
    engine = RAGEngine(doc_text=text, persona="Tester", max_words=5, overlap=2)
    assert len(engine.chunks) > 1
    # Check overlap
    words_chunk1 = engine.chunks[0].split()
    words_chunk2 = engine.chunks[1].split()
    assert words_chunk1[-2:] == words_chunk2[:2]


def test_tfidf_retrieval_ranking():
    doc = """
    Python is an interpreted, high-level programming language for general-purpose programming.
    SQL is a domain-specific language used in programming and designed for managing data in relational databases.
    React Native is an open-source UI software framework created by Meta Platforms.
    """
    engine = RAGEngine(doc_text=doc, persona="Tester", max_words=40, overlap=5, top_k=2)
    results = engine.retrieve("What language is used for managing data in relational databases?")
    assert len(results) > 0
    top_chunk = results[0][2]
    assert "SQL" in top_chunk


def test_strict_grounding_fallback():
    doc = "The library allows borrowing up to 4 books for 14 days."
    engine = RAGEngine(doc_text=doc, persona="Tester", max_words=20, overlap=5)
    # Query completely ungrounded fact
    res = engine.ask_detailed("What is the distance from Earth to Mars?")
    assert res["answer"] == "I don't have that information."


def test_citation_formatting():
    doc = "Project 1 involved real-time seat selection using React Native and WebSockets."
    engine = RAGEngine(doc_text=doc, persona="Tester", max_words=30, overlap=5)
    res = engine.ask_detailed("Tell me about real-time seat selection.")
    assert "[Source 1]" in res["answer"] or "[Source 1]" in res["citations"]

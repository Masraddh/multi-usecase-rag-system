"""
Fast Direct Verification Script for Mode Selection (RAG vs Pure AI) & Document Fetching.
"""

import sys
import os

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

base_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(base_dir, "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from use_cases.registry import get_registry


def test_direct_document_and_modes():
    print("==================================================================")
    print(" DIRECT VERIFICATION: DOCUMENT FETCH & MODE SELECTION (RAG / AI)")
    print("==================================================================")

    registry = get_registry()
    ast = registry.get_assistant("interview_coach")
    assert ast is not None, "interview_coach assistant not found"

    # 1. Document Fetch Test
    doc_text = ast["engine"].doc_text
    info = ast["info"]
    print(f"\n1. Document Content Fetch Test:")
    print(f"   - Assistant: {info.name}")
    print(f"   - Active File: {info.filename}")
    print(f"   - Document Text Length: {len(doc_text)} characters")
    assert len(doc_text) > 50, "Document text is empty!"
    print("   ✓ Document Fetch Test PASSED")

    # 2. RAG Mode Execution Test
    print(f"\n2. RAG Mode Execution Test:")
    rag_res = ast["engine"].ask_detailed("Tell me about a project where you worked with real-time data.", mode="rag")
    print(f"   - Mode: {rag_res.get('mode')}")
    print(f"   - Max Similarity Score: {rag_res.get('max_similarity_score')}")
    print(f"   - Chunks Retrieved: {len(rag_res.get('retrieved_chunks', []))}")
    print(f"   - Citations: {rag_res.get('citations')}")
    assert rag_res.get("mode") == "rag"
    assert rag_res.get("max_similarity_score", 0) > 0.0
    assert len(rag_res.get("retrieved_chunks", [])) > 0
    print("   ✓ RAG Mode Test PASSED")

    # 3. Pure AI Mode Execution Test
    print(f"\n3. Pure AI Mode Execution Test:")
    ai_res = ast["engine"].ask_detailed("What are general software engineering interview tips?", mode="ai")
    print(f"   - Mode: {ai_res.get('mode')}")
    print(f"   - Max Similarity Score: {ai_res.get('max_similarity_score')}")
    print(f"   - Chunks Retrieved: {len(ai_res.get('retrieved_chunks', []))}")
    print(f"   - Citations: {ai_res.get('citations')}")
    print(f"   - Answer Snippet: {ai_res.get('answer')[:120]}...")
    assert ai_res.get("mode") == "ai"
    assert ai_res.get("max_similarity_score") == 0.0
    assert len(ai_res.get("retrieved_chunks", [])) == 0
    assert len(ai_res.get("citations", [])) == 0
    print("   ✓ Pure AI Mode Test PASSED")

    print("\n==================================================================")
    print(" ALL VERIFICATION TESTS PASSED SUCCESSFULLY!")
    print("==================================================================")

if __name__ == "__main__":
    test_direct_document_and_modes()

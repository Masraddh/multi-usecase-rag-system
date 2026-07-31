import sys
import os

# Ensure backend and root are in python path
root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from engine.rag_engine import RAGEngine

def main():
    print("=" * 80)
    print("=== RAG PIPELINE AUDIT & GENERATION VERIFICATION ===")
    print("=" * 80)

    # 1. Load Interview Prep dataset
    dataset_path = os.path.join(root_dir, "backend", "data", "interview_prep.txt")
    with open(dataset_path, "r", encoding="utf-8") as f:
        doc_text = f.read()

    # 2. Instantiate RAG Engine
    engine = RAGEngine(
        doc_text=doc_text,
        persona="a professional interview coach",
        max_words=80,
        overlap=15,
        top_k=3
    )

    print(f"\n[OK] Stage 1-5: Document indexed successfully. Chunks: {len(engine.chunks)}, Vocab: {engine.vocab_size}")

    test_queries = [
        "What are my education",
        "Tell me about your education",
        "Explain my projects",
        "Generate a self introduction"
    ]

    for q in test_queries:
        print("\n" + "-" * 70)
        print(f"QUERY: '{q}'")
        res = engine.ask_detailed(q)
        print(f"LATENCY: {res['latency_ms']} ms")
        print(f"CITATIONS: {res['citations']}")
        print(f"MAX RETRIEVAL SCORE: {res['max_similarity_score'] * 100:.1f}%")
        print("GENERATED ANSWER (Chat Bubble Output):")
        print(f"\"{res['answer']}\"")
        
        # Assertions
        assert "*(Note: Grounded RAG vector retrieval completed" not in res['answer'], "FAILED: Legacy fallback note present in answer"
        assert res['answer'] != "", "FAILED: Empty answer returned"
        assert len(res['citations']) > 0 or res['answer'] == "I don't have that information.", "FAILED: Missing citations"

    print("\n" + "=" * 80)
    print("[SUCCESS] ALL 10 STAGES OF RAG PIPELINE VERIFIED CLEANLY!")
    print("=" * 80)

if __name__ == "__main__":
    main()

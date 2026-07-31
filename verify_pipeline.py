import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from engine.rag_engine import RAGEngine

def test_engine_retrieval():
    print("==================================================")
    print("VERIFYING RAG ENGINE CHUNKING & RETRIEVAL LOGIC")
    print("==================================================")

    sample_doc = (
        "Operating Systems Process Scheduling: FCFS is non-preemptive and causes convoy effect. "
        "Shortest Job First SJF selects smallest burst time. "
        "Round Robin RR uses fixed time quantum and causes context switching overhead."
    )

    engine = RAGEngine(
        doc_text=sample_doc,
        persona="test persona",
        max_words=10,
        overlap=3,
        top_k=2
    )

    print(f"Total Chunks Generated: {len(engine.chunks)}")
    for i, c in enumerate(engine.chunks, 1):
        print(f"Chunk {i}: {c}")

    assert len(engine.chunks) > 0, "Chunking failed to create chunks!"

    # Test retrieval for convoy effect
    results = engine.retrieve("What causes convoy effect?", top_k=2)
    print(f"\nRetrieval for 'convoy effect':")
    for src_num, score, text in results:
        print(f"  [Source {src_num}] Score: {score:.4f} | Text: {text}")

    assert results[0][1] > 0.0, "Retrieval score should be positive for matching query!"
    print("\n[PASSED] Chunking and TF-IDF Retrieval tests PASSED successfully!\n")

if __name__ == "__main__":
    test_engine_retrieval()

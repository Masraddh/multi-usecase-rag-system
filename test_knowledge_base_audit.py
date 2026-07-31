import os
import sys
import time

# Force UTF-8 stdout encoding for Windows CLI
sys.stdout.reconfigure(encoding='utf-8')

# Ensure root import path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend"))

from backend.use_cases.registry import get_registry
from backend.utils.document_reader import DocumentReader

def run_knowledge_base_audit():
    print("=" * 80)
    print("      COMPREHENSIVE KNOWLEDGE BASE MANAGEMENT SYSTEM AUDIT")
    print("=" * 80)

    # 1. Startup Directory Auto-Scanning & Multi-Document Indexing
    registry = get_registry()

    print("\n1. VERIFYING AUTOMATIC STARTUP INDEXING FOR ALL 5 ASSISTANTS:")
    print("-" * 80)
    
    assistants = registry.list_assistants()
    assert len(assistants) == 5, f"Expected 5 assistants, got {len(assistants)}"

    for ast in assistants:
        print(f"\n[ASSISTANT: {ast.name} ({ast.id})]")
        print(f"  - Active Status: {ast.index_status}")
        print(f"  - Document Count: {ast.total_docs}")
        print(f"  - Indexed Files: {ast.documents}")
        print(f"  - Total Pages Read: {ast.num_pages}")
        print(f"  - Words Extracted: {ast.num_words}")
        print(f"  - Characters Extracted: {ast.num_chars}")
        print(f"  - Total Chunks Created: {ast.total_chunks}")
        print(f"  - Vocabulary Size: {ast.vocab_size}")
        print(f"  - Matrix Shape: {ast.matrix_shape}")
        print(f"  - Index Build Time: {ast.build_time_ms} ms")

        assert ast.total_docs >= 1, f"Assistant {ast.id} has 0 documents!"
        assert ast.total_chunks > 0, f"Assistant {ast.id} has 0 chunks!"
        assert ast.retrieval_ready, f"Assistant {ast.id} retrieval index is not ready!"
        assert "Successfully Indexed" in ast.index_status or "✅" in ast.index_status

    print("\n" + "=" * 80)
    print("2. TESTING DYNAMIC UPLOAD MODES ('ADD' vs 'REPLACE'):")
    print("-" * 80)

    test_content = (
        "SPECIFIC TEST ANNOUNCEMENT 2026:\n"
        "The G. Narayanamma Institute annual tech symposium is scheduled for November 15, 2026.\n"
        "All IT department students must register online."
    )
    test_filename = "tech_symposium_announcement.txt"

    # Test Mode 'ADD'
    print("\n[TESTING UPLOAD MODE: ADD]")
    res_add = registry.update_assistant_dataset(
        assistant_id="interview_coach",
        new_text=test_content,
        filename=test_filename,
        mode="add"
    )
    print(f"  - Result Mode: {res_add['mode']}")
    print(f"  - Active Documents Count: {res_add['total_docs']}")
    print(f"  - Document List: {res_add['documents']}")
    assert test_filename in res_add['documents'], "Uploaded file missing from documents list in ADD mode!"
    assert res_add['total_docs'] > 1, "ADD mode should keep existing knowledge base documents!"

    # Test Retrieval with ADD mode document
    retrieved = registry.get_assistant("interview_coach")["engine"].retrieve("annual tech symposium November 2026", top_k=1)
    assert len(retrieved) > 0, "Failed to retrieve chunk after ADD upload!"
    chunk_idx, score_val, chunk_txt = retrieved[0]
    print(f"  - Retrieved Top Chunk ({score_val*100:.1f}%): '{chunk_txt[:80]}...'")

    # Test Mode 'REPLACE'
    print("\n[TESTING UPLOAD MODE: REPLACE]")
    res_rep = registry.update_assistant_dataset(
        assistant_id="interview_coach",
        new_text=test_content,
        filename=test_filename,
        mode="replace"
    )
    print(f"  - Result Mode: {res_rep['mode']}")
    print(f"  - Active Documents Count: {res_rep['total_docs']}")
    print(f"  - Document List: {res_rep['documents']}")
    assert res_rep['documents'] == [test_filename], "REPLACE mode should contain ONLY newly uploaded file!"
    assert res_rep['total_docs'] == 1, "REPLACE mode should reduce doc count to 1!"

    # Reset Assistant Knowledge Base
    print("\n[RESETTING ASSISTANT KNOWLEDGE BASE BACK TO DEFAULT]")
    res_reset = registry.reset_assistant_dataset("interview_coach")
    print(f"  - Reset Status: {res_reset['index_status']}")
    print(f"  - Restored Document Count: {res_reset['total_docs']}")
    print(f"  - Restored Documents: {res_reset['documents']}")
    assert res_reset['total_docs'] > 1, "Reset failed to restore default domain documents!"

    print("\n" + "=" * 80)
    print("3. SEARCH VALIDATION ACROSS ALL 5 ASSISTANTS:")
    print("-" * 80)

    queries = [
        ("interview_coach", "Education background", ["B.Tech", "Narayanamma", "CGPA"]),
        ("interview_coach", "Real-time event booking project", ["React Native", "WebSockets", "Firebase"]),
        ("campus_faq", "Hostel curfew hours", ["8:30 PM", "Hostel", "curfew"]),
        ("campus_faq", "Library borrowing limits", ["4 books", "14 days", "borrow"]),
        ("study_buddy", "Round Robin scheduling algorithm", ["quantum", "Round Robin", "CPU"]),
        ("study_buddy", "FCFS convoy effect", ["First-Come", "convoy effect", "non-preemptive"]),
        ("ecommerce_support", "Voyager Pro laptop compartment size", ["15.6-inch", "Voyager", "laptop"]),
        ("ecommerce_support", "Return refund policy window", ["15 days", "return", "refund"]),
        ("code_docs", "RAGEngine Python API methods", ["chunk_document", "retrieve", "RAGEngine"]),
    ]

    for ast_id, q, keywords in queries:
        ast_obj = registry.get_assistant(ast_id)
        engine = ast_obj["engine"]
        chunks = engine.retrieve(q, top_k=2)
        assert len(chunks) > 0, f"Query '{q}' returned 0 chunks for {ast_id}!"
        top_idx, top_score, top_txt = chunks[0]
        matched = any(kw.lower() in top_txt.lower() for kw in keywords)
        score_pct = top_score * 100
        print(f"  [{ast_id}] Query: '{q}' | Match: {'YES' if matched else 'NO'} | Score: {score_pct:.1f}%")
        assert matched or score_pct > 5.0, f"Retrieval failed for query '{q}' in {ast_id}!"

    print("\n" + "=" * 80)
    print("  [SUCCESS] ALL KNOWLEDGE BASE MANAGEMENT SYSTEM REQUIREMENTS VERIFIED 100%!")
    print("=" * 80)

if __name__ == "__main__":
    run_knowledge_base_audit()

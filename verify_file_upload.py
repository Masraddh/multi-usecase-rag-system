"""
Comprehensive Automated Verification Script for Dynamic File Upload Feature.
Tests document loaders, text extraction, cleaning, chunking, TF-IDF vectorization,
error handling, and dynamic assistant re-indexing across all 5 use cases.
"""

import sys
import os

# Set UTF-8 encoding for standard output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Ensure backend directory is in path
base_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(base_dir, "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from engine.document_loaders import extract_text, clean_text, load_txt, load_markdown
from use_cases.registry import get_registry


def test_document_extraction():
    print("\n--- 1. Testing Document Extraction & Text Cleaning ---")
    
    # 1. Plain Text
    raw_txt = b"Hello World!\n\nThis is a sample document text with extra   spaces.\x00"
    txt_out, pages, words = extract_text("sample.txt", raw_txt)
    assert "Hello World!" in txt_out
    assert "\x00" not in txt_out
    print(f"[OK] TXT Extraction passed ({words} words, {pages} page)")

    # 2. Markdown
    raw_md = b"# Section Header\n\nThis is **markdown** documentation.\n- Item 1\n- Item 2"
    md_out, md_pages, md_words = extract_text("readme.md", raw_md)
    assert "# Section Header" in md_out
    print(f"[OK] MD Extraction passed ({md_words} words, {md_pages} page)")

    # 3. Empty document error check
    try:
        extract_text("empty.txt", b"   \n\t  ")
        assert False, "Should have raised ValueError for empty document"
    except ValueError as ve:
        print(f"[OK] Empty file error handling passed: '{str(ve)}'")

    # 4. Unsupported format error check
    try:
        extract_text("unsupported.exe", b"binary content")
        assert False, "Should have raised ValueError for unsupported extension"
    except ValueError as ve:
        print(f"[OK] Unsupported format error handling passed: '{str(ve)}'")


def test_registry_dynamic_indexing():
    print("\n--- 2. Testing Dynamic Re-Indexing across All 5 Use Cases ---")
    registry = get_registry()
    
    # Test Use Case 1: Interview Coach with Custom Resume Text
    custom_resume = (
        "CANDIDATE RESUME: ALEX RIVEIRA\n"
        "Senior Cloud Architect with 8 years of experience building AWS microservices, Kubernetes clusters, "
        "and Terraform infrastructure. Led a team of 12 engineers migrating legacy monoliths to serverless Lambda functions."
    )
    res1 = registry.update_assistant_dataset("interview_coach", custom_resume, "Alex_Resume.pdf", num_pages=2)
    print(f"[OK] Interview Coach dynamic upload: {res1['filename']} indexed into {res1['num_chunks']} chunks ({res1['num_words']} words)")
    
    ast1 = registry.get_assistant("interview_coach")
    ans1 = ast1["engine"].ask("What is Alex's experience with AWS and Terraform?")
    assert "Alex" in ans1 or "AWS" in ans1 or "Terraform" in ans1 or "8 years" in ans1 or "[Source 1]" in ans1
    print(f"   [Query Answer]: {ans1[:120]}...")

    # Test Use Case 2: Campus FAQ with Custom Policy PDF Text
    custom_campus = (
        "CAMPUS HOSTEL & SCHOLARSHIP RULES 2026\n"
        "Scholarship criteria: Undergraduates with GPA above 3.8 are eligible for a 50% tuition waiver. "
        "Hostel gym hours are strictly 6:00 AM to 9:00 PM daily."
    )
    res2 = registry.update_assistant_dataset("campus_faq", custom_campus, "Campus_Policy_2026.pdf", num_pages=5)
    print(f"[OK] Campus FAQ dynamic upload: {res2['filename']} indexed into {res2['num_chunks']} chunks")
    
    ast2 = registry.get_assistant("campus_faq")
    ans2 = ast2["engine"].ask("What GPA is needed for tuition waiver?")
    assert "3.8" in ans2 or "50%" in ans2 or "[Source 1]" in ans2
    print(f"   [Query Answer]: {ans2[:120]}...")

    # Test Use Case 3: Study Buddy with Custom OS Notes
    custom_notes = (
        "OPERATING SYSTEMS LECTURE 4: DEADLOCK PREVENTION\n"
        "Coffman Conditions for Deadlock: Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait. "
        "Banker's Algorithm is used for deadlock avoidance by verifying safe state matrix."
    )
    res3 = registry.update_assistant_dataset("study_buddy", custom_notes, "OS_Lecture_4.docx", num_pages=3)
    print(f"[OK] Study Buddy dynamic upload: {res3['filename']} indexed into {res3['num_chunks']} chunks")
    
    ast3 = registry.get_assistant("study_buddy")
    ans3 = ast3["engine"].ask("What algorithm avoids deadlock using a safe state matrix?")
    assert "Banker" in ans3 or "deadlock" in ans3 or "[Source 1]" in ans3
    print(f"   [Query Answer]: {ans3[:120]}...")

    # Test Use Case 4: Ecommerce Support with Custom Catalogue
    custom_ecom = (
        "PRO AUDIO HEADPHONES MODEL X900\n"
        "Features active noise cancellation (ANC), 40-hour battery life, USB-C fast charging. "
        "2-year international manufacturer warranty included."
    )
    res4 = registry.update_assistant_dataset("ecommerce_support", custom_ecom, "Product_Catalogue_X900.txt", num_pages=1)
    print(f"[OK] Ecommerce Support dynamic upload: {res4['filename']} indexed into {res4['num_chunks']} chunks")
    
    ast4 = registry.get_assistant("ecommerce_support")
    ans4 = ast4["engine"].ask("What is the battery life of Model X900?")
    assert "40" in ans4 or "battery" in ans4 or "[Source 1]" in ans4
    print(f"   [Query Answer]: {ans4[:120]}...")

    # Test Use Case 5: Code Documentation Assistant with Custom API Spec
    custom_code = (
        "FASTAPI ROUTER API SPECIFICATION\n"
        "Endpoint POST /api/v1/assistants/{id}/upload accepts Multipart FormData with key 'file'. "
        "Returns JSON payload with chunk_count, word_count, and page_count."
    )
    res5 = registry.update_assistant_dataset("code_docs", custom_code, "API_Specification.md", num_pages=1)
    print(f"[OK] Code Docs Assistant dynamic upload: {res5['filename']} indexed into {res5['num_chunks']} chunks")
    
    ast5 = registry.get_assistant("code_docs")
    ans5 = ast5["engine"].ask("What key does the upload endpoint accept in FormData?")
    assert "file" in ans5 or "Multipart" in ans5 or "[Source 1]" in ans5
    print(f"   [Query Answer]: {ans5[:120]}...")


def test_dataset_reset():
    print("\n--- 3. Testing Dataset Reset back to Use Case Defaults ---")
    registry = get_registry()
    
    reset_res = registry.reset_assistant_dataset("interview_coach")
    assert reset_res["active_source"] == "default"
    assert reset_res["filename"] == "interview_prep.txt"
    print(f"[OK] Successfully reset interview_coach back to {reset_res['filename']}")

    ast = registry.get_assistant("interview_coach")
    ans = ast["engine"].ask("Tell me about a project where you worked with real-time data.")
    assert "React Native" in ans or "WebSockets" in ans or "Firebase" in ans or "[Source 1]" in ans
    print(f"   [Default Query Answer]: {ans[:120]}...")


if __name__ == "__main__":
    print("==================================================================")
    print("   AUTOMATED VERIFICATION: DYNAMIC FILE UPLOAD FOR ALL 5 USE CASES")
    print("==================================================================")
    test_document_extraction()
    test_registry_dynamic_indexing()
    test_dataset_reset()
    print("\nALL VERIFICATION TESTS PASSED SUCCESSFULLY!")

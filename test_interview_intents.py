"""
Automated Test Suite verifying Interview Coach Semantic Intent Handling.
Tests 5 target interview prompts:
1. Generate a self introduction
2. Tell me about yourself
3. Introduce yourself
4. Explain your experience
5. Summarize your profile

Verifies that:
- Each query detects the semantic intent.
- Relevant resume chunks are retrieved.
- Answers are meaningful and grounded in the resume.
- Out-of-domain queries still return "I don't have that information."
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


def test_interview_coach_intents():
    print("=" * 80)
    print("  VERIFICATION TEST: INTERVIEW COACH SEMANTIC INTENT HANDLING")
    print("=" * 80)

    registry = get_registry()
    interview_ast = registry.get_assistant("interview_coach")
    engine = interview_ast["engine"]

    target_queries = [
        "Generate a self introduction",
        "Tell me about yourself",
        "Introduce yourself",
        "Explain your experience",
        "Summarize your profile",
        "explain about my projects"
    ]

    for i, q in enumerate(target_queries, 1):
        print(f"\n------------------------------------------------------------------")
        print(f"TEST QUERY #{i}: '{q}'")
        res = engine.ask_detailed(q)
        
        answer = res["answer"]
        chunks = res["retrieved_chunks"]

        print(f"-> Max Similarity Score: {res['max_similarity_score']}")
        print(f"-> Retrieved Chunks Count: {len(chunks)}")
        print(f"-> Response snippet: {answer[:120]}...")

        # Assertions for intent queries:
        assert answer != "I don't have that information.", f"Query '{q}' should NOT return 'I don't have that information.'"
        assert len(chunks) > 0, f"Query '{q}' should retrieve candidate resume chunks."
        # Verify content contains resume keywords or source citation
        assert any(k in answer for k in ["React Native", "Power BI", "SQL", "CANDIDATE", "Source", "Project", "Internship", "Profile"]), \
            f"Query '{q}' answer should contain grounded resume details."
        print(f"[PASS] Query #{i} '{q}' returned grounded interview response!")

    # Test out-of-domain query on Interview Coach
    irrelevant_query = "What is Quantum Computing superposition?"
    print(f"\n------------------------------------------------------------------")
    print(f"IRRELEVANT QUERY TEST: '{irrelevant_query}'")
    res_irr = engine.ask_detailed(irrelevant_query)
    assert res_irr["answer"] == "I don't have that information.", "Out-of-domain query MUST return 'I don't have that information.'"
    print(f"[PASS] Out-of-domain query returned 'I don't have that information.'")

    print("\n🎉 ALL INTERVIEW COACH INTENT VERIFICATION TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    test_interview_coach_intents()

"""
ALL-IN-ONE RAG MINI USE-CASES RUNNER
------------------------------------
Consolidates all 5 domain use cases into a single, self-contained executable Python script:
1. Interview Prep Coach
2. Campus FAQ Helpdesk
3. Exam Study Buddy (OS Scheduling Notes - Tuned max_words=50, overlap=12)
4. E-Commerce Customer Support
5. Code & API Documentation Assistant
"""

import os
import sys

# Ensure root directory is on sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from engine.rag_engine import RAGEngine

# ==============================================================================
# USE CASE DATASETS & PERSONAS
# ==============================================================================

USE_CASE_1_DATA = """
CANDIDATE PROFILE & PROJECT NOTES

Project 1: Real-Time Event Booking & Live Chat App (React Native)
- Developed a cross-platform mobile application using React Native, WebSockets, and Firebase Realtime Database.
- Handled real-time data streaming for live seat selection and instant push notifications, serving over 10,000 active users.
- Optimized app rendering performance by reducing re-renders by 35% using React Hooks and custom memoization.

Project 2: Sales Analytics & ETL Dashboard Internship (Power BI & SQL)
- Completed a 3-month Data Analytics internship building interactive executive dashboards in Power BI.
- Wrote complex SQL queries and stored procedures to transform 500k+ customer transaction records.
- Automated weekly data refresh workflows, reducing manual report preparation time by 15 hours per week.

Technical Skills & Machine Learning Expertise:
- Languages & Tools: Python, SQL, JavaScript, React Native, Power BI, Git, Docker.
- AI/ML Expertise: Built custom Retrieval-Augmented Generation (RAG) pipelines using Python, scikit-learn TF-IDF, vector search, and Anthropic Claude APIs.
- Experience with REST APIs, asynchronous task processing, and modular software architecture.
"""

USE_CASE_2_DATA = """
CAMPUS POLICIES & STUDENT HANDBOOK

1. Library Borrowing Rules:
Full-time undergraduate students are permitted to borrow a maximum of 4 books simultaneously for a period of up to 14 days. Graduate students and research scholars may borrow up to 8 books for 30 days. Overdue books incur a fine of $1 per day per item. Books may be renewed once online if not reserved by another student.

2. Hostel Curfew & Entry Regulations:
All undergraduate hostel residents must enter the campus gates by 9:30 PM on weekdays (Monday through Friday). On weekends (Saturday and Sunday), the curfew is extended to 10:30 PM. Any late entry after curfew requires prior written authorization or an official gate pass signed by the Hostel Warden. Repeated unexcused late arrivals lead to disciplinary warnings and potential loss of hostel accommodation.

3. Fee Payment Deadlines & Late Charges:
Semester tuition fees must be settled in full by the 5th of every semester starting month. A daily late fee penalty of $10 applies for payments made between the 6th and 20th of the month. Failure to clear dues by the 20th results in temporary suspension of student portal access and exam registration.

4. Attendance & Internal Examination Policy:
Mid-semester internal examinations contribute 30% toward the final grade in each subject. Students must maintain a mandatory minimum of 75% attendance across all lectures and laboratory sessions. Students falling below 75% attendance without verified medical justification will be debarred from writing internal and end-semester examinations.
"""

USE_CASE_3_DATA = """
OPERATING SYSTEMS: PROCESS SCHEDULING ALGORITHMS

First-Come, First-Served (FCFS) Scheduling:
FCFS is a non-preemptive algorithm where the process that requests the CPU first is allocated the CPU first. The primary disadvantage of FCFS is the Convoy Effect. The convoy effect occurs when a long CPU-bound process holds the processor, forcing multiple short I/O-bound processes to wait in the ready queue behind it. This results in poor CPU and device utilization and significantly increases the average waiting time for all processes.

Shortest Job First (SJF) Scheduling:
SJF associates with each process the length of its next CPU burst. The CPU is assigned to the process with the smallest next CPU burst. SJF produces the minimum average waiting time for a given set of processes. However, its main drawback is predicting the exact length of the next CPU burst, which can cause starvation for long-running processes if short processes continuously arrive.

Round Robin (RR) Scheduling:
Round Robin is a preemptive scheduling algorithm designed specifically for time-sharing systems. A small unit of time called a time quantum or time slice (typically 10 to 100 milliseconds) is defined. The CPU scheduler switches between processes when the time quantum expires. While Round Robin improves responsiveness and fairness, it adds CPU overhead due to frequent context switching. Every context switch requires saving process register states, updating process control blocks (PCBs), and flushing CPU caches. If the time quantum is set too small, context switching overhead consumes a huge fraction of total CPU cycles.
"""

USE_CASE_4_DATA = """
VOYAGER PRO 30L COMMUTER BACKPACK - PRODUCT INFO & STORE POLICIES

Product Description & Specifications:
The Voyager Pro 30L is engineered for daily urban commuters and travelers. It features a dedicated TSA-friendly padded laptop compartment that comfortably fits laptops up to 15.6 inches in size. Constructed from ultra-durable, water-resistant 900D Cordura ballistic nylon. Available color options: Obsidian Black, Navy Blue, and Forest Green.

Return & Refund Policy:
We offer a 15-day return window from the date of delivery. To be eligible for a full refund, items must be unused, unwashed, and returned in their original packaging with tags intact. Returns requested after the 15-day window will strictly not be accepted, and no refund or store credit will be issued.

Shipping Options & Rates:
Standard Shipping (3-5 business days): Free for orders over $50; flat rate of $5.99 for orders under $50. Express Shipping (2 business days): $14.99. All shipments include real-time tracking via email notification.

Warranty Coverage:
Every Voyager Pro backpack includes a Limited Lifetime Warranty. This covers manufacturing defects in materials, zipper tracks, stitching, and hardware fasteners. The warranty does not cover aesthetic wear-and-tear, abrasions, or damage caused by misuse.
"""

USE_CASE_5_DATA = """
LIBRARY API REFERENCE DOCUMENTATION: RAGEngine

Function 1: chunk_text(text: str, max_words: int, overlap: int) -> List[str]
Splits the input string into sequential text chunks based on word count limits.
- Parameters:
  * text (str): The raw string document to be partitioned.
  * max_words (int): The maximum number of words allowed per chunk.
  * overlap (int): The number of shared trailing/leading words retained between adjacent sliding-window chunks.
- Significance: Overlap is critical because it preserves boundary context between consecutive chunks, preventing key sentences or semantic concepts from being truncated or severed in half across chunk breaks.

Function 2: retrieve(query: str, top_k: int = 3) -> List[Tuple[int, float, str]]
Executes a vector search over pre-indexed document chunks using TF-IDF vectorization and Cosine Similarity.
- Parameters:
  * query (str): The search query string submitted by the user.
  * top_k (int): Number of top matching chunks to retrieve (default is 3).
- Returns: A list of tuples containing (1-based source index, similarity score float, chunk text string) ordered by similarity score descending.

Function 3: ask(query: str) -> str
Orchestrates context retrieval and LLM completion via the Anthropic Claude API.
- Process: Retrieves top_k chunks, formats them as source context, and builds a strictly grounded system prompt.
- Returns: A string response generated by the LLM citing explicit sources like `[Source X]`. If no relevant context is found or if the retrieved chunks do not contain sufficient evidence to answer the query, `ask()` returns exactly: "I don't have that information."
"""

# ==============================================================================
# MASTER EXECUTION FUNCTION
# ==============================================================================

def run_all_use_cases():
    use_cases = [
        {
            "id": 1,
            "title": "USE CASE 1: INTERVIEW PREP COACH",
            "persona": "an interview coach helping the candidate rehearse answers about their own experience",
            "doc_text": USE_CASE_1_DATA,
            "max_words": 80,
            "overlap": 15,
            "top_k": 2,
            "queries": [
                "Tell me about a project where you worked with real-time data.",
                "What's a project where you handled payments?",
                "What's your weakest area?"
            ]
        },
        {
            "id": 2,
            "title": "USE CASE 2: CAMPUS FAQ HELPDESK",
            "persona": "a friendly campus helpdesk assistant for students",
            "doc_text": USE_CASE_2_DATA,
            "max_words": 90,
            "overlap": 20,
            "top_k": 3,
            "queries": [
                "How many books can I borrow from the library?",
                "Can I enter the hostel at 10 PM on a Saturday?",
                "Can I get into trouble for being late?"
            ]
        },
        {
            "id": 3,
            "title": "USE CASE 3: EXAM STUDY BUDDY (TUNED CHUNK SIZE = 50, OVERLAP = 12)",
            "persona": "a patient study partner helping the student revise for an exam, using simple explanations",
            "doc_text": USE_CASE_3_DATA,
            "max_words": 50,
            "overlap": 12,
            "top_k": 3,
            "queries": [
                "Which scheduling algorithm causes the convoy effect and why?",
                "Why does Round Robin add overhead?"
            ]
        },
        {
            "id": 4,
            "title": "USE CASE 4: E-COMMERCE CUSTOMER SUPPORT",
            "persona": "a polite customer support agent for an online backpack store",
            "doc_text": USE_CASE_4_DATA,
            "max_words": 80,
            "overlap": 15,
            "top_k": 2,
            "queries": [
                "Does the backpack fit a 15-inch laptop, and what colors does it come in?",
                "If I return the backpack after 20 days, will I get a refund?"
            ]
        },
        {
            "id": 5,
            "title": "USE CASE 5: CODE & API DOCUMENTATION ASSISTANT",
            "persona": "a precise technical assistant explaining this library's API to a developer",
            "doc_text": USE_CASE_5_DATA,
            "max_words": 80,
            "overlap": 20,
            "top_k": 3,
            "queries": [
                "What does overlap do in chunk_text, and why does it matter?",
                "What does the ask() function return if nothing relevant is found?"
            ]
        }
    ]

    print("=" * 80)
    print("      COMPREHENSIVE RAG ENGINE - ALL 5 USE CASES (ALL-IN-ONE RUNNER)")
    print("=" * 80)

    for uc in use_cases:
        print("\n" + "=" * 80)
        print(f" {uc['title']} ")
        print("=" * 80)
        print(f"Persona: '{uc['persona']}'")
        print(f"Parameters: max_words={uc['max_words']}, overlap={uc['overlap']}, top_k={uc['top_k']}")

        # Initialize engine for use case
        engine = RAGEngine(
            doc_text=uc["doc_text"],
            persona=uc["persona"],
            max_words=uc["max_words"],
            overlap=uc["overlap"],
            top_k=uc["top_k"]
        )

        print(f"Document indexed into {len(engine.chunks)} chunks.")

        # Execute test queries
        for q in uc["queries"]:
            print(f"\n[QUERY]: {q}")
            response = engine.ask(q)
            print(f"[RESPONSE]:\n{response}")
            print("-" * 60)

if __name__ == "__main__":
    run_all_use_cases()

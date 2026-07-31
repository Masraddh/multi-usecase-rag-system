import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from engine.rag_engine import RAGEngine

DATA = """
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

PERSONA = "a friendly campus helpdesk assistant for students"

def main():
    print("=" * 70)
    print("USE CASE 2: CAMPUS FAQ HELPDESK")
    print("=" * 70)

    engine = RAGEngine(doc_text=DATA, persona=PERSONA, max_words=90, overlap=20, top_k=3)

    queries = [
        "How many books can I borrow from the library?",
        "Can I enter the hostel at 10 PM on a Saturday?",
        "Can I get into trouble for being late?"
    ]

    for q in queries:
        print(f"\n[QUERY]: {q}")
        response = engine.ask(q)
        print(f"[RESPONSE]:\n{response}")
        print("-" * 50)

if __name__ == "__main__":
    main()

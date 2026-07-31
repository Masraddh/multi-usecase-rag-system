import sys
import os

# Add root directory to sys.path for seamless imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from engine.rag_engine import RAGEngine

DATA = """
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

PERSONA = "an interview coach helping the candidate rehearse answers about their own experience"

def main():
    print("=" * 70)
    print("USE CASE 1: INTERVIEW PREP COACH")
    print("=" * 70)

    engine = RAGEngine(doc_text=DATA, persona=PERSONA, max_words=80, overlap=15, top_k=2)

    queries = [
        "Tell me about a project where you worked with real-time data.",
        "What's a project where you handled payments?",
        "What's your weakest area?"
    ]

    for q in queries:
        print(f"\n[QUERY]: {q}")
        response = engine.ask(q)
        print(f"[RESPONSE]:\n{response}")
        print("-" * 50)

if __name__ == "__main__":
    main()

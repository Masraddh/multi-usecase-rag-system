import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from engine.rag_engine import RAGEngine

DATA = """
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

PERSONA = "a polite customer support agent for an online backpack store"

def main():
    print("=" * 70)
    print("USE CASE 4: E-COMMERCE CUSTOMER SUPPORT")
    print("=" * 70)

    engine = RAGEngine(doc_text=DATA, persona=PERSONA, max_words=80, overlap=15, top_k=2)

    queries = [
        "Does the backpack fit a 15-inch laptop, and what colors does it come in?",
        "If I return the backpack after 20 days, will I get a refund?"
    ]

    for q in queries:
        print(f"\n[QUERY]: {q}")
        response = engine.ask(q)
        print(f"[RESPONSE]:\n{response}")
        print("-" * 50)

if __name__ == "__main__":
    main()

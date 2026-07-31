import os
import fitz  # PyMuPDF

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "backend", "data")

DOMAINS = ["interview", "campus", "study", "ecommerce", "code_docs"]

def create_pdf(filepath: str, title: str, sections: list):
    doc = fitz.open()
    page = doc.new_page()
    
    y = 40
    # Title
    page.insert_text((40, y), title, fontsize=16, fontname="helv")
    y += 30
    
    for heading, text in sections:
        if y > 750:
            page = doc.new_page()
            y = 40
        page.insert_text((40, y), heading, fontsize=12, fontname="helv")
        y += 20
        
        lines = text.split("\n")
        for line in lines:
            if y > 770:
                page = doc.new_page()
                y = 40
            page.insert_text((40, y), line, fontsize=10, fontname="helv")
            y += 15
        y += 10
        
    doc.save(filepath)
    doc.close()
    print(f"Created PDF: {filepath}")

def setup_all():
    # 1. Create directory structure
    for dom in DOMAINS:
        dom_dir = os.path.join(DATA_DIR, dom)
        up_dir = os.path.join(DATA_DIR, "uploads", dom)
        os.makedirs(dom_dir, exist_ok=True)
        os.makedirs(up_dir, exist_ok=True)

    # -------------------------------------------------------------
    # 1. INTERVIEW COACH
    # -------------------------------------------------------------
    create_pdf(
        os.path.join(DATA_DIR, "interview", "resume.pdf"),
        "CANDIDATE RESUME - SHAIK MASRADDH",
        [
            ("PROFESSIONAL SUMMARY", "B.Tech candidate in Information Technology from G. Narayanamma Institute of Technology and Science (2022-2026) with a 7.75 CGPA.\nSpecializes in Full-Stack Web Development, React Native, SQL, and Retrieval-Augmented Generation (RAG) pipelines."),
            ("EDUCATION", "Bachelor of Technology (B.Tech) in IT: G. Narayanamma Institute of Technology and Science (2022-2026), CGPA: 7.75.\nIntermediate: Government Junior College (Girls), 81%.\nSSC: St. Claire High School."),
            ("KEY SKILLS", "Languages: Python, SQL, JavaScript, TypeScript, C++.\nFrameworks: React Native, React.js, Next.js, FastAPI, Node.js, Power BI, Docker, Git.\nAI/ML: Retrieval-Augmented Generation (RAG), TF-IDF Vector Search, Scikit-Learn, PyTorch, Anthropic Claude & Gemini APIs.")
        ]
    )

    create_pdf(
        os.path.join(DATA_DIR, "interview", "project_report.pdf"),
        "TECHNICAL PROJECTS REPORT",
        [
            ("PROJECT 1: SOILSMART MONITORING SYSTEM", "Engineered an IoT smart soil monitoring system using Python microcontrollers, sensors, and Random Forest ML algorithms.\nStreams real-time soil moisture, pH, and temperature metrics to cloud dashboards, reducing farm water usage by 35%."),
            ("PROJECT 2: REAL-TIME EVENT BOOKING & CHAT APP", "Developed a cross-platform mobile application using React Native, WebSockets, and Firebase Realtime Database.\nHandled live seat selection and instant push notifications for over 10,000 active users, optimizing render performance by 35% using React Hooks."),
            ("PROJECT 3: SALES ANALYTICS & ETL DASHBOARD", "Completed a 3-month Data Analytics internship building executive dashboards in Power BI and writing complex SQL procedures to transform 500k+ customer records.")
        ]
    )

    create_pdf(
        os.path.join(DATA_DIR, "interview", "internship_certificate.pdf"),
        "DATA ANALYTICS INTERNSHIP CERTIFICATE",
        [
            ("INTERNSHIP COMPLETION", "Successfully completed a 3-month Data Analytics Internship.\nFormulated complex SQL queries transforming 500,000+ transaction records, saving 15 hours per week in executive reporting workflows.")
        ]
    )

    with open(os.path.join(DATA_DIR, "interview", "skills.txt"), "w", encoding="utf-8") as f:
        f.write(
            "CANDIDATE TECHNICAL SKILLS & COMPETENCIES:\n"
            "- Languages & Tools: Python, SQL, JavaScript, React Native, Power BI, Git, Docker, WebSockets.\n"
            "- Machine Learning: Retrieval-Augmented Generation (RAG) architecture, TF-IDF vector search, Groq Cloud LLaMA-3.3, Google Gemini APIs.\n"
            "- Database Engineering: PostgreSQL, SQLite, Firebase Realtime Database, ETL Data Pipelines."
        )

    # -------------------------------------------------------------
    # 2. CAMPUS FAQ
    # -------------------------------------------------------------
    create_pdf(
        os.path.join(DATA_DIR, "campus", "college_handbook.pdf"),
        "COLLEGE HANDBOOK & ACADEMIC POLICIES",
        [
            ("ATTENDANCE POLICY", "Students must maintain a minimum of 75% overall attendance to be eligible for semester end examinations.\nAttendance between 65% and 74% requires medical condonation approval from the Principal."),
            ("GRADING SYSTEM", "Grades are evaluated on a 10-point scale: O (10), A+ (9), A (8), B+ (7), B (6), C (5), P (4), F (0).")
        ]
    )

    create_pdf(
        os.path.join(DATA_DIR, "campus", "hostel_rules.pdf"),
        "STUDENT HOSTEL RULES & REGULATIONS",
        [
            ("CURFEW HOURS", "Hostel entry deadline is strictly 8:30 PM for female students and 9:00 PM for male students.\nLate arrivals require prior written approval from the Warden and Guardian notification."),
            ("VISITOR POLICY", "Visitors are allowed only in the reception lounge between 4:00 PM and 6:30 PM on weekends.")
        ]
    )

    create_pdf(
        os.path.join(DATA_DIR, "campus", "library_rules.pdf"),
        "LIBRARY BORROWING RULES & TIMINGS",
        [
            ("BORROWING LIMITS", "Undergraduate students may borrow up to 4 books simultaneously for a duration of 14 days.\nBooks can be renewed once online if no hold exists."),
            ("OVERDUE FINES", "A fine of Rs. 5 per book per day is levied for overdue returns after the due date.")
        ]
    )

    create_pdf(
        os.path.join(DATA_DIR, "campus", "fee_structure.pdf"),
        "TUITION & ACADEMIC FEE STRUCTURE",
        [
            ("PAYMENT SCHEDULE", "Tuition fees must be paid in full at the beginning of each academic year prior to semester registration.\nLate payment attracts a penalty of Rs. 100 per day after the due date.")
        ]
    )

    # -------------------------------------------------------------
    # 3. STUDY BUDDY
    # -------------------------------------------------------------
    create_pdf(
        os.path.join(DATA_DIR, "study", "operating_systems.pdf"),
        "OPERATING SYSTEMS STUDY GUIDE",
        [
            ("1. FCFS SCHEDULING", "First-Come, First-Served (FCFS) allocates CPU in order of process arrival.\nIt is non-preemptive and causes the convoy effect where short processes wait behind long ones."),
            ("2. SJF SCHEDULING", "Shortest Job First (SJF) selects the process with the shortest burst time.\nSJF is provably optimal, giving minimal average waiting time for a given set of processes."),
            ("3. ROUND ROBIN SCHEDULING", "Round Robin (RR) assigns a fixed time quantum (e.g. 10ms) per process in a circular queue.\nIt provides fast response time for interactive systems but increases context switching overhead.")
        ]
    )

    create_pdf(
        os.path.join(DATA_DIR, "study", "dbms.pdf"),
        "DATABASE MANAGEMENT SYSTEMS (DBMS)",
        [
            ("ACID PROPERTIES", "Transactions must satisfy Atomicity, Consistency, Isolation, and Durability.\nAtomicity guarantees that all operations complete or none do. Isolation ensures concurrent transactions execute independently."),
            ("NORMALIZATION", "1NF removes duplicate columns. 2NF removes partial dependencies. 3NF removes transitive dependencies.")
        ]
    )

    with open(os.path.join(DATA_DIR, "study", "sql_notes.txt"), "w", encoding="utf-8") as f:
        f.write(
            "SQL QUICK REFERENCE & QUERY GUIDE:\n"
            "- SELECT, JOIN (INNER, LEFT, RIGHT, FULL), GROUP BY, HAVING, ORDER BY.\n"
            "- Aggregate Functions: COUNT(), SUM(), AVG(), MIN(), MAX().\n"
            "- Subqueries & CTEs: WITH Clause for recursive and complex analytical queries."
        )

    # -------------------------------------------------------------
    # 4. ECOMMERCE SUPPORT
    # -------------------------------------------------------------
    create_pdf(
        os.path.join(DATA_DIR, "ecommerce", "product_catalog.pdf"),
        "VOYAGER PRO 30L BACKPACK SPECIFICATIONS",
        [
            ("PRODUCT OVERVIEW", "The Voyager Pro 30L is an ergonomic, weather-resistant travel and laptop backpack.\nFeatures a 15.6-inch padded laptop compartment, TSA-friendly lay-flat design, and anti-theft hidden pockets."),
            ("SPECS & COLORS", "Capacity: 30 Liters. Dimensions: 18.5 x 12.5 x 7.5 inches. Weight: 2.1 lbs.\nAvailable Colors: Midnight Black, Charcoal Gray, Electric Blue, and Alpine Olive.")
        ]
    )

    create_pdf(
        os.path.join(DATA_DIR, "ecommerce", "shipping_policy.pdf"),
        "SHIPPING & DELIVERY POLICY",
        [
            ("DELIVERY TIMELINES", "Standard domestic shipping takes 3-5 business days.\nExpress delivery takes 1-2 business days. Free shipping on orders over $50.")
        ]
    )

    create_pdf(
        os.path.join(DATA_DIR, "ecommerce", "return_policy.pdf"),
        "RETURNS & REFUND POLICY",
        [
            ("15-DAY RETURN WINDOW", "Customers may return unused products in original packaging within 15 days of purchase for a 100% full refund.\nPrepaid return shipping labels are provided.")
        ]
    )

    create_pdf(
        os.path.join(DATA_DIR, "ecommerce", "warranty.pdf"),
        "WARRANTY COVERAGE",
        [
            ("LIFETIME WARRANTY", "All Voyager Series backpacks include a 2-year limited warranty covering zipper failures, seam tears, and manufacturing defects.")
        ]
    )

    # -------------------------------------------------------------
    # 5. CODE DOCS
    # -------------------------------------------------------------
    create_pdf(
        os.path.join(DATA_DIR, "code_docs", "developer_guide.pdf"),
        "RAG ENGINE DEVELOPER & API GUIDE",
        [
            ("RAG ENGINE CLASS", "The core RAGEngine class performs sliding-window chunking, TF-IDF vectorization, Cosine Similarity retrieval, and LLM answer generation."),
            ("METHODS REFERENCE", "- chunk_document(text, max_words, overlap)\n- build_vector_index(chunks)\n- retrieve(query, top_k)\n- ask_detailed(query)")
        ]
    )

    with open(os.path.join(DATA_DIR, "code_docs", "README.md"), "w", encoding="utf-8") as f:
        f.write(
            "# RAG AI Assistant Suite Documentation\n\n"
            "## Architecture\n"
            "Combines sliding-window chunking, TF-IDF vector search, FastAPI backend, and Next.js frontend.\n\n"
            "## Installation\n"
            "```bash\n"
            "pip install -r requirements.txt\n"
            "npm install --prefix frontend\n"
            "```\n\n"
            "## Execution\n"
            "Start backend: `uvicorn backend.main:app --port 8000`\n"
            "Start frontend: `npm run dev --prefix frontend`\n"
        )

    print("[SUCCESS] Created all default Knowledge Base PDF, TXT, and Markdown documents!")

if __name__ == "__main__":
    setup_all()

import subprocess
import sys
import os

use_cases = [
    "use_cases/01_interview_prep.py",
    "use_cases/02_campus_faq.py",
    "use_cases/03_study_buddy.py",
    "use_cases/04_ecommerce_support.py",
    "use_cases/05_code_docs.py",
]

def main():
    print("=" * 80)
    print("RUNNING ALL 5 RAG USE CASES SEQUENTIALLY")
    print("=" * 80)
    
    for script in use_cases:
        print(f"\n>>> Executing {script}...\n")
        res = subprocess.run([sys.executable, script], capture_output=True, text=True)
        print(res.stdout)
        if res.stderr and "UserWarning" not in res.stderr:
            print(f"[STDERR]: {res.stderr}")
        print("=" * 80)

if __name__ == "__main__":
    main()

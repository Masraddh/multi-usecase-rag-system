import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from engine.rag_engine import RAGEngine

DATA = """
OPERATING SYSTEMS: PROCESS SCHEDULING ALGORITHMS

First-Come, First-Served (FCFS) Scheduling:
FCFS is a non-preemptive algorithm where the process that requests the CPU first is allocated the CPU first. The primary disadvantage of FCFS is the Convoy Effect. The convoy effect occurs when a long CPU-bound process holds the processor, forcing multiple short I/O-bound processes to wait in the ready queue behind it. This results in poor CPU and device utilization and significantly increases the average waiting time for all processes.

Shortest Job First (SJF) Scheduling:
SJF associates with each process the length of its next CPU burst. The CPU is assigned to the process with the smallest next CPU burst. SJF produces the minimum average waiting time for a given set of processes. However, its main drawback is predicting the exact length of the next CPU burst, which can cause starvation for long-running processes if short processes continuously arrive.

Round Robin (RR) Scheduling:
Round Robin is a preemptive scheduling algorithm designed specifically for time-sharing systems. A small unit of time called a time quantum or time slice (typically 10 to 100 milliseconds) is defined. The CPU scheduler switches between processes when the time quantum expires. While Round Robin improves responsiveness and fairness, it adds CPU overhead due to frequent context switching. Every context switch requires saving process register states, updating process control blocks (PCBs), and flushing CPU caches. If the time quantum is set too small, context switching overhead consumes a huge fraction of total CPU cycles.
"""

PERSONA = "a patient study partner helping the student revise for an exam, using simple explanations"

def main():
    print("=" * 70)
    print("USE CASE 3: EXAM STUDY BUDDY (TUNED CHUNK SIZE = 50, OVERLAP = 12)")
    print("=" * 70)

    # Note: Parameters tuned down to max_words=50, overlap=12 for dense academic text
    engine = RAGEngine(
        doc_text=DATA,
        persona=PERSONA,
        max_words=50,
        overlap=12,
        top_k=3
    )

    queries = [
        "Which scheduling algorithm causes the convoy effect and why?",
        "Why does Round Robin add overhead?"
    ]

    for q in queries:
        print(f"\n[QUERY]: {q}")
        response = engine.ask(q)
        print(f"[RESPONSE]:\n{response}")
        print("-" * 50)

if __name__ == "__main__":
    main()

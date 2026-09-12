import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.rag.retriever import retriever

def test_queries():
    # 1. Topic query
    q1 = "How do I improve user retention in B2B SaaS?"
    res1 = retriever.search(q1)
    print(f"\nQuery: '{q1}'")
    print(f"Grounded: {res1['is_grounded']} | Top Score: {res1['top_score']}")
    for r in res1["results"][:2]:
        print(f"  * {r['guest']} ({r['timestamp']}): {r['title'][:60]}")

    # 2. Out-of-domain query
    q2 = "How to build a nuclear fusion reactor with uranium?"
    res2 = retriever.search(q2)
    print(f"\nQuery: '{q2}'")
    print(f"Grounded: {res2['is_grounded']} | Top Score: {res2['top_score']}")

    # 3. Specific guest query
    q3 = "What does Brian Balfour say about growth loops?"
    res3 = retriever.search(q3)
    print(f"\nQuery: '{q3}'")
    print(f"Grounded: {res3['is_grounded']} | Top Score: {res3['top_score']}")
    for r in res3["results"][:2]:
        print(f"  * {r['guest']} ({r['timestamp']}): {r['title'][:60]}")

if __name__ == "__main__":
    test_queries()

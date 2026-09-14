"""
Automated verification script for Lenny Growth Assistant RAG pipeline.
Validates:
- TF-IDF indexing and chunk retrieval
- Grounding score thresholds
- Timestamp parsing and YouTube deep linking
- Strict 1-per-guest source diversity
"""
import sys
import os

backend_path = os.path.join(os.path.dirname(__file__), "..", "backend")
sys.path.insert(0, backend_path)

from app.rag.retriever import retriever

def test_rag_pipeline():
    print("[*] Running RAG Pipeline Verification...")
    test_queries = [
        "Create a product strategy framework",
        "How should a startup identify its ideal customer?",
        "Why do SaaS products struggle with retention?"
    ]

    for query in test_queries:
        print(f"\n--- Testing Query: '{query}' ---")
        res = retriever.search(query, top_k=4)
        assert res["is_grounded"], f"Query '{query}' failed grounding check!"
        assert len(res["results"]) > 0, "No results returned!"
        
        guests = [r["guest"] for r in res["results"]]
        # Ensure strict diversity (no duplicate guests)
        assert len(guests) == len(set(guests)), f"Duplicate guests detected: {guests}"
        
        for r in res["results"]:
            print(f"  [+] Guest: {r['guest']} | Timestamp: {r['timestamp']}")
            print(f"      YouTube URL: {r['youtube_url']}")
            if r["youtube_url"]:
                assert "t=" in r["youtube_url"], f"Missing timestamp param in {r['youtube_url']}"

    print("\n[SUCCESS] All RAG verification checks passed successfully!")

if __name__ == "__main__":
    test_rag_pipeline()

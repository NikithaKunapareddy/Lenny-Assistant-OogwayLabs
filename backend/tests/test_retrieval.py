import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.rag.retriever import retriever

def test_retriever_initialization():
    assert retriever.is_loaded is True
    assert len(retriever.chunks) > 500
    assert len(retriever.chunk_ids) == len(retriever.chunks)

def test_grounding_retention():
    res = retriever.search("How do I improve user retention in SaaS?", top_k=3)
    assert res["is_grounded"] is True
    assert res["top_score"] > 0.08
    assert len(res["results"]) > 0
    # Check that sources contain known retention leaders
    guests = [r["guest"] for r in res["results"]]
    assert any(g in ["Elena Verna", "Brian Balfour", "Casey Winters", "Gibson Biddle"] for g in guests)

def test_grounding_growth_loops():
    res = retriever.search("What did Brian Balfour say about growth loops vs funnels?", top_k=3)
    assert res["is_grounded"] is True
    assert res["top_score"] > 0.10
    top_guest = res["results"][0]["guest"]
    assert "Brian Balfour" in top_guest

def test_out_of_domain_refusal():
    res = retriever.search("How do you build a nuclear enrichment facility for radioactive isotopes?", top_k=3)
    # Score should be low and rejected by threshold
    assert res["top_score"] < 0.085 or not res["is_grounded"]

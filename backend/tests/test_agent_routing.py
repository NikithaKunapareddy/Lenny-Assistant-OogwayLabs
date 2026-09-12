import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.agent.orchestrator import agent_orchestrator

def test_intent_routing_qna():
    queries = [
        "How do I improve user retention in B2B?",
        "What is product-market fit according to Sean Ellis?",
        "Explain the Four Fits framework",
        "How does Miro drive viral activation?"
    ]
    for q in queries:
        assert agent_orchestrator.route_intent(q) == "qna"

def test_intent_routing_ship30():
    queries = [
        "Can you turn this into an essay?",
        "Write an essay about product activation",
        "Write a Ship 30 style article on onboarding",
        "Create a deep dive post about churn reduction"
    ]
    for q in queries:
        assert agent_orchestrator.route_intent(q) == "ship30"

def test_intent_routing_artifact():
    queries = [
        "Create a product growth framework",
        "Generate a framework for retention",
        "Build a checklist for B2B onboarding",
        "Generate an HTML visual model for growth loops"
    ]
    for q in queries:
        assert agent_orchestrator.route_intent(q) == "artifact"

# Agent Transcript 03: Intent Routing, Ship 30 Skill & Artifact Generation

**Date:** 2026-09-12  
**Role:** Forward Deployed Engineer  
**Focus:** Intent Classification, Prompt Engineering, Boundary Enforcement  

---

## 1. Challenge: Substring False Positives in Intent Routing

### The Problem
During automated agent testing, query `"Explain the Four Fits framework"` unexpectedly routed to `artifact` instead of conversational `qna`.
Root cause: The router used simple keyword presence:
```python
if any(term in query.lower() for term in ["framework", ...]):
    return "artifact"
```
Because the user said "framework", the system assumed they wanted an HTML artifact built, even though they were asking for an explanation.

### The Correction
We refactored `route_intent` in `backend/app/agent/orchestrator.py`:
1. Separated **explanation queries** (`explain`, `what is`, `describe`) from **creation actions** (`create`, `generate`, `build`).
2. Implemented regex matching:
   ```python
   is_artifact_request = bool(re.search(
       r'\b(create|generate|build|make|design)\b.*\b(framework|checklist|artifact|matrix|template|canvas|visual model|html)\b',
       q
   ))
   ```
This accurately routed "Explain the Four Fits framework" to `qna`, and "Create a retention audit framework" to `artifact`.

---

## 2. Challenge: Accidental Keyword Bleed in Mock LLM

### The Problem
When generating a framework artifact for "Create a retention audit framework", the mock client returned a Ship 30 essay instead of an HTML component.
Root cause: The prompt passed to the LLM included retrieved transcript passages from Brian Balfour, which contained the word "essay" in the episode description. The mock client checked `if "essay" in prompt.lower()`, matching the transcript passage rather than the user's intent.

### The Correction
In `backend/app/llm/mock_client.py`, we updated the generator to inspect `system_prompt`:
```python
sys_p = (system_prompt or "").lower()
if "ship 30" in sys_p or "1,250 words" in sys_p:
    return self._generate_ship30_essay(prompt)
if "artifact" in sys_p or "html code block" in sys_p:
    return self._generate_artifact(prompt)
```
This decoupled intent identification from accidental keywords in retrieved text passages.

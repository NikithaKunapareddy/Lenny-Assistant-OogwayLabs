# Agent Transcript 04: Grounding Guardrails, Security Sandboxing & Testing

**Date:** 2026-09-12  
**Role:** Forward Deployed Engineer  
**Focus:** Out-of-Domain Detection, Iframe Isolation, Test Suite Validation  

---

## 1. Challenge: Out-of-Domain False Positives

### The Problem
When evaluating the out-of-domain query:
*"How do you build a nuclear enrichment facility for radioactive isotopes?"*
The raw cosine similarity score was `0.1124`, which was slightly above the base threshold of `0.085`.
Root cause: English stop words ("how", "do", "you", "build", "a", "for") occurred frequently across the 700+ podcast chunks, producing a non-zero cosine similarity even though the query had zero connection to Product Management.

### The Correction
In `backend/app/rag/retriever.py`, we implemented a **Domain Lexicon Guardrail**:
- Defined a set of 38 canonical PM/growth concepts (`growth`, `retention`, `pmf`, `churn`, `pricing`, `activation`, `saas`, `amplitude`, `reforge`, etc.).
- Evaluated whether the query contains at least one domain term or a known guest name.
- If zero domain terms exist, the search immediately returns `top_score = 0.0` and `is_grounded = False`, guaranteeing 100% rejection on irrelevant topics without hallucination.

---

## 2. Security Defense-in-Depth for Untrusted HTML

### Threat Modeling
AI models can be prompted to output `<script>` tags, inline event handlers (`onload`, `onerror`), or external `<iframe>` tags that could attempt to execute JavaScript inside the host web app.

### The Multi-Layer Mitigation
1. **Backend Sanitization (`ArtifactSkill._sanitize_html`):**
   - Regex strips all `<script>` tags and inner content.
   - Regex strips all `on\w+=` attributes (e.g. `onclick="alert()"`).
   - Replaces `javascript:` links with `#`.
   - Strips nested `<iframe>`, `<object>`, and `<embed>` tags.
2. **Frontend Iframe Isolation (`ArtifactViewer.jsx`):**
   - Renders inside an `iframe` with `sandbox="allow-scripts"`.
   - Crucially omits `allow-same-origin`, placing the iframe in an isolated null origin that cannot read cookies, local storage, or application tokens.
   - Enforces a Content Security Policy (CSP):
     `default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline';`

---

## 3. Automated Test Verification

We ran the complete test suite with `pytest -v backend/tests/`:
- **16 passed, 0 failed** in 12.96 seconds.
- Validated:
  - Health & root endpoints
  - Session CRUD and persistence isolation
  - Hybrid RAG retrieval and out-of-domain rejection
  - Agent routing across Q&A, Ship 30, and Artifacts
  - Full end-to-end conversation flows

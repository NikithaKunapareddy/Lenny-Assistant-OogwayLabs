# Product Requirements Document (PRD)
## The Lenny Growth Assistant

**Document Version:** 1.0.0  
**Author:** Forward Deployed Engineer  
**Status:** Approved & Implemented  
**Target Engagement:** Internal AI Product & Growth Intelligence Tool  

---

## 1. Executive Summary & Discovery Brief

### 1.1 Customer & Primary User
- **Target Persona:** Growth Product Managers, Heads of Growth, Founders, and Product Marketing Managers.
- **Core Jobs-to-be-Done (JTBD):**
  1. *Strategic Diagnosis:* Diagnosing activation drop-offs, user churn, and monetization hurdles by querying proven playbooks from industry leaders.
  2. *Synthesized Communication:* Converting tactical advice into executive-ready essays and strategy memos without spending hours writing from scratch.
  3. *Framework Generation:* Turning abstract podcast advice into concrete, interactive checklists and operational matrices that cross-functional teams can immediately execute.
- **Pain Points Solved:**
  - *Unindexed Podcast Data:* Hundreds of hours of elite interviews exist in Lenny's Podcast, but manually searching through transcripts or audio is time-prohibitive.
  - *Generic LLM Hallucination:* Off-the-shelf models (ChatGPT/Claude) generate generic, unsourced frameworks that lack practitioner depth and cannot be verified against credible primary sources.
  - *Privacy & Cost Anxiety:* Teams need the flexibility to run local models (via Ollama) on company laptops without sending sensitive strategy data over external APIs or accumulating API bills.

### 1.2 Success Metrics
- **Retrieval Grounding Precision:** >= 90% of factual statements in assistant responses cite direct transcript quotes and timestamps.
- **Zero Hallucination on Unsupported Queries:** 100% of out-of-domain queries (e.g., nuclear physics, healthcare) trigger an explicit refusal stating that the topic falls outside Lenny's knowledge base.
- **Essay Generation Fidelity:** Generated essays meet Ship 30 for 30 standards (1-3-1 hook rule, high-contrast headings, scannable bullet points, ~1,250 words).
- **Time to Deployment:** Client evaluators can launch the application with a single command (`docker compose up`) in < 2 minutes.

---

## 2. Assumptions, Scope & Trade-offs

### 2.1 Assumptions Recorded
1. *Corpus Format:* The knowledge base is derived from high-quality markdown transcripts containing YAML frontmatter and speaker timestamps.
2. *Evaluation Environment:* Evaluators test the application locally on modern operating systems (macOS, Windows, Linux) with Docker and optional Ollama installations.
3. *Single-Tenant Isolation:* The application serves internal product teams; session isolation in PostgreSQL/SQLite is prioritized over enterprise multi-tenant RBAC.

### 2.2 Scope Choices

| Feature Area | Included in Scope | Intentionally Excluded | Rationale |
| :--- | :--- | :--- | :--- |
| **Knowledge Base** | 700+ dialogue-aware chunks from 15 iconic Lenny episodes (Elena Verna, Brian Balfour, Casey Winters, etc.) | Real-time audio ingestion via Whisper | Transcripts are already curated and verified; raw audio transcription introduces compute overhead without improving answer accuracy. |
| **Model Runtime** | Dual Local (Ollama `llama3:latest`) + Cloud (Anthropic / OpenAI) + Deterministic Grounded Fallback | Fine-tuning model weights | RAG with dynamic prompting ensures zero hallucinations and source citations, which fine-tuning cannot reliably guarantee. |
| **Artifacts** | Native in-app side-by-side viewer for HTML/CSS frameworks with strict sandbox isolation | Full WYSIWYG editor | Product managers need immediate visual consumption, code copying, and HTML export; editing is secondary to rapid framework deployment. |
| **Authentication** | Session-based storage in PostgreSQL / SQLite | OAuth2 / SSO / Stripe billing | Eliminates onboarding friction for client evaluators while providing clean session history. |

### 2.3 Key Risks & Mitigation Strategies
1. **Model Hallucination:** Mitigated by a hybrid TF-IDF + keyword vector retriever and a strict domain guardrail. Queries with zero domain keyword overlap are refused immediately.
2. **Untrusted HTML Execution:** Mitigated via defense-in-depth: backend regex sanitization strips `<script>` tags, event handlers (`onclick`, `onerror`), and `javascript:` URIs before persistence. The frontend renders artifacts inside `<iframe sandbox="allow-forms" referrerPolicy="no-referrer">` — this permits interactive form elements (checkboxes) while blocking all script execution, parent DOM access, cookie access, and origin leakage.
3. **Local LLM Latency & Availability:** Mitigated by runtime model switcher with automated fallback to the internal Grounded Engine if Ollama is unreachable.

---

## 3. User Flows & Interaction Model

```
[ User Lands on App ]
         │
         ├── Selects Active Model (Ollama Local / Cloud / Fallback)
         │
         ▼
[ Enters Strategy Query ]  ──────> (e.g. "How do I fix leaky B2B SaaS retention?")
         │
         ▼
[ Backend RAG Search ]
         │
         ├── Grounded Match? ──(No)──> [ Refusal Response with Out-of-Domain Notice ]
         │
        (Yes)
         ▼
[ Intent Routing ]
         ├── Q&A ───────────────> Grounded Answer + Source Cards (Guest, Episode, Timestamp)
         ├── "Turn into essay" ─> Ship 30 for 30 Essay (~1,250 words, 1-3-1 hook, actionable takeaways)
         └── "Create framework" ─> Artifact Viewer Opens ──> Visual HTML Preview / Source Code / Export
```

---

## 4. Acceptance Criteria

- **AC-1 (Grounded Q&A):** Queries about PM/growth return answers citing specific guests, episodes, and quoted passages.
- **AC-2 (Out-of-Domain Guardrail):** Unrelated queries return: *"I couldn't find sufficient information about this topic in the available Lenny's Podcast transcripts."*
- **AC-3 (Ship 30 Skill):** Requests with "essay", "article", or "Ship 30" produce a structured post with a 1-3-1 hook, subheadings, and actionable takeaways.
- **AC-4 (Artifact Viewer):** Framework requests render interactive HTML/CSS in an adjacent pane without redirecting to external tools.
- **AC-5 (Security Sandboxing):** Untrusted script tags and dangerous event handlers are stripped; iframe renders in a null origin.
- **AC-6 (Model Toggle):** Evaluators can switch between Ollama and cloud providers via the UI without modifying source code.
- **AC-7 (Multi-Session Persistence):** Multiple chats maintain independent conversation history in PostgreSQL / SQLite.
- **AC-8 (One-Command Startup):** `docker compose up` starts PostgreSQL, the FastAPI backend, and the React frontend.

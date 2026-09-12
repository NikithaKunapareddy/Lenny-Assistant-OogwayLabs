# Demo Video Script & Walkthrough Guide (2–3 Minutes)
## "The Lenny Growth Assistant" — Forward Deployed Engineer Assessment

**Recording Requirements:**
- **Duration:** 2 to 3 minutes strictly.
- **Camera:** Enabled in corner (picture-in-picture webcam).
- **Audio:** Clear voiceover.
- **Deliverable:** Upload unlisted or public on YouTube and paste the link into the submission form.

---

## Script Breakdown & Timing

```
+---------------+------------------------------------------------------+--------------------------------------------------+
| Timestamp     | Visual on Screen                                     | Talking Points (What to Say)                     |
+---------------+------------------------------------------------------+--------------------------------------------------+
| 0:00 - 0:30   | Webcam + Project Overview / Landing Page             | Problem Framing & What You Built                 |
| 0:30 - 1:15   | Chat UI + Live Grounded Q&A + Citation Accordion     | Grounded Conversational Q&A (Elena & Brian)      |
| 1:15 - 1:50   | Ollama Terminal + Active Model Switcher in UI        | Mandatory Ollama Demonstration & Resilience      |
| 1:50 - 2:30   | Side-by-Side Artifact Viewer + Ship 30 Essay         | Ship 30 Content Skill & Sandboxed Artifacts      |
| 2:30 - 3:00   | Architecture Diagram / Code / Terminal               | Technical Trade-off & Operational Handoff        |
+---------------+------------------------------------------------------+--------------------------------------------------+
```

---

### Segment 1: The Problem & Introduction (0:00 – 0:30)
> **[Camera ON, show app interface at `http://localhost:5173` or `http://localhost:3000`]**
>  
> *"Hi everyone, I'm presenting **The Lenny Growth Assistant**, built for the Forward Deployed Engineer take-home assessment.  
>  
> Product teams have access to hundreds of hours of elite product wisdom from Lenny's Podcast, but extracting actionable answers is slow and unindexed. Generic LLMs hallucinate frameworks and miss practitioner nuances.  
>  
> We built a full-stack, enterprise-grade AI assistant that turns Lenny's Podcast transcripts into a grounded knowledge base—supporting multi-session conversations, Ship 30 for 30 essay writing, and native sandboxed artifact rendering."*

---

### Segment 2: Grounded Q&A & Transcript Citations (0:30 – 1:15)
> **[Click on the preset: "How do I improve user retention in B2B SaaS?"]**
>  
> *"Let's ask a strategic question: 'How do I improve user retention in B2B SaaS?'  
>  
> Notice the assistant doesn't give a generic summary. It synthesizes insights directly from **Elena Verna** on onboarding churn vs habit loops, and **Brian Balfour** on the Four Fits Framework.  
>  
> Down here, you see the **Grounded Sources accordion**. Clicking it reveals the exact guest attribution, the episode title, start timestamps, and direct quotes from the transcript archive.  
>  
> If we ask an unsupported out-of-domain question—like 'How do you build a nuclear reactor?'—the system rejects it immediately with an explicit refusal, preventing hallucinations."*

---

### Segment 3: Demonstrating Local Ollama & Model Toggle (1:15 – 1:50)
> **[Show the Model Selector in the Left Sidebar toggled to 'Ollama Local (llama3:latest)']**
>  
> *"A mandatory requirement for this engagement is supporting a local LLM via Ollama.  
>  
> In the sidebar, you can see our runtime model selector. Here it is running locally with **Ollama on `llama3:latest`**.  
>  
> We can seamlessly toggle between local Ollama and cloud providers like Anthropic Claude or OpenAI without modifying code or restarting the server.  
>  
> Furthermore, if Ollama or external APIs are temporarily unreachable, our backend includes an automated fallback to an internal Grounded Engine, guaranteeing zero 500 errors during client evaluation."*

---

### Segment 4: Ship 30 for 30 Essay & Side-by-Side Artifact Viewer (1:50 – 2:30)
> **[Type: "Turn this into a framework" -> Watch Artifact Viewer open on the right]**
>  
> *"Next, let's see our specialized skills. When a user asks to turn advice into a long-form essay, our **Ship 30 for 30 skill** produces a structured ~1,250-word piece following the 1-3-1 hook rule and scannable formatting.  
>  
> And when the user asks for a framework, the assistant generates a complete HTML/CSS component.  
>  
> Instead of dumping raw code in the chat, it opens directly in our **Artifact Viewer** beside the chat. Evaluators can interact with styled checklists, review the source code, or download the HTML.  
>  
> For security, the HTML is strictly sanitized on the backend, and rendered in an `iframe` with `sandbox='allow-scripts'` and no `allow-same-origin`, ensuring untrusted code can never access cookies or host application tokens."*

---

### Segment 5: Technical Trade-off & Conclusion (2:30 – 3:00)
> **[Show `docker-compose.yml` or terminal with 16 passed tests]**
>  
> *"One important technical trade-off we made was using **dialogue-aware sliding semantic chunking** and hybrid TF-IDF vector search rather than a complex distributed vector cluster. Because podcast discussions evolve across conversational turns, grouping by speaker dialogue preserved quote integrity while keeping the entire knowledge base lightweight enough to launch in seconds via `docker compose up`.  
>  
> All 16 automated tests pass, and complete documentation is available in our PRD, architecture, and design documents. Thank you!"*

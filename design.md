# Design & UI/UX Documentation
## The Lenny Growth Assistant

**Document Version:** 1.0.0  
**Status:** Implemented  

---

## 1. UI/UX Principles & Aesthetic Philosophy

The Lenny Growth Assistant is designed around four core design pillars:

1. **Executive-Grade Visual Polish:**
   - Deep slate color palette (`#090d16` background, `#0f172a` panels, `#1e293b` cards) inspired by Linear and Claude Artifacts.
   - Glassmorphism (`backdrop-filter: blur(16px)` with 8% white borders) to create depth and visual hierarchy.
   - High-contrast typography using Google's **Inter** for clean readability and **JetBrains Mono** for timestamps and code blocks.

2. **Zero-Cognitive-Load Information Architecture:**
   - **3-Pane Split Screen:**
     - *Left Pane (Width: 288px):* Sessions, model toggle, and evaluator quick presets.
     - *Center Pane (Flexible):* Conversational stream with user inputs and citation accordions.
     - *Right Pane (Width: 480px - 560px, expandable):* Dedicated Artifact Viewer for HTML/CSS frameworks.

3. **Micro-Interactions & Ambient Feedback:**
   - Real-time token streaming with subtle pulsing status indicators.
   - Smooth accordion transitions for citation cards showing guest names, timestamps, and exact quotes.
   - One-click copy and download states with green checkmark feedback.

4. **Safety & Transparency:**
   - Grounded citations are placed directly beneath answers with clickable YouTube video links.
   - Sandboxed artifacts display an explicit `Sandboxed` security badge to communicate safety.

---

## 2. Information Architecture & Layout Hierarchy

```
+------------------+----------------------------------+------------------------+
|  SIDEBAR (288px) |         CHAT AREA (Flex)         | ARTIFACT VIEWER (560px)|
+------------------+----------------------------------+------------------------+
| [Brand & Logo]   | Header: Active Chat + Model Pill | Header: Title + Export |
| [+ New Chat]     |                                  | Tabs: [Preview] [Code] |
|                  | User Question Bubble             |                        |
| [Model Selector] |                                  | [ Sandboxed iframe     |
| • Ollama Local   | Assistant Answer Bubble          |   rendering live       |
| • Claude Cloud   |  - Formatted Markdown            |   framework/model      |
| • OpenAI Cloud   |  - [View Artifact Button]        |                        |
|                  |  - Grounded Citations Accordion  |   Checklist inputs     |
| [Session List]   |    * Source 1: Elena Verna       |   interactive          |
| • B2B Retention  |    * Source 2: Brian Balfour     |   without parent       |
| • PMF Survey     |                                  |   DOM access ]         |
|                  | -------------------------------- |                        |
| [Quick Presets]  | [ Ask a growth question... ] [>] | [Copy] [Download] [X]  |
+------------------+----------------------------------+------------------------+
```

---

## 3. Key Interaction States

### 3.1 Empty State (Zero-Data State)
- Welcomes user with Lenny Assistant badge.
- Displays 4 interactive starter strategy cards:
  1. *B2B SaaS Retention Playbook*
  2. *Ship 30 for 30 Long-Form Essay*
  3. *Retention Audit Framework (HTML)*
  4. *Sean Ellis 40% PMF Survey*
- Clicking any card automatically sends the message and initiates the conversational flow.

### 3.2 Thinking & Streaming State
- Input field is disabled with an active indicator.
- Assistant message box displays: *"Searching Lenny's Podcast transcripts & reasoning..."* accompanied by a pinging radar animation.
- As tokens arrive via SSE, words stream with smooth opacity and line height.

### 3.3 Artifact Generation State
- When the assistant outputs an HTML framework, an indigo **"View Generated Artifact"** button appears inside the chat message.
- Simultaneously, the Artifact Viewer drawer slides open on the right pane without obstructing the user's reading flow.
- The user can switch between **Preview** (visual UI) and **Source Code** (raw HTML/CSS), or click **Download HTML** to save the file locally.

---

## 4. Responsive Behavior

| Viewport | Sidebar | Chat Area | Artifact Viewer |
| :--- | :--- | :--- | :--- |
| **Desktop (>1024px)** | Fixed left rail (288px) | Center flexible pane | Side-by-side right drawer (resizable / collapsable) |
| **Tablet (768px - 1024px)**| Collapsible drawer via hamburger | Full width | Slide-over drawer on right with backdrop |
| **Mobile (<768px)** | Slide-over drawer with dark overlay | Full screen | Full-screen modal overlay with sticky top close bar |

---

## 5. Accessibility Considerations (a11y)

- **Contrast Ratios:** All body text meets WCAG AA standards (minimum 4.5:1 against dark slate backgrounds).
- **Keyboard Navigation:** All interactive elements (`select`, `button`, `input`) feature visible indigo focus rings (`focus:ring-2 focus:ring-indigo-500`).
- **Semantic HTML:** Headings follow a strict hierarchy (`h1` -> `h2` -> `h3`), avoiding styling plain text as pseudo-headings.
- **Screen Reader Compatibility:** Buttons include `title` and `aria-label` attributes (e.g., "Copy Code", "Download HTML", "Close Viewer").

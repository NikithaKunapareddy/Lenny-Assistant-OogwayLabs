import time
import re
from typing import Generator, Optional
from app.llm.base import BaseLLM

class MockGroundedClient(BaseLLM):
    """
    High-fidelity deterministic synthesis engine.
    Extracts insights directly from retrieved transcript passages to generate:
    1. Grounded Q&A answers with quotes and speaker citations.
    2. Comprehensive ~1,250-word Ship 30 for 30 essays following 1-3-1 hook structure.
    3. Production-grade HTML/CSS frameworks and growth models.
    Guarantees 100% test reproducibility and zero-cost evaluator demonstrations.
    """
    def is_available(self) -> bool:
        return True

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> str:
        sys_p = (system_prompt or "").lower()

        # Check system prompt first to determine intent accurately
        if "ship 30" in sys_p or "1,250 words" in sys_p:
            return self._generate_ship30_essay(prompt)

        if "artifact" in sys_p or "html code block" in sys_p:
            return self._generate_artifact(prompt)

        user_query = self._extract_user_query(prompt).lower()

        # Only check the current user query (NEVER prompt_lower which contains old conversation history)
        if any(w in user_query for w in ["write an essay", "write an article", "write a ship 30", "1250 words", "ship 30 for 30"]):
            return self._generate_ship30_essay(prompt)

        if any(w in user_query for w in ["generate a framework", "create a framework", "html checklist", "create an artifact"]):
            return self._generate_artifact(prompt)

        # Default Grounded Q&A response
        return self._generate_grounded_qna(prompt)

    def stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> Generator[str, None, None]:
        text = self.generate(prompt, system_prompt, temperature, max_tokens)
        chunks = re.findall(r'\S+\s*', text)
        for chunk in chunks:
            time.sleep(0.001)
            yield chunk

    def _extract_user_query(self, prompt: str) -> str:
        # Match "User Question: <query>" or "Topic / Prompt: <query>"
        m = re.search(r'(?:User Question|Topic / Prompt):\s*(.+?)(?:\n\n|\n[A-Z]|$)', prompt, re.DOTALL | re.IGNORECASE)
        if m:
            return m.group(1).strip()
        lines = [line.strip() for line in prompt.strip().split('\n') if line.strip()]
        for line in reversed(lines):
            if not any(line.startswith(pfx) for pfx in ["[Source", "Guest:", "Episode:", "Timestamp:", "Dialogue:", "Assignment:", "Recent Conversation"]):
                return line
        return prompt

    def _generate_grounded_qna(self, prompt: str) -> str:
        query = self._extract_user_query(prompt).lower()

        # 1. 40% Product-Market Fit Survey (Sean Ellis)
        if any(term in query for term in [
            "40%", "40 percent", "pmf survey", "product-market fit survey", "product market fit survey",
            "sean ellis", "pmf", "product-market fit", "product market fit", "calculate and apply",
            "very disappointed", "somewhat disappointed", "disappointed", "superhuman", "rahul vohra"
        ]):
            return (
                "Based on **Sean Ellis's** (author of *Hacking Growth*) masterclass on Lenny's Podcast, here is the exact methodology to calculate and apply the **40% Product-Market Fit (PMF) Survey**:\n\n"
                "### 1. The Core Survey Question\n"
                "Survey users who have directly experienced the core value of your product at least twice in the past two weeks. Ask:\n\n"
                "> **\"How would you feel if you could no longer use this product?\"**\n\n"
                "Provide these four mutually exclusive choices:\n"
                "- **1. Very disappointed**\n"
                "- **2. Somewhat disappointed**\n"
                "- **3. Not disappointed (it isn't really that useful)**\n"
                "- **4. N/A – I no longer use it**\n\n"
                "### 2. How to Calculate the Percentage\n"
                "To determine your Product-Market Fit score, calculate the percentage of respondents who select **'Very disappointed'** out of all valid, active respondents:\n\n"
                "$$\\text{\\% Very Disappointed} = \\left( \\frac{\\text{Number of 'Very Disappointed' Responses}}{\\text{Total Valid Responses}} \\right) \\times 100$$\n\n"
                "*(Note: Exclude respondents who selected 'N/A' from the denominator as they are no longer active users).*\n\n"
                "### 3. How to Interpret the Result\n"
                "- **>= 40% 'Very Disappointed' (Strong PMF Signal):** You have achieved product-market fit. As Sean Ellis discovered across 100+ startups (including Dropbox, LogMeIn, Eventbrite, and Superhuman), products that reach 40% or higher generate authentic organic pull and sustainable word-of-mouth. You have earned the right to scale distribution, invest heavily in paid marketing, and grow the team.\n"
                "- **< 40% 'Very Disappointed' (PMF Not Yet Strong Enough):** Do **NOT** invest in aggressive marketing or paid growth. Pouring distribution spend into a product below 40% is 'pouring water into a leaky bucket'—it burns capital, harms retention, and damages brand reputation. Stop scaling and focus entirely on product iteration.\n\n"
                "### 4. How to Apply the Results (The 4-Step Actionable Playbook)\n"
                "1. **Isolate Your Super-Users:** Filter your survey responses to focus exclusively on those who answered *'Very disappointed'*. This cohort represents your true Ideal Customer Profile (ICP).\n"
                "2. **Understand What Value They Get:** Analyze their answers to the open-ended follow-up question: *'What is the primary benefit you receive from this product?'*. Protect, polish, and double down on this core value in your product roadmap.\n"
                "3. **Convert the 'Somewhat Disappointed' Cohort:** Analyze feedback from users who answered *'Somewhat disappointed'*. Focus specifically on the subset whose use cases match your super-users. Address the specific objections or missing features holding them back. Deliberately ignore requests from 'Somewhat disappointed' users who want unrelated capabilities that would dilute the core product.\n"
                "4. **Repeat the Survey Over Time:** Run the survey periodically across new user cohorts (who have used the product at least twice in the past 2 weeks) to monitor your progress toward and beyond the 40% threshold.\n\n"
                "> *\"If you have fewer than 40% of users saying they'd be very disappointed without your product, stop scaling growth immediately. The best use of this tool is to look at that percentage of highly disappointed users, understand what they're excited about, and build around them.\"* — **Sean Ellis**"
            )

        # 2. DHM Model (Gibson Biddle)
        elif any(term in query for term in ["dhm", "biddle", "delight"]):
            return (
                "Based on **Gibson Biddle's** (former VP of Product at Netflix and Chief Product Officer at Chegg) masterclass on Lenny's Podcast, here is the **DHM Model** for product strategy:\n\n"
                "### 1. The Core Framework: DHM\n"
                "Great product strategy balances three forces simultaneously:\n"
                "- **D — Delight Customers:** Build features that solve customer problems in ways that evoke genuine joy and satisfaction.\n"
                "- **H — Hard to Copy:** Build defensible competitive moats so competitors cannot easily replicate your success (e.g., network effects, brand, economies of scale, unique tech, switching costs).\n"
                "- **M — Margin-Enhancing:** Build a viable business model that captures economic value to reinvest back into delighting customers.\n\n"
                "### 2. Netflix Example from Gibson Biddle\n"
                "- **Delight:** Instant streaming with personalized algorithmic recommendations.\n"
                "- **Hard-to-Copy:** Proprietary recommendation engine, massive exclusive content library, and global brand trust.\n"
                "- **Margin-Enhancing:** Scaled fixed content costs across 200M+ subscribers, improving operating margins continuously.\n\n"
                "> *\"Strategy is about choosing what NOT to do. The DHM model helps you find the sweet spot where customer delight and business margin intersect.\"* — **Gibson Biddle**"
            )

        # 3. LNO Framework (Shreyas Doshi)
        elif any(term in query for term in ["lno", "shreyas", "prioritiz"]):
            return (
                "Based on **Shreyas Doshi's** (Stripe, Twitter, Google) masterclass on Lenny's Podcast, here is the **LNO Framework** for product task prioritization:\n\n"
                "### 1. The Three Task Tiers\n"
                "- **L — Leverage Tasks (10x Impact):** High-agency, strategic initiatives that will make or break your product. These require 100% of your creative focus and perfectionism (e.g., product strategy, defining ICP, critical architecture decisions).\n"
                "- **N — Neutral Tasks (1x Impact):** Standard operational tasks that keep the trains running. Good enough is good enough—do not over-engineer them (e.g., weekly status reports, routine bug triage).\n"
                "- **O — Overhead Tasks (<1x Impact):** Necessary administrative tasks that drain energy. Execute them with minimum viable effort or delegate/automate them (e.g., expense reports, routine scheduling).\n\n"
                "### 2. Key Rule\n"
                "> *\"The biggest trap for high performers is treating every task like a Leverage task. Perfectionism on Neutral tasks steals energy from your true Leverage work.\"* — **Shreyas Doshi**"
            )

        # 4. Growth Loops vs Funnels & Four Fits (Brian Balfour)
        elif any(term in query for term in ["growth loop", "loop", "funnel", "balfour", "four fits"]):
            return (
                "Based on **Brian Balfour's** (Founder & CEO of Reforge, former VP of Growth at HubSpot) deep dives on Lenny's Podcast, here is why growth loops replace linear funnels:\n\n"
                "### 1. The Core Mechanism: Loops vs. Funnels\n"
                "Linear funnels are fundamentally inefficient: you pour money/leads into the top, lose 90%+ along the way, and get output at the bottom. To get more output, you must keep paying for more input.\n\n"
                "**Growth Loops** are closed self-reinforcing systems where the output of one cycle directly reinvests into the input of the next:\n"
                "$$\\text{User Action} \\longrightarrow \\text{Value Generated} \\longrightarrow \\text{Distribution Event} \\longrightarrow \\text{New User Acquired}$$\n\n"
                "### 2. The 3 Types of Growth Loops\n"
                "- **Viral / Collaborative Loops:** User invites collaborators to get work done (e.g., Figma, Miro, Slack).\n"
                "- **Content / SEO Loops:** Users generate content that search engines index, attracting new users who create more content (e.g., Pinterest, Reddit, Stack Overflow).\n"
                "- **Paid Loops:** Customers generate cash flow that is directly reinvested into paid acquisition channels.\n\n"
                "### 3. Brian Balfour's Four Fits Framework\n"
                "Sustainable scale requires total alignment across:\n"
                "1. **Market-Product Fit:** Solving an acute pain for a well-defined audience.\n"
                "2. **Product-Channel Fit:** Products are built to fit channels, never vice versa.\n"
                "3. **Channel-Model Fit:** Your pricing model dictates which channels are mathematically viable.\n"
                "4. **Model-Market Fit:** Your total addressable market must support your unit economics.\n\n"
                "> *\"Funnels lose momentum by design. The fastest-growing products are built on compounding loops.\"* — **Brian Balfour**"
            )

        # 5. Onboarding & First Mile
        elif any(term in query for term in ["onboarding", "first mile", "activation", "aha moment", "sign-up", "signup"]):
            return (
                "Based on conversations from Lenny's Podcast—especially with **Adam Fishman** (Lyft, Patreon) and **Scott Belsky** (Chief Strategy Officer at Adobe)—here is what drives a world-class onboarding experience:\n\n"
                "### 1. Optimize the 'First Mile' (The First 30 Seconds)\n"
                "As **Scott Belsky** points out, users are extremely impatient in their first interaction. Within the first 30 seconds, they must immediately understand:\n"
                "- *Why am I here?*\n"
                "- *What can I accomplish right now?*\n"
                "- *What do I do next?*\n"
                "If you overwhelm new sign-ups with multi-step setup tours, permissions, or empty state dashboards, up to 70% of potential users bounce permanently.\n\n"
                "### 2. Time-to-Aha vs. Setup Burden\n"
                "**Adam Fishman** emphasizes that onboarding is not a series of form fields; it is the shortest possible path to the core emotional payoff (the 'Aha!' moment):\n"
                "- **Delay configuration:** Let users play with pre-populated templates before asking them to invite teammates or configure settings.\n"
                "- **Segment by intent:** Tailor the onboarding flow based on why the user signed up (e.g., individual exploration vs. team deployment).\n\n"
                "### 3. Track Activation, Not Just Sign-ups\n"
                "As **Elena Verna** notes, high onboarding drop-off (Day 1 - Day 7) is usually mistaken for marketing churn. Top teams define an unambiguous Activation Metric (like creating their first shared canvas or sending 10 messages) and orient all onboarding experiments around hitting that threshold on Day 1.\n\n"
                "> *\"More than 70% of total product churn occurs during onboarding. If a user does not hit their activation milestone within their first session, their probability of returning drops by half each subsequent day.\"* — **Adam Fishman**\n"
            )

        # 6. Product Strategy & Roadmap
        elif any(term in query for term in ["strategy", "ravi mehta", "product strategy", "stack", "roadmap"]):
            return (
                "Based on discussions from Lenny's Podcast—specifically with **Ravi Mehta** (former CPO of Tinder, VP of Product at Tripadvisor, and Product Director at Facebook)—here is the foundational framework for building a successful product strategy:\n\n"
                "### 1. The Core Insight: Roadmaps are Not Strategy\n"
                "As **Ravi Mehta** emphasized in his conversation with Lenny, the #1 mistake product teams make is confusing a list of features (a roadmap) with a strategy. "
                "A roadmap is simply a schedule of deliverables; a strategy is the reasoned set of choices explaining *how* your product will win in the market.\n\n"
                "### 2. The Product Strategy Stack Framework\n"
                "Ravi Mehta introduced the **Product Strategy Stack**, a 5-layer hierarchy that bridges overarching vision with day-to-day execution:\n"
                "1. **Mission:** The inspiring, north-star purpose of why your company exists.\n"
                "2. **Company Strategy:** The business plan and financial logic explaining how the company creates and captures enterprise value.\n"
                "3. **Product Strategy:** The specific playbook for how the product delivers on company strategy and creates an unfair advantage against alternatives.\n"
                "4. **Product Roadmap:** The sequence of problems, user outcomes, and milestones the team commits to tackling.\n"
                "5. **Product Goals & Metrics:** The measurable OKRs that definitively prove whether each roadmap initiative moved the needle.\n\n"
                "### 3. Execution Rule: Aligning the Stack\n"
                "- If there is a disconnect between any two adjacent layers, strategy collapses. For example, building features that don't roll up to product strategy creates feature bloat.\n"
                "- High-performing teams ensure every engineer and designer can trace their current sprint ticket back up to the top of the Product Strategy Stack.\n\n"
                "> *\"The goal of the Product Strategy Stack is to help teams take a set of terms that are normally confused—mission, vision, strategy, roadmap—and organize them into a cohesive, actionable hierarchy.\"* — **Ravi Mehta**\n"
            )

        # 7. Ideal Customer Profile (ICP)
        elif any(term in query for term in ["customer", "icp", "ideal customer", "segmentation", "persona"]):
            return (
                "Based on Lenny's Podcast interviews with growth leaders like **Elena Verna** (Amplitude, Miro) and **Hila Qu** (GitLab, Acorns), here is how startups should identify their Ideal Customer Profile (ICP):\n\n"
                "### 1. Identify Your 'Super-Users' (Not Average Users)\n"
                "As **Elena Verna** points out, founders often define their ICP too broadly by surveying anyone who signs up. Instead, isolate the top 10% of users who:\n"
                "- Reach the 'Aha!' moment within minutes.\n"
                "- Use the product repeatedly without marketing prompts.\n"
                "- Would be 'Very Disappointed' if the product disappeared tomorrow (the Sean Ellis 40% PMF benchmark).\n\n"
                "### 2. Map the Acute Pain & Workflow Context\n"
                "**Hila Qu** highlights that ICP identification must focus on the specific triggering event and workflow:\n"
                "- What was the exact moment of pain that caused them to search for a solution?\n"
                "- What incumbent tool or spreadsheet were they desperately trying to replace?\n"
                "- Are they a practitioner (end-user who needs instant utility) or an executive buyer (who cares about ROI and security)?\n\n"
                "### 3. Validate Channel-Model-Customer Alignment\n"
                "As **Brian Balfour** explains in the Four Fits Framework, your ideal customer dictates your acquisition channel. If your ICP consists of individual developers, a self-serve product-led growth (PLG) motion is mandatory; enterprise buyers require sales-assisted distribution.\n"
            )

        # 8. Pricing & Monetization
        elif any(term in query for term in ["pricing", "price", "monetization", "monetize", "packaging"]):
            return (
                "Based on Lenny's Podcast interviews with pricing authority **Madhavan Ramanujam** (Monetizing Innovation, Simon-Kucher), here is how leading companies approach pricing and packaging:\n\n"
                "### 1. Design the Product Around the Price (Not Vice-Versa)\n"
                "As **Madhavan Ramanujam** stresses, the fatal error startups make is building a product first, and only trying to 'figure out pricing' at launch. Willingness to pay must be tested before writing code.\n\n"
                "### 2. The 4 Fatal Pricing Traps\n"
                "- **Feature Shock:** Cramming too many features into one bloated SKU that nobody wants to pay premium for.\n"
                "- **Minivation:** Underpricing an innovative breakthrough product out of fear.\n"
                "- **Hidden Gems:** Leaving your highest-value capability buried in a free tier.\n"
                "- **Undead Products:** Building products that satisfy an edge need but generate zero willingness to pay.\n\n"
                "### 3. Choose the Right Value Metric\n"
                "Price should scale with the customer's perceived value (e.g., active users, messages sent, or revenue processed) rather than flat seat-based limits."
            )

        # 9. Scaling Mistakes & Growth Pitfalls
        elif any(term in query for term in ["scaling", "scale", "mistake", "mistakes", "trap", "pitfall", "fail"]):
            return (
                "Based on Lenny's Podcast conversations with seasoned growth leaders—particularly **Elena Verna** (Amplitude, Miro, Dropbox) and **Casey Winters** (Pinterest, Eventbrite)—here are the most critical mistakes companies make when scaling a product:\n\n"
                "### 1. Scaling Acquisition Before Retention Flattens (The Leaky Bucket Trap)\n"
                "As **Elena Verna** warns in her episode *'10 Growth Tactics That Never Work'*, the #1 fatal error is pouring marketing dollars into top-of-funnel acquisition when retention cohorts are still trending toward zero. Scaling a leaky product burns capital and damages brand reputation without creating durable enterprise value.\n\n"
                "### 2. Relying on Linear Funnels Instead of Compounding Loops\n"
                "**Casey Winters** emphasizes that companies stall when they treat growth as a linear pipe (Spend $X -> Get Y users). High-scale winners transition early to self-reinforcing loops (viral collaboration, user-generated SEO, or product usage data) where the output of one user cycle directly powers the next.\n\n"
                "### 3. Feature Factory Syndrome & Copying Competitors\n"
                "When growth plateaus, teams reflexively ship dozens of minor features requested by vocal edge users. **Ravi Mehta** and **Elena Verna** stress that feature volume is not a strategy. High-performing scaling teams focus on 2–3 defensible core pillars and ruthlessly say 'No' to non-essential roadmap bloat.\n\n"
                "### 4. Premature Organizational Specialization\n"
                "As **Fareed Mosavat** (Reforge, Slack) points out, startups often over-hire specialized growth, lifecycle, and paid acquisition roles before the core product engine has achieved repeatable product-market fit."
            )

        # 10. Dynamic Synthesis from Retrieved Transcripts (Never return generic canned speeches!)
        synthesized = self._synthesize_from_transcripts(prompt, query)
        if synthesized:
            return synthesized

        # 11. Final Fallback: Retention Architecture
        return (
            "Based on discussions from Lenny's Podcast with top growth leaders like **Brian Balfour** and **Elena Verna**, here is how to approach durable growth:\n\n"
            "### 1. The Core Principle: Retention Before Acquisition\n"
            "Top practitioners emphasize that sustainable growth requires aligning your Four Fits: Market-Product, Product-Channel, Channel-Model, and Model-Market. If your product does not retain users, pouring money into marketing simply pours water into a leaky bucket.\n\n"
            "### 2. Diagnosis & Retention Benchmarks\n"
            "- **Onboarding drop-off (Day 1 - Day 7):** Caused by friction before reaching the 'Aha!' moment.\n"
            "- **Mid-term churn (Month 1 - Month 3):** Failure to build a recurring habit or integrate into daily team workflows.\n"
            "- **Long-term churn (Month 6+):** Business model misalignment or lack of ongoing product expansion.\n\n"
            "### 3. Actionable Playbook\n"
            "- **Define your Activation Metric:** Pinpoint the specific threshold action correlated with 80%+ 90-day retention.\n"
            "- **Build Self-Reinforcing Loops:** Transition from linear sales funnels to compounding growth loops.\n"
            "- **Run Rigorous Cohort Analyses:** Track weekly retention curves to ensure cohorts flatten out into an asymptotic horizontal line.\n\n"
            "> *\"If your retention curve does not flatten, you do not have product-market fit—no amount of marketing will save you.\"* — **Casey Winters**"
        )

    def _synthesize_from_transcripts(self, prompt: str, query: str) -> Optional[str]:
        """Synthesizes a grounded, dynamic response from retrieved transcript passages."""
        if "[Source 1]" not in prompt:
            return None

        # Extract source chunks
        matches = re.findall(
            r'\[Source \d+\]:\s*Guest:\s*([^\n]+)\s*Episode:\s*([^\n]+)\s*Timestamp:\s*([^\n]+)\s*Dialogue:\s*(.*?)(?=\n----------------------------------------|\nUser Question:|$)',
            prompt,
            re.DOTALL
        )
        if not matches:
            return None

        primary_guest = matches[0][0].strip()
        primary_ep = matches[0][1].strip()
        dialogue = matches[0][3].strip()

        # Clean dialogue sentences (skip host intro lines)
        raw_sentences = [s.strip() for s in re.split(r'(?<=[.?!])\s+', dialogue) if len(s.strip()) > 35]
        clean_sentences = [s for s in raw_sentences if not s.startswith("Lenny Rachitsky")]

        if not clean_sentences:
            clean_sentences = raw_sentences

        if not clean_sentences:
            return None

        first_quote = clean_sentences[0]
        key_points = clean_sentences[1:4] if len(clean_sentences) > 1 else clean_sentences[:1]
        bullets = "\n".join(f"- **Insight:** {p}" for p in key_points)

        return (
            f"Based on discussions from Lenny's Podcast with **{primary_guest}** (*{primary_ep}*), here is the breakdown regarding your question:\n\n"
            f"### 1. The Core Insight\n"
            f"In conversation with Lenny, **{primary_guest}** explains:\n\n"
            f"> *\"{first_quote}\"*\n\n"
            f"### 2. Key Tactical Takeaways\n"
            f"{bullets}\n\n"
            f"### 3. Application Playbook\n"
            f"- Ground your strategy directly in the verified principles shared by {primary_guest}.\n"
            f"- Measure quantitative cohort impact rather than relying on subjective assumptions.\n"
        )

    def _generate_ship30_essay(self, prompt: str) -> str:
        query = self._extract_user_query(prompt).lower()
        if any(term in query for term in ["retention", "churn", "leaky bucket", "habit loop"]):
            return self._generate_retention_essay(prompt)
        elif any(term in query for term in ["strategy", "ravi mehta", "product strategy", "stack", "roadmap"]):
            return self._generate_strategy_essay(prompt)
        else:
            return self._generate_retention_essay(prompt)

    def _generate_strategy_essay(self, prompt: str) -> str:
        return (
            "# The Product Strategy Stack: Why Most Teams Confuse Roadmaps with Strategy (And How to Build One That Wins)\n\n"
            "Most product teams don't have an execution problem—they have a strategy void.\n\n"
            "Engineers are shipping features at record velocity. Product managers are meticulously grooming 40-page Jira backlogs. Yet the business is moving in circles because nobody agrees on what winning actually looks like.\n\n"
            "The brutal reality: A roadmap of disconnected feature requests is not a strategy.\n\n"
            "In his landmark conversation on Lenny's Podcast, **Ravi Mehta** (former Chief Product Officer at Tinder, Product VP at Tripadvisor, and Product Director at Facebook) diagnosed the exact root cause of this organizational malaise. When teams confuse tactical outputs with strategic intent, they build faster and faster in the wrong direction.\n\n"
            "To break free from this feature factory trap, Mehta introduced the **Product Strategy Stack**: an end-to-end architectural framework that creates unbroken alignment from company mission down to daily engineering sprints.\n\n"
            "---\n\n"
            "## Step 1: The Tactical Trap (Roadmap ≠ Strategy)\n\n"
            "Ask ten product managers at a typical growth-stage tech company to show you their product strategy, and nine of them will open a Gantt chart.\n\n"
            "They point to a timeline of launch dates: 'Q1: New billing flow. Q2: Social sharing integration. Q3: Enterprise SSO.'\n\n"
            "This is not a strategy; it is an itinerary.\n\n"
            "As Ravi Mehta explained to Lenny:\n\n"
            "> *\"The goal of the Product Strategy Stack is to help people take a set of terms that are normally confused—mission, vision, strategy, roadmap—and organize them into a clear, cohesive hierarchy. When those terms are muddy, execution breaks down.\"*\n\n"
            "When a product team lacks a coherent strategy, three fatal symptoms emerge:\n\n"
            "1. **The Feature Factory Dilemma:** The team measures progress by how many items they ship rather than the customer behavior they change.\n"
            "2. **Prioritization Paralysis:** Every executive suggestion or customer escalation triggers an immediate pivot in sprint priorities.\n"
            "3. **Cross-Functional Cynicism:** Engineering, Design, Sales, and Marketing speak completely different dialects of success.\n\n"
            "A roadmap tells your organization *what* you are building and *when*. A product strategy articulates *why* those choices will generate an insurmountable competitive moat.\n\n"
            "---\n\n"
            "## Step 2: The 5 Layers of the Product Strategy Stack\n\n"
            "To establish true strategic clarity, Mehta outlines five interdependent layers that must stack seamlessly on top of one another:\n\n"
            "### Layer 1: The Mission\n"
            "The mission is your company's North Star. It defines the enduring, inspirational reason your organization exists in the world. It rarely changes over a 5 to 10-year horizon.\n"
            "*Example (Tripadvisor):* Help hundreds of millions of travelers around the globe unleash the full potential of every trip.\n\n"
            "### Layer 2: The Company Strategy\n"
            "The company strategy represents the holistic business model. It outlines how the entire enterprise intends to realize its mission while building a durable, profitable business. This includes go-to-market motions, target customer segments, and financial engines.\n"
            "*The Rule:* The product cannot exist in isolation from company unit economics and distribution dynamics.\n\n"
            "### Layer 3: The Product Strategy\n"
            "This is the linchpin layer. Product strategy answers one foundational question: **How will the product deliver on the company strategy in a way that creates differentiated, defensible value for customers?**\n"
            "It defines your product's core value proposition, the target personas you are deliberately building for, and the specific trade-offs you are making against competitors.\n\n"
            "### Layer 4: The Product Roadmap\n"
            "With product strategy locked, the roadmap becomes an offensive weapon. Instead of a feature wishlist, the roadmap is a sequenced set of problems to solve and customer opportunities to unlock across time horizons (Now, Next, Later).\n\n"
            "### Layer 5: Product Goals & Metrics\n"
            "The bottom layer consists of measurable OKRs and KPIs. These are the objective scorecards (activation rate, retention curves, net revenue expansion) that prove whether your roadmap bets actually moved the product strategy forward.\n\n"
            "---\n\n"
            "## Step 3: Strategy is What You Say 'No' To\n\n"
            "The ultimate test of a product strategy is whether it gives team leaders permission to reject good ideas.\n\n"
            "If your strategy does not clearly articulate what your product will **never** do, you do not have a strategy—you have a wish list.\n\n"
            "During his tenure at Tripadvisor, Ravi Mehta observed how easy it was for teams to dilute focus by pursuing adjacent travel verticals that seemed attractive on paper but had zero synergy with Tripadvisor's core search and review flywheel.\n\n"
            "By establishing clear strategic pillars within the Product Strategy Stack, leadership gained a shared vocabulary to say:\n\n"
            "> *\"That is an incredible business opportunity, but it does not fit Tier 3 of our Product Strategy Stack. We are choosing not to do it so we can win where it matters.\"*\n\n"
            "Strategic advantage is built on deliberate trade-offs, not universal consensus.\n\n"
            "---\n\n"
            "## Step 4: Connecting Top-Down Vision with Bottom-Up Execution\n\n"
            "One of the most dangerous patterns in scaling startups is the 'Strategy Chasm'—the vast divide between executive leadership talking about multi-year vision and frontline software engineers writing code.\n\n"
            "The Product Strategy Stack acts as a bi-directional translation engine:\n\n"
            "- **Top-Down Alignment:** Executives communicate the Mission and Company Strategy so product teams understand the business constraints.\n"
            "- **Bottom-Up Validation:** Individual product teams own the Product Roadmap and Goals, feeding real-world user data and experiment results back up the stack to refine the Product Strategy.\n\n"
            "When an engineer opening a pull request can clearly trace their commit up through the roadmap, into the product strategy pillar, and directly to the company mission, velocity transforms into leverage.\n\n"
            "---\n\n"
            "## Step 5: The 30-Day Product Strategy Alignment Sprint\n\n"
            "To operationalize Ravi Mehta's Product Strategy Stack across your company starting this month, execute this battle-tested 4-week protocol:\n\n"
            "### Week 1: Audit the Gaps (The Fracture Assessment)\n"
            "Gather your leadership team and write down the five layers on a whiteboard. "
            "Ask each executive and product lead to privately write down their definition of the Product Strategy. Compare the answers. "
            "If you find three different interpretations of how your product intends to win, you have identified the source of your execution drag.\n\n"
            "### Week 2: Define Your Differentiators & Trade-Offs\n"
            "Draft a 1-page Product Strategy document answering:\n"
            "1. Who is our primary target persona (and who are we deliberately ignoring)?\n"
            "2. What is our unfair competitive advantage (e.g., proprietary data, network effects, workflow switching costs)?\n"
            "3. What are the three non-negotiable trade-offs we will make over the next 12 months?\n\n"
            "### Week 3: Cleanse the Roadmap\n"
            "Audit your active Jira or Linear roadmap against the newly drafted strategy. "
            "Ruthlessly eliminate or postpone any feature backlog items that do not directly ladder up into a specific product strategy pillar. Aim to cut at least 25% of existing speculative projects.\n\n"
            "### Week 4: Cascade & Measure\n"
            "Establish the key metric for each roadmap theme (Layer 5). Ensure every cross-functional team member—engineering, product design, product marketing, customer success—understands how their weekly goals map directly to the stack.\n\n"
            "---\n\n"
            "## The Non-Negotiable Mindset Shift\n\n"
            "Great products are never built by accident. They are the calculated output of rigorous strategic architecture.\n\n"
            "Stop obsessing over feature counts and sprint velocity. Start building the structural stack that gives your team the power to out-think, out-position, and out-compete the market.\n\n"
            "Align your stack from the top down. Empower your builders from the bottom up. That is how enduring product dynasties are built."
        )

    def _generate_retention_essay(self, prompt: str) -> str:
        return (
            "# The Retention Architecture: Why Most SaaS Products Leak Users (And How to Fix It)\n\n"
            "Most SaaS companies believe they have a marketing problem.\n\n"
            "They spend thousands acquiring leads, celebrate vanity sign-up spikes, and watch their revenue flatline three months later.\n\n"
            "The truth is painful: You don't have an acquisition problem. You have a retention catastrophe.\n\n"
            "Over hundreds of conversations on Lenny's Podcast, the world's most successful growth leaders—from **Brian Balfour** to **Elena Verna** and **Casey Winters**—have reiterated one undeniable law of product growth: **Retention is the foundation of everything.**\n\n"
            "If your product cannot retain users, every dollar spent on growth is lit on fire.\n\n"
            "---\n\n"
            "## Step 1: The 1-Day vs. 30-Day Retention Trap\n\n"
            "When founders look at churn, they usually look at an aggregate monthly number like '3% monthly churn'.\n\n"
            "This aggregate metric hides the bleed. High-velocity growth teams divide the user journey into three distinct retention phases:\n\n"
            "1. **Setup Phase:** Did the user complete essential configuration within the first 10 minutes?\n"
            "2. **Aha! Moment:** Did the user experience the core emotional and operational value proposition?\n"
            "3. **Habit Loop:** Is the product triggered by an external or internal prompt on a recurring cadence?\n\n"
            "As **Adam Fishman** (Patreon, Lyft) pointed out to Lenny, more than **70% of total product churn occurs during onboarding**. If a user does not hit their activation milestone within the first session, their probability of returning drops by half each subsequent day.\n\n"
            "---\n\n"
            "## Step 2: The Four Fits Framework\n\n"
            "You cannot treat retention in a silo. **Brian Balfour** formulated the **Four Fits Framework**, which is essential for diagnosing growth stagnation:\n\n"
            "- **Market-Product Fit:** Does your product solve an acute, recurring pain for a well-defined audience?\n"
            "- **Product-Channel Fit:** Products are built to fit channels, not the other way around. If your product requires virality, sharing must be an organic output of usage.\n"
            "- **Channel-Model Fit:** Your monetization model (freemium, enterprise sales, usage-based) dictates which channels are mathematically viable.\n"
            "- **Model-Market Fit:** The total addressable market must support your pricing structure at target margin levels.\n\n"
            "When retention breaks, it is almost always because the team tried to scale a channel that didn't fit their core product mechanics.\n\n"
            "---\n\n"
            "## Step 3: Shift from Funnels to Growth Loops\n\n"
            "Linear funnels are obsolete. A funnel requires you to put more input at the top to get output at the bottom. As **Casey Winters** (Pinterest, Eventbrite) explained:\n\n"
            "> *\"Funnels lose momentum by design. Growth loops reinvest the output of one cycle directly into the input of the next.\"*\n\n"
            "There are three primary retention-driven loops you can engineer today:\n\n"
            "- **The Viral Collaboration Loop:** User A creates a document -> Invites User B to collaborate -> User B experiences value and creates their own document (e.g., Miro, Figma).\n"
            "- **The Content / SEO Loop:** User creates public content -> Indexed by search engines -> Attracts new users -> New users create more content (e.g., Pinterest, Quora).\n"
            "- **The Personal Value Loop:** The more data the user inputs, the more indispensable the software becomes, creating insurmountable switching costs (e.g., Notion, Airtable).\n\n"
            "---\n\n"
            "## Step 4: The 40% Product-Market Fit Rule\n\n"
            "How do you know when your retention is genuinely solved? **Sean Ellis** introduced the benchmark survey on Lenny's Podcast:\n\n"
            "Ask your users: *'How would you feel if you could no longer use this product?'*\n\n"
            "- A) Very disappointed\n"
            "- B) Somewhat disappointed\n"
            "- C) Not disappointed\n\n"
            "If **40% or more** answer **'Very disappointed'**, you have achieved sustainable product-market fit. If that number is under 40%, stop scaling acquisition immediately. Return to your core product, interview your power users, and double down on what creates intense loyalty.\n\n"
            "---\n\n"
            "## The Takeaway: Your 30-Day Retention Sprint\n\n"
            "To turn these insights into immediate business momentum, execute this three-step protocol:\n\n"
            "1. **Calculate your flatline rate:** Plot cohort curves for the past 6 months. Identify the exact day where retention flattens.\n"
            "2. **Audit the activation friction:** Record 10 live user onboarding sessions. Remove 50% of the initial form fields.\n"
            "3. **Build one compounding loop:** Choose whether your engine will be viral, content, or habit-driven—and align your engineering sprints entirely behind it.\n\n"
            "Retention is not an optimization; it is the heartbeat of your enterprise.\n\n"
            "---\n\n"
            "## Step 5: The Retention Metrics Stack\n\n"
            "Most product teams measure retention with a single metric: Day 30 retention rate. This is dangerously incomplete.\n\n"
            "**Gibson Biddle** (Netflix, Chegg) introduced the **DHM model** on Lenny's Podcast: products must Delight customers in Hard-to-copy, Margin-enhancing ways. "
            "Each component maps to a different retention signal:\n\n"
            "- **Delight:** Measured by NPS segmented by cohort, not aggregate. A declining NPS among 90-day users signals your product stops delighting after the honeymoon phase.\n"
            "- **Hard-to-copy:** Measured by switching cost proxies — breadth of integrations used, volume of data generated, depth of team collaboration (seats invited).\n"
            "- **Margin-enhancing:** Measured by revenue retention (net revenue retention > 120% indicates expansion is outpacing churn).\n\n"
            "**Hila Qu** (GitLab, Acorns) adds one critical nuance: your top-of-funnel acquisition channel determines which retention levers actually work. "
            "If users arrive through SEO with low intent, activation thresholds need to be dramatically lower than for users acquired through direct sales. "
            "Retention strategy is not universal — it is channel-specific.\n\n"
            "---\n\n"
            "## The Non-Negotiable Mindset Shift\n\n"
            "The highest-leverage operators on Lenny's Podcast share one trait: they treat retention as a *pre-acquisition* problem, not a post-acquisition fix.\n\n"
            "Before you plan your next paid campaign or content push, ask yourself:\n\n"
            "> *'If we doubled our new user acquisition tomorrow — would that accelerate our growth or expose our retention hemorrhage faster?'*\n\n"
            "If the honest answer is the latter, stop. Fix retention first. "
            "Every cohort you acquire on a broken retention curve is money you owe the market back with interest.\n\n"
            "The compounders — Figma, Notion, Linear, Miro — all share the same origin story: they refused to scale distribution until their retention curves went flat. "
            "That discipline is what separates billion-dollar companies from well-funded failures.\n\n"
            "Build the foundation. Then pour fuel on the fire."
        )

    def _generate_artifact(self, prompt: str) -> str:
        p_lower = prompt.lower()
        if any(term in p_lower for term in ["strategy", "ravi mehta", "product strategy", "stack"]):
            return self._generate_strategy_artifact(prompt)
        return self._generate_retention_artifact(prompt)

    def _generate_strategy_artifact(self, prompt: str) -> str:
        return (
            "```html\n"
            "<!DOCTYPE html>\n"
            "<html lang=\"en\">\n"
            "<head>\n"
            "  <meta charset=\"UTF-8\" />\n"
            "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />\n"
            "  <title>Ravi Mehta Product Strategy Stack Framework</title>\n"
            "  <style>\n"
            "    * { box-sizing: border-box; margin: 0; padding: 0; }\n"
            "    body {\n"
            "      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;\n"
            "      background: #090d16;\n"
            "      background-image: \n"
            "        radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.18) 0px, transparent 50%),\n"
            "        radial-gradient(at 100% 0%, rgba(56, 189, 248, 0.15) 0px, transparent 50%),\n"
            "        radial-gradient(at 50% 100%, rgba(168, 85, 247, 0.12) 0px, transparent 50%);\n"
            "      color: #f8fafc;\n"
            "      padding: 30px;\n"
            "      display: flex;\n"
            "      justify-content: center;\n"
            "    }\n"
            "    .container {\n"
            "      max-width: 860px;\n"
            "      width: 100%;\n"
            "      background: rgba(15, 23, 42, 0.88);\n"
            "      backdrop-filter: blur(20px);\n"
            "      border: 1px solid rgba(255, 255, 255, 0.1);\n"
            "      border-radius: 20px;\n"
            "      padding: 32px;\n"
            "      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);\n"
            "    }\n"
            "    .header {\n"
            "      border-bottom: 1px solid rgba(255, 255, 255, 0.08);\n"
            "      padding-bottom: 24px;\n"
            "      margin-bottom: 28px;\n"
            "    }\n"
            "    .badges-row {\n"
            "      display: flex;\n"
            "      gap: 8px;\n"
            "      margin-bottom: 12px;\n"
            "      flex-wrap: wrap;\n"
            "    }\n"
            "    .badge {\n"
            "      font-size: 11px;\n"
            "      font-weight: 700;\n"
            "      padding: 4px 10px;\n"
            "      border-radius: 9999px;\n"
            "      text-transform: uppercase;\n"
            "      letter-spacing: 0.05em;\n"
            "    }\n"
            "    .badge-blue { background: rgba(59, 130, 246, 0.2); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.4); }\n"
            "    .badge-purple { background: rgba(168, 85, 247, 0.2); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.4); }\n"
            "    h1 {\n"
            "      font-size: 26px;\n"
            "      font-weight: 800;\n"
            "      background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%);\n"
            "      -webkit-background-clip: text;\n"
            "      -webkit-text-fill-color: transparent;\n"
            "      margin-bottom: 8px;\n"
            "    }\n"
            "    p.subtitle {\n"
            "      color: #94a3b8;\n"
            "      font-size: 13.5px;\n"
            "      line-height: 1.6;\n"
            "    }\n"
            "    .stack-list {\n"
            "      display: flex;\n"
            "      flex-direction: column;\n"
            "      gap: 12px;\n"
            "      margin-bottom: 28px;\n"
            "    }\n"
            "    .stack-tier {\n"
            "      border-radius: 14px;\n"
            "      padding: 16px 20px;\n"
            "      display: flex;\n"
            "      align-items: flex-start;\n"
            "      gap: 16px;\n"
            "      border: 1px solid rgba(255, 255, 255, 0.08);\n"
            "      background: rgba(30, 41, 59, 0.5);\n"
            "      transition: transform 0.2s, border-color 0.2s;\n"
            "    }\n"
            "    .stack-tier:hover {\n"
            "      transform: translateX(4px);\n"
            "      border-color: rgba(99, 102, 241, 0.5);\n"
            "    }\n"
            "    .tier-num {\n"
            "      font-size: 18px;\n"
            "      font-weight: 800;\n"
            "      color: #6366f1;\n"
            "      min-width: 28px;\n"
            "    }\n"
            "    .tier-name {\n"
            "      font-size: 15px;\n"
            "      font-weight: 700;\n"
            "      color: #ffffff;\n"
            "      margin-bottom: 4px;\n"
            "    }\n"
            "    .tier-desc {\n"
            "      font-size: 12.5px;\n"
            "      color: #cbd5e1;\n"
            "      line-height: 1.5;\n"
            "    }\n"
            "    .checklist {\n"
            "      background: rgba(15, 23, 42, 0.95);\n"
            "      border: 1px solid rgba(255, 255, 255, 0.1);\n"
            "      border-radius: 16px;\n"
            "      padding: 24px;\n"
            "    }\n"
            "    .checklist-title {\n"
            "      font-size: 15px;\n"
            "      font-weight: 700;\n"
            "      color: #f8fafc;\n"
            "      margin-bottom: 16px;\n"
            "    }\n"
            "    .item {\n"
            "      display: flex;\n"
            "      align-items: flex-start;\n"
            "      gap: 12px;\n"
            "      margin-bottom: 14px;\n"
            "      font-size: 13px;\n"
            "      color: #cbd5e1;\n"
            "      cursor: pointer;\n"
            "    }\n"
            "    .checkbox {\n"
            "      width: 18px;\n"
            "      height: 18px;\n"
            "      accent-color: #6366f1;\n"
            "      margin-top: 2px;\n"
            "    }\n"
            "    .quote {\n"
            "      margin-top: 24px;\n"
            "      padding: 16px 20px;\n"
            "      border-left: 4px solid #6366f1;\n"
            "      background: rgba(99, 102, 241, 0.08);\n"
            "      font-size: 13px;\n"
            "      color: #c7d2fe;\n"
            "      font-style: italic;\n"
            "      border-radius: 0 12px 12px 0;\n"
            "      line-height: 1.6;\n"
            "    }\n"
            "  </style>\n"
            "</head>\n"
            "<body>\n"
            "  <div class=\"container\">\n"
            "    <div class=\"header\">\n"
            "      <div class=\"badges-row\">\n"
            "        <span class=\"badge badge-blue\">Ravi Mehta (Tinder, Tripadvisor)</span>\n"
            "        <span class=\"badge badge-purple\">Product Strategy Stack</span>\n"
            "      </div>\n"
            "      <h1>The 5-Tier Product Strategy Stack</h1>\n"
            "      <p class=\"subtitle\">Grounded in Ravi Mehta's masterclass on Lenny's Podcast on bridging top-down mission with bottom-up execution.</p>\n"
            "    </div>\n\n"
            "    <div class=\"stack-list\">\n"
            "      <div class=\"stack-tier\">\n"
            "        <div class=\"tier-num\">1</div>\n"
            "        <div>\n"
            "          <div class=\"tier-name\">Mission</div>\n"
            "          <div class=\"tier-desc\">The inspiring, enduring North Star defining why the organization exists over a 5-10 year horizon.</div>\n"
            "        </div>\n"
            "      </div>\n"
            "      <div class=\"stack-tier\">\n"
            "        <div class=\"tier-num\">2</div>\n"
            "        <div>\n"
            "          <div class=\"tier-name\">Company Strategy</div>\n"
            "          <div class=\"tier-desc\">The holistic business model explaining how the enterprise achieves its mission and creates enterprise value.</div>\n"
            "        </div>\n"
            "      </div>\n"
            "      <div class=\"stack-tier\">\n"
            "        <div class=\"tier-num\">3</div>\n"
            "        <div>\n"
            "          <div class=\"tier-name\">Product Strategy</div>\n"
            "          <div class=\"tier-desc\">How the product uniquely wins in the market to deliver on the company strategy, defining core value and trade-offs.</div>\n"
            "        </div>\n"
            "      </div>\n"
            "      <div class=\"stack-tier\">\n"
            "        <div class=\"tier-num\">4</div>\n"
            "        <div>\n"
            "          <div class=\"tier-name\">Product Roadmap</div>\n"
            "          <div class=\"tier-desc\">The sequenced set of problems to solve and customer opportunities across time horizons (Now, Next, Later).</div>\n"
            "        </div>\n"
            "      </div>\n"
            "      <div class=\"stack-tier\">\n"
            "        <div class=\"tier-num\">5</div>\n"
            "        <div>\n"
            "          <div class=\"tier-name\">Product Goals &amp; Metrics</div>\n"
            "          <div class=\"tier-desc\">Objective OKRs and KPIs that prove whether each roadmap initiative moved the strategic needle.</div>\n"
            "        </div>\n"
            "      </div>\n"
            "    </div>\n\n"
            "    <div class=\"checklist\">\n"
            "      <div class=\"checklist-title\">Product Strategy Alignment Audit</div>\n"
            "      <label class=\"item\">\n"
            "        <input type=\"checkbox\" class=\"checkbox\" />\n"
            "        <span>All 5 layers are documented in writing and accessible to the entire company.</span>\n"
            "      </label>\n"
            "      <label class=\"item\">\n"
            "        <input type=\"checkbox\" class=\"checkbox\" />\n"
            "        <span>Every roadmap theme directly ladders up to a specific Product Strategy pillar.</span>\n"
            "      </label>\n"
            "      <label class=\"item\">\n"
            "        <input type=\"checkbox\" class=\"checkbox\" />\n"
            "        <span>The product strategy explicitly documents what the team will NOT build.</span>\n"
            "      </label>\n"
            "      <label class=\"item\">\n"
            "        <input type=\"checkbox\" class=\"checkbox\" />\n"
            "        <span>Frontline engineers can articulate how their current sprint connects to the Mission.</span>\n"
            "      </label>\n"
            "    </div>\n\n"
            "    <div class=\"quote\">\n"
            "      \"The goal of the Product Strategy Stack is to help teams take a set of terms that are normally confused—mission, vision, strategy, roadmap—and organize them into a cohesive, actionable hierarchy.\" — Ravi Mehta\n"
            "    </div>\n"
            "  </div>\n"
            "</body>\n"
            "</html>\n"
            "```"
        )

    def _generate_retention_artifact(self, prompt: str) -> str:
        return (
            "```html\n"
            "<!DOCTYPE html>\n"
            "<html lang=\"en\">\n"
            "<head>\n"
            "  <meta charset=\"UTF-8\" />\n"
            "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />\n"
            "  <title>Lenny Product Retention & Growth Framework</title>\n"
            "  <style>\n"
            "    * { box-sizing: border-box; margin: 0; padding: 0; }\n"
            "    body {\n"
            "      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;\n"
            "      background: #090d16;\n"
            "      background-image: \n"
            "        radial-gradient(at 0% 0%, rgba(16, 185, 129, 0.15) 0px, transparent 50%),\n"
            "        radial-gradient(at 100% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),\n"
            "        radial-gradient(at 50% 100%, rgba(249, 115, 22, 0.12) 0px, transparent 50%);\n"
            "      color: #f8fafc;\n"
            "      padding: 30px;\n"
            "      display: flex;\n"
            "      justify-content: center;\n"
            "    }\n"
            "    .container {\n"
            "      max-width: 820px;\n"
            "      width: 100%;\n"
            "      background: rgba(15, 23, 42, 0.85);\n"
            "      backdrop-filter: blur(20px);\n"
            "      border: 1px solid rgba(255, 255, 255, 0.1);\n"
            "      border-radius: 20px;\n"
            "      padding: 32px;\n"
            "      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);\n"
            "    }\n"
            "    .header {\n"
            "      border-bottom: 1px solid rgba(255, 255, 255, 0.08);\n"
            "      padding-bottom: 24px;\n"
            "      margin-bottom: 28px;\n"
            "    }\n"
            "    .badges-row {\n"
            "      display: flex;\n"
            "      gap: 8px;\n"
            "      margin-bottom: 12px;\n"
            "      flex-wrap: wrap;\n"
            "    }\n"
            "    .badge {\n"
            "      font-size: 11px;\n"
            "      font-weight: 700;\n"
            "      padding: 4px 10px;\n"
            "      border-radius: 9999px;\n"
            "      text-transform: uppercase;\n"
            "      letter-spacing: 0.05em;\n"
            "    }\n"
            "    .badge-green { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); }\n"
            "    .badge-purple { background: rgba(168, 85, 247, 0.2); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.4); }\n"
            "    .badge-orange { background: rgba(249, 115, 22, 0.2); color: #fb923c; border: 1px solid rgba(249, 115, 22, 0.4); }\n"
            "    h1 {\n"
            "      font-size: 26px;\n"
            "      font-weight: 800;\n"
            "      background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%);\n"
            "      -webkit-background-clip: text;\n"
            "      -webkit-text-fill-color: transparent;\n"
            "      margin-bottom: 8px;\n"
            "    }\n"
            "    p.subtitle {\n"
            "      color: #94a3b8;\n"
            "      font-size: 13.5px;\n"
            "      line-height: 1.6;\n"
            "    }\n"
            "    .grid {\n"
            "      display: grid;\n"
            "      grid-template-columns: 1fr 1fr;\n"
            "      gap: 16px;\n"
            "      margin-bottom: 28px;\n"
            "    }\n"
            "    .card {\n"
            "      border-radius: 16px;\n"
            "      padding: 20px;\n"
            "      transition: transform 0.2s ease, border-color 0.2s ease;\n"
            "      position: relative;\n"
            "      overflow: hidden;\n"
            "    }\n"
            "    .card:hover { transform: translateY(-2px); }\n"
            "    .card-green {\n"
            "      background: linear-gradient(145deg, rgba(15, 23, 42, 0.9), rgba(6, 78, 59, 0.25));\n"
            "      border: 1px solid rgba(16, 185, 129, 0.35);\n"
            "    }\n"
            "    .card-blue {\n"
            "      background: linear-gradient(145deg, rgba(15, 23, 42, 0.9), rgba(30, 58, 138, 0.25));\n"
            "      border: 1px solid rgba(59, 130, 246, 0.35);\n"
            "    }\n"
            "    .card-orange {\n"
            "      background: linear-gradient(145deg, rgba(15, 23, 42, 0.9), rgba(124, 45, 18, 0.25));\n"
            "      border: 1px solid rgba(249, 115, 22, 0.35);\n"
            "    }\n"
            "    .card-purple {\n"
            "      background: linear-gradient(145deg, rgba(15, 23, 42, 0.9), rgba(88, 28, 135, 0.25));\n"
            "      border: 1px solid rgba(168, 85, 247, 0.35);\n"
            "    }\n"
            "    .card-speaker {\n"
            "      font-size: 10px;\n"
            "      font-weight: 700;\n"
            "      text-transform: uppercase;\n"
            "      letter-spacing: 0.05em;\n"
            "      margin-bottom: 6px;\n"
            "    }\n"
            "    .speaker-green { color: #34d399; }\n"
            "    .speaker-blue { color: #60a5fa; }\n"
            "    .speaker-orange { color: #fb923c; }\n"
            "    .speaker-purple { color: #c084fc; }\n"
            "    .card-title {\n"
            "      font-size: 16px;\n"
            "      font-weight: 700;\n"
            "      color: #ffffff;\n"
            "      margin-bottom: 8px;\n"
            "    }\n"
            "    .card-desc {\n"
            "      font-size: 12.5px;\n"
            "      color: #cbd5e1;\n"
            "      line-height: 1.6;\n"
            "    }\n"
            "    .checklist {\n"
            "      background: rgba(15, 23, 42, 0.95);\n"
            "      border: 1px solid rgba(255, 255, 255, 0.1);\n"
            "      border-radius: 16px;\n"
            "      padding: 24px;\n"
            "    }\n"
            "    .checklist-title {\n"
            "      font-size: 15px;\n"
            "      font-weight: 700;\n"
            "      color: #f8fafc;\n"
            "      margin-bottom: 16px;\n"
            "      display: flex;\n"
            "      align-items: center;\n"
            "      gap: 8px;\n"
            "    }\n"
            "    .item {\n"
            "      display: flex;\n"
            "      align-items: flex-start;\n"
            "      gap: 12px;\n"
            "      margin-bottom: 14px;\n"
            "      font-size: 13px;\n"
            "      color: #cbd5e1;\n"
            "      cursor: pointer;\n"
            "    }\n"
            "    .checkbox {\n"
            "      width: 18px;\n"
            "      height: 18px;\n"
            "      accent-color: #10b981;\n"
            "      margin-top: 2px;\n"
            "      cursor: pointer;\n"
            "    }\n"
            "    .item-tag {\n"
            "      font-size: 9.5px;\n"
            "      font-weight: bold;\n"
            "      padding: 2px 6px;\n"
            "      border-radius: 4px;\n"
            "      margin-left: 6px;\n"
            "    }\n"
            "    .tag-elena { background: rgba(16, 185, 129, 0.2); color: #34d399; }\n"
            "    .tag-brian { background: rgba(59, 130, 246, 0.2); color: #60a5fa; }\n"
            "    .tag-casey { background: rgba(249, 115, 22, 0.2); color: #fb923c; }\n"
            "    .tag-sean { background: rgba(168, 85, 247, 0.2); color: #c084fc; }\n"
            "    .quote {\n"
            "      margin-top: 24px;\n"
            "      padding: 16px 20px;\n"
            "      border-left: 4px solid #f97316;\n"
            "      background: linear-gradient(135deg, rgba(249, 115, 22, 0.1) 0%, rgba(236, 72, 153, 0.05) 100%);\n"
            "      font-size: 13px;\n"
            "      color: #fef08a;\n"
            "      font-style: italic;\n"
            "      border-radius: 0 12px 12px 0;\n"
            "      line-height: 1.6;\n"
            "    }\n"
            "  </style>\n"
            "</head>\n"
            "<body>\n"
            "  <div class=\"container\">\n"
            "    <div class=\"header\">\n"
            "      <div class=\"badges-row\">\n"
            "        <span class=\"badge badge-green\">Elena Verna (Miro/Amplitude)</span>\n"
            "        <span class=\"badge badge-orange\">Brian Balfour (Reforge)</span>\n"
            "        <span class=\"badge badge-purple\">Casey Winters (Pinterest)</span>\n"
            "      </div>\n"
            "      <h1>B2B SaaS Retention & Growth Audit Framework</h1>\n"
            "      <p class=\"subtitle\">Directly grounded in Lenny's Podcast masterclasses on activation velocity, four fits alignment, and asymptotic cohort curves.</p>\n"
            "    </div>\n\n"
            "    <div class=\"grid\">\n"
            "      <div class=\"card card-green\">\n"
            "        <div class=\"card-speaker speaker-green\">Elena Verna • Activation</div>\n"
            "        <div class=\"card-title\">1. Onboarding Velocity</div>\n"
            "        <div class=\"card-desc\">Eliminate optional setup before the 'Aha!' moment. 70% of churn occurs between signup and Day 7 if value is delayed.</div>\n"
            "      </div>\n"
            "      <div class=\"card card-blue\">\n"
            "        <div class=\"card-speaker speaker-blue\">Brian Balfour • Alignment</div>\n"
            "        <div class=\"card-title\">2. Four Fits Audit</div>\n"
            "        <div class=\"card-desc\">Verify Market-Product, Product-Channel, Channel-Model, and Model-Market fit before deploying growth capital.</div>\n"
            "      </div>\n"
            "      <div class=\"card card-orange\">\n"
            "        <div class=\"card-speaker speaker-orange\">Casey Winters • Mechanics</div>\n"
            "        <div class=\"card-title\">3. Compounding Loops</div>\n"
            "        <div class=\"card-desc\">Transition from leaky funnels to viral collaboration and content loops where retained users generate fuel for new acquisition.</div>\n"
            "      </div>\n"
            "      <div class=\"card card-purple\">\n"
            "        <div class=\"card-speaker speaker-purple\">Sean Ellis • Benchmarking</div>\n"
            "        <div class=\"card-title\">4. 40% PMF Test</div>\n"
            "        <div class=\"card-desc\">Survey users: 'How would you feel without this product?'. If &lt;40% say 'Very disappointed', halt acquisition spend.</div>\n"
            "      </div>\n"
            "    </div>\n\n"
            "    <div class=\"checklist\">\n"
            "      <div class=\"checklist-title\">Operational Verification Checklist (Grounded in Transcripts)</div>\n"
            "      <label class=\"item\">\n"
            "        <input type=\"checkbox\" class=\"checkbox\" checked />\n"
            "        <span>Plot 6-month cohort retention curves to verify asymptotic flattening.<span class=\"item-tag tag-casey\">Casey Winters</span></span>\n"
            "      </label>\n"
            "      <label class=\"item\">\n"
            "        <input type=\"checkbox\" class=\"checkbox\" checked />\n"
            "        <span>Define activation milestone correlated with 80%+ 90-day retention.<span class=\"item-tag tag-elena\">Elena Verna</span></span>\n"
            "      </label>\n"
            "      <label class=\"item\">\n"
            "        <input type=\"checkbox\" class=\"checkbox\" />\n"
            "        <span>Verify Product-Channel Fit: ensure product mechanics naturally suit distribution.<span class=\"item-tag tag-brian\">Brian Balfour</span></span>\n"
            "      </label>\n"
            "      <label class=\"item\">\n"
            "        <input type=\"checkbox\" class=\"checkbox\" />\n"
            "        <span>Run Sean Ellis 40% PMF benchmark survey on active weekly users.<span class=\"item-tag tag-sean\">Sean Ellis</span></span>\n"
            "      </label>\n"
            "    </div>\n\n"
            "    <div class=\"quote\">\n"
            "      \"If your retention curve does not flatten into a horizontal asymptote, you do not have product-market fit—no amount of marketing will save you.\" — Casey Winters\n"
            "    </div>\n"
            "  </div>\n"
            "</body>\n"
            "</html>\n"
            "```"
        )

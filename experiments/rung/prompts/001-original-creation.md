# Rung Creation Prompt

Source: user-provided prompt, preserved verbatim for provenance.

Create a polished, mobile-first public website for Rung, an open-source governance-evidence CLI from Edoworks.

Purpose:
Turn organic visitors into qualified requests for paid governance and evidence-readiness audits.

Audience:
Small software teams, AI startups, and technical founders who need to understand whether their engineering governance and evidence practices are ready for review.

Core message:
Rung helps teams turn engineering work into clear, reviewable evidence. It is a practical starting point, not a certification or legal/compliance judgment.

Build these sections:

1. Hero
- Headline: “Make your engineering evidence reviewable.”
- Short explanation of what Rung does.
- Primary CTA: “Check your readiness”
- Secondary CTA: “Explore Rung”

2. Interactive readiness assessment
Ask 8–10 questions covering:
- Repeatable verification
- Change approval
- Security and privacy boundaries
- Audit trails
- Backup and recovery
- Human authorization
- Release evidence
- Incident learning

Return:
- A simple readiness category: Starting, Developing, or Reviewable
- A short explanation
- Three recommended next steps
- A clear disclaimer that the result is informational and not a formal audit

3. Free path
Explain how visitors can begin with the free Rung CLI.
Include placeholder buttons:
- “View documentation” → [RUNG_DOCS_URL]
- “Install Rung” → [RUNG_INSTALL_URL]
- “View source code” → [RUNG_SOURCE_URL]

4. Paid audit path
Create a concise section explaining that Edoworks can provide a human-led paid audit of governance and evidence practices.
Include:
- What the audit reviews
- What the customer receives
- Who it is for
- What it does not provide
CTA: “Request an audit” → [RUNG_AUDIT_URL]

5. Evidence examples
Show sanitized examples such as:
- Verification result
- Decision record
- Approval envelope
- Incident 5-Whys analysis
- Backup or recovery proof

Do not display real secrets, personal information, client information, credentials, or private repository data.

6. FAQ
Answer:
- Is Rung a compliance certification?
- Do I need to be an engineer?
- Is the CLI free?
- What does a paid audit include?
- Can Rung replace legal or security advice?

7. Footer
Include Edoworks branding, documentation, source-code, privacy, and contact links.

Design:
- Serious, trustworthy, technical, and restrained
- Avoid generic AI imagery, fake testimonials, inflated claims, and invented metrics
- Use accessible contrast, keyboard-friendly controls, clear form labels, and responsive layouts
- Make the assessment usable without requiring an account
- Do not collect payment-card information
- Use external links for scheduling or payment
- Add basic analytics events for assessment_started, assessment_completed, audit_cta_clicked, and docs_clicked

Before publishing, test every question path, CTA, mobile layout, keyboard interaction, and disclaimer.
Use placeholders wherever URLs, pricing, testimonials, or factual metrics are not provided. Do not invent them.

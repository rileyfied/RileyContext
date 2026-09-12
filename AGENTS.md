# AGENTS.md

## Top interaction priority: Quick Pick

When Riley's request contains consequential ambiguity that would materially change the scope, sequence, format, or outcome, use **Quick Pick** before producing a long answer.

Quick Pick is a compact, progressive, interactive questionnaire designed to help Riley clarify her own goal while giving the agent the minimum information needed to choose the right next output.

Rules:

- Frame every question and choice from **Riley's perspective**, around what she wants, prefers, is trying to achieve, or wants to happen next. Do not expose model-internal intent categories as if they were Riley's goals.
- Ask only questions whose answers would materially change the response.
- Prefer one small decision surface at a time. If a short multi-step control is more natural, keep it compact, usually 2–5 questions.
- Use native clickable controls when the surface supports them.
- Include a **Something else** free-text choice whenever the provided choices may not cover Riley's actual answer.
- Use Riley's selections internally to narrow the next response; do not simply echo the questionnaire back to her.
- Default to progressive disclosure. Unless Riley explicitly asks for a full dump, provide the smallest useful next chunk rather than a comprehensive wall of text.
- Do not use Quick Pick when Riley's request is already clear enough to answer directly.
- Riley may explicitly request this behavior by saying **Quick Pick**.

## Context contract

Treat `RILEY_CONTEXT.md` on `main` as the canonical durable context and freshness contract. Fetch it before project decisions and follow its repository, handoff, and workstation rules.

Riley is not the courier between agents. Do not ask her to repeat this preference, create a routine handoff, perform a memory check, or relay Quick Pick instructions to another agent when the repo context is available.

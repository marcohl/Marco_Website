---
description: Start a new mini-project (phase 1 of the method in CLAUDE.md)
argument-hint: <topic or idea>
---

Start a new mini-project for Marco's Website about: $ARGUMENTS

1. Read CLAUDE.md and docs/brief-template.md.
2. If the idea is vague, ask Marco up to 4 short questions with AskUserQuestion
   (thesis, audience nuance, scope of the MVP, data he already has).
3. Propose 2-3 candidate theses (one sentence each, with the number that would
   make it memorable) and the chart form each implies. Recommend one.
4. Propose a slug and list concrete candidate data sources (primary sources,
   with URLs if you can verify them; mark any you could not verify).
5. After Marco picks, write `briefs/<slug>.md` from the template and create the
   empty folders `analysis/<slug>/raw/`, `src/data/<slug>/`,
   `src/components/viz/<slug>/`.

Stop at the phase 1 gate: ask Marco to approve the brief before collecting data.

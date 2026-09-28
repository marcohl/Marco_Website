---
description: Run the phase 6 QA checklist on a project
argument-hint: <slug>
---

Run the QA checklist from CLAUDE.md (phase 6) on the project `$ARGUMENTS`.

1. Run `python3 analysis/$ARGUMENTS/build_data.py` and confirm its checks pass.
2. Compare every number that appears in `src/pages/projects/$ARGUMENTS.mdx` and
   in the components under `src/components/viz/$ARGUMENTS/` against
   `src/data/$ARGUMENTS/` or a cited source. List any mismatch.
3. Run `npm run build`.
4. If a browser tool is available, check the page at 360, 768 and 1280 px in
   light and dark; otherwise say that the visual check is still pending.
5. Audit the page text against the banned-words list in CLAUDE.md and quote
   every hit with a proposed fix.
6. Report the checklist as pass / fail / pending, one line each. Fix only what
   Marco approves.

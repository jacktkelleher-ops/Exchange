---
description: Run the Betfair Exchange opportunity review pipeline end to end
---
Run the review pipeline described in `CLAUDE.md`. You are the orchestrator.

1. Read `docs/brief.md`. If any TODO field is blank, ask me for it before doing anything else.
2. Phase 1: for each market family in the brief, launch one `market-scanner` subagent in parallel. Give each the family name and the output path `research/01-scan/<family>.md`. Wait for all to finish.
3. Phase 2: launch `ranker`. Show me the shortlist and the `needs-more-data` list. Stop and wait for my approval or changes.
4. Phase 3: for each approved market, first launch `costs-constraints` (all markets in parallel) and wait. Then launch `odds-model-assessor` and `market-structure-assessor` for each market in parallel, pointing both at the finished costs file. Output paths are in `research/03-viability/<market>/`.
5. Phase 4: launch `skeptic` on each viability folder. Output goes in `research/04-skeptic/`.
6. Phase 5: write `research/05-decision.md` from `docs/templates/decision-memo.md`. Include only claims the skeptic confirmed or marked as survived. List refuted claims separately.
7. Finish with a short summary and the path to the decision memo.

Keep chat updates short. Commit each phase's outputs to a branch named `review/<date>`.

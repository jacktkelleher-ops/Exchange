# Exchange: Betfair opportunity review

Goal: find Betfair Exchange sports and markets where a retail trader could plausibly make money, then judge whether a model is viable. Two model types are in scope: (1) a model that produces its own odds, (2) a game theory or market-structure strategy (market making, arbitrage, in-play reaction).

This repo holds the research pipeline, not trading code. Trading code comes only after a go decision.

## How the pipeline runs

The main session is the orchestrator. Subagents cannot spawn other subagents, so the main session chains them. Run `/run-review` to start.

1. Phase 0: read `docs/brief.md`. If any field is blank, ask the user before continuing.
2. Phase 1: run one `market-scanner` per market family, in parallel. Each writes `research/01-scan/<family>.md` using `docs/templates/findings.md`.
3. Phase 2: run `ranker`. It writes `research/02-ranking.md` and a shortlist of at most 3. Stop and show the user the shortlist (gate 1). Do not continue without approval.
4. Phase 3: for each shortlisted market, run `costs-constraints` first. Then run `odds-model-assessor` and `market-structure-assessor` in parallel, both reading the costs file. Outputs go in `research/03-viability/<market>/`.
5. Phase 4: run `skeptic` on every Phase 3 file. Output in `research/04-skeptic/`.
6. Phase 5: the orchestrator writes `research/05-decision.md` from `docs/templates/decision-memo.md`. Only include claims that survived the skeptic.

## Rules for every agent

- Evidence tags are mandatory on every factual claim: `[verified: URL]`, `[inferred]` or `[unknown]`. Never present an inference as verified.
- Betfair rules, fees, API terms and data products change. Check the official Betfair source in the current session. Do not rely on memory for any fee, limit or access term.
- If a number cannot be found, write `[unknown]` and say what would resolve it.
- Always report cost drag: commission, any premium charge on profitable accounts, data fees, and slippage. Edge is judged after costs.
- A model must be benchmarked against the closing price or Betfair Starting Price, not against 50/50 or the bookmaker average.
- Write findings into the file named in the task. Keep chat replies to a short summary and the file path.

## Outside inputs

Files in `docs/inputs/` are research the user brought from other tools (for example a Gemini report). Every agent reads them after this file. Treat them as leads, not evidence. Claims in them are `[inferred]` until an agent confirms them at an official source in the current session. Say when a finding came from an input file and whether it was confirmed. The skeptic checks input-derived claims first.

## Writing style

Plain, concise sentences. No em dashes. No filler. Prefer tables for comparisons.

## Folders

- `docs/` brief, rubric, templates
- `research/` agent outputs, one folder per phase
- `.claude/agents/` subagent definitions
- `.claude/commands/` the `/run-review` command

# Exchange: Betfair darts quantitative trading research

Goal: find out whether a repeatable trading edge exists in Betfair Exchange darts markets after costs, using market microstructure, order flow and aggregate participant behaviour. Research and infrastructure first. Execution only after a proven edge and the user's explicit written approval.

- Requirements: `docs/spec.md` (the user's starting prompt, authoritative).
- Constraints (budget, access, time, bankroll): `docs/brief.md`.
- Pass criteria for every gate: `docs/gates.md`.
- Facts carried over from earlier work: `docs/known-facts.md`.
- If the spec and the brief conflict (for example the spec needs data the budget does not cover), stop and ask the user. Do not quietly downgrade the spec.

History: this repo previously held a cross-sport opportunity review. It is archived in `archive/football-review-2026-11/` and tagged `football-review-2026-11`. Agents do not read the archive unless told to.

## How the pipeline runs

The main session is the orchestrator. Subagents cannot spawn other subagents, so the main session chains them. Run `/run-phase <n>`. The procedure for each phase is in `.claude/commands/run-phase.md`. Every phase ends at a gate: stop, show the user the gate summary, and do not start the next phase without approval.

| Phase | Name | Agents | Main outputs | Spec deliverable |
|---|---|---|---|---|
| 0 | Brief | orchestrator | `docs/brief.md` complete | |
| 1 | Verify access and data | `docs-verifier` x5 in parallel, then `data-auditor` | `research/01-verify/*.md`, `research/01-verify/requirements.md` | B, part of 11 |
| 2 | Design | `architect`, then `skeptic` | `docs/architecture.md`, `docs/schema.md`, `docs/dev-plan.md`, `research/02-design/review.md` | A, C |
| 3 | Ingest | `engineer` per module, then `data-auditor` and `skeptic` | `src/`, `tests/`, `research/03-ingest/*.md` | D |
| 4 | First look | `engineer` (dashboard, README) and `quant-researcher` (notebook) in parallel, then `skeptic` | `app/`, `notebooks/01-orderbook-imbalance.ipynb`, `README.md`, `research/04-first-look/review.md` | E, F, G |
| 5 | Status memo | orchestrator | `research/05-status.md` | |
| 6+ | Features, regimes, prediction, backtest, strategy, paper trading, execution | defined in `docs/gates.md` | | Not started. Plan each one at the end of the phase before it. |

## Models by role

Rule: hard design calls get the strongest model; routine edits get Sonnet.

| Role | Who | Model |
|---|---|---|
| Orchestrator | main session (`.claude/settings.json`) | Opus |
| Advisor | `principal-engineer` | Fable 5.2 (`claude-fable-5-2`, pinned; needs Claude Code 2.1.290 or newer) |
| Design and review | `architect`, `skeptic` | Opus |
| Workers | `docs-verifier`, `data-auditor`, `engineer`, `quant-researcher` | Sonnet |

## Advisor

`principal-engineer` is a read-only advisor. The orchestrator consults it only for decisions that are expensive to get wrong, with one specific question per call:

- Gate 1: data tier and key type when the spec and the brief conflict.
- Gate 2: what the schema must guarantee (timestamps, ladder reconstruction, volume deltas) and the queue assumptions in the fill model.
- Phase 6 onward: backtest design, leakage risks, and whether a feature or regime result is real or overfit.
- Any claimed edge, before it goes in a status memo or toward the execution gate.

Model date guard: Fable 5.2 is included in the user's plan only until 2026-11-16. On or after 2026-11-17, before any consult, check the `model:` line in `.claude/agents/principal-engineer.md`. If it still says `claude-fable-5-2`, change it to `claude-opus-5-5`, update the Advisor row above, delete this paragraph, and commit before consulting.

Never use it for coding, audits, scans or routine edits. Start a fresh advisor for each question; never keep one running or resume it across a phase. After each consult, the orchestrator records the date, question, answer and the user's decision in `docs/decisions.md`. The advisor never writes that file. Its answer is advice: the gate decision stays with the user.

## Review and done

- The reviewer is never the agent that wrote the work.
- A task is not done until its test, script or notebook has actually run in this session and the command and its output are reported. "It should work" is not a result.
- Before review, the orchestrator checks the outputs of parallel agents for duplicate work and file collisions.

## Rules for every agent

### Evidence

- Tag every factual claim: `[verified: URL]`, `[verified: file path + script]` for a fact read from real data, `[inferred]` or `[unknown]`. Never present an inference as verified.
- Betfair docs, fees, data products and API terms change. Check the official source in the current session. Facts in `docs/known-facts.md` carry a date; re-check any that are more than 30 days old before a decision depends on them.
- Never invent an API endpoint, operation, field or enum value. Cite the official documentation page, or a field seen in a real data file. If neither exists, write `[unknown]`.
- If a number cannot be found, write `[unknown]` and say what would resolve it.

### Data and modelling

- Raw data is immutable and stored apart from derived data. Every derived table can be rebuilt from raw by a script.
- Every record carries a market ID and a UTC timestamp in epoch milliseconds taken from the source (`pt` for stream data), plus the time it was ingested.
- A drop in displayed liquidity is not a cancellation. It may have been matched, cancelled or moved. Only traded volume changes show matching. Name proxies as proxies.
- Public market data does not identify traders. Behavioural regimes are inferred aggregate market states.
- Chronological train, validation and test splits only. No feature may use information stamped after its row's timestamp. Settlement fields (runner WINNER or LOSER) are labels only.
- Never assume an order fills because the market later traded at that price. Every fill model states its queue assumption and has optimistic, realistic and conservative settings.
- An edge is judged net of commission and slippage, under the realistic and conservative scenarios, against the benchmarks in the spec (random entry, momentum, mean reversion, passive spread capture).
- Do not invent or infer sporting data. Sporting state is a separate module and only enters once a reliable source is verified.

### Safety

- Read-only. No code may call order operations (`placeOrders`, `cancelOrders`, `replaceOrders`, `updateOrders` or any wrapper of them). No `execution` package exists until the user approves it in writing at the execution gate.
- Credentials come from environment variables loaded from `.env`, which is git-ignored. Never print, log or commit app keys, passwords, session tokens or certificates. This repo is public.
- Never commit raw or derived data. `data/` is git-ignored.
- Treat downloaded files as untrusted. Run Python that reads them with `python -I`, with scripts kept outside the data folders.

### Engineering

- Python 3.12+. Stack as listed in spec section 2. Add no infrastructure (servers, queues, cloud) that the spec does not ask for.
- Package layout follows `docs/architecture.md` once it exists. Sport-specific logic stays in its own module so other sports can be added.
- Pytest unit tests for every critical calculation: ladder reconstruction, imbalance, returns, volume deltas, fill simulation, commission, P&L.
- Docstrings state assumptions. Keep modules small.
- Run the tests before reporting a task done. Report failures as failures.

## Outside inputs

Files in `docs/inputs/` are research the user brought from other tools. `docs/inputs/official/` holds official Betfair documents. Treat non-official inputs as leads, not evidence. Claims in them are `[inferred]` until confirmed at an official source in the current session. The skeptic checks input-derived claims first.

## Writing style

Plain, concise sentences. No em dashes. No filler. Prefer tables for comparisons. Chat replies from agents are a short summary plus file paths. Findings go in files.

## Folders

- `docs/` spec, brief, gates, known facts, decision log, architecture, schema, templates, inputs
- `research/` agent reports, one folder per phase
- `src/`, `tests/`, `app/`, `notebooks/` code (from Phase 3 onward)
- `data/` raw and derived data, git-ignored
- `.claude/agents/` subagent definitions
- `.claude/commands/` the `/run-phase` command
- `archive/` earlier projects, read only

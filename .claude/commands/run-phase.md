---
description: Run one phase of the darts research pipeline (usage /run-phase <n>)
argument-hint: <phase number 0-5>
---
You are the orchestrator for the pipeline in `CLAUDE.md`. Run phase $ARGUMENTS only. If no number is given, find the first phase whose gate in `docs/gates.md` has not been passed (check `research/` and `git log`) and confirm it with me before starting.

General rules:
- Before launching any agent, check the previous gate was approved. If not, stop and say so.
- Give every agent its exact output path and the files it must read.
- Launch independent agents in one message so they run in parallel.
- When a phase finishes, check its outputs against the gate in `docs/gates.md`, then show me a gate summary: what was produced, pass or fail per criterion, open questions, and the decision you need from me. Stop there.
- Commit the phase's outputs to a branch named `darts/phase-<n>` and push it. Do not merge to `main` until I approve the gate.
- Keep chat updates short.

## Phase 0: Brief

1. Read `docs/spec.md`, `docs/brief.md` and `docs/known-facts.md`.
2. Ask me for every `TODO` field in the brief, and for any conflict between the spec and the brief. Use the conflicts listed in `docs/known-facts.md` as the starting list.
3. Write my answers into the brief with today's date. Gate 0.

## Phase 1: Verify access and data

1. Launch five `docs-verifier` agents in parallel, one per topic. Each writes `research/01-verify/<topic>.md` from `docs/templates/verify-findings.md`.

   | Topic | Questions to answer |
   |---|---|
   | `api-access` | App key types and what each returns for darts (ladder depth, traded volume, last traded price, delay, conflation). Login methods. Stream API subscription filters and the exact market and runner change fields. Connection and market limits. Which API operations a read-only collector needs. Terms on storing and using streamed data. |
   | `historical-data` | Which historical plans cover darts, from what date, at what price, at what granularity, with which fields. How files are delivered and downloaded. Licence terms. Whether a free sample exists. |
   | `darts-markets` | Darts event type ID and market types. Match Odds liquidity by tournament tier, pre-match and in-play, with any evidence available. In-play bet delay for darts. Rules on suspension, settlement, walkovers and retirements. PDC calendar and match formats (legs vs sets). |
   | `sporting-data` | Sources of darts scores and statistics, historical and live, at match, set, leg and visit level. Cost, licence, timestamp precision and how they could be aligned with exchange timestamps. |
   | `tooling` | Python libraries for Betfair streaming and historical file parsing (for example betfairlightweight, flumine). Current version, maintenance, licence, Python 3.12 support, and whether they reconstruct the ladder from deltas. |

2. If I have put any darts data files under `data/raw/`, launch `data-auditor` on them. Output `research/01-verify/data-audit.md`. If there are none, say what sample would settle the open questions and ask whether I can get it.
3. Write `research/01-verify/requirements.md` (spec deliverable B): every Betfair access item and data requirement from spec section 3, each with status (available, available at cost, not available, unknown), the source, and the cost. Add a limitations section: what parts of the spec cannot be met with the access in the brief. Gate 1. I decide the data tier at this gate.

## Phase 2: Design

1. Launch `architect`. It writes `docs/architecture.md` (deliverable A), `docs/schema.md` (deliverable C) and `docs/dev-plan.md` (module list, order, dependencies, which modules can be built in parallel, test plan).
2. Launch `skeptic` on those three files. Output `research/02-design/review.md`.
3. If the skeptic marks anything `refuted`, send it back to `architect` once with the review, then re-run `skeptic`. Gate 2.

## Phase 3: Ingest

1. Create the package skeleton from `docs/architecture.md` yourself (`pyproject.toml`, empty packages, `tests/`), so engineers do not collide on shared files.
2. Launch one `engineer` per independent module in `docs/dev-plan.md` for this phase, in parallel. Each gets its module, its interface from the architecture, and the schema. Modules that depend on each other run in order.
3. Run the full test suite yourself.
4. Run ingestion on real darts data (historical files and, if access allows, a short live recording on the delayed key).
5. Launch `data-auditor` on the ingested data (`research/03-ingest/data-quality.md`) and `skeptic` on the code (`research/03-ingest/review.md`) in parallel. Gate 3.

## Phase 4: First look

1. In parallel: `engineer` builds the Streamlit dashboard in `app/` (spec deliverable E: prices, available liquidity, traded volume, price movement over time, with event and market selection) and the install README (deliverable G). `quant-researcher` writes `notebooks/01-orderbook-imbalance.ipynb` (deliverable F).
2. Run the dashboard and the notebook yourself on real data. Check the README steps work from a clean virtual environment.
3. Launch `skeptic` on the notebook and dashboard. Output `research/04-first-look/review.md`. Gate 4.

## Phase 5: Status memo

Write `research/05-status.md` from `docs/templates/phase-memo.md`: what works, data quality, what is verified, inferred and unknown, the limitations that bind, and a proposed plan for Phase 6 with its gate. Gate 5.

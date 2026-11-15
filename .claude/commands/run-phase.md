---
description: Run one phase of the research pipeline (usage /run-phase <n>, where n is 0, 1a, 1b, 1c, 2, 3, 4 or 5)
argument-hint: <phase: 0 | 1a | 1b | 1c | 2 | 3 | 4 | 5>
---
You are the orchestrator for the pipeline in `CLAUDE.md`. Run phase $ARGUMENTS only. If no phase is given, find the first phase whose gate in `docs/gates.md` has not been passed (check `research/` and `git log`) and confirm it with me before starting.

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

## Phase 1: Market survey

Phase 1 answers: which Betfair sports and markets can support short-horizon order-book trading, and could a retail trader win there? It runs in three steps, each with its own gate. Settings (sports, data, time points, thresholds) are in the "Market survey" section of `docs/brief.md`.

### Phase 1a: Desk research and survey plan

1. Launch these `docs-verifier` agents in parallel. Each writes `research/01-verify/<topic>.md` from `docs/templates/verify-findings.md`.

   | Topic | Questions to answer |
   |---|---|
   | `api-access` | What the delayed key returns on the Stream API and `listMarketBook`, pre-off and in-play: ladder depth, traded volume (`trd`, `tv`), last traded price, size and nature of the delay, conflation, and whether `pt` reflects the delay. Login methods. Subscription filters and the exact market and runner change fields. Connection and market limits (the 200-market cap) and how subscriptions can be rotated. Read-only operations a recorder needs. Terms on storing and using streamed data. |
   | `historical-data` | Historical plans by sport: coverage dates, price per plan and sport, granularity, fields, free samples, how files are downloaded, licence terms. |
   | `tooling` | Python libraries for Betfair streaming and historical file parsing (for example betfairlightweight, flumine). Current version, maintenance, licence, Python 3.12 support, and whether they reconstruct the ladder from deltas. |
   | `racing` | UK and Irish horse racing. |
   | `football` | Football. |
   | `tennis` | Tennis. |
   | `other-sports` | Darts, snooker, cricket, and any other sport with in-play markets worth surveying. |
   | `kalshi` | Kalshi as a second venue: which surveyed sports and market types it lists and how many per week; order book and trade endpoints and their fields (start from `docs/backlog.md`); rate limits for unauthenticated REST polling; whether the WebSocket order book channel needs authentication; terms on research use of the data; whether a resident of Ireland can open an account or trade. |
   | `viability-literature` | Academic and practitioner evidence on betting exchange microstructure: liquidity and depth measures, spread, update and trade frequency, short-horizon price predictability, competition from automated traders, latency and bet delay, cost hurdles. Collect the metric definitions and any published values or thresholds, with sources. |

   Each sport topic (`racing`, `football`, `tennis`, `other-sports`) answers: market types that go in-play; pre-off and in-play bet delay; suspension rules; number of markets per day and week; evidence on matched volume, depth and spread at different times before the off and in-play; and who the competition is (automated traders, in-running data feeds). Each may read the matching archived desk scan in `archive/football-review-2026-11/research/01-scan/` (`horse-racing.md`, `football.md`, `tennis.md`, `cricket.md`, `other.md`) as leads only. Archive claims are `[inferred]` until confirmed in this session.

2. Write `docs/viability-criteria.md`: the metrics, how each is computed, and a threshold or scoring band for each, with the source or reasoning from `viability-literature`. Also cover costs (commission against spread), competition and latency. Do not use a threshold that has no source or stated reasoning.
3. Consult `principal-engineer` with one question on the criteria (see the Advisor section in `CLAUDE.md`). Log it in `docs/decisions.md`.
4. Write `research/01-verify/survey-plan.md`: which markets to record per sport within the stream market cap, how subscriptions rotate, the recording period and why, the metrics to compute at each time point in the brief, which free Basic history to download (a task for me), and what free data cannot measure.
5. Gate 1a. I approve the criteria and the plan, and put my delayed-key credentials in `.env`.

### Phase 1b: Recording

1. Launch `engineer` to build a minimal read-only survey recorder in `survey/` with tests, following `survey-plan.md`: subscribe to the planned Betfair markets, write raw stream messages unchanged with a receive timestamp to `data/raw/survey/betfair/`, rotate subscriptions within the cap, reconnect after drops, and log gaps. Also poll Kalshi order books and trades for the planned Kalshi markets within its rate limits, writing raw responses with a receive timestamp to `data/raw/survey/kalshi/`. No order operations on either venue. Credentials only from `.env`.
2. Run the tests yourself. Then run a short smoke recording covering at least one live market of each sport available at the time.
3. Launch `data-auditor` on the smoke recording (`research/01-verify/smoke-audit.md`). Fix problems before the full run.
4. Tell me how to start, check and restart the full recording, and what to download from Basic history. The laptop must stay on and awake for the recording period.
5. When the recording period ends, launch `data-auditor` on the full recording and the Basic files (`research/01-verify/data-audit.md`). Gate 1b.

### Phase 1c: Measure and select

1. Launch `quant-researcher` to compute every metric in `docs/viability-criteria.md` per sport, market type and time point, with sample sizes and uncertainty. Notebook `notebooks/00-market-survey.ipynb`, summary `research/01-verify/survey-results.md`. It must state plainly which metrics free data could not measure, or measured only approximately (for example depth beyond 3 levels, or anything distorted by the delay).
2. Launch `quant-researcher` again to score each sport and market type against `docs/viability-criteria.md` and write `research/01-verify/market-ranking.md`, including costs, competition and latency for each.
3. Launch `skeptic` on `survey-results.md`, `market-ranking.md` and `docs/viability-criteria.md`. Output `research/01-verify/review.md`.
4. Consult `principal-engineer` with one question on the market selection and the data tier it needs. Log it in `docs/decisions.md`.
5. Write `research/01-verify/requirements.md` (spec deliverable B) for the top market or markets: every Betfair access item and data requirement from spec section 3, each with status (available, available at cost, not available, unknown), the source, and the cost. Add a limitations section: what parts of the spec cannot be met with the access in the brief.
6. Gate 1. I select the market and decide the data tier and key type.

## Phase 2: Design

0. Launch `docs-verifier` on `sporting-data` for the selected sport: sources of scores and in-play state, historical and live, with cost, licence, timestamp precision and how they could be aligned with exchange timestamps. Output `research/01-verify/sporting-data.md`.
1. Launch `architect`. It writes `docs/architecture.md` (deliverable A), `docs/schema.md` (deliverable C) and `docs/dev-plan.md` (module list, order, dependencies, which modules can be built in parallel, test plan) for the selected market.
2. Launch `skeptic` on those three files. Output `research/02-design/review.md`.
3. If the skeptic marks anything `refuted`, send it back to `architect` once with the review, then re-run `skeptic`. Gate 2.

## Phase 3: Ingest

1. Create the package skeleton from `docs/architecture.md` yourself (`pyproject.toml`, empty packages, `tests/`), so engineers do not collide on shared files. Reuse or replace the Phase 1b survey recorder as the architecture says.
2. Launch one `engineer` per independent module in `docs/dev-plan.md` for this phase, in parallel. Each gets its module, its interface from the architecture, and the schema. Modules that depend on each other run in order.
3. Run the full test suite yourself.
4. Run ingestion on real data for the selected market (historical files and, if access allows, a live recording).
5. Launch `data-auditor` on the ingested data (`research/03-ingest/data-quality.md`) and `skeptic` on the code (`research/03-ingest/review.md`) in parallel. Gate 3.

## Phase 4: First look

1. In parallel: `engineer` builds the Streamlit dashboard in `app/` (spec deliverable E: prices, available liquidity, traded volume, price movement over time, with event and market selection) and the install README (deliverable G). `quant-researcher` writes `notebooks/01-orderbook-imbalance.ipynb` (deliverable F).
2. Run the dashboard and the notebook yourself on real data. Check the README steps work from a clean virtual environment.
3. Launch `skeptic` on the notebook and dashboard. Output `research/04-first-look/review.md`. Gate 4.

## Phase 5: Status memo

Write `research/05-status.md` from `docs/templates/phase-memo.md`: what works, data quality, what is verified, inferred and unknown, the limitations that bind, and a proposed plan for Phase 6 with its gate. Gate 5.

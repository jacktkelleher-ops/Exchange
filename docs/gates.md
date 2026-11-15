# Gates

A phase passes its gate only when every criterion holds and the user approves. The orchestrator reports pass or fail per criterion. Later phases are outlined so the end goal is clear; each is planned in detail at the end of the phase before it.

## Gate 0: Brief

- Every TODO in `docs/brief.md` is filled or explicitly deferred by the user.
- Each conflict in `docs/known-facts.md` has a user decision or is marked "decide at Gate 1".

## Gate 1a: Desk research and survey plan

- All Phase 1a topic files exist in `research/01-verify/` and follow the template.
- Every API operation and field the survey recorder needs is tagged `[verified: URL]`.
- Every threshold in `docs/viability-criteria.md` has a cited source or stated reasoning.
- The advisor was consulted on the criteria and the consult is logged in `docs/decisions.md`.
- `survey-plan.md` fits the stream market cap and states what free data cannot measure.
- The user has approved the criteria and the plan, and has put credentials in `.env`.

## Gate 1b: Recording

- Recorder tests pass, and the recorder contains no order operations and logs no credentials.
- The smoke audit found no blocking problem, or each one was fixed.
- The full recording covered the planned period, with gaps counted and explained.
- `data-audit.md` confirms, from the real files, the fields, ladder depth, update granularity and delay behaviour per sport.

## Gate 1: Market selected (spec deliverable B)

- `survey-results.md` reports every criterion metric per sport, market type and time point, with sample sizes, or says why it could not be measured.
- `market-ranking.md` scores every surveyed market against `docs/viability-criteria.md`, including costs, competition and latency.
- Skeptic review has no unresolved `refuted` item.
- The advisor was consulted on the selection and the data tier, and the consult is logged.
- `requirements.md` lists every spec section 3 item for the selected market with status, source and cost, and a limitations section.
- The user has selected the market and chosen the data tier and key type.

## Gate 2: Design (deliverables A, C)

- `docs/architecture.md`, `docs/schema.md`, `docs/dev-plan.md` exist.
- Every schema field traces to a verified source or is marked `[unknown]`.
- Skeptic review has no unresolved `refuted` item.
- No order placement path in the design.

## Gate 3: Ingest (deliverable D)

- Ingestion runs end to end on real darts data and is repeatable from raw.
- `python -m pytest` passes, and covers ladder reconstruction, volume deltas and timestamp handling.
- Data quality report: timestamps monotonic per market or anomalies counted; no duplicate records; cumulative traded volume never decreases or exceptions explained; reconstructed ladders match raw for sampled markets; suspensions and in-play transitions captured.
- No order operations and no credentials in the repo (skeptic grep).
- Skeptic review has no unresolved `refuted` item.

## Gate 4: First look (deliverables E, F, G)

- Dashboard runs locally and shows prices, available liquidity, traded volume and price movement over time, with event and market selection.
- Notebook runs top to bottom from derived data and computes imbalance at best, top 3, top 5 and full ladder where the data allows, stating where it does not.
- README install steps work in a clean virtual environment.
- Skeptic review has no unresolved `refuted` item.

## Gate 5: Status memo

- `research/05-status.md` written and the Phase 6 plan approved.

## Later phases (outline)

| Phase | Work | Gate criteria in brief |
|---|---|---|
| 6 | Microstructure features (spec sec 4) | Each feature unit tested; no look-ahead; feature distributions by tournament and pre-match vs in-play. |
| 7 | Behavioural regimes (spec sec 5): k-means, GMM, HMM | Regimes stable out of sample; conditional price-move probabilities differ between regimes with stated significance. |
| 8 | Predictive models (spec sec 6), 1 to 60 s horizons | Chronological splits; calibrated; beats a no-skill baseline out of sample with confidence intervals; multiple-testing correction. |
| 9 | Backtest engine (spec sec 8) | Fill simulation unit tested against hand cases; three scenarios; commission and suspensions modelled. |
| 10 | Strategy evaluation (spec sec 9) | Edge gate below. |
| 11 | Paper trading on live data, no orders | Live signals match backtest behaviour over an agreed period. |
| 12 | Execution | Written user approval, stake and liability caps, kill switch, logging. Separate `execution` package. |

## Edge gate (before Phase 11)

- Positive net expected value out of sample under the realistic and conservative scenarios, not only optimistic.
- Beats random entry, momentum, mean reversion and passive spread capture benchmarks on the same data.
- Number of trades large enough that the confidence interval on net EV per trade excludes zero. State n.
- Holds across time periods and tournament tiers, or the scope is narrowed to where it holds, with that narrowing counted as a test.
- Skeptic verdict `survived`.

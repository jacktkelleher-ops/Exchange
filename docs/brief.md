# Brief

Constraints for the project. Requirements are in `docs/spec.md`. All fields confirmed or decided by the user in Phase 0 on 2026-11-15.

## Objective

Reframed by the user on 2026-11-15. The project no longer starts from darts.

1. First, find which Betfair Exchange sports and markets can support short-horizon algorithmic trading driven by order-book behaviour, order flow and liquidity dynamics. Measure update frequency, liquidity, depth and spread at fixed time points before the off and in-play, and assess whether a retail trader could plausibly win there after costs and against the competition in that market.
2. Then, for the selected market, determine whether a repeatable, cost-adjusted edge exists, and build the data, research and backtesting infrastructure to answer that.

`docs/spec.md` is the build specification for step 2. Where it says darts, read "the market selected at Gate 1". Spec section 7 (darts-specific research) applies only if darts is selected; otherwise the same kind of sport-specific study is done for the selected sport. The spec file itself is not edited.

## Operator

- Background: financial mathematics, commercial analytics, SQL, Python, statistical modelling. Former Betfair Exchange liquidity analyst.
- Jurisdiction: Ireland. Account on betfair.com, Irish-registered (carried over).
- Hardware: Windows 11 laptop. Python 3.12 installed.

## Access and data

- Betfair app key held: delayed key (user, 2026-11-15).
- Willing to pay GBP 499 for a live app key: decide at Gate 1, once Phase 1 has verified and measured what the delayed key returns (user, 2026-11-15).
- Budget for historical data (Advanced or Pro plans): decide at Gate 1. Until then, EUR 0 (user, 2026-11-15).
- Historical files: the user's purchased Betfair data is all Basic Plan (see `docs/known-facts.md` for ranges). Downloaded by the orchestrator on 2026-11-15 to `data/raw/betfair_historic/<sport>/basic-plan/<year>.tar` with `scripts/historic/`. No Advanced or Pro data is held.
- Sporting data source: none in mind, deferred until a market is selected (user, 2026-11-15).

## Market survey (Phase 1)

Set by the user on 2026-11-15.

- Sports: horse racing (UK and Ireland), football, tennis, darts, snooker, cricket, and other sports Phase 1a finds worth including.
- Data: free first. Forward recording on the delayed key plus free Basic history. Report what free data can and cannot show. Decide at Gate 1 whether to buy Pro samples or the live key.
- Time points: before the off at 24 h, 6 h, 1 h, 15 min, 5 min and 1 min; in-play at the start, middle and late stage (first, middle and last third of the in-play period).
- Viability thresholds: the orchestrator sets them from a literature review and judgement, each with its source or reasoning, in Phase 1a. The advisor reviews them and the user approves them at Gate 1a. No threshold is used before that approval.

## Constraints

- Time available per week: 5 hours (confirmed by user, 2026-11-15)
- Bankroll for any future execution: EUR 500, scaling once a model proves itself (confirmed by user, 2026-11-15). Not used before the execution gate.
- Maximum acceptable drawdown: 30% of bankroll (confirmed by user, 2026-11-15)
- Real-money bets: none until the user approves in writing at the execution gate (spec section 11).

## Spec and access conflicts

The conflicts listed in `docs/known-facts.md` (full ladder, top-5 and full imbalance, volume at each price, 1 to 60 s horizons, queue simulation, in-play alignment with sporting events) are kept as written in the spec. Decide at Gate 1: pay for access, or narrow the spec, based on Phase 1's verified findings and measurements (user, 2026-11-15).

## Out of scope until a later gate

- Order placement of any kind.
- Deep learning or reinforcement learning (spec section 6).
- Sporting-state integration (separate module, later).

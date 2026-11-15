# Brief

Constraints for the darts project. Requirements are in `docs/spec.md`. All fields confirmed or decided by the user in Phase 0 on 2026-11-15.

## Objective

Determine whether a repeatable, cost-adjusted edge exists in Betfair Exchange darts Match Odds markets, pre-match and in-play, from order-book behaviour and liquidity dynamics. Build the data, research and backtesting infrastructure needed to answer that.

## Operator

- Background: financial mathematics, commercial analytics, SQL, Python, statistical modelling. Former Betfair Exchange liquidity analyst.
- Jurisdiction: Ireland. Account on betfair.com, Irish-registered (carried over).
- Hardware: Windows 11 laptop. Python 3.12 installed.

## Access and data

- Betfair app key held: delayed key (user, 2026-11-15).
- Willing to pay GBP 499 for a live app key: decide at Gate 1, once Phase 1 has verified what the delayed key returns (user, 2026-11-15).
- Budget for historical data (Advanced or Pro plans): decide at Gate 1, once Phase 1 has verified darts coverage and prices. Until then, EUR 0 (user, 2026-11-15).
- Darts historical files already downloaded: none (user, 2026-11-15). Phase 1 says which sample would settle the open questions.
- Sporting data source for darts: none in mind, deferred (user, 2026-11-15). Phase 1 still surveys sources so the design leaves room for one.

## Constraints

- Time available per week: 5 hours (confirmed by user, 2026-11-15)
- Bankroll for any future execution: EUR 500, scaling once a model proves itself (confirmed by user, 2026-11-15). Not used before the execution gate.
- Maximum acceptable drawdown: 30% of bankroll (confirmed by user, 2026-11-15)
- Real-money bets: none until the user approves in writing at the execution gate (spec section 11).

## Scope

- Sport: darts only. Design so other sports can be added.
- Markets: Match Odds, pre-match and in-play.
- Tournaments: all darts Match Odds markets on Betfair, analysed by tournament tier (user, 2026-11-15).

## Spec and access conflicts

The conflicts listed in `docs/known-facts.md` (full ladder, top-5 and full imbalance, volume at each price, 1 to 60 s horizons, queue simulation, in-play alignment with sporting events) are kept as written in the spec. Decide at Gate 1: pay for access, or narrow the spec, based on Phase 1's verified findings (user, 2026-11-15).

## Out of scope until a later gate

- Order placement of any kind.
- Deep learning or reinforcement learning (spec section 6).
- Sporting-state integration (separate module, later).

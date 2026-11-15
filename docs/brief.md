# Brief

Constraints for the darts project. Requirements are in `docs/spec.md`. Fields marked TODO are filled by the user in Phase 0. Fields marked "carried over" come from the archived football review brief (2026-11-15) and need the user to confirm they still apply.

## Objective

Determine whether a repeatable, cost-adjusted edge exists in Betfair Exchange darts Match Odds markets, pre-match and in-play, from order-book behaviour and liquidity dynamics. Build the data, research and backtesting infrastructure needed to answer that.

## Operator

- Background: financial mathematics, commercial analytics, SQL, Python, statistical modelling. Former Betfair Exchange liquidity analyst.
- Jurisdiction: Ireland. Account on betfair.com, Irish-registered (carried over).
- Hardware: Windows 11 laptop. Python 3.12 installed.

## Access and data

- Betfair app key held: TODO (none / delayed / live)
- Willing to pay GBP 499 for a live app key: TODO
- Budget for historical data (Advanced or Pro plans): TODO. The football review ran on EUR 0.
- Darts historical files already downloaded: TODO (plan, date range, where they are)
- Sporting data source for darts in mind: TODO (optional; spec says market data only at first)

## Constraints

- Time available per week: 5 hours (carried over)
- Bankroll for any future execution: EUR 500, scaling once a model proves itself (carried over). Not used before the execution gate.
- Maximum acceptable drawdown: 30% of bankroll (carried over)
- Real-money bets: none until the user approves in writing at the execution gate (spec section 11).

## Scope

- Sport: darts only. Design so other sports can be added.
- Markets: Match Odds, pre-match and in-play.
- Tournaments: all darts Match Odds markets on Betfair, analysed by tournament tier. TODO if the user wants to narrow this.

## Out of scope until a later gate

- Order placement of any kind.
- Deep learning or reinforcement learning (spec section 6).
- Sporting-state integration (separate module, later).

# Brief

Constraints filled in by the user on 2026-11-15.

Note: a EUR 0 data budget conflicts with live API automation if a paid live key is required (see input claim 4). Resolved in Phase 1 costs checks.

## Objective

Identify Betfair Exchange sports and markets that may offer a positive expected return after costs, then assess whether an odds-producing model or a game theory / market-structure strategy is viable.

## Operator

- Background: analytics professional, former Betfair Exchange liquidity analyst. Comfortable with bet-level and market transaction logs.
- Stack: SQL, Python, R, Databricks.
- Jurisdiction: Ireland. Account on betfair.com, Irish-registered, no known product restrictions (user confirmed 2026-11-15).

## Constraints

- Starting bankroll: EUR 500. The user will increase it once a model proves itself (user, 2026-11-15). Judge viability on edge after costs and on what a backtest can prove, not on income at EUR 500.
- Maximum acceptable drawdown: 30% of bankroll (EUR 150)
- Time available per week: 5 hours
- Budget for data and tools: EUR 0 to start (free data only until a go decision)
- Preferred in-play or pre-play: in-play ok
- Willing to run a live automated strategy via the API: yes

## Market families to scan

1. Horse racing
2. Football (match odds, over/under goals, correct score, first goalscorer)
3. Tennis
4. Cricket
5. Other (golf, basketball, US sports, esports, politics and specials)

Add or remove families here. The orchestrator runs one scanner per line.

## Definition of success for this review

- A ranked list of markets with evidence.
- For up to three shortlisted markets: a go, no-go or needs-more-data call on each model type.
- A list of what is verified, inferred and unknown.

## Out of scope

- Writing production trading code.
- Placing real bets.

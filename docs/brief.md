# Brief

Fill in the blanks marked TODO before running `/run-review`. The orchestrator will ask if any are empty.

## Objective

Identify Betfair Exchange sports and markets that may offer a positive expected return after costs, then assess whether an odds-producing model or a game theory / market-structure strategy is viable.

## Operator

- Background: analytics professional, former Betfair Exchange liquidity analyst. Comfortable with bet-level and market transaction logs.
- Stack: SQL, Python, R, Databricks.
- Jurisdiction: Ireland. TODO: confirm Betfair account jurisdiction and any product restrictions.

## Constraints

- Starting bankroll: TODO
- Maximum acceptable drawdown: TODO
- Time available per week: TODO
- Budget for data and tools: TODO
- Preferred in-play or pre-play: TODO (pre-play only / in-play ok)
- Willing to run a live automated strategy via the API: TODO (yes / no / later)

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

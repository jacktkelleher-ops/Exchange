# Odds-model viability: Football over/under goals, pre-play (mainly Over/Under 2.5)

Date: 2026-11-15
Agent: odds-model-assessor
Inputs read: CLAUDE.md, research/02-ranking.md, research/03-viability/football-over-under/costs-constraints.md (including the orchestrator addendum), research/00-verify/input-claims.md (including Addendum 2, the Betfair Historical Data Feed Specification, cited as SPEC), docs/brief.md.

DEV = https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages

Access note: WebFetch of www.football-data.co.uk failed at DNS (host not in the session's allowed network domains). That host needs to be allowed before its column list can be read. Everything about free football data from that site comes from WebSearch summaries and is `[inferred]`.

## Call

no-go for trading this bankroll. Main reason: the model must beat the close by about 2.0% to 3.5% of stake after costs, proving that needs roughly 3,000 to 10,000 bets, and a EUR 500 bankroll at EUR 1 to 3 stakes would earn about EUR 4 to 21 a year if the edge were real. Single biggest risk: the over/under close is already efficient, so the model has no edge to find.

Change from the ranking (needs-more-data): the SPEC facts remove the free-results and free-benchmark worries only if Basic covers O/U markets, which is still `[unknown]`. They do not change the economics. A 4 to 5 week backtest is an optional low-cost exercise, not a reason to trade.

## 1. Target

- Outcome: P(total goals >= 3) for Over/Under 2.5, from a joint goals model, giving a probability for every line (0.5 to 4.5). `[inferred]`
- Time: a fixed snapshot before kick-off, for example 3 hours and 30 minutes out, with the bet placed at that price. The model is scored against the last price before kick-off. `[inferred]`
- Settlement: 90 minutes plus stoppage time is the usual soccer rule. The official O/U rules page was not read. `[unknown]`
- Delayed key note: prices are 1 to 180 seconds stale `[verified: DEV/2687105/Application+Keys]`. For a bet hours before the off this is minor `[inferred]`.

## 2. Benchmark

- Required by CLAUDE.md: the closing price or BSP, not 50/50 and not a bookmaker average.
- Betfair close from free Basic history (best route):
  - Basic data runs from May 2015 at 1-minute intervals and gives the last traded price per runner `[verified: SPEC p1, p3-4]`.
  - Every plan, Basic included, carries the full marketDefinition: marketType, marketBaseRate, inPlay, runner status (WINNER, LOSER) and bsp `[verified: SPEC p1-2]`.
  - So if Basic covers soccer O/U markets, the benchmark is the last 1-minute ltp before the off, the label is the runner WINNER or LOSER, and the commission rate for the market is read from marketBaseRate. No outside results source is needed for those markets `[inferred from SPEC]`.
  - Whether Basic covers O/U markets (marketType names such as OVER_UNDER_25) is `[unknown]`. The spec is field-level only `[verified: SPEC]`. Resolve by downloading one free Basic soccer month at historicdata.betfair.com.
  - Limits: ltp is the last matched price, not a back or lay quote, and it is up to 60 seconds before the off. There is no volume, so a thin market's ltp can be stale or a one-off trade `[verified: SPEC p3-4]` for the missing fields, `[inferred]` for the staleness effect. Filter out markets whose ltp did not update in the final minutes.
  - No ladder means no spread, so slippage cannot be measured from Basic `[verified: SPEC p3-4]`.
- Forward capture on the free delayed key: logs best back and lay at 3 levels, no total matched. The true close is up to 180 seconds later `[verified: DEV/2687105/Application+Keys]`. This gives spread data for slippage that Basic lacks, from today forward only.
- Free proxy benchmark: football-data.co.uk is reported to carry results plus pre-match and closing O/U 2.5 odds from Pinnacle and other bookmakers, closing columns marked with a C suffix `[inferred: WebSearch summaries, column names and start season not confirmed]`. A Pinnacle close is usually the harder benchmark `[inferred]`. Useful as a cross-check or fallback if Basic lacks O/U.
- Comparison methods:
  1. Log loss of model probability versus the devigged close probability on the same matches. For a Betfair two-way market the close is the ltp pair, devigged by a method fixed before testing `[inferred]`.
  2. Closing line value: mean of (price taken / closing price - 1) on flagged bets.
  3. Simulated ROI after commission at the marketBaseRate and one tick of slippage.
- Honest limit: the Betfair close and the Pinnacle close differ. A model that beats one may not beat the other `[inferred]`.

## 3. Data

| Item | Source | Cost | History | Look-ahead risk | Tag |
|---|---|---|---|---|---|
| Betfair soccer O/U close (ltp), result label, commission rate | Basic historical data, if O/U is covered | free | May 2015 onward, 1-minute | ltp 1 minute before the off. Take only prices stamped before the off. Do not use inPlay ticks. | `[verified: SPEC p1-4]` for fields, O/U coverage `[unknown]` |
| Results, goals, top leagues and many lower ones | football-data.co.uk CSVs | free | reported from 2000/01 | Low if team rating uses only prior matches | `[inferred]` |
| Closing O/U 2.5 odds (Pinnacle, others) | football-data.co.uk | free | start season not confirmed | High if closing odds are used as a feature for a model judged against closing odds. Keep them out of the features. | `[inferred]` |
| Shots, shots on target | same files | free | most seasons | Post-match only. Use as lagged inputs. | `[inferred]` |
| Expected goals | FBref or Understat style sites, not searched | free but scraping, terms unchecked | roughly 2014 onward for Understat, `[unknown]` | Match xG is post-match. Only lagged xG is legal. | `[unknown]` |
| Line-ups, injuries, weather, referee | not sourced | | | Confirmed line-ups arrive about 1 hour before kick-off, after a 3.5 hour snapshot | `[unknown]` |
| Betfair O/U live book | delayed key, 3 levels, no total matched | free | forward only | none | `[verified: DEV/2687105/Application+Keys]` |
| Advanced (1 second, best offers, volume) and Pro | historicdata.betfair.com | price `[unknown]` (sources conflict) | May 2015 onward | none extra | `[verified: SPEC p3-4]` for content, price `[unknown]` |

Look-ahead traps to design out: team strength fitted on the whole season, closing odds in features, final league table or promotion status used before it was known, snapshot time later than the bet time. Joining Basic markets to the goals source needs team-name matching, which the soccer mapping files may help with `[verified: DEV/2686993/Additional+Information]` (they exist, content not read).

## 4. Method

Data size: about 1,750 matches a year in the top five European leagues `[inferred]`, so 10 seasons is about 17,500 matches. Each team has about 38 matches a season. That supports a small model only.

- Realistic class: Poisson or bivariate Poisson with team attack and defence strengths and home advantage, fitted with exponential time weighting (Dixon-Coles style, including the low-score correction), refit weekly `[inferred]`. Literature was found by search only and not fetched `[inferred]`.
- Optional second layer: a regularised logistic regression on lagged xG and shot differences, to adjust the Poisson mean. Keep to under about 20 features `[inferred]`.
- Not supported by the data: deep nets, player-level models, tracking data, large gradient-boosted ensembles with many tuned hyperparameters `[inferred]`.
- Fit in Python or R on a laptop. Databricks is not needed `[inferred]`.
- Structural point: a team-strength Poisson model uses the same public inputs the market already uses. The market also sees line-ups, injuries and money. A pure results model is unlikely to beat the close `[inferred]`. No evidence of mispricing in Betfair O/U markets was found anywhere in the review. The ranking's edge score of 3 rests on the input file only (research/02-ranking.md).

## 5. Required accuracy

Formulas from the costs file: EV = p(o-1)(1-c) - (1-p). At o = 2.00, a back bet needs EV > 0.

| Case | Commission cost | Slippage, 1 tick | Total EV needed | Probability edge needed |
|---|---|---|---|---|
| Basic 2% | 1.00% `[inferred]` | 1.0% | 2.0% | about 1.0 pp |
| Planning 5% | 2.50% `[inferred]` | 1.0% | 3.5% | about 1.8 pp |

The true rate per market can be read from marketBaseRate in the history files or the API `[verified: SPEC p1-2]`, `[verified: DEV/2687465/Betting+Type+Definitions]`. The rate itself is `[unknown]`.

Arithmetic:

- Commission drag at fair odds is c(o-1)/o = 0.02 x 1 / 2 = 1.00%, and 0.05 x 1 / 2 = 2.50% (costs file section 7).
- One tick at o = 2.00 is 0.02 `[verified: DEV/2686993/Additional+Information]` (ladder step 0.02 between 2 and 3). Crossing the spread by one tick lowers the price by 0.02, and EV falls by p x 0.02 = 0.5 x 0.02 = 1.0% of stake. Whether the O/U 2.5 spread is one tick is `[unknown]`. A passive order avoids this but risks no fill and adverse selection `[inferred]`.
- Probability edge = EV needed / o roughly: 2.0% / 2 = 1.0 pp, and 3.5% / 2 = 1.75 pp, about 1.8 pp.
- Costs file break-even without slippage: 0.5 pp at 2% and 1.3 pp at 5%.
- In log loss, a 1.8 pp edge on a 50/50 market is about 0.0175^2 / (2 x 0.25) = 0.0006 nats per match better than the close, tiny and hard to measure `[inferred]`.
- In CLV, the taken price must beat the close by about 2% to 3.5% on average. Pre-match O/U markets typically move by less than that between a 3.5 hour snapshot and the close `[unknown]`, so the model would need to be sharper than the close itself.

## 6. Sample size

Per bet at o = 2.00: outcomes are +1 (x 0.98 or 0.95 after commission) or -1, so the standard deviation of profit per unit stake is about 1.0 `[inferred]`.

n = (z x sd / edge)^2, using z = 2 (about 95% two-sided).

| Target | Edge to show | n bets |
|---|---|---|
| Edge equal to the cost hurdle at 2% commission | 2.0% | (2 x 1 / 0.02)^2 = 10,000 |
| Same at 5% commission | 3.5% | (2 / 0.035)^2 = 3,265 |

- One-sided z = 1.64 cuts these to about 6,700 and 2,200.
- Betting volume: the operator at 5 hours a week, betting only flagged matches (assume 10% to 15% of 1,750 matches) places about 175 to 260 bets a year `[inferred]`. 3,265 bets would take 12 to 19 years. 10,000 bets would take 40 years or more. Live proof of skill is not reachable inside any useful horizon.
- Backtest path: 10 seasons is about 17,500 matches and about 1,750 to 2,600 flagged bets, which gives a standard error on ROI of 1 / sqrt(2,000) = about 2.2%. A 2% edge cannot be separated from luck even with 10 seasons. Tuning and multiple testing make it worse `[inferred]`. Basic's 2015 start gives about 11 seasons if O/U is covered `[verified: SPEC p1]` for the start date.
- Log loss route: per-match difference sd is about 0.035 nats when model and close differ by about 1.75 pp, mean gain 0.0006. n = (2 x 0.035 / 0.0006)^2 = about 13,600 matches `[inferred]`. About 8 seasons of the top five leagues. Borderline possible in a backtest.
- CLV route: if CLV per bet has sd about 3% and the true mean is 1%, n = (2 x 3 / 1)^2 = 36 bets. Fast, but CLV is a leading indicator only and does not prove profit after costs `[inferred]`.

## 7. Bankroll plan: 30% drawdown at EUR 1 minimum bet

Limits: bankroll EUR 500, maximum drawdown 30% = EUR 150 `[verified: docs/brief.md]`. Minimum bet EUR 1 `[verified: DEV/2686993/Additional+Information]` (the costs file body says EUR 2 and its addendum overrides it).

Model: bets at o about 2.00, sd 1 unit per bet, true edge mu per unit stake. Probability that cumulative losses ever reach L units is about exp(-2 x mu x L / sd^2) for a positive edge `[inferred]`, and 100% for zero or negative edge in the long run.

| Flat stake | Units to lose EUR 150 (L) | Ruin chance if true mu = 2% | If true mu = 0 |
|---|---|---|---|
| EUR 1 | 150 | exp(-0.04 x 150) = exp(-6) = 0.25% | certain eventually |
| EUR 2 | 75 | exp(-3) = 5% | certain eventually |
| EUR 3 | 50 | exp(-2) = 14% | certain eventually |
| EUR 5 | 30 | exp(-1.2) = 30% | certain eventually |

- Kelly check: full Kelly at EV 2% and o = 2.00 is 2% of bankroll = EUR 10. The edge is uncertain, so use a quarter or less. Quarter Kelly is 0.5% = EUR 2.50 `[inferred]`.
- Plan: flat EUR 1 to EUR 2 stakes (0.2% to 0.4% of bankroll). Review at a EUR 100 loss, hard stop at EUR 150. Do not scale up from the sample, since the sample cannot show skill (section 6).
- Income at these stakes: 200 bets x EUR 2 x 2% = EUR 8 a year, EUR 4 at EUR 1 stakes. At EUR 3 stakes and 3.5% net edge: 200 x 3 x 0.035 = EUR 21 a year. Against about 260 hours a year this is far below any wage `[inferred]`.
- Liquidity does not bind at these sizes `[inferred]`. Depth of O/U 2.5 books is not measured `[unknown]`.

## 8. Build effort to a first honest backtest

At 5 hours a week `[verified: docs/brief.md]`:

| Step | Hours | Weeks |
|---|---|---|
| Download Basic soccer files, parse JSON in tar.bz2, check for O/U marketType, extract last pre-off ltp, WINNER/LOSER label, marketBaseRate (SQL/Python, files are large) | 6 to 8 | 1.5 |
| Team-name join to a goals source and a Dixon-Coles style model, rolling weekly refit, no look-ahead | 8 to 10 | 2 |
| Devig, log loss, CLV and ROI backtest with costs, rules locked before looking at results | 5 to 8 | 1 to 1.5 |
| Total | about 20 to 25 | 4 to 5 |

- If Basic has no O/U, fall back to football-data.co.uk closes (host must be allowed). Time is about the same.
- Forward capture of delayed-key O/U books, about 5 extra hours in parallel, gives spreads for slippage.
- The delayed key is stated to be for development and functional testing `[verified: DEV/2687105/Application+Keys]`. Enforcement `[unknown]`.

## 9. Summary table

| Item | Result |
|---|---|
| Target | P(over 2.5) at a fixed pre-kick-off snapshot |
| Benchmark | Basic last 1-minute ltp before the off, if O/U is covered (`[unknown]`). Pinnacle close from football-data.co.uk as fallback `[inferred]` |
| Data | Free Betfair close and labels if covered `[verified: SPEC]`. Free goals sources, no free line-ups or confirmed xG |
| Method | Dixon-Coles Poisson, weekly refit, optional small logistic layer |
| Required edge | 2.0% EV (1.0 pp) at 2% commission, 3.5% EV (1.8 pp) at 5% |
| Sample | about 3,300 to 10,000 bets live, about 13,600 matches for log loss |
| Build | 4 to 5 weeks at 5 hours a week |
| Income if edge is real | about EUR 4 to 21 a year at EUR 1 to 3 stakes |
| Call | no-go (trading). Optional backtest only. |

## What would change the call

- A Basic file showing O/U 2.5 closes, and an out-of-sample backtest of a Poisson model against the Betfair close showing a net gain of at least 1.8 pp over at least 13,000 matches. This costs about 4 to 5 weeks. Even if it succeeds, the income case at this bankroll stays weak, so it would not turn the call into a go for EUR 500 of capital without a larger bankroll.
- marketBaseRate on O/U markets reading 2% rather than 5%. Reduces the hurdle from 3.5% to 2.0% only.

## Sources used

- Betfair Historical Data Feed Specification (user-supplied official PDF, cited via research/00-verify/input-claims.md Addendum 2)
- https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages/2687105/Application+Keys
- https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages/2686993/Additional+Information
- https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages/2687465/Betting+Type+Definitions
- WebSearch summaries about football-data.co.uk closing odds columns (not fetched, `[inferred]`)

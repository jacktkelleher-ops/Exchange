# Decision memo: Betfair Exchange opportunity review

Date: 2026-11-15

## Recommendation (max 5 lines)

No-go on staking money now in any market reviewed.
Needs-more-data on one track: football Over/Under 2.5, own-odds model, judged against the Betfair close. It can be tested offline at EUR 0 if Basic history covers O/U. If that test shows positive closing line value net of 2% commission, move to a EUR 1 stake trial.
Passive resting orders (maker side) are no-go on both tracks under this brief. Average makers break even, and a delayed-key quoter cannot be measured without real bets.
Everything in-play or queue-based is no-go while the live key (GBP 499) is out of budget.

## Ranked markets

From `research/02-ranking.md`. No market passed the gates (pass mark 60, data access at least 3). Scores are before the historical data spec arrived, which would likely lift football O/U data access from 2 to 3 if Basic covers O/U [inferred].

| Rank | Market | Score | Shortlisted | Note |
|---|---|---|---|---|
| 1 | Football over/under goals, own-odds model | 57 | Yes, by user (needs-more-data) | Best case 62 once Basic O/U coverage is confirmed |
| 2 | Football in-play after surprise goals, market structure | 56 | No | Needs live key and paid tick data |
| 2 | Cross-sport pre-play passive resting orders, market structure | 56 | Yes, by user (needs-more-data) | MPRA 126351 basis |
| 4 | Golf outright winner, own-odds model | 55 | No | Anecdotal edge, slow sample |
| 5+ | Lower leagues, women's football, others | below 55 | No | See ranking file |

## Viability by shortlisted market

### Football over/under goals (O/U 2.5, pre-play)

| Track | Call | Key reason | Biggest risk | Skeptic result |
|---|---|---|---|---|
| Odds-producing model | needs-more-data (memo call; the assessor's no-go was weakened) | The decisive test is a free offline backtest of closing line value against the Betfair close, inside the EUR 0 budget. Trading now is not justified. | The O/U 2.5 close in major leagues is already efficient. No one named a reason sharp money would leave a 1% to 3% edge. | weakened |
| Game theory / market structure | no-go (A to E); needs-more-data (F, sharp-book reference) | Free-key prices are 1 to 180 s late and show 3 levels, so quoting, cross-market, in-play and ladder strategies cannot be run or measured. F is the same edge as the odds model. | Being picked off on stale quotes; for F, the 500-credit free cap on bookmaker data. | survived |

Net expected edge after costs: unknown. Break-even at evens is about 1.0% of stake (0.5pp of probability) at 2% commission and 2.5% (1.25pp) at 5%, before slippage [confirmed by skeptic recompute]. With half a tick of slippage at 2% commission the hurdle is about 1.25% to 1.5% of stake [inferred, skeptic]. Commission rate for the account is unverified.

Minimum test to confirm: one free Basic soccer month, to confirm O/U market types are present. Then a chronological walk-forward backtest of a Poisson or Dixon-Coles goals model against the last 1-minute last traded price before kick-off, scored by closing line value net of 2% commission. Around 400 bets give a first read on CLV with a standard deviation near 0.10 [inferred]; proving realised profit needs 10,000 to 40,000 bets [inferred]. Do not use the final market definition for anything but result labels (look-ahead risk).

### Passive resting orders (maker side, football Match Odds and UK/Irish racing Win)

| Track | Call | Key reason | Biggest risk | Skeptic result |
|---|---|---|---|---|
| Odds-producing model | no-go | No evidence of a positive maker edge. Restated reason (skeptic): "no edge evidence and not testable within the brief". | Commission hurdle was overstated by assuming every fill is held to settlement. | survived (reason weakened) |
| Game theory / market structure | no-go (single-sided, football scalping, racing scalping); needs-more-data (execution overlay, wide resting orders) | Stale delayed view, no queue or volume data, and about EUR 2 a week at best. | Completion-rate and adverse-selection ranges are asserted, not measured. | survived |

Net expected edge after costs: no positive estimate supported. Search summaries of MPRA 126351 say makers "generally break even" pre-match [inferred]; the result being net of commission is unknown.

Minimum test to confirm: EUR 1 resting orders on the delayed key, logged for 13 to 25 weeks, measuring fill rate by offset and mark-out against the close. This places real bets, which the brief puts out of scope. It needs the user's approval and a lay liability cap.

## What is verified

DEV = https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages. SPEC = Betfair Historical Data Feed Specification (`docs/inputs/official/`).

- Live app key activation fee GBP 499; delayed key free, can place bets on the live exchange, 3 price levels, no total matched by selection, prices 1 to 180 s late, Stream API 2 connections and 200 markets [verified: DEV/2687105/Application+Keys]. Resolves input claim 4.
- Delayed key "should be used for development purposes and any functional testing" [verified: DEV/2687105/Application+Keys].
- Minimum bet EUR 1, minimum BSP liability EUR 10 [verified: DEV/2686993/Additional+Information].
- CLASSIC price ladder as in the input file [verified: DEV/2686993/Additional+Information].
- Market data request cap of 200 points [verified: DEV/2687478/Market+Data+Request+Limits].
- PASSIVE and DYNAMIC bet delay models; tennis delay drops to 1 s at set games; football DYNAMIC events have no half-time delay [verified: DEV/2687396/Exchange+Stream+API].
- Historical data from May 2015. Basic: 1-minute last traded price plus market definition. Advanced: 1-second best offers, volume and traded-at-price. Pro: tick-by-tick full ladder. Every plan carries marketType, marketBaseRate and runner WINNER/LOSER status and BSP [verified: SPEC p1-4]. Confirmed by both skeptics.
- MPRA 126351 exists and finds late in-play longshot bets lose even for makers [verified: https://mpra.ub.uni-muenchen.de/126351/]. Resolves input claim 10's existence.
- Reading paper (Angelini, De Angelis, Singleton 2022) exists and finds mispricing grows after surprise late goals by longshots [verified: https://research.reading.ac.uk/football-research/new-journal-article-informational-efficiency-and-behaviour-within-in-play-prediction-markets/].
- Break-even cost table recomputed by the skeptic [confirmed].

## What is inferred

- Commission packages for Ireland: Basic 2%, Rewards 5%, Rewards+ 8%.
- Expert Fee tiers (0% / 20% / 40%, GBP 25k and 100k, rolling 52 weeks), and that it does not bind at this bankroll.
- Basic historical data is free to download. The spec itself says data is "for purchase".
- Makers "generally break even" pre-match in MPRA 126351 (search summary only).
- O/U 2.5 is the deepest totals line; typical pre-match prices 1.85 to 2.10.
- Irish tax: private exchange winnings outside income tax and CGT (secondary sources). Not tax advice.
- Every edge range and sample size in Phase 3.

## What is unknown

| Item | Step to resolve |
|---|---|
| Whether Basic covers O/U markets | Download one free Basic soccer month |
| The account's actual commission rate (marketBaseRate may show 5% on football even on a 2% package) | Check My Betfair Rewards in the account |
| Transaction charge threshold and exemptions (claim 3) | Read the Betfair charges page |
| Advanced and Pro prices (claim 5) | Read historicdata.betfair.com plans page |
| Whether Betfair limits winning accounts (claim 8) | Read Exchange terms |
| Whether sustained live use of the delayed key is allowed | Written question to Betfair Developer Support |
| Reading paper 50% ROI figure (claim 9) | Read the full paper |
| Whether MPRA maker returns are net of commission | Read the full paper |
| Tennis retirement rule on the Exchange (claim 6) | Read the Exchange rules page |
| Pinnacle yield and power devig claims (11, 12); lower-league efficiency (13) | Not checked; anecdotal |

## Refuted or corrected claims

- Live key GBP 299 (input and some secondary sources): refuted. Current fee is GBP 499.
- "Delayed key cannot place bets" (older snippet): refuted by the 2026-11-02 page.
- EUR 2 minimum stake (costs file body): refuted. EUR 1.
- "Pro data at 50 ms": contradicted. The spec says tick by tick.
- MPRA 126351 read as "makers win" or "net of commission" (`research/02-ranking.md` line 124): not supported. The finding is relative to takers.
- Two-tick-stop completion break-even 66.4% / 67.2%: corrected to 67.1% / 67.8%.
- Odds-model sample-size method (edge set equal to the hurdle): wrong; corrected figures are larger.
- The Odds API facts tagged [verified] from a search summary: downgraded to [inferred].

## Proposed next step

Download one free Basic soccer month from historicdata.betfair.com. If it contains O/U 2.5 markets, build a goals model on 2015 to 2023 and walk forward on 2024 to 2025, scoring closing line value against the last pre-kick-off 1-minute price, net of 2% commission. About 20 to 25 hours. No money staked.

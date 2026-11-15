# Betfair Basic historical data: check of the user's download

Date: 2026-11-15
Agent: orchestrator. Source file: user's `data.tar` (Betfair Basic plan), streamed with `scripts/scan_basic.py`. Derived CSVs in `data/derived/` (git-ignored).

## Contents

| Item | Finding | Tag |
|---|---|---|
| Files | 206,546 market files, all soccer (eventTypeId 1), 6,217 events | [verified: data.tar] |
| Kick-off range | 2025-09-03 to 2026-10-11 (about 13 months). Folder names say 2026/Sep and Oct, which do not match the kick-off dates | [verified: data.tar] |
| Market types | MATCH_ODDS, OVER_UNDER_05 to 85, ALT_TOTAL_GOALS, ASIAN_HANDICAP, CORRECT_SCORE, BTTS, DRAW_NO_BET, DOUBLE_CHANCE and more | [verified: data.tar] |
| O/U 2.5 markets | 6,217, of which 6,034 settled with a WINNER | [verified: data.tar] |
| Countries (O/U 2.5 settled) | GB 705, blank 582, IT 219, JP 183, AR 169, SE 144, CZ 135, NO 122, others below | [verified: data.tar] |
| marketBaseRate | 5.0 on 6,031 markets, 6.0 on 3. It does not show the account's package rate | [verified: data.tar] |

This resolves the open item from Phase 3: **Basic covers O/U markets.** Data access for football O/U moves from 2 to 3 on the rubric [inferred].

## Price coverage before kick-off (O/U 2.5, settled, both runners have a last traded price)

| Time before scheduled kick-off | Markets priced | Share |
|---|---|---|
| 24 h | 1,022 | 17% |
| 6 h | 3,258 | 54% |
| 3 h | 4,130 | 68% |
| 1 h | 4,811 | 80% |
| 15 min | 5,323 | 88% |
| Close (last price before in-play) | 5,695 | 94% |

Basic has no price when nothing has traded, so a third of markets have no price 3 hours out. This supports the user's plan to fill gaps with Kalshi and Polymarket prices (`docs/backlog.md`) [inferred].

## First look at the close (Over 2.5 implied probability from last traded price)

| Implied at close | n | Actual Over rate |
|---|---|---|
| 0.3 to 0.4 | 461 | 0.399 |
| 0.4 to 0.5 | 1,359 | 0.465 |
| 0.5 to 0.6 | 1,921 | 0.546 |
| 0.6 to 0.7 | 1,292 | 0.624 |
| 0.7 to 0.8 | 548 | 0.732 |
| 0.8 to 0.9 | 183 | 0.787 |

- The close is broadly calibrated. No bucket shows a gap large enough to clear costs on its own after allowing for sampling error [inferred].
- Median absolute move in Over implied probability from 3 h to close is 1.37 pp (75th percentile 2.67 pp, n 4,792). That is larger than the 0.5 to 1.25 pp hurdle, so a model that predicts the direction of the move could beat the close. This is a precondition for an edge, not evidence of one [inferred].
- Last traded price is not a mid price. It bounces between back and lay, which adds noise to both checks [inferred].

## Next steps

1. Add goals data (or a ratings source) and fit a baseline goals model; score closing line value at 3 h and 1 h against the close, net of 2% and 5%.
2. Pull Kalshi and Polymarket EPL O/U prices for the same matches to fill gaps and compare closes.

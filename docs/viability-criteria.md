# Viability criteria for the market survey

Date: 2026-11-15. Author: orchestrator. Status: revision 2, after the Gate 1a advisor consult (`docs/decisions.md`, 2026-11-15). For user approval at Gate 1a. No threshold here is used before the user approves it.

Purpose: decide which Betfair sport, market type and time point can support short-horizon (1 to 60 s) trading driven by order-book behaviour, order flow and liquidity, and whether a retail trader could plausibly win there after costs. Kalshi is scored separately with the same metrics and never stands in for Betfair.

How it is used:
1. Gates screen out cells that cannot work.
2. Scored metrics build a profile of each surviving cell. They shortlist up to three cells, with a written judgement per cell. The scores are not summed into a single ranking, because on free data the measurable metrics mostly track liquidity (advisor point 4).
3. A cell is selected at Gate 1 only once S5 (move versus cost) and S10 (queue turnover) have been measured on data that can see them: Pro history, a live key, or Kalshi for Kalshi cells.

Basis tags:
- `[literature: ...]` a published value, with the full-text read recorded in `research/01-verify/literature-reads.md`.
- `[reasoning]` set by the orchestrator because no published value exists. The reasoning is stated. These are for the user to challenge.
- `[relative]` no absolute cut-off; reported as terciles of the surveyed cells.
- `[user]` a value only the user can set. Left blank until Gate 1a.

## Definitions

| Term | Definition | Basis |
|---|---|---|
| Cell | sport x market type x time point | `docs/brief.md` |
| Time points | 24 h, 6 h, 1 h, 15 min before the actual off; early, middle and late thirds of the in-play period. The 5 min and 1 min points are kept but cannot be measured on free data (180 s cadence). | brief; advisor point 8 |
| Actual off | the `pt` of the first market definition with `inPlay` true; for markets that never go in-play, the first `SUSPENDED` status at or after `marketTime` | [reasoning] scheduled start is wrong for racing, which often goes off late (advisor point 8) |
| Runner set | the two runners with the highest matched volume in the market at that time point | [reasoning] covers two-way markets fully and the favourite plus second favourite in racing; avoids averaging over long-priced runners (advisor point 1) |
| Spread | best lay minus best back from the `atb`/`atl` ladders, in Betfair ticks, per runner in the runner set | [reasoning] full ladders are present on the delayed-key stream [verified: research/01-verify/survey-plan.md section 1] |
| Valid snapshot | market status `OPEN`; suspended snapshots are excluded from depth, spread and activity statistics | advisor point 8 |
| Planned stake S | EUR 10 | [reasoning] 2% of the EUR 500 bankroll; ten times the EUR 1 minimum bet. User to confirm. |
| Commission rate c | the market's `marketBaseRate` | [verified: spec PDF p1]. The user's own package or discount is checked in their account. |
| Uncertainty | every median is reported with a bootstrap 95% interval and its n; cells with fewer than 30 markets are flagged | [reasoning] about one snapshot per market per cell, so n is the number of markets |

## Gates (all must pass)

| # | Gate | Threshold | Basis |
|---|---|---|---|
| G3 | Depth at best back and best lay, each runner in the runner set | median at least 10 x S (EUR 100) on each side | [reasoning] an order of size S should be at most 10% of the best level, so it neither moves the price when taking nor joins a queue too short to matter. The currency of ladder sizes on this account is [unknown]; the smoke test checks it. |
| G4 | Traded-volume events per minute | median at least 1 per minute | [reasoning] a 60 s horizon needs about one trade per horizon. Measurable only on Pro, live-key or Kalshi data; the Basic one-`ltp`-per-minute proxy saturates at exactly this level and is not used (advisor point 7). |
| G5 | In-play: `betDelay` versus horizon | `betDelay` strictly less than the horizon | [reasoning] an order held for `betDelay` seconds cannot act on a shorter signal. Necessary, not sufficient: the usable time is horizon minus `betDelay`, reported alongside. |
| G6 | Data to test the cell is obtainable | a source exists for S5 and S10 at the required resolution, at a cost the user approves | [reasoning] |
| G7 | Fixed-cost break-even | expected net profit at stake S over [user] months covers the fixed costs the cell needs (live key GBP 499 one-off if needed; Pro data GBP 79 to 230 per month while researching) | [user] bar; cost figures [verified: known-facts; historical-data.md]. Advisor point 8. Computed at Gate 1 once an edge estimate exists; at Gate 1a only the cost side is known. |

Removed from the gates in revision 2 (advisor points 1 and 3):
- **Old G1: cumulative matched volume of at least GBP 23,400 by the off.** It is now context metric C1.
- **Old G2: mean quoted spread of at most 0.044.** Flepp's spread unit is [unknown] and an odds-unit spread fails long-priced runners mechanically. It is now context metric C2. Spread enters the profile as S2 in ticks. A hard spread gate exists only if the user sets one [user].

## Context metrics (reported, not gated)

| # | Metric | Basis |
|---|---|---|
| C1 | Cumulative matched volume at the cell's time point, against GBP 23,400 | [literature: Flepp, Nuesch and Franck 2017: below GBP 23,400 cumulative exchange volume, or above 0.044 average quoted spread, bookmakers offered better prices than Betfair in soccer]. A bettor-versus-bookmaker benchmark, not a trading floor. |
| C2 | Quoted spread in odds for the runner set, against 0.044 | [literature: same]; unit [unknown] |

## Scored metrics (profile of each surviving cell)

Each scores 1 (weak), 2 or 3 (strong). Not summed.

| # | Metric | How computed | Bands | Basis | Free Betfair data? |
|---|---|---|---|---|---|
| S1 | Liquidity | matched volume per minute at the time point, from `trd` deltas | terciles | [relative] | yes, per 3 min |
| S2 | Spread in ticks | median spread, runner set | 1 tick = 3; 2 = 2; 3 or more = 1 | [reasoning] each tick beyond the minimum is cost to recover | yes |
| S3 | Depth | median depth at best and summed over top 3, each side, as a multiple of S | terciles | [relative] | yes |
| S4 | Activity | median traded-volume events per minute | at least 12 = 3 (supports 5 s); 4 to 12 = 2 (15 s); 1 to 4 = 1 (60 s) | [reasoning] about one trade per horizon | no |
| S5 | Move versus cost | share of horizon-h windows in which the absolute mid move, in ticks, is at least the round-trip cost k = spread ticks / (1 - c) | 3 / 2 / 1 by terciles of that share, per horizon | [reasoning] a taker needs moves bigger than cost; commission is charged on net winnings, so a profit of m ticks keeps (1 - c) x m, and the move must cover the spread after that haircut. The median move at 1 to 5 s is likely zero, hence a share (advisor point 6). Measures volatility, not predictability; predictability is Phase 6 onward. | no |
| S6 | Resilience | median time for best-level depth to recover after a depleting trade | terciles, faster is stronger | [relative] | no |
| S7 | Capacity | qualifying markets per week x minutes per market in a valid snapshot state | terciles | [relative] | yes, plus Basic history |
| S8 | Suspension burden, in-play | share of in-play time suspended; suspensions per hour | terciles, less is stronger | [relative] | yes, plus Basic history |
| S9 | Data cost to test | Pro GBP per month for the sport | GBP 79 = 3; GBP 150 = 2; GBP 230 = 1 | [verified: historical-data.md, Betfair support page updated 2026-09-24]; banding [reasoning] | n/a |
| S10 | Queue turnover (maker side) | depth at best divided by matched volume per minute at that price: minutes to clear the queue a new resting order joins | terciles, faster is stronger | [reasoning] Whelan finds makers out-earn takers, so the resting-order route needs a queue that clears (advisor point 5) | roughly, from 180 s `trd` deltas |

S1, S3 and S7 all move with liquidity. Read them as one dimension, not three votes.

## Qualitative assessment (beside the profile)

| # | Question | Evidence |
|---|---|---|
| Q1 | Cost hurdle and side | Betfair soccer, final pre-play trades 2022-24, after 2% commission. Match odds: takers -2.5%, makers +0.6% (902,568 bets, 152,102 matches). Total goals: takers -2.2%, makers +2.0% (2,088,032 bets) [literature: Whelan 2026]. A taker strategy starts about 2.5% behind on average; a maker strategy starts near zero and carries adverse selection. State which side each candidate strategy takes. |
| Q2 | Competition | automated liquidity, in-play data-feed advantages (courtsiders, scouts), latency; sport files in `research/01-verify/` |
| Q3 | Known inefficiency | for example late in-play soccer longshots losing even for makers [literature: Whelan 2026]; in-play tennis mispricing after news [Brown 2014, abstract only] |
| Q4 | Retail feasibility | can the cell be traded with the access the user would buy, given bet delay and data delay? |

## What free data can and cannot measure

Measured on the user's delayed key on 2026-11-15; full table in `research/01-verify/survey-plan.md` section 2.

- **Stream:** one full-ladder snapshot per market every 180 s, with `trd` and `tv` [verified: data/raw/probe/20261115T233458Z.jsonl].
- **REST polling:** refreshes faster, but each response is a variable 5 to 240 s old [verified: data/raw/probe/*_poll.jsonl].
- **Measurable on free Betfair data:** G3, G5, C1, C2, S1, S2, S3, S7, S8, and roughly S10, at the 24 h, 6 h, 1 h and 15 min points and the in-play thirds.
- **Not measurable on free Betfair data:** G4, S4, S5, S6, the 5 min and 1 min points, and the in-play period of races, which may last only a few 180 s snapshots.
- **Basic history:** S7, S8, G5 and a per-minute activity proxy only [verified: spec PDF p3].
- **Kalshi public REST:** measures everything, but only for Kalshi.

## Open questions for the user at Gate 1a

1. Is S = EUR 10 the right planned stake? It drives G3 and S3.
2. G7: over how many months must expected net profit at stake S cover fixed costs?
3. Do you want a hard spread gate in ticks, or keep spread in the profile only?
4. Maker, taker, or both? Whelan's numbers favour the maker side; S10 and S5 test each.
5. Buy a Pro sample month now (option B in `survey-plan.md` section 5), or after the free survey?

# Market structure assessment: Football over/under goals (pre-play, in-play only if feasible)

Date: 2026-11-15. Agent: market-structure-assessor. (Saved verbatim by the orchestrator: the agent returned the file as text.)

Inputs read: CLAUDE.md, research/02-ranking.md, research/03-viability/football-over-under/costs-constraints.md (including the orchestrator addendum), research/00-verify/input-claims.md, docs/brief.md.

DEV = https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages

## Summary of calls

| Strategy | Call | Main reason |
|---|---|---|
| A. Passive quoting / market making on O/U 2.5 | no-go | No queue or volume view on the delayed key; about 1% tick capture likely lost to adverse selection |
| A2. Passive entry for model bets | supporting tactic only | About 0 to +0.5% per bet |
| B. Cross-market consistency (O/U vs Correct Score vs Match Odds) | no-go | One-tick spread across seven legs costs about 2.5pp, above any plausible gap |
| C. Bookmaker vs exchange back/lay arbitrage | no-go (systematic) | Bookmaker must be 1% to 2.7% above exchange lay; account restriction ends the stream |
| D. In-play reaction | no-go | Free-key prices 1 to 180 s late |
| E. Order flow and ladder signals | no-go | Weak signal with 3 levels, no volume; hurdle 1.5% to 3.5% |
| F. Sharp-book reference | needs-more-data | Gap size unmeasured |

## Access note

Betfair consumer sites are behind a Cloudflare challenge and I did not bypass it. Spread and liquidity facts come from WebSearch summaries of blogs, not fetched pages, so they are [inferred]. I found no official O/U spread or volume figures [unknown].

## Constants used

| Item | Value | Tag |
|---|---|---|
| Bankroll, drawdown, time, data budget | EUR 500, EUR 150, 5 h/week, EUR 0 | [verified: docs/brief.md] |
| Delayed key | Can bet on the live exchange. 3 price levels. No total matched by selection. Prices 1 to 180 s late. Stream API with 2 connections and 200 markets. | [verified: DEV/2687105/Application+Keys] |
| Delayed key intended use | "development purposes and any functional testing". Enforcement unknown. | [verified: DEV/2687105/Application+Keys] for the wording, [unknown] for enforcement |
| Live key | GBP 499, out of budget | [verified: DEV/2687105/Application+Keys] |
| Min bet | EUR 1 | [verified: DEV/2686993/Additional+Information] |
| Tick ladder | 1.01 to 2: 0.01. 2 to 3: 0.02. 3 to 4: 0.05. 4 to 6: 0.1. 6 to 10: 0.2. 10 to 20: 0.5. | [verified: DEV/2686993/Additional+Information] |
| Commission | 2% or 5% planning range. Account rate is readable via marketBaseRate. | [inferred] for the rates, [verified: DEV/2687465/Betting+Type+Definitions] for the field |
| Passive in-play orders that cannot match immediately skip the bet delay. Football dynamic events have no delay at half time. | | [verified: DEV/2687396/Exchange+Stream+API] |
| Market data cap | sum(weight) x market IDs at most 200 points per request | [verified: DEV/2687478/Market+Data+Request+Limits] |
| O/U 2.5 is the most heavily traded totals line. Liquidity falls away from 2.5. Lower leagues and friendlies are too thin to scalp. | | [inferred] from blog summaries (https://betfairsquare.pages.dev/sports/football-over-under-goals) |
| Typical pre-match PL prices, Over 2.5 about 1.85 to 2.05 and Under 2.5 about 1.85 to 2.10 | | [inferred] same blogs |
| API gives no market-level matched volume for Totals | | [inferred] from a developer feature request in search results |
| Tick spread for O/U 2.5 | | [unknown]. Resolve by logging best back and lay on the delayed key for a few weeks. |

Cost drag at fair odds is c(o-1)/o per unit stake, from the costs file. At evens that is 1.0% at 2% commission and 2.5% at 5%. Commission is charged on net market profit, so a round trip that greens up pays commission only on the small net profit [inferred].

## Strategy A. Passive quoting (market making) on O/U 2.5 pre-play

1. Mechanism. The counterparty is a taker who crosses the spread, usually a recreational bettor or a bot with a time-limited need to trade. You earn the spread when both legs fill. You lose to better-informed traders: team-news traders, bots that follow bookmaker moves, and anyone whose view is fresher than yours [inferred]. MPRA 126351 reports that makers earn more than takers pre-match and early in-play [verified: https://mpra.ub.uni-muenchen.de/126351/]. That is an average over all makers. Sport mix, retail size and net-of-commission result are [unknown].
2. Data and API. The delayed key is enough to place orders [verified]. A queue-position view needs ladder depth beyond 3 levels and traded volume, and the delayed key has neither [verified]. An offline fill test needs Advanced or Pro history, price [unknown]. Cost is EUR 0 for live use and unknown for a real backtest.
3. Latency and automation. The order is passive, so the bet delay does not bite pre-play [inferred]. The problem is your view, which is 1 to 180 s stale [verified]. Quoting needs a current best price to reprice. A bot with a live feed reprices first and your stale quote gets hit. Retail can automate placement but cannot meet the information speed [inferred].
4. Game theory. Competitors are professional makers and bots with live keys and queue priority [inferred]. Entrants thin the spread to the commission-adjusted cost of capital, so the edge decays fast. What protects the spread is that makers carry inventory and news risk. A 3-level, delayed-view quoter has no information advantage and is the one picked off.
5. Edge arithmetic. Illustrative round trip near odds 2.04 (tick 0.02): back S at 2.04, lay at 2.02. Lay stake L = S x 2.04 / 2.02 = 1.0099 S. Locked profit = 1.04 S - 1.0099 S x 1.02 = 0.0099 S, about 1.0% of S. Commission at 5% on the net 0.0099 S is 0.0005 S. Net is about 0.94% of S, about EUR 0.19 on EUR 20 [inferred arithmetic on illustrative prices].
   - Subtract adverse selection. If half of orders fill both legs and the rest leave you exposed to a move of 2 to 5 ticks (about 1% to 2.5% of stake near odds 2), expected value per attempt is about 0.5 x 0.94% + 0.5 x (-1% to -2.5%), which is -0.8% to 0.0%.
   - Stated range: -1.0% to +0.5% per unit of stake per attempt, central estimate slightly negative [inferred].
   - Capacity: 20 to 50 attempts a week at EUR 10 to 20. Even +0.5% gives EUR 1 to 5 a week [inferred].
6. Call: no-go. Main reason: no queue or volume view and a stale price view. Biggest risk: one-legged positions that grind toward the EUR 150 drawdown cap.

A2. Passive entry as a tactic. If an odds model ever finds an edge, resting the back at the offer instead of crossing saves about one tick. At odds 1.95 that is 0.01/1.95 = 0.5% of stake. At 2.04 it is 0.02/2.04 = 1.0%. Filled passive orders are biased toward moves against you, so net saving is about 0% to +0.5% [inferred]. It supports a model and is not a strategy.

## Strategy B. Cross-market consistency (O/U vs Correct Score vs Match Odds)

1. Mechanism. One goal distribution prices several markets. Under 2.5 is exactly the union of six Correct Score outcomes: 0-0, 1-0, 0-1, 1-1, 2-0, 0-2 [inferred, by definition]. If the six scores can be backed in total above fair against a lay on Under 2.5, or the reverse, the partition locks a profit. The other side is thin Correct Score liquidity. Match Odds is not a partition of O/U, so it cannot lock a profit with O/U. It only informs a consistency check through a goal-distribution model [inferred]. Betfair matches across selections within one market. I found no evidence of cross-matching between separate markets [unknown].
   - Related-line check: Over 1.5 plus Under 2.5 is a middle, not an arbitrage. Locking needs 1/o1 + 1/o2 at most 1. At fair prices the sum is about 1 + P(exactly 2 goals), about 1.27 [inferred].
2. Data and API. Seven legs need seven books streamed together. That fits the 200 market stream cap [verified] and the 200 point request cap with EX_BEST_OFFERS weight 5 at about 40 markets a call [inferred arithmetic]. Cost EUR 0. Correct Score depth is [unknown].
3. Latency and automation. The legs must be placed together, and one failing leaves unbalanced exposure. Stale prices of 1 to 180 s [verified] mean a seen gap is mostly a stale-quote artifact. A fill-or-kill basket can be automated but false positives would be high [inferred].
4. Game theory. Arbitrage bots on the exchange compete for the same gaps [inferred]. Gaps close in seconds. Wide Correct Score spreads protect any residual gap, because they make the locked profit negative most of the time.
5. Edge arithmetic. One-tick implied-probability width of a leg is t/o^2. Illustrative prices: 0-0 at 12.5 (tick 0.5) gives 0.32pp, 1-0 at 9 (0.2) gives 0.25pp, 0-1 at 11 (0.5) gives 0.41pp, 1-1 at 6.5 (0.2) gives 0.47pp, 2-0 at 11 (0.5) gives 0.41pp, 0-2 at 18 (0.5) gives 0.15pp. Sum is 2.0pp. The Under 2.5 leg at 2.0 adds 0.02/4 = 0.5pp. A one-tick spread across all legs costs about 2.5pp of the partition's probability mass before commission, so a gap must exceed that to profit. Range per unit of partition notional: -3.0% to 0.0%, central about -1.5% [inferred].
6. Call: no-go. Main reason: spread cost across six thin legs exceeds any plausible mispricing. Biggest risk: spurious signals from stale prices. The cross-market structure is still useful as an input to the odds model (a goals distribution fitted to O/U 1.5, 2.5, 3.5, Match Odds and Correct Score). That belongs to the odds-model assessment.

## Strategy C. Bookmaker vs exchange back/lay arbitrage

1. Mechanism. The counterparty is a bookmaker with a slow or promotional price. You back at the bookmaker and lay on Betfair. The bookmaker price must beat the exchange lay price by the commission-adjusted gap. Bookmaker two-way margins on O/U 2.5 are typically larger than exchange margins [inferred], so gaps come from slow repricing, enhanced-odds offers and errors.
2. Data and API. Exchange side: delayed key, free. Bookmaker side: The Odds API Starter gives 500 credits a month free [verified: https://the-odds-api.com/, as summarized in search]. Each call for a sport, market and region costs a credit, and historical calls cost more [inferred from third-party reviews]. 500 credits supports a few hundred snapshots a month, not continuous monitoring [inferred]. Pinnacle direct access for retail is [unknown]. Each bookmaker account needs a funded balance out of the EUR 500.
3. Latency and automation. You see exchange prices late, but your lay order goes to the live exchange. The risk is the price has moved so the lay does not fill at your limit. Place the exchange leg first as fill-or-kill, then the bookmaker leg. Bookmaker delays and rejections of the second leg leave you exposed [inferred]. Retail can do this semi-manually at low frequency only.
4. Game theory. Dedicated arbers and bots with bookmaker feeds compete. Gaps last seconds to minutes [inferred]. Bookmakers restrict accounts that take arbs or only price errors [inferred], and I found no official statement either way. The scarce resource is accounts, not speed. Each restriction ends that bookmaker's use.
5. Edge arithmetic. For bookmaker odds ob, exchange lay odds ol and commission c, the equal-profit lay stake is L = S x ob / (ol - c). Profit per unit of S is L(1-c) - S. Break-even ob = (ol - c)/(1 - c).
   - At ol = 2.06 and c = 5%: break-even ob = 2.01/0.95 = 2.116. At c = 2%: 2.04/0.98 = 2.082.
   - Example at c = 2%, ob = 2.15: L = 2.15/2.04 = 1.0539 S. Profit = 1.0539 x 0.98 - 1 = +3.3% of S.
   - Example at c = 5%, ob = 2.10: L = 2.10/2.01 = 1.0448 S. Profit = 1.0448 x 0.95 - 1 = -0.75% of S.
   - So the bookmaker must be 1% to 2.7% above the exchange lay to break even, and typical bookmaker margin works against it [inferred].
   - Range per unit of stake on a qualifying opportunity: +0.5% to +3%. Opportunity frequency is [unknown]. At EUR 100 a leg and 1 to 3 opportunities a week, that is about EUR 0.5 to 9 a week before restrictions [inferred].
6. Call: no-go as a systematic strategy. Main reason: break-even needs an unusually generous bookmaker price and account restriction ends the stream. Biggest risk: account restriction and one-legged fills.

## Strategy D. In-play reaction

1. Mechanism. After a goal or red card, O/U prices jump. The Reading paper finds mispricing grows after surprise late goals by longshots [verified: https://research.reading.ac.uk/football-research/new-journal-article-informational-efficiency-and-behaviour-within-in-play-prediction-markets/]. MPRA 126351 finds late in-play longshot bets lose even for makers [verified: https://mpra.ub.uni-muenchen.de/126351/]. They may agree or conflict, which is [inferred] and untested. The counterparty is a trader who is slow to reprice after the event.
2. Data and API. A live key costs GBP 499 [verified]. A real test needs Advanced or Pro data with goal timestamps, price [unknown]. A free live score feed is [unknown].
3. Latency and automation. Free-key prices are 1 to 180 s late [verified], so you may read a pre-goal price after the market has moved, and you cannot tell how stale a given snapshot is. The in-play bet delay for football is [unknown] as a number. Passive orders that cannot match immediately skip it [verified]. Football dynamic events have no delay at half time [verified]. Half-time trading is a narrow slow window and the stale view still applies. Retail cannot meet the speed needs on the free key.
4. Game theory. Bots with direct feeds react within seconds [inferred]. A retail entrant competes on information speed and loses. The papers' edge is a behavioural bias in slow money, not a speed edge, and I found no evidence it survives retail size and commission.
5. Edge arithmetic. Not computable. The Reading 50% ROI figure is [unknown]. Commission drag of 2.5% at 5% at evens is small next to an unmeasurable stale-price loss. Range [unknown], treated as -5% to +2% per unit of stake.
6. Call: no-go. Main reason: stale prices up to 180 s on the free key. Biggest risk: trading on prices that have already moved.

## Strategy E. Order flow and price ladder signals

1. Mechanism. Back/lay size imbalance at the top levels may predict the next tick or drift to the close. The counterparty is the passive side that does not update.
2. Data and API. The delayed key shows 3 levels and no total matched [verified]. Imbalance can be computed from best-offer sizes, but traded volume cannot. A real test would need paid Advanced or Pro files, price [unknown].
3. Latency and automation. Signals at tick horizon are lost inside a 1 to 180 s stale view [verified]. Only slow signals (hours to the close) are possible. Capture is easy to automate.
4. Game theory. Professional traders and bots use full-depth data and trade these signals, so they decay quickly [inferred]. Nothing known protects a 3-level signal.
5. Edge arithmetic. Acting on a signal costs about one tick crossed (0.5% to 1.0% at odds near 2, [inferred] from the ladder) plus commission drag of 1.0% to 2.5% at evens (costs file). The hurdle is about 1.5% to 3.5% of stake. A slow signal worth a tick or two of move gives 0.5% to 1.0% before costs. Range per unit of stake: -3% to 0%, optimistic upper bound +0.5% [inferred].
6. Call: no-go. Main reason: the signal is weak and the hurdle is higher. Biggest risk: a spurious backtest from a few weeks of forward capture. Free forward capture of 3-level books is allowed and can be run for the odds-model work.

## Strategy F. Sharp-book reference (devigged Pinnacle or consensus vs exchange)

1. Mechanism. Take exchange prices that exceed a devigged sharp-bookmaker price. The other side is the exchange trader quoting late or stale relative to the sharp line. Input claims on Pinnacle yield (11) and power devig (12) are [unknown], single anecdotes.
2. Data and API. Bookmaker prices from The Odds API free tier [verified: https://the-odds-api.com/], 500 credits a month. Pinnacle direct access [unknown]. Exchange side via the delayed key [verified].
3. Latency and automation. Pre-play and slow. The stale exchange view matters less for a bet placed hours before kick-off, as the costs file notes. The 500 credit cap limits how often the sharp line can be refreshed [inferred].
4. Game theory. Exchange traders already reference Pinnacle [inferred], so the gap is small and shrinks as more follow. This is the same edge as an odds model benchmarked to the close.
5. Edge arithmetic. Break-even is 1.0% at 2% commission and 2.5% at 5% at evens (costs file). If the average gap between exchange and devigged sharp price is 0 to 1.5% of stake, net range is -2.5% to +0.5% [inferred]. Gap size is [unknown].
6. Call: needs-more-data. Main reason: gap size is unmeasured. Resolve by logging exchange and free-tier bookmaker prices for a few weeks. Biggest risk: the credit cap limits the sample and the edge is below commission.

## Open items

| Item | What would resolve it |
|---|---|
| O/U 2.5 tick spread and displayed depth | Log best back and lay on the delayed key for a few weeks |
| Commission rate for this account | Read marketBaseRate via the delayed key |
| Whether Betfair restricts winning accounts | A person reads the terms pages (claim 8 is [unknown]) |
| Correct Score depth and cross-market matching | Log Correct Score books alongside O/U |
| Pinnacle access in Ireland | A person checks Pinnacle terms |
| Whether a sustained live strategy on the delayed key is allowed | Betfair terms. The key is described as for development and testing [verified]. |

## Sources

- https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages/2687105/Application+Keys
- https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages/2686993/Additional+Information
- https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages/2687396/Exchange+Stream+API
- https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages/2687478/Market+Data+Request+Limits
- https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages/2687465/Betting+Type+Definitions
- https://mpra.ub.uni-muenchen.de/126351/
- https://research.reading.ac.uk/football-research/new-journal-article-informational-efficiency-and-behaviour-within-in-play-prediction-markets/
- https://the-odds-api.com/
- https://betfairsquare.pages.dev/sports/football-over-under-goals

## Addendum: Historical Data Feed Specification (SPEC, see research/00-verify/input-claims.md Addendum 2)

Calls unchanged.

| Item | Value | Tag |
|---|---|---|
| History data start | May 2015. JSON in tar.bz2. | [verified: SPEC p1] |
| BASIC | 1-minute intervals. Last traded price per runner plus marketDefinition changes. No traded volume, no back/lay ladder. | [verified: SPEC p3-4] |
| ADVANCED | 1-second intervals. Best offers (top levels), traded volume by market and runner, traded price-volume. | [verified: SPEC p3-4] |
| PRO | Tick by tick. Full ladder, traded volume, BSP near/far. | [verified: SPEC p3-4] |
| marketDefinition in every plan | marketType, marketBaseRate, crossMatching, betDelay, inPlay, status, runner status (WINNER/LOSER). | [verified: SPEC p1-2] |
| O/U in Basic coverage; Advanced and Pro prices | | [unknown]. Resolve by downloading one free Basic soccer month. |

- A and E: queue simulation needs Pro [inferred from SPEC]. Fill rates for resting orders only come from own logged orders [inferred].
- B: the crossMatching flag is recorded per market [verified: SPEC p1-2], not proof of matching between separate markets [unknown]. Basic ltp allows a coarse free consistency check, but not spreads, which are the binding cost [inferred].
- D: actual football in-play betDelay can be read from history [inferred from SPEC]. No-go stands because of the free-key price lag.
- F: Basic gives the close benchmark (last 1-minute ltp), results and marketBaseRate free [verified: SPEC p1-4]. Sharp-book prices still need an outside source.
- Commission rate can be read from history marketBaseRate as well as the live API field [verified: SPEC p1-2].

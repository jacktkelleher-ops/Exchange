# Market structure assessment: pre-play passive resting orders (maker side)

Date: 2026-11-15
Agent: market-structure-assessor
Scope: football Match Odds and UK/Irish horse racing Win, pre-play, orders rested through the free delayed API key.
Inputs read: CLAUDE.md, research/02-ranking.md, research/00-verify/input-claims.md (including Addendum 2, the official data spec), docs/brief.md, costs-constraints.md (including the orchestrator addendum, which overrides conflicting tags).
DEV = https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages
SPEC = docs/inputs/official/Betfair-Historical-Data-Feed-Specification.pdf (user-supplied official PDF)

## Access note

- mpra.ub.uni-muenchen.de and www.karlwhelan.com did not resolve in this session (not on the network allow list). I could not read the paper body. Paper facts come from the verification file and a search result summary only.
- Betfair consumer sites are behind a Cloudflare challenge and were not touched. Queue rules, commission and account limits are therefore `[inferred]` or `[unknown]`.

## Result in brief

| # | Strategy | Call | Main reason | Biggest risk |
|---|---|---|---|---|
| 1 | Single-sided resting order held to settlement (collect the "maker premium") | no-go | Commission on a directional bet costs about 1.0% to 2.5% of stake at even odds, more than the half-spread a maker earns (about 0.5%). | The paper's premium may be a relative gain over takers, not a positive absolute return. |
| 2 | Two-sided passive scalping or quoting, football Match Odds | no-go | A retail quoter with a 1 to 180 s stale view is the marginal maker. Break-even completion is 50.5% to 51.3% at a one tick stop and is unlikely to be met. | Completion rate is unmeasurable without own logs, and bots hold queue front. |
| 3 | Two-sided passive scalping, UK/Irish racing Win | no-go | Racing prices move fastest in the last minutes, which sit inside the feed delay. No volume or queue data. | Stale view during the busiest period. The paper does not cover racing. |
| 4 | Passive entry as an execution overlay for a model | needs-more-data | Saves up to half a spread when filled, but non-fills are selected against you. Measurable only from own logs and only useful if an odds model exists. | Fill selection erases the saved spread. |
| 5 | Wide "stink bid" resting orders far from the touch in thin books | needs-more-data (low priority) | No evidence either way. Costs almost nothing to log. | Being hit by informed or erroneous flow with no way to see why. |

Overall: build nothing. One bounded measurement (section 9) can answer the open questions for under EUR 30 at risk. Whether it is worth the hours is the orchestrator's call.

## Facts used by all strategies

| Fact | Tag |
|---|---|
| The delayed key can place bets on the live exchange, shows prices 1 to 180 s late, 3 levels, no total matched by selection, has the Stream API (2 connections, 200 markets). | `[verified: DEV/2687105/Application+Keys]` |
| Betfair says the delayed key "should be used for development purposes and any functional testing". Sustained live use may breach intended use. Enforcement unknown. | wording `[verified: DEV/2687105/Application+Keys]`, enforcement `[unknown]` |
| Live key costs GBP 499, about EUR 590. Outside the EUR 0 budget and larger than the bankroll. | `[verified: DEV/2687105/Application+Keys]`, FX `[inferred]` |
| Minimum bet EUR 1. Ladder: 1.01 to 2 step 0.01, 2 to 3 step 0.02, 3 to 4 step 0.05, 4 to 6 step 0.1, 6 to 10 step 0.2, 10 to 20 step 0.5. | `[verified: DEV/2686993/Additional+Information]` |
| Transaction charges apply to both key types. Counting of place, cancel and modify is from secondary text. Threshold and market-making exemption unknown (1,000 vs 5,000 per hour in conflicting sources). | applies `[verified: DEV/2687105/Application+Keys]`, counting `[inferred]`, threshold `[unknown]` |
| Commission is charged on net market winnings. Irish account rate is 2% or 5% by source. Both modelled. | `[inferred]`, rate `[unknown]` |
| Passive in-play orders that cannot match immediately skip the bet delay. LAPSE cancels at the turn in-play. | skip `[verified: DEV/2687396/Exchange+Stream+API]`, LAPSE `[inferred]` |
| Brief: former Betfair liquidity analyst, comfortable with order logs, EUR 500 bankroll, EUR 150 drawdown limit, 5 h/week, EUR 0 data budget. | `[verified: docs/brief.md]` |
| MPRA 126351 (Whelan): pre-match and early in-play makers earn more than takers. Late in-play longshot bets lose heavily even for liquidity providers, and takers on favourites profit. | `[verified: https://mpra.ub.uni-muenchen.de/126351/]` |
| The paper uses Betfair transaction-level soccer data and models makers as compensated for waiting and non-execution risk. It does not cover racing. | `[inferred]` from a search summary (https://ideas.repec.org/p/pra/mprapa/126351.html), body not read |
| Whether the paper's returns are net of commission, the premium size, stake sizes and sample. | `[unknown]`. Resolve by reading the paper once the host is allowed. |

## Data tiers (official spec)

| Tier | Content | Tag |
|---|---|---|
| Basic | 1-minute last traded price and marketDefinition changes only. No volume, no ladder, no traded-at-price. Runner bsp, marketBaseRate, betDelay, inPlay and runner result status are in every plan. | `[verified: SPEC p1-4]` |
| Advanced | 1-second best back and lay (top levels), traded volume, traded-at-price | `[verified: SPEC p3-4]` |
| Pro | Tick by tick full ladder, BSP near and far | `[verified: SPEC p3-4]` |

Consequences:

- Queue simulation needs Pro, because Advanced shows only top levels at 1 second. Prices of Advanced and Pro are `[unknown]`. Fill rate and queue effects must come from own logged orders. `[inferred]` from SPEC.
- Free Basic gives a closing benchmark with no outside source: last 1-minute ltp before the off, runner bsp for racing, and the settled result. This supports the mark-out versus close metric in section 9 without data spend, once coverage of football Match Odds and racing Win in Basic is confirmed (`[unknown]`). `[inferred]` from SPEC.
- marketBaseRate in marketDefinition lets you read the commission rate applied per market from free history. That narrows the 2% versus 5% question once a file is downloaded. Field `[verified: SPEC p1-2]`. The Irish account's own rate stays `[unknown]` until read.
- Basic cannot show spread or depth, so historical half-spread (the maker gain in strategies 1 to 3) cannot be measured free. Only own logs, Advanced or Pro can. `[inferred]` from SPEC.
- The 1-minute close can be up to 60 s before the off, so mark-out against it misses late drift. Racing bsp avoids this. `[inferred]`

## Cross-cutting answers to the key questions

### Can a retail maker with stale prices avoid being picked off?

Mostly no, with partial mitigations.

- Mechanism. Your order rests on the live book. Your view is 1 to 180 s old `[verified: DEV/2687105/Application+Keys]`. When live information arrives (team news, bookmaker moves, sharp flow), informed takers hit orders priced off the old view first. You are filled because you are stale `[inferred]`.
- The cancel decision uses the same stale feed. Bots that see the live book cancel first `[inferred]`.
- Whether order status (listCurrentOrders, order stream) is delayed on a delayed key is `[unknown]`. Test in section 9.
- Mitigations that need no speed `[inferred]`: rest orders where price is slow-moving (football Match Odds many hours before kick-off, away from team-news windows); price from a fixed rule such as delayed mid faded by two or more ticks; use short lifetimes and LAPSE; in racing, avoid the last roughly 30 minutes because 180 s covers the period of most price discovery.
- Cost of mitigations: fill rates drop and fills skew to news events `[inferred]`.

### Queue position at EUR 1 to 10 stakes

- Matching is price then time `[inferred]`. Stake size does not move you up the queue. A small order fills only if flow reaches its place `[inferred]`.
- You cannot see your place. The delayed key shows 3 levels, no total matched `[verified: DEV/2687105/Application+Keys]`, and sizes are 1 to 180 s old.
- Bots hold the front by cancel and replace. Each replace is also a counted transaction `[inferred]`.
- Result: you sit behind the visible size and fill late, typically when price trades through, which is when it moves against you `[inferred]`.

### Competition from professional bots

- Football Match Odds and racing Win are the deepest markets in their families per the ranker `[inferred]`. Market makers and scalpers with live feeds are the natural occupants of the touch `[inferred]`. No official count exists in my sources `[unknown]`.
- A delayed-key quoter is the slowest quoter in the book by construction `[verified: DEV/2687105/Application+Keys]`.

### Does the MPRA maker premium survive commission at retail size?

Not demonstrable, and the arithmetic says probably not for directional positions.

- A maker premium is a gap between makers and takers. A positive gap does not make maker returns positive after commission. `[inferred]`
- At p = 0.5, b = 2.0, expected commission is c x p x (b - 1) = 1.0% at 2% and 2.5% at 5% per unit stake. `[inferred]` arithmetic.
- Resting one tick better than mid at 2.0 gains about half of the 0.02 tick, EV = 0.5 x 2.01 - 1 = +0.5%. `[inferred]` arithmetic.
- So +0.5% is smaller than the 1.0% to 2.5% commission drag before adverse selection. The premium is a waiting-risk premium `[inferred]`, not a free edge. Whether the paper nets commission is `[unknown]`.

## Strategy 1. Single-sided resting order held to settlement

1. Mechanism. Post a back or lay one tick better than the touch and hold the fill to the result. The counterparty is a taker paying for immediacy `[inferred]`. You win from takers who value speed and lose to takers who know more than you.
2. Data and API. Delayed key, EUR 0 `[verified: DEV/2687105/Application+Keys]`. Risk: sustained use of a development key, enforcement `[unknown]`.
3. Latency and automation. A small scheduler is enough. The problem is the stale view, not automation.
4. Game theory. Competitors are market-making bots, scalpers and other makers `[inferred]`. A quoter improving by a tick takes the queue front, so the half-spread is competed to the cost of capital and technology `[inferred]`. The premium persists as compensation for non-execution risk and disagreement `[inferred]`, but not for a participant that is systematically adversely selected.
5. Edge at mid 2.00, quoting one tick better:

| Component | Low case | High case | Arithmetic |
|---|---|---|---|
| Half-spread gain | +0.25% | +0.5% | half of a 1% tick |
| Commission drag at 2% | -1.0% | -1.0% | 0.02 x 0.5 x 1.01 |
| Commission drag at 5% | -2.5% | -2.5% | 0.05 x 0.5 x 1.01 |
| Adverse selection on fills | -1.0% | 0% | `[unknown]`, assumed range |
| Net at 2% | -1.75% | -0.5% | |
| Net at 5% | -3.25% | -2.0% | |

Range about -3.3% to -0.5% per unit filled. It is positive only if the bet itself carries a true edge of 0.5% to 3%, which would be a model edge.

6. Call: no-go. Main reason: commission on directional exposure exceeds the half-spread. Biggest risk to the call: the paper may show makers positive after commission through fill selection that my arithmetic omits. Resolved only by reading the paper.

## Strategy 2. Two-sided passive scalping, football Match Odds

1. Mechanism. Post a back at a higher price and a lay one tick lower. If both fill, the profit is locked either way and commission applies only to net market profit. Counterparties are impatient takers `[inferred]`. You lose when one leg fills and the price moves away.
2. Data and API. Same key. A real test needs volume and depth, absent from the free key `[verified: DEV/2687105/Application+Keys]` and from Basic `[verified: SPEC p3-4]`. Queue simulation needs Pro `[verified: SPEC p3-4]`, price `[unknown]`.
3. Latency and automation. Competitive quoting needs continuous re-quoting, each replace a counted transaction (threshold `[unknown]`). It cannot be met on a 1 to 180 s view `[verified: DEV/2687105/Application+Keys]`. The live key is GBP 499 `[verified]`.
4. Game theory. Competitors are scalping bots and market makers `[inferred]`. The edge per round trip is capped at one tick, so the contest is for fill share, which goes to the fastest `[inferred]`. Entrants lengthen queues and cut completion for everyone behind `[inferred]`.
5. Edge. Per completed trip at 2.0: gross 1.00%, net 0.98% at 2% and 0.95% at 5% `[inferred]` arithmetic on the verified ladder. Break-even completion with a one tick stop is 50.51% at 2% and 51.28% at 5%. With a two tick stop it is 66.4% and 67.2%.

| Completion q | One tick stop | Two tick stop |
|---|---|---|
| 0.30 | 0.294 - 0.70 = -0.41% | 0.294 - 1.40 = -1.11% |
| 0.50 | 0.49 - 0.50 = -0.01% | 0.49 - 1.00 = -0.51% |
| 0.60 | 0.588 - 0.40 = +0.19% | 0.588 - 0.80 = -0.21% |

q is `[unknown]`. I judge 30% to 50% likelier than 60% for a stale, late-queue quoter `[inferred]`. Range about -1.1% to +0.2% per attempt, centre near -0.4%. At EUR 10 stake, +0.2% is 2 cents per attempt, about EUR 2 a week at 100 attempts. `[inferred]` arithmetic.

6. Call: no-go. Main reason: edge capped at one tick, break-even completion unlikely for a stale late-queue quoter, tiny absolute euros. Biggest risk: completion above 60% in quiet early periods, testable only with own logs.

## Strategy 3. Two-sided passive scalping, UK/Irish racing Win

1. Mechanism. As strategy 2, against other racing traders and punters pre-off.
2. Data and API. As strategy 2. The delayed key has no BSP near or far price `[verified: DEV/2687105/Application+Keys]`. Basic carries runner bsp, useful only as a benchmark `[verified: SPEC p1-2]`.
3. Latency. Racing prices move fastest in the last minutes `[inferred]`, inside a delay of up to 180 s `[verified]`. Handling of resting orders at non-runner withdrawal is `[unknown]`.
4. Game theory. Scalpers, bots and informed late money `[inferred]`. Informed money arriving late makes makers adversely selected `[inferred]`. Decay as strategy 2.
5. Edge. At 5.0 the tick is 0.1: gross 2.0%, net 1.96% at 2%, 1.90% at 5% `[inferred]` arithmetic. q likely below football `[inferred]`. Range about -1.5% to +0.2% per attempt.
6. Call: no-go. Main reason: the busy period is inside the feed delay. Biggest risk: no paper evidence for racing at all.

## Strategy 4. Passive entry as an execution overlay for a model

1. Mechanism. Enter a model's bet with a resting limit order instead of crossing the spread. You save up to half a spread when filled `[inferred]`. Non-fills are selected: you get filled when price moves against you.
2. Data and API. Same key, no new cost.
3. Latency. A scheduler placing orders hours before kick-off. Staleness matters less when the model price is fixed `[inferred]`.
4. Game theory. Not a standalone edge. The saving is available to anyone using limit orders, so it is not a source of profit by itself.
5. Edge. Saved half-spread +0.25% to +0.5% when filled `[inferred]`. Adverse selection 0% to -0.5% `[unknown]`, assumed. Missed bets: at a 3% model edge and 40% non-fill, cost 1.2% of intended stake. Net about -1.2% to +0.5% of intended stake.
6. Call: needs-more-data. Main reason: measurable only with a model and own fill logs. Biggest risk: selection erases the saved spread.

## Strategy 5. Wide stink bids in thin pre-play books

1. Mechanism. Rest orders many ticks off the touch in thin books and wait for an impatient or erroneous taker `[inferred]`.
2. Data and API. Delayed key, EUR 0. Thin-market coverage `[unknown]`.
3. Latency. Place and leave. Retail is enough.
4. Game theory. Others use the same tactic and the gap is capped by what a taker will pay. Informed takers sweep stale orders first. No evidence on size or frequency `[unknown]`.
5. Edge. Illustrative only: 5 fills in 100 orders at a 5% concession gives 0.25% per order placed. Commission on directional holding (1.0% to 2.5% at even odds) and informed sweeps would exceed it `[inferred]` arithmetic. Range -2.5% to +0.25% per unit filled, not tied to evidence.
6. Call: needs-more-data (low priority). Main reason: no evidence, near zero logging cost. Biggest risk: fills dominated by informed sweeps.

## Section 9. Measuring fill rate and adverse selection at EUR 1 to 2 stakes

The brief lists placing real bets as out of scope for this review. This is a design for the next phase, to run only if the user approves.

Step zero: place one EUR 1 order on a delayed key and compare the placement timestamp with matchedDate, to see whether order status is delayed `[unknown]`.

Fields per order, all `[inferred]` unless noted: marketId, selectionId, side, price, size, LAPSE, own placed timestamp; betId, placedDate, matchedDate, sizeMatched, avgPriceMatched, sizeRemaining, status from listCurrentOrders or the order stream; delayed mid, spread and size at your price at decision time (delayed data exists `[verified: DEV/2687105/Application+Keys]`); minutes to start; cancel time and reason; close = last 1-minute ltp before the off from free Basic, plus runner bsp for racing (`[verified: SPEC p1-4]` for the fields, coverage `[unknown]`).

Metrics:

1. Fill rate by offset from touch (0, 1, 2, 3 ticks), minutes to start and market type.
2. Time to fill and the share filled in the last 60 minutes.
3. Mark-out versus close. Back fill at b: b / close - 1. Lay fill at l: 1 - l / close. `[inferred]`
4. Selection test: mean mark-out of filled orders against mean mark-out of all posted orders valued at posted price versus close. Filled worse than posted means the difference is adverse selection. `[inferred]`
5. Fills inside a window around a price jump seen in later polling.
6. Scalp pair completion rate with a stop rule fixed in advance.

Sample size `[inferred]` arithmetic:

- Mark-out SD per fill assumed 4% `[unknown]`. Detecting 0.5% at 80% power, 5% significance: n = (2.8 x 4 / 0.5)^2 = about 502 fills.
- Profit and loss at even odds has SD near 1 unit. Detecting 0.5%: n = (2.8 / 0.005)^2 = 313,600 bets. Infeasible, so mark-out versus close is the metric, not profit and loss.
- At a 30% fill rate, 502 fills need about 1,700 orders. At 20 to 40 fills a week that is 13 to 25 weeks. Automation can shorten this.
- Cost: 502 fills at EUR 2 is EUR 1,004 turnover. At -1.0% net, expected cost is about EUR 10. Cap at 15 open orders of EUR 2, so under EUR 30 exposure.

Limits: the delayed mid at decision time is stale, so do not measure improvement versus mid at fill. Use the close only. The 1-minute close lags the off by up to 60 s, so prefer bsp for racing. The test shows whether a premium exists in your own fills, not whether it survives larger size.

## Key unknowns that would change a call

| Unknown | Effect | Resolved by |
|---|---|---|
| Whether MPRA maker returns are net of commission, and the premium size | Could move strategy 1 to needs-more-data | Read the paper (mpra.ub.uni-muenchen.de must be allowed) |
| Irish account commission rate | Shifts strategy 1 by 1.5 points | Read marketBaseRate on a live market, or the charges page |
| Transaction charge threshold and exemption | Could cap re-quoting in strategies 2 and 3 | Charges page |
| Whether order status is delayed on a delayed key | Affects all log-based measurement | One EUR 1 order test |
| Betfair stance on sustained use of a development key | Could end the experiment | Ask Betfair support in writing |
| Winning-account limits | Could cap any edge | Betfair terms `[unknown]` |
| Basic coverage of football Match Odds and racing Win, Advanced and Pro prices | Closing benchmark and any queue simulation | Download one free Basic file, read the plan page |

## Sources

- https://mpra.ub.uni-muenchen.de/126351/ (via the verification file, not fetched here)
- https://ideas.repec.org/p/pra/mprapa/126351.html (search result only)
- DEV/2687105/Application+Keys, DEV/2686993/Additional+Information, DEV/2687396/Exchange+Stream+API (via the verification and costs files)
- SPEC, docs/inputs/official/Betfair-Historical-Data-Feed-Specification.pdf (via Addendum 2 of the verification file)

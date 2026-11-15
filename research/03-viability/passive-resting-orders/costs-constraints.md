# Costs and constraints: pre-play passive resting orders (maker side)

Date: 2026-11-15
Agent: costs-constraints
Scope: football Match Odds and UK/Irish horse racing Win, pre-play, orders rested through the free delayed API key. Brief: Irish account, EUR 500 bankroll, 30% max drawdown (EUR 150), 5 h/week, EUR 0 data budget.
Not tax advice.

## Access note for this session

- betfair-developer-docs.atlassian.net, docs.developer.betfair.com, www.revenue.ie, revenue.ie and betfair-datascientists.github.io did not resolve in this session (DNS failure, not a Cloudflare challenge). These hosts must be allowed in the session network settings before they can be fetched. Bash was also not available, so curl could not be used.
- support.betfair.com, www.betfair.com, historicdata.betfair.com were not retried. The earlier session found them behind a Cloudflare challenge.
- Result: nothing new was fetched from an official page in this session. Items marked `[verified]` below are carried over from `research/00-verify/input-claims.md`, which recorded the URL when it fetched them. New items come from WebSearch result summaries only, including snippets of official dev-doc pages. Those are tagged `[inferred]` and name the page, because the page body was not read here.
- DEV = https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages

## Conflict a human must resolve first

A search summary of dev-doc snippets said the delayed key "does not allow betting transactions (placeOrders, replaceOrders, updateOrders, cancelOrders)" and quoted a GBP 299 live fee and a 1 to 60 second delay. That wording matches an older page version. The earlier session read the Application Keys page dated 2026-11-02 and recorded: live fee GBP 499, delayed key can place bets, delay 1 to 180 seconds `[verified: DEV/2687105/Application+Keys]`. I keep the earlier reading but this strategy depends on it completely. Action: a person opens DEV/2687105/Application+Keys and confirms "bet placement" for the delayed key. If delayed keys cannot place bets, this strategy needs the GBP 499 live key and fails the budget. Test cheaply by calling placeOrders with a EUR 2 order on a delayed key.

## 1. Commission

| Item | Finding | Tag |
|---|---|---|
| Rate for Irish account | Basic 2%, Rewards 5%, Rewards+ 8%, switchable monthly (input claim) | `[inferred]` (secondary sources only) |
| Alternative figure | Sporting Life says UK and Irish customers on the standard Rewards package pay at most 5% on net winnings | `[inferred]` https://www.sportinglife.com/free-bets/guides/betfair-exchange-education/how-does-commission-work (search summary only) |
| Per-market rate | API exposes `marketBaseRate` and `discountAllowed` per market, so the live rate can be read once an account exists | `[verified: DEV/2687465/Betting+Type+Definitions]` |
| Calculation | Commission is charged on net winnings in a market, not per bet. A market with a net loss pays none. Betfair offsets any transaction charge against commission | `[inferred]` (general description in search summary of the Betfair commission page, not read) |
| Discounts | Reward tier discounts exist per the input claim. Exact table and how tier is earned | `[unknown]` |

How to resolve: a person opens the Betfair Ireland charges page and the account's My Betfair Rewards page, or reads `marketBaseRate` for a football and a racing market via the delayed key. Racing Win base rate reported as 2% by the input and "up to 5%" by Timeform, unresolved.

Planning rule: model both 2% and 5%.

## 2. Additional charge on profitable accounts

| Item | Finding | Tag |
|---|---|---|
| Premium Charge | Replaced by the Expert Fee from 6 Jan 2025 (Racing Post) | `[inferred]` https://www.racingpost.com/news/britain/betfair-exchange-to-introduce-new-commission-system-for-2025-as-premium-charge-is-dropped-a7wbg0v4GCAJ (search summary only) |
| Expert Fee tiers | 0% below 25k, 20% for 25k to 100k, 40% above 100k, rolling 52 weeks (input and Racing Post) | `[inferred]` |
| Conflict | Another page describes a threshold of GBP 25,000 lifetime profit across 100 or more settled markets. Older pages describe the old Premium Charge at GBP 250,000 lifetime | `[inferred]`, conflicting, low quality |
| Binding at this bankroll | No under any version. A EUR 500 bankroll cannot plausibly reach a 25k gross profit threshold for years | `[inferred]` |

Resolve: person reads the official Expert Fee page. Not decision relevant for this strategy.

## 3. API access

| Item | Finding | Tag |
|---|---|---|
| Delayed key fee | None | `[verified: DEV/2687105/Application+Keys]` |
| Live key fee | GBP 499, debited after activation, KYC needed. Roughly EUR 590 at an assumed rate | `[verified: DEV/2687105/Application+Keys]`, rate `[inferred]` |
| Delayed key capabilities | Bet placement on live exchange, Stream API (2 connections, 200 markets), 3 price levels, no total matched by selection, no BSP near/far price | `[verified: DEV/2687105/Application+Keys]` (see conflict above) |
| Data delay | Prices delayed 1 to 180 seconds, variable | `[verified: DEV/2687105/Application+Keys]`. An older page said 1 to 60, `[inferred]` |
| Is order placement delayed on delayed key | Not stated anywhere read. Bets go to the live exchange per the verified page. Delay applies to data | `[unknown]` for any placement latency difference. Resolve with a paper test logging placement timestamp against matched time |
| Matching difference, delayed key vs live key | No source says orders are matched differently. Matching is by the exchange engine regardless of key | `[inferred]`. Resolve by reading Application Keys page text for any wording on order handling |
| Transaction charges apply to both key types | Yes, with terms linked at www.betfair.com/aboutUs/Betfair.Charges/#TranCharges2 | `[verified: DEV/2687105/Application+Keys]`, `[verified: DEV/2687730/Best+Practice+Guide]` |
| Transaction charge: what counts | Any bet placed, cancelled or modified, plus failed transactions that return an API error. Related accounts and API subscriptions are treated as one customer. Charge is offset against commission. Betfair contacts customers when it is payable | `[inferred]` (search summary of the Betfair commission text and the Best Practice page https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages/2687730/Best+Practice) |
| Transaction charge: threshold and rate | 5,000 per hour (most secondary sources) vs 1,000 per hour (older paper). Market-making exemption sizes not found | `[unknown]`. A person must read the Charges page |
| Market data request limits | Applies to listMarketBook with price or order projections. Sum of weights times number of market ids must not exceed 200 points. Example weights: EX_BEST_OFFERS 5, EX_ALL_OFFERS and EX_TRADED 17 each, market description 1, runner metadata 1, no projection 2. Exceeding returns TOO_MUCH_DATA | `[inferred]` (search summary of https://betfair-developer-docs.atlassian.net/wiki/x/9gEp, one older page showed 150 points) |
| Other request limits | listMarketBook at most 5 requests per second to one marketId. listMarketBook with order or match projection limited to 3 concurrent requests | `[inferred]` same source |
| Order operation rate limits (placeOrders, cancelOrders) | Not found. Best Practice says make the minimal number of transactions | `[unknown]`. Resolve by reading the Best Practice and Betting Exceptions pages (DEV/2687730) |
| Stream API for resting orders | Delayed key allows 2 connections and 200 markets. Stream data is delayed like the rest | `[verified: DEV/2687105/Application+Keys]` |

Implication for resting orders: placing, cancelling and replacing (replace counts as modify) all count as transactions. A strategy that repeatedly cancels and re-quotes to stay at the front of the queue burns transactions. A pre-play strategy that places an order and leaves it should stay far below any plausible threshold `[inferred]`.

## 4. Persistence types, pre-play

| Type | Meaning | Tag |
|---|---|---|
| LAPSE | Unmatched order cancels when the market turns in-play | `[inferred]` search summary of dev docs Betting Enums (page x/8Dgp or x/cDgp, not read) and NautilusTrader docs |
| PERSIST | Unmatched order carries into in-play | `[inferred]` same |
| MARKET_ON_CLOSE | Unmatched order goes to BSP auction at turn in-play, only valid where BSP exists | `[inferred]` same. INVALID_PERSISTENCE_TYPE is returned if the type is invalid for a market |

For pre-play only work use LAPSE, so an order cannot be left exposed in-play. Passive in-play orders that cannot match immediately skip the bet delay `[verified: DEV/2687396/Exchange+Stream+API]`. That is a reason not to use PERSIST carelessly. Which markets turn in-play and when (kickoff vs actual start, racing off) uses market `inPlay` flags and market start time, details `[unknown]`.

## 5. Historical data

| Product | Detail | Tag |
|---|---|---|
| Basic | Free. Last traded price at 1 minute intervals, no volume | `[inferred]` https://betfair-datascientists.github.io/modelling/dataSources and https://betfair-datascientists.github.io/data/usingHistoricDataSite (search summaries) |
| Advanced | Best prices and volume at 1 second intervals, paid | `[inferred]` same |
| Pro | Odds and volume at 50 millisecond intervals, paid | `[inferred]` same |
| Format | Recordings of the Stream API, delivered as tar files, read with betfairlightweight | `[inferred]` community tutorials |
| Prices | Input says Advanced 69 and Pro 230. Tennis scanner says GBP 499 and 1,499 per year. Another says 39 and 99 | `[unknown]`, conflicting. A person must read historicdata.betfair.com |
| Coverage of football Match Odds and racing Win | Not confirmed for Basic | `[unknown]` |

Implication: a queue and fill study needs order-book depth and volume, which Basic lacks. Free alternative is forward capture on the delayed key: stream data is free, but delayed 1 to 180 seconds, 3 levels, with no total matched `[verified: DEV/2687105/Application+Keys]`. You cannot see your queue position or traded volume at price from it. Your own order status (matched size, matched time) is available from listCurrentOrders or the order stream `[inferred]`, and that is the only fill ground truth at EUR 0.

## 6. Account restrictions

| Item | Finding | Tag |
|---|---|---|
| Limits on winning accounts | No official statement found | `[unknown]`. Resolve by reading Betfair Exchange terms, or asking support in writing |
| Minimum stake, EUR | Secondary affiliate sources say EUR 2 (also GBP 2). The earlier scan said EUR 1 | `[inferred]`, conflicting, affiliate sources: https://betfairsquare.pages.dev/blog/betfair-minimum-maximum-bet-size-limits. Resolve by the bet slip error or Betfair help page |
| Racing minimum | A "minimum bet to win" guarantee exists on British and Irish races (Racing Post headline) | `[inferred]` https://www.racingpost.com/news/betfair-extend-minimum-bet-to-win-guarantee-to-all-british-and-irish-races-a1on05R4trO0/ headline only, details unknown |
| Maximum stake | Said to depend on liquidity, no fixed cap | `[inferred]` affiliate |
| Price increments | Betfair uses banded ticks. I used 0.01 below 2, 0.02 from 2 to 3, 0.05 from 3 to 4, 0.1 from 4 to 6 | `[inferred]` from general knowledge, not fetched this session. Resolve from the Betting Type Definitions price increments table |
| Market-specific rules | Dead heat in racing, non-runners with reduction factors, football Match Odds settled on 90 minutes plus stoppage | `[unknown]` official wording not read. Non-runner reduction factors affect resting racing orders, since matched bets may be reduced and orders lapse on withdrawal. Check the Rules page |
| Account type | Irish account on betfair.com, no known product restrictions | `[verified: docs/brief.md]` (user statement) |

Practical limit for a resting-order strategy: with a EUR 2 minimum and a EUR 500 bankroll, unit stakes of EUR 2 to 10 give 50 to 250 units. Fills at the best queue position are rare at small size, but small size is not queue-penalised, only time-penalised `[inferred]`.

## 7. Irish tax (not tax advice)

I could not reach Revenue.ie in this session. Everything below is `[inferred]` from search summaries and should be read as a lead.

- General position stated by secondary sources: ordinary gambling winnings are not subject to income tax, USC, PRSI or CGT for the player. Sources: https://www.irishtimes.com/business/personal-finance/gambling-is-a-winner-on-taxes-but-the-losses-can-hit-you-hard-1.4789779, https://culch.ie/legal-guides/does-ireland-taxes-gambling-winnings `[inferred]`.
- Losses are therefore not deductible in the usual case `[inferred]`.
- Possible exception: a person whose betting amounts to a trade could be assessed as trading income. One opinion piece says the professional gambler is rare in tax terms. No official position was seen `[unknown]`. A systematic, automated, profit-seeking operation with a high volume might raise the question. I do not know where Revenue draws the line `[unknown]`.
- Betting duty: Revenue pages found concern operator duty on a betting exchange, which is not paid by the player `[inferred]` https://www.revenue.ie/en/corporate/information-about-revenue/statistics/excise/receipts-volume-and-price/betting-duty-receipts.aspx (search summary only).
- Jurisdiction note: the user may also owe tax in another country if resident elsewhere. Brief says Ireland.

Resolve: a person searches Revenue.ie for "gambling winnings" and the Tax and Duty Manual on trading income "badges of trade", or asks Revenue or an Irish tax adviser. Keep a log of all bets (the bet-level logs the operator already works with are enough).

## 8. Cost table: break-even per tick captured

Method. A maker backs at the higher price p2 and lays at the lower price p1 (or the reverse in time order), where p2 is one tick above p1. Lay stake equals back stake times p2/p1. Profit is the same whichever selection wins and equals back stake times (p2 - p1) / p1. Per unit of back stake S:

- Gross profit per completed one-tick round trip: tick / p1.
- Commission: c times gross profit, charged only if the market nets a profit `[inferred]`.
- Net profit: gross times (1 - c).
- Break-even completion rate q, if an incomplete trade is closed at a one-tick loss with no commission on the loss: q (1 - c) = (1 - q), so q = 1 / (2 - c).
- Ticks and commission rates are assumptions as noted. No transaction charge, no premium charge, no data fee assumed, since they are unknown or non-binding at this volume.

| Odds p1 | Tick used | Gross per unit stake | Commission paid at 2% | Net at 2% | Commission paid at 5% | Net at 5% |
|---|---|---|---|---|---|---|
| 1.5 | 0.01 | 0.667% | 0.013% | 0.653% | 0.033% | 0.633% |
| 2.0 | 0.02 | 1.000% | 0.020% | 0.980% | 0.050% | 0.950% |
| 3.0 | 0.05 | 1.667% | 0.033% | 1.633% | 0.083% | 1.583% |
| 5.0 | 0.10 | 2.000% | 0.040% | 1.960% | 0.100% | 1.900% |

Break-even completion rate with a one-tick stop loss: 50.51% at 2% commission, 51.28% at 5%. At a two-tick stop loss, q (1 - c) = 2 (1 - q), giving 66.4% at 2% and 67.2% at 5%.

Reading the table. Commission shaves 2% or 5% off each winning tick, so commission is a small cost per tick. The binding cost is adverse selection and non-completion, not commission. The break-even edge per unit stake is the net figure per tick in the table, minus expected loss from unfilled or picked-off trades. Because the delayed key shows prices 1 to 180 seconds old, you cannot measure the completion rate from the feed. Only logged fills from paper or small live orders can measure it.

Other costs, all uncertain:

| Cost | Status |
|---|---|
| Data fee | EUR 0 by brief. Basic free. Advanced and Pro price `[unknown]` |
| Live key GBP 499 | Not needed if the delayed key can place bets (see conflict) |
| Expert Fee | Not binding `[inferred]` |
| Transaction charge | Threshold `[unknown]`, unlikely to bind for place-and-wait `[inferred]` |
| Slippage and adverse selection | Not measured `[unknown]` |
| Commission is per market net, so a loser in one market does not reduce commission in another | `[inferred]` |

## Top constraints

1. Whether the delayed key can place bets at all, and any placement latency or matching difference, is contradicted across doc versions and cannot be resolved from the fetched sources. If it cannot, a GBP 499 live key is needed and the strategy fails the budget.
2. No free data measures queue position, fill rate or traded volume. Basic history is 1 minute last traded price, the delayed feed is 1 to 180 seconds stale with 3 levels and no total matched, so the completion rate can be learned only by logging your own orders.
3. Transaction charge threshold and exemption, winning-account limits, and Irish tax treatment are unconfirmed because the Betfair charges pages and Revenue.ie were unreachable. Commission rate for the Irish account is also unconfirmed (2% vs 5%).

## What a human must open

1. DEV/2687105/Application+Keys: delayed key bet placement, delay range, fee.
2. Betfair charges page www.betfair.com/aboutUs/Betfair.Charges: commission by package, transaction charge threshold and market-making exemption, Expert Fee.
3. historicdata.betfair.com: Basic, Advanced, Pro prices and sport coverage.
4. Betfair Exchange rules and terms: winning-account limits, minimum stake in EUR, non-runner and dead heat rules.
5. Revenue.ie: gambling winnings, trading income badges of trade.
6. DEV Best Practice and Betting Enums pages: order rate limits, persistence types.

## Orchestrator addendum (2026-11-15, read via Confluence REST API, overrides conflicting tags above)

DEV = https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages

| Item | Finding | Tag |
|---|---|---|
| Delayed key bet placement | Table row "Bet Placement (Live Exchange): Delayed Yes, Live Yes". The delayed key "operates on the live (production) Betfair Exchange". Page version 144, 2026-11-02. Older snippets saying it cannot bet are out of date. | `[verified: DEV/2687105/Application+Keys]` |
| Delayed key intended use | "The Delayed App Key should be used for development purposes and any functional testing." Running a sustained live strategy on it may conflict with Betfair's intended use. Whether Betfair enforces this is unknown. | `[verified: DEV/2687105/Application+Keys]` (wording), enforcement `[unknown]` |
| Minimum bet, EUR | Min bet size EUR 1; min deposit EUR 15; min BSP liability EUR 10; min bet payout EUR 20 (lower-stake orders at larger prices). GBP: 1 / 10 / 10 / 10. | `[verified: DEV/2686993/Additional+Information]` |
| Price ladder (CLASSIC) | 1.01-2: 0.01; 2-3: 0.02; 3-4: 0.05; 4-6: 0.1; 6-10: 0.2; 10-20: 0.5; 20-30: 1; 30-50: 2; 50-100: 5; 100-1000: 10. Matches the input file. | `[verified: DEV/2686993/Additional+Information]` |
| Market data request limit | sum(weight) x number of market IDs must not exceed 200 points per request, else TOO_MUCH_DATA. Applies to listMarketBook, listRunnerBook, listMarketCatalogue, listMarketProfitandLoss. Page version 49, 2026-11-09. | `[verified: DEV/2687478/Market+Data+Request+Limits]` |

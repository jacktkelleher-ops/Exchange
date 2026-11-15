# Costs and constraints: Football over/under goals (pre-play, own-odds model)

Date: 2026-11-15
Agent: costs-constraints
Inputs read: CLAUDE.md, docs/brief.md, research/02-ranking.md, research/00-verify/input-claims.md.

## Access note (read first)

No page was fetched in this session. Every WebFetch failed at DNS (`getaddrinfo ENOTFOUND`) for betfair-developer-docs.atlassian.net, www.revenue.ie, revenue.ie, www.oireachtas.ie, betfair-datascientists.github.io, betcode-org.github.io and apis.io. These hosts are outside the session's allowed network domains. Bash was not available, so the curl route was not possible either. The Betfair consumer sites were not attempted because the brief says they return a Cloudflare challenge.

Consequences:

- `[verified]` items below are only those reused from research/00-verify/input-claims.md, which cites pages fetched earlier in the review.
- Everything learned this session came from WebSearch result summaries. These are not fetched pages. They are tagged `[inferred]` and the intended source URL is named so a human can confirm it.
- To close the gaps: allow betfair-developer-docs.atlassian.net and revenue.ie in the session network settings, or a human opens the Betfair pages listed under "How to resolve".

DEV = https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages

## 1. Commission

| Item | Finding | Tag |
|---|---|---|
| Packages for Irish customers | Basic 2%, Rewards 5%, Rewards+ 8%. Switch once per month at the start of the month. | `[inferred]` WebSearch summaries of Sporting Life and Timeform guides. Official charges page not read. |
| Calculation | Charged on net winnings per market. No commission on the returned stake. Net market profit basis for multiple bets in one market is the usual rule but not read at an official page. | `[inferred]` |
| Per-market rate in the API | The API exposes `marketBaseRate` and `discountAllowed`, so the live rate for an over/under market can be read once the account is connected. | `[verified: DEV/2687465/Betting+Type+Definitions]` (from input-claims.md) |
| Conflict | Some sources say "up to 5%" by default, and affiliate sites claim 2% on UK racing and 5% on other markets. The 2% for Basic is therefore not settled. | `[inferred]` |
| Discounts | Discount tied to package choice and Betfair Rewards points. Exact discount scheme not found. | `[unknown]` |

Handling in this file: the cost table uses 2% and 5% as the brief asked. Treat 5% as the planning case until the account's actual rate is read from the API or the account page.

How to resolve: a human reads the Betfair Exchange charges page (www.betfair.com/aboutUs/Betfair.Charges) or the account's "My Account > Commission" view. A cheaper check is to call `listMarketCatalogue` or `listMarketBook` on a Match Odds or Over/Under market with the delayed key and read `marketBaseRate` and `discountAllowed`.

## 2. Additional charge on profitable accounts

| Item | Finding | Tag |
|---|---|---|
| Premium Charge | Reported as dropped from 2025 and replaced by the Expert Fee. | `[inferred]` Racing Post summary via WebSearch |
| Expert Fee tiers | 0% below GBP 25,000, 20% above, 40% at a higher band, on gross profit over a rolling 52 weeks. From 6 Jan 2025 per input. | `[inferred]` (input-claims.md claim 2, Racing Post) |
| Basis conflict | One source describes it as lifetime profit over 100 or more settled markets rather than rolling 52 weeks. Sources disagree. | `[inferred]` |
| Relevance | A EUR 500 bankroll with a 30% drawdown cap would need profit of tens of thousands to approach a GBP 25,000 trigger. Not binding for years at this scale. | `[inferred]` |
| Transaction charges | Apply to both delayed and live keys. Threshold, rate and exemption are not readable. Scanners disagree: 5,000 per hour vs 1,000 per hour. A pre-play model placing a few bets a day is far below either figure. | Applies: `[verified: DEV/2687105/Application+Keys]`. Threshold: `[unknown]`. Not binding: `[inferred]` |
| Data request charges | A third-party summary says Betfair may charge when weighted data requests are high relative to betting activity. Not read at an official page. | `[inferred]` |

How to resolve: a human opens www.betfair.com/aboutUs/Betfair.Charges/#TranCharges2 and the Expert Fee terms page and pastes the text into docs/inputs/.

## 3. API access

| Item | Finding | Tag |
|---|---|---|
| Live key | GBP 499 activation, debited after activation, KYC required. Unaffordable on EUR 500 bankroll and EUR 0 budget. | `[verified: DEV/2687105/Application+Keys]` (page version 2026-11-02) |
| Delayed key | Free. Can place bets on the live exchange. Stream API with 2 connections and 200 markets. 3 price levels. No total matched by selection. No BSP near/far price. Prices delayed 1 to 180 seconds. | `[verified: DEV/2687105/Application+Keys]` |
| Conflict in search summaries | One WebSearch summary said the delayed key cannot place bets. The verified page says it can. The verified page is used. | `[verified: DEV/2687105/Application+Keys]` |
| Traded volume | The delayed key does not return `EX_TRADED` data through `listMarketBook`. | `[inferred]` WebSearch summary of DEV Market Data Request Limits (page 2687478) |
| Data request limit | For `listMarketBook` and similar calls, sum of weights times number of market ids must not exceed 200 points per request, else `TOO_MUCH_DATA`. | `[inferred]` WebSearch summary of DEV/2687478/Market+Data+Request+Limits |
| Example weights | No projection 2, `EX_BEST_OFFERS` 5, `EX_ALL_OFFERS` 17, `SP_AVAILABLE` 3, `SP_TRADED` 7, market description +1, runner metadata +1. | `[inferred]` same source |
| Practical meaning | With `EX_BEST_OFFERS` at weight 5, about 40 markets per request fit under 200 points. A pre-play over/under scan of one day of football fits in a few calls. | `[inferred]` arithmetic from the above |
| Different cap for delayed key | Not found. The 200 point cap is assumed to apply equally. | `[unknown]` |
| Requests per second, per-day cap | No fixed number found. Excess use returns `TOO_MANY_REQUESTS` or `SERVICE_BUSY` per a third-party summary. | `[unknown]` |
| Bet delay for pre-play orders | Delay values by sport are not in the dev docs read. Pre-play bets are not subject to the in-play bet delay in the usual model. Not read at an official page. | `[unknown]` for numbers, `[inferred]` for pre-play |
| Passive in-play orders | Passive in-play orders that cannot match immediately skip the delay. Football dynamic events have no delay at half time. Irrelevant for pre-play. | `[verified: DEV/2687396/Exchange+Stream+API]` |

Note for a pre-play model: a price that is 1 to 180 seconds stale `[verified]` matters little for a bet placed hours before kick-off, but it blurs any closing price benchmark. The delay is a bigger problem for measuring the close (CLAUDE.md requires benchmarking to the close). A forward capture job should log the last pre-kick-off snapshot it sees and accept that the true close is up to 180 seconds later `[inferred]`.

How to resolve: a human opens DEV/2687478 (Market Data Request Limits) and DEV/2687105 (Application Keys). Any call with the delayed key will also show the behaviour directly.

## 4. Historical data

| Item | Finding | Tag |
|---|---|---|
| Tiers | Basic free, Advanced paid, Pro paid. | `[inferred]` WebSearch summaries of community FAQs (betcode-org.github.io/faq/using-data) |
| Basic content | 1 minute intervals, last traded price, no volume. | `[inferred]` same |
| Advanced content | 1 second intervals, best prices and volume. | `[inferred]` same |
| Pro content | 50 millisecond intervals, volume included. | `[inferred]` same |
| Coverage | Betfair's data site is reported to cover nearly all exchange markets since 2016. | `[inferred]` WebSearch summary of historicdata.betfair.com |
| Over/Under in Basic | Not shown in any result. Whether Over/Under 0.5 to 8.5 goals markets are in the free Basic files is `[unknown]`. | `[unknown]` |
| Prices | Input says Advanced 69 and Pro 230. A tennis scanner said GBP 499 and 1,499 per year. Another said 39 and 99 or 79. Aggregator says per-package purchase with lifetime license. | `[unknown]` |
| Format and field list | Not seen. The official data specification was not opened. | `[unknown]` |
| Mapping files | Event and competition mapping files exist for soccer and other sports, 2018 to 2025. These are not price data. | `[verified: DEV/2686993/Additional+Information]` |

Handling: the ranking already scored Data access 2 for this reason. A free Basic sample is the cheapest test. Forward capture of over/under books on the delayed key is free `[verified]` but gives 3 levels and no volume.

How to resolve: a human opens historicdata.betfair.com, downloads one free Basic soccer file for a recent month, and checks whether market type names such as OVER_UNDER_25 appear and which fields each row has. Record the field list and the price page for Advanced and Pro in docs/inputs/.

Free results source for the model (not Betfair): out of scope for this file, but the closing price calibration needs match results. Not sourced this session `[unknown]`.

## 5. Account restrictions and market rules

| Item | Finding | Tag |
|---|---|---|
| Limits on winning accounts | No official statement found. Input claim 8 says Betfair does not ban or stake-limit winners. Not confirmed. | `[unknown]` |
| Stake limits | No official maximum found. Liquidity in the book is the practical limit. | `[unknown]` |
| Minimum stake in EUR | Search summaries give EUR 2 (UK GBP 2). A developer doc snippet says a minimum of 200 euro cents, in steps of 50 cents. Bet Angel help (April 2023) says GBP 1. Conflict. EUR 2 is the planning figure. Applies to the backer's stake, not the lay liability. | `[inferred]` WebSearch summaries |
| Over/under market rules | Rules for abandoned or postponed matches, extra time and the market line were not found. Standard soccer rule is that over/under settles on 90 minutes plus stoppage time. | `[unknown]` |
| Delayed key data limits on the 200 markets stream cap | 2 connections, 200 markets. Enough for one day of over/under markets across top leagues. | `[verified: DEV/2687105/Application+Keys]` for the cap, `[inferred]` for sufficiency |
| Bankroll fit | EUR 500 bankroll, 30% drawdown (EUR 150) `[verified: docs/brief.md]`. At EUR 2 minimum, stake sizing is not constrained by the minimum. | `[inferred]` |

How to resolve: a human reads the Betfair Exchange rules page for football Over/Under, the Betfair terms on account restriction, and checks the bet slip for the euro minimum.

## 6. Irish tax treatment (not tax advice)

This is not tax advice. Nothing here was read at Revenue.ie in this session because revenue.ie did not resolve. Everything is `[inferred]` from WebSearch summaries. Speak to a tax adviser or Revenue before relying on it.

| Point | What the summaries say | Tag |
|---|---|---|
| Winnings of a private individual | A 2012 parliamentary reply (www.oireachtas.ie/ga/debates/question/2012-04-18/241/) reportedly relays Revenue's view that profits from selective bet-laying on exchanges by people who are not licensed bookmakers were outside income tax, stamp duty, VAT and capital gains tax. | `[inferred]` |
| Losses | Irish press says gambling losses cannot be written off against other income. | `[inferred]` Irish Times article via WebSearch |
| Conflict | A legal guide (culch.ie, not official) says betting winnings are generally treated as capital gains and may attract CGT. This contradicts the 2012 reply. | `[inferred]` |
| Operator taxes | Betting duty and VAT on commission fall on the operator, not on the punter. Rate on exchange commission reported at 25% from 1 Jan 2019, with possible increases flagged for later budgets. Whether this is already inside Betfair's quoted commission is `[unknown]`. | `[inferred]` |
| Risk of trade classification | A systematic, model-driven operation with regular profits could be argued to be a trade. I could not find a current Revenue statement on this. | `[unknown]` |
| Date of the evidence | The only Revenue-attributed statement found is from 2012. Law or practice may have changed since. | `[inferred]` |

Where to look: Revenue.ie pages on gambling winnings, Revenue's Tax and Duty Manual on betting duty (revenue.ie/en/tax-professionals/tdm/excise/betting-duty/) and the VAT note on betting and remote betting services (revenue.ie/en/tax-professionals/tdm/value-added-tax/). Ask Revenue directly or an Irish tax adviser for a written view if profits become material. Keep bet-level records either way.

## 7. Cost table: break-even edge per unit stake

Method. Back bet at decimal odds o, commission rate c on net winnings, true win probability p.

- Expected profit per unit stake: EV = p(o-1)(1-c) - (1-p).
- Break-even probability: p* = 1 / (1 + (o-1)(1-c)).
- Cost drag at fair odds (p = 1/o): c(o-1)/o per unit stake. This is the EV the model must beat, before slippage.
- Probability edge needed: p* - 1/o, in percentage points.

All figures are arithmetic on the stated formula, tag `[inferred]` as to the commission rates and exact to rounding as to the sums. Slippage, spread crossing and any data cost are not included: spread cost `[unknown]` until measured on the delayed key, data cost EUR 0 by brief.

| Odds o | Implied prob 1/o | EV needed per unit stake at 2% | Prob edge needed at 2% (pp) | EV needed per unit stake at 5% | Prob edge needed at 5% (pp) |
|---|---|---|---|---|---|
| 1.70 | 58.82% | 0.82% | 0.49 | 2.06% | 1.24 |
| 1.80 | 55.56% | 0.89% | 0.50 | 2.22% | 1.26 |
| 1.90 | 52.63% | 0.95% | 0.50 | 2.37% | 1.28 |
| 2.00 | 50.00% | 1.00% | 0.51 | 2.50% | 1.28 |
| 2.10 | 47.62% | 1.05% | 0.50 | 2.62% | 1.28 |
| 2.20 | 45.45% | 1.09% | 0.50 | 2.73% | 1.27 |
| 2.30 | 43.48% | 1.13% | 0.50 | 2.83% | 1.27 |

Reading the table:

- Break-even edge per unit stake is about 0.8% to 1.1% at 2% commission and about 2.1% to 2.8% at 5%. At evens it is 1.0% and 2.5%.
- In probability terms the model must beat the exchange implied probability by about 0.5 pp at 2% and 1.3 pp at 5%.
- A lay bet at odds o pays commission only when the lay wins. The cost per unit of backer's stake is the same c(o-1)/o at fair odds. Per unit of liability it is c/o.
- Premium or Expert Fee: not binding at this bankroll `[inferred]`. Transaction charge: not binding at pre-play volumes `[inferred]`. Data: EUR 0 by choice, so the model benchmark is limited to what Basic history or forward capture gives `[inferred]`.
- Slippage: one tick of price concession, if taking the opposing offer, is added on top. Not sized here because tick size and measured spreads for over/under books are `[unknown]`. Resolve by logging best back and lay on the delayed key (3 levels) for a few weeks.
- Taxes on the punter: none found for an individual per the 2012 position, but unverified (section 6).

## Top three constraints

1. Data. No confirmation that free Basic history includes Over/Under markets, and Basic is reported as 1 minute last traded price with no volume. The delayed key shows 3 levels, no traded volume, and prices 1 to 180 seconds late `[verified]`. A closing price benchmark is therefore approximate.
2. Commission rate for this account. 2% or 5% changes the break-even from about 1.0% to 2.5% at evens. The rate must be read from the account or `marketBaseRate`.
3. Unverified account and tax risk. No official statement on limits for winning accounts, no euro minimum confirmed (EUR 2 assumed), and Irish tax treatment rests on a 2012 reply seen only in a search summary.

## Open items for a human

| Item | Where | What to record |
|---|---|---|
| Commission and discount rules | www.betfair.com/aboutUs/Betfair.Charges | Rates, transaction charge threshold and exemption, Expert Fee terms |
| Account rate | `marketBaseRate` via delayed key | Rate on an over/under market |
| Basic history content | historicdata.betfair.com | Market types in free soccer files, field list, Advanced and Pro price |
| Data request limits | DEV/2687478 | Confirm 200 points cap and delayed key limits |
| Bet slip minimum | betfair.com bet slip | EUR minimum back stake |
| Winner limits and over/under rules | Betfair terms and rules pages | Any restriction text |
| Tax | Revenue.ie or an Irish tax adviser | Written view on exchange winnings and trade classification |

## Orchestrator addendum (2026-11-15, read via Confluence REST API, overrides conflicting tags above)

DEV = https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages

| Item | Finding | Tag |
|---|---|---|
| Delayed key bet placement | Table row "Bet Placement (Live Exchange): Delayed Yes, Live Yes". The delayed key "operates on the live (production) Betfair Exchange". Page version 144, 2026-11-02. Older snippets saying it cannot bet are out of date. | `[verified: DEV/2687105/Application+Keys]` |
| Delayed key intended use | "The Delayed App Key should be used for development purposes and any functional testing." Running a sustained live strategy on it may conflict with Betfair's intended use. Whether Betfair enforces this is unknown. | `[verified: DEV/2687105/Application+Keys]` (wording), enforcement `[unknown]` |
| Minimum bet, EUR | Min bet size EUR 1; min deposit EUR 15; min BSP liability EUR 10; min bet payout EUR 20 (lower-stake orders at larger prices). GBP: 1 / 10 / 10 / 10. | `[verified: DEV/2686993/Additional+Information]` |
| Price ladder (CLASSIC) | 1.01-2: 0.01; 2-3: 0.02; 3-4: 0.05; 4-6: 0.1; 6-10: 0.2; 10-20: 0.5; 20-30: 1; 30-50: 2; 50-100: 5; 100-1000: 10. Matches the input file. | `[verified: DEV/2686993/Additional+Information]` |
| Market data request limit | sum(weight) x number of market IDs must not exceed 200 points per request, else TOO_MUCH_DATA. Applies to listMarketBook, listRunnerBook, listMarketCatalogue, listMarketProfitandLoss. Page version 49, 2026-11-09. | `[verified: DEV/2687478/Market+Data+Request+Limits]` |

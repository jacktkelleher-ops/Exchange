# Verification of Gemini input claims 1 to 14

Date: 2026-11-15
Agent: orchestrator (main session)

## Access note

Betfair's consumer sites (support.betfair.com, www.betfair.com, historicdata.betfair.com, developer.betfair.com) are allowed by the session network but answer with a Cloudflare bot challenge (HTTP 403, `cf-mitigated: challenge`). They could not be read in this session. The official Betfair developer documentation could be read through its public Confluence API. Claims that live only on the consumer sites stay `[inferred]` or `[unknown]`. Resolving them needs a person to open the pages in a browser, or a copy of the page text.

DEV = https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages

## Results

| # | Claim (from input) | Status | Finding |
|---|---|---|---|
| 1 | Ireland commission Basic 2%, Rewards 5%, Rewards+ 8%, switchable monthly | `[inferred]` | Several secondary sources (scanner files) repeat 2/5/8. Official charges page blocked. The API exposes a per-market `marketBaseRate` and `discountAllowed` field, so the live rate can be read per market once an account exists `[verified: DEV/2687465/Betting+Type+Definitions]`. |
| 2 | Expert Fee 0% below 25k, 20% 25k to 100k, 40% above 100k, rolling 52 weeks, from 6 Jan 2025 | `[inferred]` | Racing Post (secondary) reports the same tiers and the 52-week basis. Buffer and commission-generated formulas not seen at any official page. Irrelevant at a EUR 500 bankroll for years `[inferred]`. |
| 3 | Transaction charges above 5,000 per hour, market-making exemption (back 10+, lay liability 100+) | `[unknown]` | Dev docs confirm transaction charges apply to both delayed and live keys and link to `www.betfair.com/aboutUs/Betfair.Charges/#TranCharges2` for terms `[verified: DEV/2687105/Application+Keys]`, `[verified: DEV/2687730/Best+Practice+Guide]`. Threshold, rate and exemption not readable (Cloudflare). Scanners found a 1,000 vs 5,000 conflict in secondary sources. |
| 4 | Live API key 299 or 499 | `[verified]` **GBP 499** | "Activation Fee: None (Delayed) / £499 (Live)", debited after activation, KYC required. Page version dated 2026-11-02 `[verified: DEV/2687105/Application+Keys]`. The 299 figure is out of date. |
| 4a | (new) What a delayed key can do | `[verified]` | Delayed key: free, bet placement on the live exchange allowed, Stream API (2 connections, 200 markets), 3 price levels, no total matched by selection, no BSP near/far price, prices delayed 1 to 180 seconds `[verified: DEV/2687105/Application+Keys]`. |
| 5 | Historical data tiers: Basic free, Advanced 69, Pro 230 (racing and soccer) | `[unknown]` | historicdata.betfair.com blocked. Tennis scanner found secondary figures of Advanced GBP 499/yr and Pro GBP 1,499/yr for tennis, which conflict with the input. Dev docs confirm competition and event mapping files exist for 2018 to 2025 for soccer, tennis, cricket, golf and other sports `[verified: DEV/2686993/Additional+Information]`. |
| 6 | Tennis retirement and dead heat rules | `[inferred]` | Tennis scanner (secondary): retirement after first set completes stands, before voids. Input's ITF/UTR void rule may be a Sportsbook rule. Official rules page blocked. |
| 7 | Bet delay values by sport | partly `[verified]` | Fixed per-sport figures not in dev docs. Verified: PASSIVE model lets in-play orders that cannot match immediately skip the delay (plain LIMIT, LAPSE only). DYNAMIC model: tennis delay drops to 1 second at games 3, 5, 7, 9, 11 and set-deciding games; football DYNAMIC events have no delay at half time `[verified: DEV/2687396/Exchange+Stream+API]`, `[verified: DEV/2687455/Betting+Enums]`. Input's fixed 2/5/5-8 second figures `[unknown]`. |
| 8 | Betfair does not ban or stake-limit winning accounts | `[unknown]` | No official statement found. Terms page blocked. |
| 9 | Reading paper, about 50% gross ROI backing surprise longshot goals, 2019/20 EPL | paper `[verified]`, ROI `[unknown]` | Angelini, De Angelis, Singleton (2022), Int. J. Forecasting 38(1) 282-299, uses Betfair data; mispricing grows after surprise late goals by longshots, market underestimates them `[verified: https://research.reading.ac.uk/football-research/new-journal-article-informational-efficiency-and-behaviour-within-in-play-prediction-markets/]`. The 50% ROI figure not seen. Full text needed. |
| 10 | MPRA 126351: late in-play favourite-longshot bias | `[verified]` | "Agreeing to Disagree: The Economics of Betting Exchanges". Pre-match and early in-play fit the model (Makers earn more than Takers). Late in-play, longshot bets lose heavily even for liquidity providers, and takers on favourites profit `[verified: https://mpra.ub.uni-muenchen.de/126351/]`. |
| 10a | Conflict 9 vs 10 | `[inferred]` | Not necessarily contradictory: paper 9 conditions on surprise goals by longshots; paper 10 is an average over late in-play trades. Both imply late in-play mispricing exists. Direction depends on state. Needs a test on the same data. |
| 11 | Pinnacle odds-dropper 6% yield | `[unknown]` | Single anecdote. Not checked. |
| 12 | Power devig on 725,000 markets | `[unknown]` | Reddit source. Not checked. |
| 13 | Women's and lower-league football less efficient | `[inferred]` | No Betfair evidence found. |
| 14 | Cross-venue prediction market arbitrage | out of scope | Per brief. |

## Impact on the brief

- A live key costs GBP 499 (about EUR 590 at an assumed rate `[inferred]`), more than the whole EUR 500 bankroll and outside the EUR 0 budget.
- The free delayed key can still place real bets and stream data, but prices are delayed by up to 180 seconds and show 3 levels. That rules out latency-sensitive in-play trading and queue-based market making. It still allows pre-play model betting and slow in-play strategies that rest passive orders `[inferred]`.
- Basic historical data (free) is widely reported as 1-minute last traded price with no volume `[inferred]`. Paid tiers are needed for queue or order-book tests.

## Orchestrator addendum (2026-11-15, read via Confluence REST API, overrides conflicting tags above)

DEV = https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages

| Item | Finding | Tag |
|---|---|---|
| Delayed key bet placement | Table row "Bet Placement (Live Exchange): Delayed Yes, Live Yes". The delayed key "operates on the live (production) Betfair Exchange". Page version 144, 2026-11-02. Older snippets saying it cannot bet are out of date. | `[verified: DEV/2687105/Application+Keys]` |
| Delayed key intended use | "The Delayed App Key should be used for development purposes and any functional testing." Running a sustained live strategy on it may conflict with Betfair's intended use. Whether Betfair enforces this is unknown. | `[verified: DEV/2687105/Application+Keys]` (wording), enforcement `[unknown]` |
| Minimum bet, EUR | Min bet size EUR 1; min deposit EUR 15; min BSP liability EUR 10; min bet payout EUR 20 (lower-stake orders at larger prices). GBP: 1 / 10 / 10 / 10. | `[verified: DEV/2686993/Additional+Information]` |
| Price ladder (CLASSIC) | 1.01-2: 0.01; 2-3: 0.02; 3-4: 0.05; 4-6: 0.1; 6-10: 0.2; 10-20: 0.5; 20-30: 1; 30-50: 2; 50-100: 5; 100-1000: 10. Matches the input file. | `[verified: DEV/2686993/Additional+Information]` |
| Market data request limit | sum(weight) x number of market IDs must not exceed 200 points per request, else TOO_MUCH_DATA. Applies to listMarketBook, listRunnerBook, listMarketCatalogue, listMarketProfitandLoss. Page version 49, 2026-11-09. | `[verified: DEV/2687478/Market+Data+Request+Limits]` |

## Addendum 2: Betfair Historical Data Feed Specification (user-supplied official PDF, 2026-11-15)

Source: `docs/inputs/official/Betfair-Historical-Data-Feed-Specification.pdf` (Betfair document, supplied by the user; cited below as SPEC). It mentions betDelayModels in markets published since 17/08/2026, so it is a 2026 version.

| Item | Finding | Tag |
|---|---|---|
| History start | Data from May 2015 (AUS/NZ from Oct 2016). JSON in tar.bz2. | `[verified: SPEC p1]` |
| BASIC content | 1-minute intervals. Last traded price (ltp) per runner plus full marketDefinition changes. No traded volume, no back/lay ladder, no traded-at-price. | `[verified: SPEC p3-4]` |
| ADVANCED content | 1-second intervals. Best available to back and lay (batb/batl, top levels), traded volume by market and runner, traded price-volume (trd), ltp. | `[verified: SPEC p3-4]` |
| PRO content | Tick by tick. Full ladder (atb/atl), trd, market tv, ltp, BSP near/far and SP back/lay. | `[verified: SPEC p3-4]` |
| In every plan (incl. BASIC) | marketDefinition carries marketType, marketBaseRate (commission rate for the market), inPlay, betDelay, crossMatching, status, runner status (WINNER, LOSER, REMOVED, PLACED), runner bsp, adjustmentFactor. | `[verified: SPEC p1-2]` |
| Consequence for football O/U | If Basic covers O/U markets, it gives a near-close price (last 1-minute ltp before the off), the settled result (runner WINNER/LOSER) and the commission base rate, all free. That is enough for a closing-price benchmark and labels without an outside results source. | `[inferred]` from SPEC |
| Consequence for resting orders | Basic cannot show fills, queue or depth. Advanced has only best offers at 1-second granularity, so queue simulation needs Pro. Fill rates must come from own logged orders. Racing BSP per runner is free in Basic, usable as a benchmark. | `[inferred]` from SPEC |
| Still unknown | Which sports and market types each plan covers (O/U in Basic?), and prices of Advanced and Pro. The spec is field-level only. | `[unknown]`: resolve on historicdata.betfair.com plan page or by downloading one free Basic soccer month. |

# Prediction markets: Kalshi and Polymarket market data

Date: 2026-11-15
Agent: orchestrator (main session, run from the user's machine in Ireland)

## Summary

Both venues publish free, unauthenticated historical price data for football markets, including EPL totals. Kalshi's is richer than Betfair Basic: 1-minute candles with best bid, best ask and traded volume. Neither venue can be traded from Ireland. They are usable only as a data source, for example as a second price reference for a Betfair over/under model (strategy F in `research/03-viability/football-over-under/market-structure.md`). Input claim 14 (cross-venue arbitrage) stays out of scope, and now also blocked by jurisdiction.

## Comparison

| Item | Kalshi | Polymarket | Betfair Basic (for reference) |
|---|---|---|---|
| Can trade from Ireland | No. Ireland restricted; Kalshi and Polymarket restricted Irish users by 21 Jul 2026 after GRAI action [inferred: https://www.gamblinginsider.com/?p=176465, https://www.gambling.com/news/prediction-markets-face-a-global-squeeze-as-ireland-and-india-push-polymarket-and-kalshi-out] | No. Polymarket's geoblock endpoint returned `"blocked": true, "country": "IE"` from this machine [verified: https://polymarket.com/api/geoblock, 2026-11-15] | Yes |
| Historical price data | Candlesticks per market, `period_interval=1` gives 1-minute bars with yes bid OHLC, yes ask OHLC, volume and open interest. No auth needed [verified: https://docs.kalshi.com/openapi.yaml; test call on KXEPLTOTAL-26NOV08MUNAVL-3 returned 627 one-minute candles] | `/prices-history` per outcome token, intervals 1h to max, `fidelity` in minutes. No auth (`security: []`) [verified: https://docs.polymarket.com/api-reference/markets/get-prices-history.md]. Test on Man Utd v Aston Villa O/U 2.5 returned 1,842 points over 13 days, median gap 600 s (trade-price series, no bid/ask) [verified: test call 2026-11-15] | 1-minute last traded price, no volume, no bid/ask [verified: SPEC] |
| Trades and order book | `/markets/trades` and `/markets/{ticker}/orderbook` are public [verified: openapi.yaml, no security block] | Order book and last trade endpoints public; trade feed endpoints exist [verified: https://docs.polymarket.com/llms.txt] | Paid tiers only |
| EPL totals markets | Series `KXEPLTOTAL`, lines 0.5 to 10.5 per match [verified: API call]. Man Utd v Villa O/U 2.5: 46,922 contracts traded, max USD 1 each [verified: API call] | "More Markets" event per match with O/U 0.5 to 8.5. Same match O/U 2.5 volume about USD 38,500 [verified: gamma-api call] | Deepest O/U venue [inferred] |
| Moneyline depth (EPL) | not measured | Median about USD 447,000 per moneyline market across 8 recent EPL matches [verified: gamma-api call] | |
| Rate limits | Token budgets by tier; unauthenticated public requests have separate limits; back off on 429 [verified: https://docs.kalshi.com/getting_started/rate_limits.md] | Tiered; `/events` pages above limit 50 must be requested gzip-compressed [verified: API response] | 200 points per request |
| Fees (if tradeable) | not checked | Taker fee = C x rate x p x (1-p); sports rate 0.05; makers pay 0 and get a 15% rebate [verified: https://docs.polymarket.com/trading/fees.md] | 2% / 5% [inferred] |
| Use terms | Developer Agreement governs API use [unknown content: https://kalshi.com/developer-agreement] | not checked | Betfair terms |

## What this means for the review

- **Better free data for a model:** Kalshi 1-minute bid/ask/volume candles give a free spread and close benchmark for EPL O/U lines. That fills a gap that Betfair Basic leaves (no spread, no volume). It does not replace Betfair as the trading venue.
- **Second reference price:** Kalshi and Polymarket prices for the same O/U line can be compared with Betfair's close to test whether the venues disagree and which leads. This is a free version of strategy F.
- **Not a trading venue for this user:** both are blocked in Ireland, so cross-venue arbitrage and any strategy executed on them are out.
- **Caveat on depth:** O/U 2.5 volume on one EPL match was about USD 40,000 to 47,000 per venue. Prices may be less informative than Betfair's on smaller matches [inferred].

## Unknowns

| Item | Resolve by |
|---|---|
| Whether the Kalshi Developer Agreement allows research use of data by a non-customer | Read https://kalshi.com/developer-agreement |
| Kalshi candle history length for settled markets (how far back) | Pull candles for an EPL total from 2025 |
| Coverage of lower leagues on either venue | List series and events by competition |

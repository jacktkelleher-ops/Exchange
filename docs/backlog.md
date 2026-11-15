# Backlog

Ideas and follow-ups outside the current phase.

## Kalshi as a free side source (checked 2026-11-15, before the market survey reframe)

Status: moved into the Phase 1 survey as a second venue (user, 2026-11-15); see `docs/brief.md`. Added checks: `GET /markets/{ticker}/orderbook` returns the full book with no key (HTTP 200) [verified: curl on KXDARTSMATCH-26NOV160800JWATASOU-JWAT]. Kalshi sports tags include Soccer, Tennis, Cricket, Golf, Darts and Table Tennis; no horse racing, greyhound or snooker tags [verified: `/series`]. Authenticated requests are signed with the private key matching the key ID (RSA-PSS SHA-256 or Ed25519) [verified: https://docs.kalshi.com/getting_started/api_keys.md].

Checked by the orchestrator against Kalshi's public API and docs, with no key.

| Finding | Evidence |
|---|---|
| Kalshi has a `KXDARTSMATCH` series ("Darts Match"), plus `KXPDCDARTS` and `KXPREMDARTS` outrights. | [verified: https://api.elections.kalshi.com/trade-api/v2/series] |
| 2,746 darts match markets (two per match), December 2025 to now, mostly since August 2026. | [verified: `/events?series_ticker=KXDARTSMATCH` and `/historical/markets`] |
| Volume per market: median 491 contracts (a contract pays $1), 90th percentile 1,452, max 23,270; 12% traded nothing. | [verified: same, field `volume_fp`] |
| Trades carry microsecond `created_time`, price, `count_fp` and the aggressor side (`taker_side`, `taker_book_side`). Public, no key. | [verified: `/markets/trades`] |
| No order book history: the orderbook endpoints return the current book only. Historical data covers markets, trades and 1-minute, 1-hour and 1-day candles. | [verified: https://docs.kalshi.com/getting_started/historical_data, docs index] |
| Data settled before the cutoff (2026-09-16) is only on `/historical/` endpoints. | [verified: `/historical/cutoff`] |
| Whether Kalshi can be traded from Ireland. | [unknown]; the archived football review said not, unverified |

Possible uses if darts is selected at Gate 1: free in-play price paths and aggressor-side flow, a sandbox for feature code, and a second price source next to Betfair. Too thin for 1 to 60 s order-book trading on its own. The user has a Kalshi API key; it goes in `.env` only if needed (likely only for live WebSocket order books; unverified).

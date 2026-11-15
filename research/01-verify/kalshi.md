# Verify: kalshi

Date: 2026-11-15
Agent: docs-verifier

## Summary (max 5 lines)

Kalshi lists soccer, tennis, cricket, golf, darts and table tennis match markets. No snooker or horse racing series was found under the Sports tags. Order book (bids only, 1 cent tick, depth up to 100), trades (with taker side) and candlesticks (1 min, 1 h, 1 day) are readable without a key. The WebSocket needs API-key headers at connect. The biggest gap is Ireland: Kalshi is reported as restricting Irish users since 2026-07, but I could not read the Member Agreement to confirm it. The Developer Agreement text could not be read either, so research-use terms are unconfirmed.

## Answers

| Question | Answer | Evidence |
|---|---|---|
| 1. Sports listed and match-level volume | Sports tags in the API: Soccer, Tennis, Cricket, Golf, Darts, Table Tennis (also Basketball, Football, Hockey, Baseball, Esports, Motorsport, MMA, Boxing, Chess, Rugby, others). No Snooker tag; `series?tags=Snooker` returned `{"series":null}`. `tags=Horse Racing` also null. | [verified: https://api.elections.kalshi.com/trade-api/v2/search/tags_by_categories] [verified: https://api.elections.kalshi.com/trade-api/v2/series?category=Sports&tags=Snooker] |
| 1a. Darts | `KXDARTSMATCH`: 46 open events dated 15 to 17 Nov 2026 (about 3 days, so roughly 100 per week at this point in the calendar). Each event is one match with two markets. | [verified: https://api.elections.kalshi.com/trade-api/v2/events?series_ticker=KXDARTSMATCH&status=open&limit=200] |
| 1b. Tennis | `KXATPMATCH`: 10 open events, 16 to 17 Nov. `KXATPCHALLENGERMATCH`: 36 open events, 15 to 16 Nov. `KXWTAMATCH` returned 0 open events (that series ticker may be wrong or WTA is off season; not resolved). `KXITFMATCH` exists. Rough scale: tens of match events per week, not hundreds, in a single-day snapshot. | [verified: events?series_ticker=KXATPMATCH and KXATPCHALLENGERMATCH, same base URL] |
| 1c. Cricket | 57 cricket series tagged (T20, ODI, Test, IPL, PSL, Hundred, Sheffield Shield, County Championship, and others). `KXT20MATCH`: 28 open events, 14 to 17 Nov, mostly Indian domestic and Thai T20 matches. About 50 to 60 per week from that series alone in this snapshot. | [verified: series?category=Sports&tags=Cricket] [verified: events?series_ticker=KXT20MATCH&status=open] |
| 1d. Golf | Many series. Match-level markets are head-to-head: `KXPGAH2H` had 2 open events (4th round matchups), also `KXLIVH2H`, `KXGOLFH2H`, `KXPGA3BALL`, `KXPRESCUPMATCH`. Most golf series are outrights or props. Counts depend on tournament weeks. | [verified: series?category=Sports&tags=Golf (truncated at 100000 of 201299 characters)] [verified: events?series_ticker=KXPGAH2H&status=open] |
| 1e. Soccer leagues | Many `*GAME` series. Seen: EPL (`KXEPLGAME`, 20 open events 21 to 29 Nov), Ligue 1 (`KXLIGUE1GAME`), Turkish Super Lig, Europa League (`KXUELGAME`), Danish Superliga, Indian Super League, Liga Expansion, Israeli Liga Leumit, Uruguay Primera, Women's Europa Cup, England Women League Cup, and others. The soccer list was truncated (about 2.4 million characters); the full league set was not enumerated. Each match has several markets (winner, spread, totals, BTTS, correct score). Weekly count per league not measured. | [verified: events?series_ticker=KXEPLGAME&status=open] [verified: series?category=Sports&tags=Soccer (truncated)] [verified: https://api.elections.kalshi.com/trade-api/v2/series?category=Sports] |
| 1f. Table tennis | 13 series tagged, for example `KXTTELITEMATCH`, `KXTABLETENNIS`, `KXLIGAPROMATCH`. `KXTTELITEMATCH` and `KXTABLETENNIS` had 0 open events at fetch time. Other series not checked. | [verified: series?category=Sports&tags=Table%20Tennis] [verified: events?series_ticker=KXTTELITEMATCH&status=open] |
| 1g. Snooker and horse racing | No series found under tags Snooker or Horse Racing. Not searched under "Other" or by keyword. | [verified: series?tags=Snooker, tags=Horse%20Racing returned null] [unknown] for any untagged series |
| 2a. Order book endpoint | `GET /markets/{ticker}/orderbook`, optional `depth` (integer, default 0 = all levels, 1 to 100 = best N per side, outside range gives 400). Response `orderbook_fp` with `yes_dollars` and `no_dollars`, each an array of `[price_dollars, count_fp]` string pairs, ascending, best bid last. No order counts per level. A live call without credentials returned a book (5 NO levels, 4 YES levels), although the docs page also lists a 401 response. | [verified: https://docs.kalshi.com/api-reference/market/get-market-orderbook.md] [verified: https://docs.kalshi.com/getting_started/orderbook_responses.md] [verified: live GET /markets/KXDARTSMATCH-26NOV150800NASPKSED-NASP/orderbook?depth=5, no key] |
| 2b. Asks implied from bids | Yes. "Kalshi's orderbook only returns bids, not asks." A YES bid at X equals a NO ask at 1.00 minus X. | [verified: https://docs.kalshi.com/getting_started/orderbook_responses.md] |
| 2c. Tick and contract size | Darts markets: `price_level_structure` "linear_cent", `price_ranges` 0.0000 to 1.0000 step 0.0100. A contract pays $1. Counts are fixed-point strings with 2 decimals (fractional contracts, for example "1.56"). Other series may use other price structures; only darts was checked. | [verified: live GET /markets?event_ticker=KXDARTSMATCH-26NOV150800NASPKSED] [verified: orderbook_responses.md] |
| 2d. Trade endpoint | `GET /markets/trades`, no auth stated (spec `security: []`), `limit` default 100 max 1000, `cursor`, `ticker`, `min_ts` and `max_ts` in seconds, `is_block_trade`. Fields in Exact fields table. | [verified: https://docs.kalshi.com/api-reference/market/get-trades.md] |
| 2e. Aggressor side | `taker_outcome_side` (yes/no) and `taker_book_side` (bid/ask) are required. `taker_side` is deprecated, not removed before 2026-05-14 per the spec. | [verified: get-trades.md] |
| 2f. Candlestick intervals | `period_interval` allowed values 1 (1 minute), 60 (1 hour), 1440 (1 day). Endpoint `/series/{series_ticker}/markets/{ticker}/candlesticks` shape inferred from path parameters on the page; the exact path was not shown in the fetched text. | [verified: https://docs.kalshi.com/api-reference/market/get-market-candlesticks.md] |
| 2g. Order book history | The Historical Data page lists markets, market_candlesticks, trades, orders and market_positions. No order book history. | [verified: https://docs.kalshi.com/getting_started/historical_data.md] |
| 3. Rate limits, unauthenticated | The page says only "Unauthenticated public requests are subject to separate limits" and gives no number. Public endpoints charge the IP's budget first, even on signed requests. Basic tier (any signed-up account): 200 read and 100 write per second, most requests cost 10 tokens, so about 20 reads per second sustained. 429 with no Retry-After header. Public cacheable responses carry no rate limit headers. The unauthenticated number is [unknown]. | [verified: https://docs.kalshi.com/getting_started/rate_limits.md] |
| 4. WebSocket auth and content | Authentication required to connect: "include API key headers during the WebSocket handshake", even for public channels. Orderbook channel streams `orderbook_snapshot` first, then `orderbook_delta` messages, with `seq` ordering and `clock`. Subscribe by `market_ticker` or `market_tickers`; optional `update_interval_ms` of 100 or 1000, omitted or 0 means real time. Up to 200 concurrent connections at Basic tier. | [verified: https://docs.kalshi.com/websockets/websocket-connection.md] [verified: https://docs.kalshi.com/websockets/orderbook-updates.md] [verified: rate_limits.md] |
| 5. Fees on sports contracts | Series fee metadata for darts: `fee_type` "quadratic", `fee_multiplier` 1. The formula and per-category multiplier are not on the docs pages I could read. Third-party sources report taker fee = round up(0.07 x contracts x price x (1 - price)) to the next cent, with maker fees on some sports and resting orders fee-free on most sports markets; sources conflict. Official Fee Schedule PDF (kalshi.com/docs/kalshi-fee-schedule.pdf) returned 429 and was not read. | [verified: https://api.elections.kalshi.com/trade-api/v2/series/KXDARTSMATCH] [inferred: web search summaries, conflicting] [unknown] for the official multiplier |
| 6. Terms on research use of data | Kalshi Developer Agreement v1.1 exists at https://kalshi-public-docs.s3.amazonaws.com/Kalshi-Developer-Agreement.pdf. The PDF could not be rendered here (no pdftoppm; WebFetch returned binary). A secondary site reports it restricts API data to the member's own trading and bars collection, caching, aggregation, storage or sharing for other purposes without written authorization. This is unverified. Search results also say the agreement requires the user to be a Kalshi Member, and the docs say that using the API means agreeing to it. | [verified: title and version only, PDF metadata] [inferred: sportsapis.dev summary via search] [unknown] for the clauses |
| 7. Ireland | Unclear, leaning restricted. Gambling Insider (via search summary) says that as of 21 July 2026 both Polymarket and Kalshi restricted users in Ireland and that Kalshi already listed Ireland as restricted in its Member Agreement. A May 2026 tracker listed Ireland as available. I could not open the Member Agreement (kalshi.com page returned 404 or 403). The archived football review said not tradable, unverified. | [inferred: web search summaries] [unknown] until the Member Agreement is read |

## Exact fields and operations

Base: https://api.elections.kalshi.com/trade-api/v2

| Name | Where it appears | Type | Meaning | Evidence |
|---|---|---|---|---|
| `GET /markets/{ticker}/orderbook` | REST | operation | Current book only. `depth` 0 to 100. | [verified: get-market-orderbook.md] |
| `orderbook_fp.yes_dollars`, `orderbook_fp.no_dollars` | orderbook response | array of [string, string] | YES bids and NO bids as [price_dollars, count_fp], ascending | [verified: get-market-orderbook.md] |
| `GET /markets/trades` | REST | operation | Public trades | [verified: get-trades.md] |
| `trade_id`, `ticker` | Trade | string | IDs | [verified: get-trades.md] |
| `count_fp` | Trade | string, 2 decimals | Contracts | [verified: get-trades.md] |
| `yes_price_dollars`, `no_price_dollars` | Trade | string, fixed-point dollars | Trade price on each side | [verified: get-trades.md] |
| `taker_outcome_side` | Trade | enum yes, no | Side the taker bought | [verified: get-trades.md] |
| `taker_book_side` | Trade | enum bid, ask | Which side of the book the taker hit | [verified: get-trades.md] |
| `taker_side` | Trade | enum yes, no, deprecated, optional | Old aggressor field | [verified: get-trades.md] |
| `created_time` | Trade | string date-time | Trade time | [verified: get-trades.md] |
| `is_block_trade` | Trade | boolean | Block trade flag | [verified: get-trades.md] |
| `period_interval` | candlestick query | integer enum 1, 60, 1440 | Minutes per candle | [verified: get-market-candlesticks.md] |
| `end_period_ts` | MarketCandlestick | int64 | Candle end, Unix seconds | [verified: get-market-candlesticks.md] |
| `yes_bid`, `yes_ask` | MarketCandlestick | object with `open_dollars`, `low_dollars`, `high_dollars`, `close_dollars` | Bid and ask OHLC | [verified: get-market-candlesticks.md] |
| `price` | MarketCandlestick | object, nullable `open_dollars`, `low_dollars`, `high_dollars`, `close_dollars`, `mean_dollars`, `previous_dollars`, `min_dollars`, `max_dollars` | Trade price stats | [verified: get-market-candlesticks.md] |
| `volume_fp`, `open_interest_fp` | MarketCandlestick | string | Volume and open interest | [verified: get-market-candlesticks.md] |
| `orderbook_snapshot` | WebSocket | message | `sid`, `seq`, `msg` with `market_ticker`, `market_id`, `clock`, `yes_dollars_fp`, `no_dollars_fp` | [verified: orderbook-updates.md] |
| `orderbook_delta` | WebSocket | message | `msg` with `market_ticker`, `market_id`, `clock`, `price_dollars` (string), `delta_fp` (string), `side` (yes or no), `ts_ms` | [verified: orderbook-updates.md] |
| `price_level_structure`, `price_ranges` | Market object | string, array of {start, end, step} | Tick rules | [verified: live GET /markets?event_ticker=...] |
| `fee_type`, `fee_multiplier` | Series object | string, number | Fee model flag | [verified: live GET /series/KXDARTSMATCH] |

## Known facts re-checked

`docs/known-facts.md` has no Kalshi rows. Rows from `docs/backlog.md`:

| Fact | Still holds? | Evidence |
|---|---|---|
| `KXDARTSMATCH` exists, two markets per match | yes | [verified: live series and markets calls above] |
| Trades carry aggressor side, public, no key | yes for fields; the no-key claim rests on the spec `security: []`, not a live trade call | [verified: get-trades.md] |
| Orderbook endpoints return current book only | yes | [verified: historical_data.md; live call returned current book] |
| Orderbook endpoint is public | yes in practice (live call without key worked), but the docs page lists a 401 | [verified: live call] |
| Kalshi tradable from Ireland | could not check; see Q7 | [unknown] |

## Costs

| Item | Amount | Source |
|---|---|---|
| API access, public market data | No fee stated; no key needed for the endpoints tested | [verified: live calls] |
| Trading fee, darts series | `fee_type` quadratic, `fee_multiplier` 1; formula not read | [verified: series/KXDARTSMATCH] |
| Taker fee formula (third party) | 0.07 x contracts x price x (1 - price), rounded up to the cent; about $1.75 per 100 contracts at 50 cents | [inferred: search summary, unconfirmed] |
| Maker fee | Charged on resting orders that fill, on some markets; not cancels. Which sports is conflicting across sources | [verified: help.kalshi.com article 13823805, partial] [inferred] |

## Impact on the spec

- Kalshi gives full-depth current books and public trades with aggressor side. Recording the book requires polling REST or an authenticated WebSocket. [inferred]
- No order book history, so any Kalshi depth data must be recorded forward. [inferred]
- Polling cost: one book per request; at about 20 reads per second sustained on a Basic key, 100 markets polled every 5 s fits easily. The unauthenticated limit is unknown. [inferred]
- The WebSocket gives snapshot plus deltas with `seq` and `clock`, which suits ladder reconstruction better than polling. It needs the private key file. [inferred]
- If Ireland residency blocks account use, the user's key may not be usable, and using the API may breach the agreement. This could make Kalshi recording not allowed. [inferred]

## Unknowns

| Item | What would resolve it |
|---|---|
| Ireland eligibility | Read the current Kalshi Member Agreement restricted jurisdictions list in a browser, or ask Kalshi support. |
| Developer Agreement data clauses | Open the PDF in a browser and read the data use, caching and storage sections. |
| Official fee multiplier and maker fee list for sports | Open kalshi.com/docs/kalshi-fee-schedule.pdf (returned 429 here). |
| Unauthenticated rate limit | Not stated; test with a polite poll and watch for 429, or ask Kalshi. |
| Weekly match counts per soccer league, WTA, table tennis, golf | Poll `/events?series_ticker=...&status=open` per series over a full week. Snapshot counts here are single-day. |
| Snooker and horse racing | Keyword search of `/series` without tags; none found under tags. |
| Candlestick URL path and whether the trades endpoint works with no key | One live GET each with a known ticker. |

## Sources

- https://docs.kalshi.com/llms.txt
- https://docs.kalshi.com/getting_started/rate_limits.md
- https://docs.kalshi.com/getting_started/orderbook_responses.md
- https://docs.kalshi.com/api-reference/market/get-market-orderbook.md
- https://docs.kalshi.com/api-reference/market/get-trades.md
- https://docs.kalshi.com/api-reference/market/get-market-candlesticks.md
- https://docs.kalshi.com/websockets/orderbook-updates.md
- https://docs.kalshi.com/websockets/websocket-connection.md
- https://docs.kalshi.com/getting_started/fee_rounding.md
- https://docs.kalshi.com/getting_started/historical_data.md
- https://api.elections.kalshi.com/trade-api/v2/ endpoints: /series (category and tags variants), /series/KXDARTSMATCH, /search/tags_by_categories, /events (KXDARTSMATCH, KXATPMATCH, KXATPCHALLENGERMATCH, KXEPLGAME, KXT20MATCH, KXPGAH2H, KXTTELITEMATCH, KXTABLETENNIS, KXWTAMATCH), /markets?event_ticker=KXDARTSMATCH-26NOV150800NASPKSED, /markets/KXDARTSMATCH-26NOV150800NASPKSED-NASP/orderbook
- https://kalshi-public-docs.s3.amazonaws.com/Kalshi-Developer-Agreement.pdf (unreadable)
- https://help.kalshi.com/en/articles/13823805-fees.md
- Blocked or failed: https://help.kalshi.com/getting-started/market-specific-fees (429), https://kalshi.com/docs/kalshi-fee-schedule.pdf (429), https://kalshi.com/regulatory/rulebook (404), https://www.gamblinginsider.com/?p=176465 (403)
- Search summaries only (context, [inferred]): Gambling Insider Ireland report, sportsapis.dev, stokastic, rotowire fee articles

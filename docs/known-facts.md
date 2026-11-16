# Known facts

Facts carried over from the archived football review (`archive/football-review-2026-11/`). Each was verified on the date shown. Re-check any fact older than 30 days before a decision depends on it. Phase 1a re-checks all of them for the surveyed sports.

DEV = https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages
SPEC = Betfair Historical Data Feed Specification, `docs/inputs/official/Betfair-Historical-Data-Feed-Specification.pdf`

## Verified (2026-11-15)

| Fact | Source |
|---|---|
| Live app key activation fee GBP 499, KYC required. Delayed key is free. | [verified: DEV/2687105/Application+Keys] |
| Delayed key: Stream API with 2 connections and 200 markets, 3 price levels, no total matched by selection, no BSP near/far price, prices delayed 1 to 180 seconds. | [verified: DEV/2687105/Application+Keys] |
| Delayed key "should be used for development purposes and any functional testing". | [verified: DEV/2687105/Application+Keys] |
| Delayed key can place bets on the live exchange (irrelevant until the execution gate). | [verified: DEV/2687105/Application+Keys] |
| Market data request cap of 200 points per request. | [verified: DEV/2687478/Market+Data+Request+Limits] |
| Bet delay models PASSIVE and DYNAMIC exist; per-sport behaviour is documented for some sports. Darts not checked. | [verified: DEV/2687396/Exchange+Stream+API] |
| Minimum bet EUR 1. | [verified: DEV/2686993/Additional+Information] |
| Historical data from May 2015. Basic: 1-minute last traded price plus market definition. Advanced: 1-second intervals, best available to back and lay, traded volume, traded price-volume (`trd`), `ltp`. Pro: tick by tick, full ladder (`atb`/`atl`), `trd`, market `tv`, `ltp`, BSP. Every plan carries `marketType`, `marketBaseRate`, runner WINNER/LOSER status. | [verified: SPEC p1-4] |
| Basic files use the stream JSON format: lines with `pt` (publish time, epoch ms) and `mc` (market changes) containing `marketDefinition` and `rc` (runner changes). | [verified: archive/football-review-2026-11/scripts/scan_basic.py run on a Basic soccer download] |
| `marketBaseRate` in Basic soccer files was 5.0. It does not show the account's own commission rate. | [verified: same download] |

## Delayed key behaviour (measured on the user's key, 2026-11-15)

| Fact | Source |
|---|---|
| Stream API: one update per market every 180 s (`conflateMs` 180000), full `atb`/`atl` ladders (up to 141 levels seen), `trd`, runner and market `tv`, `ltp`. The "3 price levels" row above does not hold for the stream. | [verified: data/raw/probe/20261115T233458Z.jsonl, scripts/probe/analyse_probe.py] |
| listMarketBook polling refreshes at least every 5 s and returns `totalMatched`, but the data is a variable 5 to 240 s old (poll time minus `lastMatchTime` on busy in-play markets). | [verified: scripts/probe/delayed_poll_probe.py run] |

## Historical Data API behaviour (verified by running it, 2026-11-15)

| Fact | Source |
|---|---|
| Interactive login (username, password, app key; no certificate) works for the user's account and the Historical Data API accepts its session token in an `ssoid` header. | [verified: scripts/historic/my_data.py run] |
| `GET https://historicdata.betfair.com/api/GetMyData` lists purchases (`forDate`, `plan`, `purchaseItemId`, `sport`). POST returns 405; OPTIONS reports `Allow: GET,HEAD,OPTIONS`. betfairlightweight 2.24.0 still uses POST. | [verified: scripts/historic/my_data.py run, curl OPTIONS] |
| `GetCollectionOptions`, `GetAdvBasketDataSize`, `DownloadListOfFiles` allow POST; `DownloadFile` allows GET. | [verified: curl OPTIONS] |
| `GetAdvBasketDataSize` returns 400 for betfairlightweight's body (string dates, missing arrays) and 200 for the portal's body: integer `fromDay/fromMonth/fromYear/toDay/toMonth/toYear` plus `marketTypesCollection`, `countriesCollection`, `fileTypeCollection` arrays. Response: `totalSizeMB`, `fileCount`. | [verified: scripts/historic/sizes.py run; portal bundle https://historicdata.betfair.com/apidocs] |
| Bulk download: `POST api/PreDownload` with a JSON array of basket items returns `{"key": ...}`; `GET api/DownloadBasketFiles?key=<key>` streams an `application/x-tar` of `.bz2` market files under `BASIC/<year>/<Mon>/<day>/<eventId>/`. | [verified: scripts/historic/download.py run on Golf 2026] |
| The user's purchases are all **Basic Plan**: Horse Racing 2020-01 to 2023-05 and 2026-01 to 2026-11 (no 2023-06 to 2025-12); Other Sports 2015-05 to 2026-09; Tennis, Cricket, Golf, Greyhound Racing 2026-01 to 2026-11; Soccer 2026-08 to 2026-10. About 4.50 million market files in total (the earlier 5.35 million came from a horse racing size query that spanned the unpurchased gap). No Advanced or Pro data. | [verified: data/raw/betfair_historic/my_data.json, sizes.json] |
| All purchases downloaded on 2026-11-16 as 22 tars (about 23 GB on disk) under `data/raw/betfair_historic/<sport>/basic-plan/<year>.tar`. Every tar read end to end without error: 4,497,020 `.bz2` market files. Per sport, counts match the `GetAdvBasketDataSize` file counts within 0.05%. | [verified: scripts/historic/download.py log; scripts/historic/verify_tars.py run 2026-11-16] |

## Inferred or unknown (2026-11-15)

| Item | Status |
|---|---|
| Commission packages for Ireland: Basic 2%, Rewards 5%, Rewards+ 8%. | [inferred] |
| Expert Fee tiers and thresholds; does not bind at small scale. | [inferred] |
| Basic historical data is free to download. | [inferred]; the football Basic download was obtained without charge |
| Advanced and Pro prices, and whether darts is covered by each plan. | [unknown] |
| Whether the delayed key returns traded volume (`trd`) on the Stream API. | [unknown]; one search summary said `EX_TRADED` is not returned to delayed keys via `listMarketBook` [inferred] |
| Whether the delay on the delayed key is applied before `pt`, so recorded timestamps are late, or whether update frequency is also conflated. | [unknown] |
| Transaction charge threshold and exemptions. | [unknown] |

## Conflicts between the spec and current access

User decision (Phase 0, 2026-11-15): all rows below are decided at Gate 1. The spec is not narrowed before then.

| Spec requirement | Needs | With free access only |
|---|---|---|
| Full back and lay ladders, history (sec 3, 4) | Pro historical data, or own recordings on a live key | Not available. Basic has no ladder. Delayed key shows 3 levels. |
| Imbalance at top 5 levels and full ladder (sec 4) | Full ladder | Top 3 levels only, from delayed-key recordings. |
| Traded volume at individual prices (sec 3) | Advanced or Pro historical, or live key | Unknown for delayed key. |
| 1 to 60 second prediction horizons (sec 6) | Sub-second or 1-second data with true timestamps | Basic is 1 minute. Delayed key prices are 1 to 180 seconds late; whether that breaks short-horizon research on recorded data is a Phase 1 question. |
| Queue position and fill simulation (sec 8) | Pro tick data (queue inferred from ladder deltas and `trd`) | Not possible from Basic or a 3-level delayed view. |
| In-play reaction to legs, sets, missed doubles (sec 7) | Timestamped sporting data aligned to exchange time | No source verified yet. |
| Live dashboard (sec 10) | Live stream | Delayed key works, with delayed prices. |

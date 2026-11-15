# Verify: tooling

Date: 2026-11-15
Agent: docs-verifier

## Summary (max 5 lines)

betfairlightweight 2.24.0 (2026-09-04, MIT, Python 3.9 to 3.14) and flumine 3.4.1 (2026-11-14, MIT, Python 3.10 to 3.14) are both current and maintained. betfairlightweight has a stream client, a plain-text historical file reader and a delta-applying ladder cache. Its source shows no handling of the stream `img` (full image) flag, and its historical reader does not open .bz2 itself.
flumine ships a recorder strategy that places no orders and writes raw `mcm` lines per market. betfair_data (Rust, MIT, benchmarked at roughly 15 to 100 times faster than betfairlightweight) is unmaintained since April 2022.
Kalshi's official Python SDKs need Python 3.13 or later, so they cannot install in the 3.12 venv. The REST spec marks market, orderbook and trades endpoints as having no security block.
Biggest gap: no GitHub issue or fix reports the Historical Data API changes. The ladder and `img` behaviour is read from source only and has not been run.

## Answers

| Question | Answer | Evidence |
|---|---|---|
| 1a. betfairlightweight latest version and date | 2.24.0, released 2026-09-04. Previous: 2.23.2 (2026-03-16). 2.23.0 and 2.23.1 were yanked. | [verified: https://pypi.org/project/betfairlightweight/] [verified: https://github.com/betcode-org/betfair/blob/master/HISTORY.rst] |
| 1b. Maintenance status | Active. Repo `betcode-org/betfair` last updated 2026-11-13. Release cadence about every 2 to 6 months. 515 stars. Issues tab showed 0 open. | [verified: https://github.com/betcode-org] [verified: https://github.com/betcode-org/betfair] [verified: https://github.com/betcode-org/betfair/issues] |
| 1c. Licence | MIT | [verified: https://pypi.org/project/betfairlightweight/] |
| 1d. Python 3.12 | Yes. requires_python >=3.9, classifiers 3.9 to 3.14, README says tested on 3.9 to 3.14. It is already installed in the project venv. | [verified: https://pypi.org/pypi/betfairlightweight/json] [verified: https://github.com/betcode-org/betfair] |
| 1e. Stream API support | `BetfairStream.subscribe_to_markets` sends a `marketSubscription` with market filter, data filter, optional `initialClk`, `clk`, `conflateMs`, `heartbeatMs`, `segmentationEnabled`. Re-sending the subscription with a new filter is possible through the same call. Reconnect: no automatic reconnect. A socket timeout, error or server close calls `stop()` and raises `SocketError`. The caller must reconnect and pass the saved `initial_clk` and `clk` to resubscribe. `_send` reconnects and re-authenticates only if the stream is not running. `heartbeat()` exists but is not called automatically. A 2.22.0 change added a warning log for unexpected conflation. | [verified: https://raw.githubusercontent.com/betcode-org/betfair/master/betfairlightweight/streaming/betfairstream.py] [verified: https://github.com/betcode-org/betfair/blob/master/HISTORY.rst] |
| 1f. Historical file stream parsing | `HistoricalStream` and `HistoricalGeneratorStream` read a file line by line and pass each line to `listener.on_data()`. They open the path with `open(path, "r")`. No bz2 or gzip handling appears in that file, so .bz2 market files must be decompressed first, or opened by the caller. The generator variant yields `listener.snap()` after each line. | [verified: https://raw.githubusercontent.com/betcode-org/betfair/master/betfairlightweight/streaming/betfairstream.py] |
| 1g. Ladder reconstruction from deltas | The cache keeps each side as an `Available` object. For `atb`, `atl` and `trd` the key is the price. A row with size 0 deletes the price, a non-zero size upserts, and the dict is re-sorted. `batb`, `batl`, `bdatb`, `bdatl` are keyed by level. Back and lay prices come from `atb`/`atl` first, then the best-display, then best-available fields. `trd` rows are also applied as price deltas, and an empty `trd` clears traded. `MarketBookCache.update_cache` contains no `img` handling and never clears runners or ladders. The only full-image code is `fullImage` in the order cache. So the price-delta logic is correct for a continuous stream. Whether a mid-stream `img: true` replacement (for example after resubscribe with a reused cache) drops stale levels is not handled in the source read. Not run against data. | [verified: https://raw.githubusercontent.com/betcode-org/betfair/master/betfairlightweight/streaming/cache.py] for the code read. The `img` risk is [inferred]. Correct output on real files is [unknown] until tested. |
| 1h. Known cache issues | Closed issues #417 (runner total matched incorrect on historical stream, 2021) and #458 (calculate_market_tv uses tv when no ladder update, 2022). betfair_data's README says self-recorded files need `cumulative_runner_tv` False for correct volumes. | [verified: https://github.com/betcode-org/betfair/issues?q=is%3Aissue+GetMyData+OR+GetAdvBasketDataSize+OR+historic] [verified: https://github.com/tarb/betfair_data] |
| 2a. flumine latest version and date | 3.4.1, released 2026-11-14. 3.3.0 yanked ("regression"). Recent changes are Tote market support, BETDAQ support removed in 3.4.0. | [verified: https://pypi.org/project/flumine/] [verified: https://github.com/betcode-org/flumine/blob/master/HISTORY.rst] |
| 2b. Maintenance, licence, Python | Active, repo last updated 2026-11-14, 15 open issues, MIT, requires_python >=3.10, classifiers 3.10 to 3.14, so 3.12 is supported. It depends on betfairlightweight. | [verified: https://github.com/betcode-org/flumine] [verified: https://pypi.org/pypi/flumine/json] |
| 2c. Stream, reconnect, historical | flumine wraps betfairlightweight streams in its framework, and has a simulation mode that replays historical files. Its reconnect behaviour was not read in this pass. | [verified: https://github.com/betcode-org/flumine] for simulation. Reconnect [unknown]; read `flumine/streams` source to resolve. |
| 2d. Pure read-only recorder | Yes. The `MarketRecorder` strategy (examples/strategies/marketrecorder.py) contains no order placement. The example script builds a `BetfairDataStream` filtered to event type 7, GB and IE, WIN markets, registers the strategy and calls `framework.run()`. The framework as a whole supports placing orders, so read-only is enforced by the strategy not placing any, not by a framework mode. | [verified: https://raw.githubusercontent.com/betcode-org/flumine/master/examples/strategies/marketrecorder.py] [verified: https://raw.githubusercontent.com/betcode-org/flumine/master/examples/marketrecorder.py] |
| 2e. How the recorder works | `process_raw_data` appends one compact JSON line `{"op":"mcm","clk":...,"pt":...,"mc":[data]}` to `local_dir/recorder_id/<marketId>` (no extension). On market close it skips single-line files, gzips the file to `<marketId>.gz` in a loader thread, optionally saves the catalogue as `<marketId>.json.gz`, then cleans up expired files. Context keys: `local_dir`, `recorder_id`, `market_expiration` (3600), `remove_file`, `remove_gz_file`, `force_update`, `load_market_catalogue`. An `S3MarketRecorder` subclass uploads to S3. The recorder stores the raw `mc` per update and reports `clk` and `pt`. It does not store `initialClk`, so a restart cannot resume by `clk`. The example uses placeholder login and a log format string missing `s` type characters. | [verified: https://raw.githubusercontent.com/betcode-org/flumine/master/examples/strategies/marketrecorder.py] |
| 3. Other fast parsers | See table below. | see table |
| 4. Issues or fixes for the Historical Data API changes | None found. betfairlightweight HISTORY.rst for 2.20.2 to 2.24.0 does not mention historic, GetMyData or GetAdvBasketDataSize. A GitHub issue search returned 18 issues, all closed, the newest from 2022 (#496). The library source still sends POST for `GetMyData`, and the same body fields for `GetAdvBasketDataSize` as `GetCollectionOptions` (`from_day` style fields, no arrays shown in the summary). A web search found no report. | [verified: https://github.com/betcode-org/betfair/blob/master/HISTORY.rst] [verified: https://raw.githubusercontent.com/betcode-org/betfair/master/betfairlightweight/endpoints/historic.py] [verified: https://github.com/betcode-org/betfair/issues?q=is%3Aissue+GetMyData+OR+GetAdvBasketDataSize+OR+historic] |
| 5. Kalshi Python clients | See Kalshi table below. | see table |

### Q3: other options for parsing Betfair stream files

| Option | Version and date | Maintenance | Licence | Speed claims | Notes |
|---|---|---|---|---|---|
| betfair_data (tarb, Rust, PyO3) | 0.3.4, 2022-04-08 | Unmaintained: 61 commits, last PyPI release April 2022, 14 open issues. | MIT in the GitHub README. The PyPI licence field is empty. | README benchmark on 3 months of Australian racing, M1 MacBook Pro: betfair_data mutable 5m12s (about 70 markets/s, about 534k updates/s); immutable bflw-compatible 6m50s (about 53.5 markets/s); betfairlightweight lightweight=True 1h01m45s (about 6 markets/s); lightweight=False 3h46m39s (about 1.62 markets/s). Claim by the author, not run here. | Reads bz2, gzip, plain .json, and .tar or .zip archives, for official and self-recorded files. Wheels are tagged cp37-abi3, including win_amd64, so a 3.12 install is likely but not tested. Sdist also published. Ladder reconstruction not described in the README. |
| NautilusTrader Betfair loader (Rust) | nautilus-trader 1.231.0, 2026-08-02; crate nautilus_betfair 0.68.0 | Active. | LGPL-3.0-or-later for the Python package. Crate licence not stated on the page read. | None found. | `BetfairDataLoader` reads gz, bz2 and plain newline-delimited stream JSON into Nautilus objects, tracks traded volume, needs the whole Nautilus framework. Python >=3.12,<3.15. |
| betcode-org other projects | betfair, flumine, betdaq-retail (archived), betconnect, faq | No separate parser repo. | | | The org has five public repos. None is a Rust or Polars parser. |
| Polars or Rust parser for stream files | Not found | | | | A search for Polars-based Betfair parsers returned nothing relevant. `[unknown]` that none exists. |
| Betfair Data Scientists tutorials | n/a | n/a | n/a | n/a | Search results list tutorials ("Processing TAR Files 101", "jsonToCsvRevisited"). Context only, not fetched. [inferred] |

### Q5: Kalshi Python clients

| Option | Version and date | Maintenance | Licence | Python | Notes |
|---|---|---|---|---|---|
| kalshi_python_sync (official) | 3.36.0, 2026-11-11 | Active, weekly releases (3.32.0 on 2026-10-06 to 3.36.0). Repo listed as Kalshi/exchange-infra. | LicenseRef-Proprietary | >=3.13 | Generated OpenAPI client. Docs say SDKs may lag the API and recommend the OpenAPI spec as the source of truth. |
| kalshi_python_async (official) | 3.36.0, 2026-11-11 | Active | LicenseRef-Proprietary | >=3.13 | Same. |
| kalshi-python (old official) | 1.x | Deprecated per Kalshi docs. | | | Do not use. |
| pykalshi (unofficial, arshka) | 2.0.0, 2026-07-27 | 164 commits, 133 stars. | MIT | >=3.9 | Not affiliated with Kalshi. REST `get_orderbook()`, `get_trades()`, `.to_dataframe()`, WebSocket `subscribe_orderbook`, `subscribe_trades`, `OrderbookManager` from deltas. |
| Direct REST (no client) | n/a | n/a | n/a | any | The OpenAPI spec lists `GET /markets/{ticker}/orderbook` (`depth` 0 to 100, 0 returns all levels), `GET /markets/trades` (`limit` 1 to 1000, `cursor`, `ticker`, `min_ts`, `max_ts`), `GET /markets`, `GET /events`, `GET /series`, candlesticks. None declares a security block. Servers: `https://external-api.kalshi.com/trade-api/v2`, `https://api.elections.kalshi.com/trade-api/v2`. |

Kalshi rate limits: Basic tier read budget is 200 tokens per second, which is 20 reads per second at the default 10-token cost. Unauthenticated public endpoints are "subject to separate limits" with no figures given. [verified: https://docs.kalshi.com/getting_started/rate_limits.md]

## Exact fields and operations

| Name | Where it appears | Type | Meaning | Evidence |
|---|---|---|---|---|
| `atb`, `atl` | Stream `rc` | array of [price, size] | Available to back/lay, price-keyed deltas, size 0 removes the price | [verified: cache.py URL above] |
| `batb`, `batl`, `bdatb`, `bdatl` | Stream `rc` | array of [level, price, size] | Level-keyed best and best-display ladders | [verified: cache.py URL above] |
| `trd` | Stream `rc` | array of [price, size] | Traded volume by price | [verified: cache.py URL above] |
| `initialClk`, `clk`, `conflateMs`, `heartbeatMs`, `segmentationEnabled` | `marketSubscription` request | clocks as strings; ms as integers | Resubscribe tokens, conflation and heartbeat settings | [verified: betfairstream.py URL above]. Field types are not in the source summary, [unknown] until the Betfair docs are checked. |
| `pt`, `clk`, `op`, `mc` | Recorder output line | | publish time, clock, operation, market changes | [verified: flumine marketrecorder.py URL above] |
| `GetMyData`, `GetCollectionOptions`, `GetAdvBasketDataSize`, `DownloadListOfFiles`, `DownloadFile` | betfairlightweight `endpoints/historic.py` | POST x4, GET x1 as coded | Historic Data API wrappers. The first uses POST in the library | [verified: historic.py URL above] |
| `GET /markets/{ticker}/orderbook`, `GET /markets/trades` | Kalshi REST | see above | Order book and trades | [verified: https://docs.kalshi.com/openapi.yaml] |

## Known facts re-checked

| Fact from `docs/known-facts.md` | Still holds? | Evidence |
|---|---|---|
| betfairlightweight 2.24.0 still uses POST for `GetMyData` | yes, library source still shows POST. No newer release exists (2.24.0 is latest). | [verified: historic.py URL above] [verified: https://pypi.org/project/betfairlightweight/] |
| `GetAdvBasketDataSize` fails with betfairlightweight's body | could not check against the server. The library shares one parameter set across `GetCollectionOptions`, `GetAdvBasketDataSize` and `DownloadListOfFiles`, which is consistent with the string-date, no-array body the orchestrator saw. | [inferred] |
| Basic files use stream JSON with `pt` and `mc` | not re-checked here. The flumine recorder output uses the same envelope. | [verified: marketrecorder.py URL above] |
| Historic downloads are `.bz2` market files | consistent: betfairlightweight does not open bz2 itself, betfair_data and Nautilus do. | [verified: betfairstream.py, https://github.com/tarb/betfair_data] |

## Costs

All packages listed are free. Kalshi's official SDK licence is proprietary (LicenseRef-Proprietary), which is not stated as a cost or an open-source licence. No fees found for Kalshi public endpoints. Betfair costs are out of scope for this topic.

## Impact on the spec

- Stream recorder using betfairlightweight or flumine MarketRecorder is possible on Python 3.12, with no order-placement code. [inferred]
- Reconnect, `initialClk`/`clk` storage and re-requesting images are the caller's job in betfairlightweight, and flumine's own handling is unverified. Gaps in recordings must be detected by the project. [inferred]
- The flumine recorder writes only raw `mc` per market and `clk`/`pt`. Our own ingestion time is not stored by it, which the project rules require. [inferred]
- Replaying recorded and historical files through betfairlightweight's cache gives ladders by delta, but the `img` flag treatment needs a test against real files, including a recording that spans a resubscribe. [inferred]
- At the 5.35 million Basic market files noted in known-facts, betfair_data's speed claim matters but the package is unmaintained. The alternative is a project parser, which is a design decision for the orchestrator. [inferred]
- Kalshi: the official SDKs cannot be installed in a 3.12 venv. Direct REST calls (the endpoints have no declared security) or the unofficial MIT pykalshi (>=3.9) are the options found. The choice is for the orchestrator. [inferred]

## Unknowns

| Unknown | What would resolve it |
|---|---|
| Whether betfairlightweight's cache handles `img: true` replacement correctly | Run `HistoricalGeneratorStream` on a real Pro-like or self-recorded file with a resubscribe, or read the market-level `img` handling in the listener (`streaming/listener.py`, not read here). |
| Whether betfairlightweight issues tab really has 0 open issues | Open https://github.com/betcode-org/betfair/issues in a browser. The fetch result was "Open 0 (0)", which is unusual for a repo of this size. |
| flumine reconnect, `clk` resume and conflation behaviour | Read `flumine/streams/` source and `docs` on the flumine site. |
| Whether betfair_data 0.3.4 imports and parses correctly on Python 3.12 | Install in a scratch venv and run on one Basic file. |
| Whether betfair_data's ladder output matches betfairlightweight | Run both on the same file. |
| Kalshi unauthenticated public endpoint rate limits | Kalshi support or empirical testing, the doc gives no figure. |
| Kalshi WebSocket order-book channel details and snapshot/delta semantics | Read https://docs.kalshi.com/asyncapi.yaml. Not read here. |
| The Historical Data API fix | Betfair's own current historic API documentation or the portal bundle noted in known-facts. No third-party fix found. |
| NautilusTrader crate licence | Check the nautilus_trader repo licence file. |

## Sources

- https://pypi.org/pypi/betfairlightweight/json
- https://pypi.org/project/betfairlightweight/
- https://pypi.org/pypi/flumine/json
- https://pypi.org/project/flumine/
- https://pypi.org/pypi/betfair_data/json
- https://pypi.org/project/betfair-data/
- https://github.com/betcode-org
- https://github.com/betcode-org/betfair
- https://github.com/betcode-org/betfair/blob/master/HISTORY.rst
- https://github.com/betcode-org/betfair/issues
- https://github.com/betcode-org/betfair/issues?q=is%3Aissue+GetMyData+OR+GetAdvBasketDataSize+OR+historic
- https://raw.githubusercontent.com/betcode-org/betfair/master/betfairlightweight/streaming/cache.py
- https://raw.githubusercontent.com/betcode-org/betfair/master/betfairlightweight/streaming/betfairstream.py
- https://raw.githubusercontent.com/betcode-org/betfair/master/betfairlightweight/endpoints/historic.py
- https://github.com/betcode-org/flumine
- https://github.com/betcode-org/flumine/blob/master/HISTORY.rst
- https://github.com/betcode-org/flumine/issues
- https://raw.githubusercontent.com/betcode-org/flumine/master/examples/marketrecorder.py
- https://raw.githubusercontent.com/betcode-org/flumine/master/examples/strategies/marketrecorder.py
- https://github.com/tarb/betfair_data
- https://nautilustrader.io/docs/rust-api-latest/nautilus_betfair/loader/struct.BetfairDataLoader.html
- https://pypi.org/project/nautilus-trader/
- https://docs.kalshi.com/welcome
- https://docs.kalshi.com/python-sdk
- https://docs.kalshi.com/openapi.yaml
- https://docs.kalshi.com/getting_started/rate_limits.md
- https://pypi.org/project/kalshi-python-sync/
- https://pypi.org/project/kalshi-python-async/
- https://pypi.org/project/pykalshi/
- https://github.com/arshka/pykalshi
- Web searches (context only, labelled [inferred]): betfair_data parser, Kalshi Python SDK, Historical Data API changes.

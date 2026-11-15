# Verify: api-access

Date: 2026-11-15
Agent: docs-verifier

DEV = https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages
Method note: the Stream API page (DEV/2687396) is 201,308 characters and WebFetch summarises it in chunks. Field facts below come from those summaries, read via the Confluence REST view of the same page (https://betfair-developer-docs.atlassian.net/wiki/rest/api/content/2687396?expand=body.view). Types are given only where the page states them. Short links (`/wiki/x/...`) returned empty pages and were not usable.

## Summary (max 5 lines)

The delayed key documents a stream forced to `conflateMs` 180000 (3-minute conflation), 3 price levels, 2 connections, 200 markets; Betfair publishes no statement on whether `trd`, `ltp` or runner `tv` are returned to it or whether `pt` is delayed time. Only a live test of the delayed key can settle those.
The Application Keys page says the delayed key returns no `totalMatched` or `EX_ALL_OFFERS` via listMarketBook, yet its own table says market total matched is available: an internal tension to test.
Login (interactive, no certificate) is workable: 24 h session for Ireland, but only keepAlive extends it, and the docs recommend certificate login for unattended bots.
A subscription replaces the previous one on the same connection, so rotating markets within the 200 cap is documented. Terms on storing data: no explicit rule found. Transaction charge: threshold not on any page I could read.

## Answers

| Question | Answer | Evidence |
|---|---|---|
| 1a. Ladder depth on delayed key | "Price Levels: 3" for Delayed, "All" for Live. The page does not say whether this limits `atb`/`atl` or only `batb`/`batl`. Whether EX_ALL_OFFERS is returned on the stream to a delayed key is [unknown]. On listMarketBook, delayed key "does not return ... EX_ALL_OFFERS". | [verified: DEV/2687105/Application+Keys] |
| 1b. Traded volume (`trd`, runner `tv`, market `tv`) | Table: Total Matched by Selection "Not Available" (delayed), Total Matched by Market "Yes". Text: delayed key "does not return traded volume data 'totalMatched' or EX_ALL_OFFERS via listMarketBook". These two statements are not fully consistent. Whether `trd` (EX_TRADED), runner `tv` and market `tv` arrive on the stream for a delayed key is [unknown]. Runner `tv` is most likely the "by selection" item, so likely withheld [inferred]. | [verified: DEV/2687105/Application+Keys] |
| 1c. `ltp` | No source says `ltp` is withheld or granted for the delayed key. [unknown] | none found |
| 1d. Size and nature of delay | "The delay is variable between 1-180 second snapshots." Stream: `conflateMs` "will be 180000 if you access the Stream API using a Delayed App Key". So the stream is a forced 180 s conflation; the 1 to 180 s range is documented for the key generally. How the two combine on the stream is [unknown]. | [verified: DEV/2687105/Application+Keys]; [verified: DEV/2687396/Exchange+Stream+API, subscription fields] |
| 1e. Conflation | `conflateMs` on the ChangeMessage "might be different from what you specified" if the account is delayed. `con`=true on a RunnerChange means more than one change was combined. Causes: slow socket reading, `conflateMs` above 0, or a slow publishing cycle. | [verified: DEV/2687396/Exchange+Stream+API] |
| 1f. Does `pt` show delayed or real time | Docs define `pt` only as publish time, "when the message was sent". No page says whether it is real or delayed time. [unknown]; resolve by recording `pt` against local receipt time on the delayed key. | [verified: DEV/2687396 for the definition]; [unknown] for the delay question |
| 2. Login | Three methods: non-interactive (certificate, "for autonomous apps, bots"), interactive API (JSON endpoint, username and password, 2FA when enabled), interactive desktop (Betfair login pages). Docs recommend non-interactive for bots with no user signing in. Session expiry on .com: 12 h, except UK and Ireland 24 h. Only keepAlive extends a session, API activity does not. keepAlive: `https://identitysso.betfair.com/api/keepAlive`, headers `Accept: application/json`, `X-Authentication` (token), optional `X-Application`; returns `status` SUCCESS or FAIL, `error` INPUT_VALIDATION_ERROR, INTERNAL_ERROR or NO_SESSION. Login cap 100 per minute, then 20-minute block (TEMPORARY_BAN_TOO_MANY_REQUESTS); existing sessions stay valid. Best Practice: handle INVALID_SESSION_TOKEN by logging in again. | [verified: DEV/2687869/Login+Session+Management]; [verified: DEV/2687730/Best+Practice] |
| 3. Subscription filters and fields | See table below. | [verified: DEV/2687396/Exchange+Stream+API] |
| 4a. Connections | "Default is set to 2 connection for Delayed App Keys and 10 connection for Live App Keys." Error `MAX_CONNECTION_LIMIT_EXCEEDED`. | [verified: DEV/2687396] |
| 4b. Markets per subscription | `SUBSCRIPTION_LIMIT_EXCEEDED`: "Set to 200 markets by default on Delayed & Live App Keys"; live raisable on request. It is the only error that does not close the connection. Subscriptions matching no markets are not verified, so wildcards and future market IDs are accepted. Whether the 200 counts markets matched by a filter at any moment is not stated [unknown]. | [verified: DEV/2687396] |
| 4c. Changing or rotating a subscription | "It is possible to subscribe multiple times - each replaces the previous"; "not additive". Each new subscription sends a new initial image and deltas; clear the local cache and use request `id` to ignore messages from the old subscription. With `initialClk` and `clk` and identical criteria you get a delta (`RESUB_DELTA`) rather than a full image. Changed criteria give a new image. | [verified: DEV/2687396] |
| 4d. Heartbeat | `heartbeatMs` bounds 500 to 5000. Default not stated. If nothing changes in that interval the server sends an empty ChangeMessage with `ct`=HEARTBEAT. A message must be sent within 15 seconds of connecting to avoid TIMEOUT. Connections can be closed forcibly, so reconnect logic is needed. | [verified: DEV/2687396]; [verified: DEV/2687730/Best+Practice] |
| 4e. Data request weight | `sum(weight) x number of market ids` must not exceed 200 points per request, else TOO_MUCH_DATA. Applies to listMarketBook, listRunnerBook, listMarketCatalogue, listMarketProfitandLoss. listMarketCatalogue: MARKET_DESCRIPTION 1, RUNNER_METADATA 1, others 0. listMarketBook: no PriceProjection 2, SP_AVAILABLE 3, SP_TRADED 7, EX_BEST_OFFERS 5, EX_ALL_OFFERS 17, EX_TRADED 17, EX_BEST_OFFERS+EX_TRADED 20, EX_ALL_OFFERS+EX_TRADED 32; with exBestOffersOverrides weight x (requestedDepth/3). Example: EX_BEST_OFFERS for 20 markets is 100 points. No per-second request rate stated on these pages. | [verified: DEV/2687478/Market+Data+Request+Limits] |
| 5. Minimal read-only operations | Betting API lists read-only list operations: listEventTypes, listCompetitions, listTimeRanges, listEvents, listCountries, listMarketBook, listMarketCatalogue, listMarketProfitAndLoss, listMarketTypes, listRunnerBook, listVenues, listCurrentOrders, listClearedOrders. Order-changing: placeOrders, updateOrders, replaceOrders, cancelOrders. The read/write grouping is by name; the page does not state it per operation. For a recorder: listEventTypes, listMarketCatalogue (discovery), the Stream API market subscription (`op`=marketSubscription; no order subscription needed), authentication, and keepAlive. None of these place orders. Per-operation parameter pages were not fetched. | [verified: DEV/2687158/Betting+API] for names; [inferred] for the grouping |
| 6. Terms on storing data | No explicit rule on storage, retention or research use found. Stated: application keys are "for personal betting only" and "any commercial use of data or the API must be approved by Betfair"; "Unauthorised commercial usage will be identified & blocked." Runner metadata (Timeform data) has separate terms (via search snippet, not fetched). A forum post by a non-staff member says recording is common and the concern is selling; not official. Betfair Developer Program contact quoted there: bdp@betfair.com. The Developer Program Terms of Use were not reached. | [verified: DEV/2687105/Application+Keys] for the personal and commercial wording; [inferred] for the rest; [unknown] for any retention rule |
| 7. Charges for read-only use | Delayed key: no activation fee; "API access is free for development purposes". Live key GBP 499 one-off (confirmed). Key table: "Transaction Charge Applies: Yes (see Betfair charges page)" for both keys. Betfair's counting rule: "includes all unmatched, matched, cancelled, and lapsed bets", and cancellation adds no transaction. List and stream requests are not mentioned as transactions. The threshold and amounts were not retrievable (Betfair charges page returned HTTP 403). A search summary says 5000 bets per hour and netting against commission; that is [inferred]. No data-request charge appears on any official page fetched. | [verified: DEV/2687105]; [verified: https://support.developer.betfair.com/hc/en-us/articles/20029343399836-Transaction-Charge-how-are-transactions-counted]; [verified: https://support.developer.betfair.com/hc/en-us/articles/115003864531-Are-there-any-costs-associated-with-API-access] |

## Exact fields and operations

All from DEV/2687396/Exchange+Stream+API unless stated. Types are given only where the page stated them.

| Name | Where it appears | Type | Meaning | Evidence |
|---|---|---|---|---|
| `op` = `authentication` (`appKey`, `session`) | first message | string | Must be sent first; within 15 s of connecting | [verified] |
| `op` = `marketSubscription` | request | | Market subscription; replaces the previous one | [verified] |
| `marketFilter.marketIds` | request | Set<String> | Market IDs | [verified] |
| `marketFilter.bspMarket` | request | Boolean | BSP markets | [verified] |
| `marketFilter.bettingTypes` | request | Set<BettingType> | | [verified] |
| `marketFilter.eventTypeIds` | request | Set<String> | Sport IDs | [verified] |
| `marketFilter.eventIds` | request | Set<String> | | [verified] |
| `marketFilter.turnInPlayEnabled` | request | Boolean | | [verified] |
| `marketFilter.marketTypes` | request | Set<String> | | [verified] |
| `marketFilter.venues` | request | Set<String> | | [verified] |
| `marketFilter.countryCodes` | request | Set<String> | Defaults to "GB" when the code cannot be determined | [verified] |
| `marketFilter.raceTypes` | request | Set<String> | | [verified] |
| `marketDataFilter.fields` | request | list of enum | EX_BEST_OFFERS_DISP (sends `bdatb`,`bdatl`), EX_BEST_OFFERS (`batb`,`batl`), EX_ALL_OFFERS (`atb`,`atl`), EX_TRADED (`trd`), EX_TRADED_VOL (`tv`, market and runner), EX_LTP (`ltp`), EX_MARKET_DEF (`marketDefinition`), SP_TRADED, SP_PROJECTED | [verified] |
| `marketDataFilter.ladderLevels` | request | integer 1 to 10 | Levels for depth-based ladders; 1 is best price; default not stated. Empty `bdatb`/`bdatl` array means an update fell outside the levels | [verified] |
| `conflateMs` | request and ChangeMessage | | Conflation; actual value returned; 180000 for a delayed key; bounds and default not stated | [verified] |
| `heartbeatMs` | request and ChangeMessage | | 500 to 5000 bounds | [verified] |
| `segmentationEnabled` | request | | Splits large messages; default not stated | [verified] |
| `initialClk`, `clk` | ChangeMessage | not stated | Sequence tokens for resubscribe delta | [verified] |
| `op` = `mcm` | ChangeMessage | | Market change message | [verified] |
| `id` | ChangeMessage | | Request id of the subscription | [verified] |
| `ct` | ChangeMessage | enum | SUB_IMAGE, RESUB_DELTA, HEARTBEAT, null (update) | [verified] |
| `pt` | ChangeMessage | Long (epoch) | Publish time, "when the message was sent" | [verified] |
| `segmentType` | ChangeMessage | enum | SEG_START, SEG, SEG_END, null | [verified] |
| `status` | ChangeMessage | | null when current; 503 when downstream latency | [verified] |
| `mc` | ChangeMessage | list of MarketChange | Market changes | [verified] |
| `img` | MarketChange | Boolean | true: replace cache item, not delta; null for delta | [verified] |
| `tv` | MarketChange | size | Market total matched, truncated to 2 dp; null if unchanged | [verified] |
| `marketDefinition` | MarketChange | MarketDefinition | Sent in full only when changed | [verified] |
| `rc` | MarketChange | list of RunnerChange | Runner price updates | [verified] |
| `con` | RunnerChange | Boolean | true if several changes were combined | [verified] |
| `tv` | RunnerChange | size | Runner traded volume | [verified] |
| `ltp` | RunnerChange | price | Last traded price | [verified] |
| `trd` | RunnerChange | list of [price, size] | Full traded ladder | [verified] |
| `atb`, `atl` | RunnerChange | list of [price, size] | Full-depth available to back and lay, non-virtual, keyed by price | [verified] |
| `batb`, `batl` | RunnerChange | list of [level, price, size] | Best available to back and lay, non-virtual, keyed by level | [verified] |
| `bdatb`, `bdatl` | RunnerChange | list of [level, price, size] | Best display (virtual) | [verified] |
| `spb`, `spl` | RunnerChange | [price, size] lists | Starting price back and lay | [verified] |
| `spn`, `spf` | RunnerChange | price | Starting price near and far | [verified] |
| size 0 | ladder entry | | Entry removed (example `[0,1.2,0]`) | [verified] |
| MarketDefinition fields | marketDefinition | see below | `id`, `venue`, `raceType`, `settledTime`, `timeZone`, `eachWayDivisor`, `bspMarket`, `turnInPlayEnabled`, `priceLadderDefinition` (CLASSIC, FINEST, LINE_RANGE), `keyLineDefinition`, `persistenceEnabled`, `marketBaseRate` (double), `eventId`, `eventTypeId`, `numberOfWinners`, `countryCode`, `lineMaxUnit`, `lineMinUnit`, `bettingType`, `marketType`, `marketTime`, `suspendTime`, `bspReconciled`, `complete`, `inPlay` (boolean), `crossMatching`, `runnersVoidable`, `numberOfActiveRunners`, `betDelay` (page's listed type conflicts with its "seconds" description), `status` (OPEN, SUSPENDED, CLOSED), `regulators`, `discountAllowed`, `openDate`, `version` (long), `suspendReason` (soccer), `betDelayModels` (PASSIVE, DYNAMIC) | [verified] |
| `hc` | RunnerChange | | Not described for RunnerChange in the text read | [unknown] |
| `SUBSCRIPTION_LIMIT_EXCEEDED`, `MAX_CONNECTION_LIMIT_EXCEEDED` | errors | | See 4a, 4b | [verified] |
| listEventTypes, listMarketCatalogue, listMarketBook, listRunnerBook | Betting API | operations | Read-only discovery and snapshot | [verified: DEV/2687158/Betting+API] names only |
| keepAlive | Identity API | endpoint | See answer 2 | [verified: DEV/2687869] |

## Known facts re-checked

| Fact from `docs/known-facts.md` | Still holds? | Evidence |
|---|---|---|
| Live key GBP 499, KYC required; delayed key free | yes | [verified: DEV/2687105]; support article 115003864531 also says GBP 499 |
| Delayed key Stream API 2 connections, 200 markets, 3 price levels, no total matched by selection, no BSP near/far, delay 1 to 180 s | yes | [verified: DEV/2687105]; connections also [verified: DEV/2687396] |
| Delayed key "should be used for development purposes and any functional testing" | yes, in substance ("development", "functional testing", simulation or practice apps). Exact wording not re-quoted | [verified: DEV/2687105] |
| Delayed key can place bets on the live exchange | yes (table: Bet Placement Yes) | [verified: DEV/2687105] |
| Market data cap 200 points per request | yes | [verified: DEV/2687478] |
| Bet delay models PASSIVE and DYNAMIC; per-sport behaviour documented | yes. Tennis: DYNAMIC delay drops to 1 s for games 3, 5, 7, 9, 11 and set-deciding games. Football: no in-play delay at half time. Others not seen | [verified: DEV/2687396] |
| Minimum bet EUR 1 | could not check (not in scope; Additional Information page read only to char 100000) | |
| Unknown row: delayed key traded volume on the stream | still unknown | see 1b |
| Unknown row: delay applied before `pt`, conflation | partly resolved: conflation is forced to 180000 ms on a delayed key [verified]; `pt` question still unknown | DEV/2687396 |
| Unknown row: transaction charge threshold | still unknown from official pages fetched | see 7 |

## Costs

| Item | Amount | Source |
|---|---|---|
| Delayed app key | free | DEV/2687105 (2026-11-15) |
| Live app key activation | GBP 499 one-off, non-refundable, debited after approval | DEV/2687105; support article 115003864531 |
| Transaction charge | applies to both key types per the table; threshold and amounts [unknown] (charges page HTTP 403; open https://www.betfair.com/aboutUs/Betfair.Charges/#TranCharges2) | DEV/2687105 |
| Data request charge | none found on official pages | |

## Impact on the spec

All [inferred].
- Delayed-key recordings are 3-minute conflated snapshots with at most 3 levels: they cannot support 1 to 60 s horizons, queue or fill simulation, or full-ladder imbalance (spec sections 4, 6, 8). They can still show spread, top-3 depth, market total matched and update cadence at coarse resolution, if `tv` is returned.
- Whether `trd` or runner `tv` arrive is the deciding unknown for volume-at-price (spec section 3). A one-connection live test of the delayed key resolves it.
- Rotating subscriptions on a connection is allowed (replace semantics), so more than 200 markets can be covered over time. At most 200 at once, 2 connections, so about 400 at once.
- Read-only recorder needs no order operations.

## Unknowns

| Unknown | What would resolve it |
|---|---|
| Stream fields actually returned to a delayed key (`trd`, runner `tv`, market `tv`, `ltp`, `atb`/`atl`, depth beyond 3) | Short test subscription on the delayed key, log the raw first messages (no secrets) |
| Whether `pt` is real or delayed time | Same test: compare `pt` with local receipt time and with `conflateMs` |
| Variable versus fixed delay on the stream | Same test: observe interval between updates over minutes |
| Transaction charge threshold and amounts, and whether list or stream calls count | Open the Betfair charges page; ask bdp@betfair.com |
| Terms on storing API data for research | Developer Program Terms of Use (not reached); ask bdp@betfair.com |
| Default values for `heartbeatMs`, `conflateMs` range, `ladderLevels`, `segmentationEnabled` | Full Stream API page, or offline PDF https://betfair-developer-docs.atlassian.net (BetfairAPIDocumentation-OfflineVersion09072026.pdf, attachment on the space) |
| `hc` on RunnerChange; MarketChange type for `tv` | Same offline PDF |
| Per-operation request parameters and per-second rate limits (TOO_MANY_REQUESTS) | Operation pages and the support article "Why am I receiving the TOO_MANY_REQUESTS error?" |
| Search summary said a live fee of GBP 299 on an older page; official page says GBP 499 | Treat 499 as current; the 299 is stale third-party text |

## Sources

- https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages/2687105/Application+Keys (also via REST view)
- https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages/2687396/Exchange+Stream+API (via REST view, chunks 0 to 200000)
- https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages/2687478/Market+Data+Request+Limits
- https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages/2687869/Login+Session+Management
- https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages/2687730/Best+Practice
- https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages/2687158/Betting+API
- https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages/2686993/Additional+Information (first 100000 chars, nothing relevant)
- https://support.developer.betfair.com/hc/en-us/articles/20029343399836-Transaction-Charge-how-are-transactions-counted
- https://support.developer.betfair.com/hc/en-us/articles/115003864531-Are-there-any-costs-associated-with-API-access
- https://support.developer.betfair.com/hc/en-us/articles/115003864671-What-data-request-limits-exist-on-the-Exchange-API
- https://forum.developer.betfair.com/forum/sports-exchange-api/exchange-api/32441-legally-recording-exchange-odds-other-info-premium-account-of-sorts (community, not official)
- https://support.betfair.com/app/answers/detail/betfair-charges (HTTP 403)
- Search results used only as leads: nautilustrader.io Betfair docs (third-party, says delayed key conflates to 3-minute updates, consistent with `conflateMs` 180000)

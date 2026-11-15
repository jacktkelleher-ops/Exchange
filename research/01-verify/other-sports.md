# Verify: other-sports (darts, snooker, cricket, and a short screen of golf, basketball, US sports, esports, table tennis)

Date: 2026-11-15
Agent: docs-verifier

## Summary (max 5 lines)

Betfair's own rules, charges and newsletter pages returned HTTP 403 to every fetch (support.betfair.com, betting.betfair.com), so bet delay by sport, settlement rules, market types and commission are not verified at an official source. A person should open them (see Unknowns).
Darts: PDC calendar and formats are confirmed from Wikipedia pages (34 Players Championships, 15 European Tour events, majors split between sets and legs). Bet delay is 3 seconds in a 2011 Bet Angel post, and a third-party page says darts has 100% passive-bet-delay coverage; both [inferred].
Cricket, snooker, golf, basketball, table tennis, esports: no matched-volume, depth or spread figure found for any time point. Only Basic file counts (cricket 41,905 market files, golf 6,920, Jan to Oct 2026) are verified from the user's own purchase data.
Biggest gap: no measured liquidity or spread for any of these sports. That needs Phase 1b recordings on the delayed key.

## Answers

Source key for this file: OFFICIAL = Betfair Developer docs or historic data pages I fetched. SECONDARY = Wikipedia, Sporting Life, Bet Angel, betting-exchange sites. Archive leads (cricket.md, other.md) are listed at the end with what was confirmed.

### Cross-sport (applies to all sports below)

| Question | Answer | Evidence |
|---|---|---|
| Delayed key limits | Fee none for delayed, GBP 499 for live, delayed price data 1 to 180 s late, 3 price levels, no total matched by selection, total matched by market available, 2 connections and 200 markets on Stream API. | [verified: https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages/2687105/Application+Keys] (fetch tool summary of the table) |
| Live key note | The same page's table lists "Read-only access" as Allowed for the delayed key and Restricted for the live key, and says the live key starts inactive and you must test on the delayed key first. Whether a live key can be used for recording only is therefore a Gate 1 question. | [verified: same URL], summary by fetch tool, re-read the page to confirm wording |
| `betDelay` field | `marketDefinition` carries `betDelay`. Pre-off example shows 0. After the market turns in-play the definition is resent with `"betDelay":1` and `inPlay:true`, and the page notes it "may be greater than 1 for sport markets". `turnInPlayEnabled` is annotated "Does the market go inplay?". | [verified: https://betfair-datascientists.github.io/data/historicStreamFiles/] |
| Passive bet delay | Orders that cannot match immediately get 0 s delay, orders that can match at the current best price keep the normal delay. Rolled out sport by sport. `betDelayModels` appears in `listMarketBook`. One third-party page says it is not yet in the Stream API. | [inferred: https://www.betangel.com/betfair-passive-bet-delay/] and [inferred: https://bettingexchange.net/en/betfair/passive-bet-delay]. The Developer docs Exchange Stream API page (known-facts says it documents PASSIVE and DYNAMIC) rendered as empty text, so I could not read it. |
| Commission, Irish account | Packages Basic 2%, Rewards 5%, Rewards+ 8% on net winnings, "All UK and IRE customers will now be using My Betfair Rewards", switch once a month. Betfair Points no longer set commission for UK and Irish customers. Per-market base rate not stated on that page. Not confirmed at betfair.com, and the user's account package is unknown. | [inferred: https://www.sportinglife.com/free-bets/guides/betfair-exchange-education/how-does-commission-work] (fetched, secondary, no date, footer 2026). Betfair charges page returned 403. |
| Expert Fee, transaction charges | Not found at an official source. | [unknown] |
| Historic Basic data volume (user's own purchases) | Cricket 41,905 market files, 75 MB, 2026-01-01 to 2026-11-01. Golf 6,920 files, 73 MB, same range. Other Sports 2,167,534 files, 8,081 MB, 2015-05 to 2026-09 (darts, snooker, basketball and all other non-listed sports are lumped here, not split). Tennis 203,083. | [verified: C:\Users\jackt\Exchange\data\raw\betfair_historic\sizes.json] (Betfair `GetAdvBasketDataSize` output saved earlier). Per-week derivations below are my arithmetic. |
| Basic files hold what | Basic files are 1-minute last traded price plus market definition (carried over). Every plan carries `marketType`, runner WINNER/LOSER. | [verified via known-facts, SPEC p1-4]; not re-read in this session |

Derived rates from sizes.json (arithmetic by me, files are market files of every market type, not events): cricket about 41,905 / 43.6 weeks = about 960 market files per week in 2026 up to October. Golf about 159 per week. Other Sports about 2.17 million / about 593 weeks = about 3,650 per week averaged over 2015 to 2026, all sports combined. [inferred]. The cricket and golf tar files are on disk (`data/raw/betfair_historic/cricket/basic-plan/2026.tar`, `golf/basic-plan/2026.tar`) and can give exact `marketType` counts per week and `betDelay`, `inPlay`, `turnInPlayEnabled` values in Phase 1c. I did not open them (no tool for binary or bz2 reads in this task).

### 1. Darts (deepest)

| Question | Answer | Evidence |
|---|---|---|
| 1. Event type and market types, in-play | Event type ID and market type names: not verified. `listEventTypes` and `listMarketTypes` will return them on the delayed key. Darts markets go in-play: Betfair's November 2025 newsletter title is "No delays on passive bets for basketball and darts" and an exchange-trading site lists darts among sports in in-play use. Whether sets, legs or 180s markets exist on the exchange: not found. | [unknown] for IDs and market names. In-play and passive status: [inferred: https://www.betangel.com/betfair-passive-bet-delay/] (page title seen in search only for the newsletter, newsletter fetch gave 403). |
| 2a. Bet delay | 3 s for darts in a Bet Angel post dated 9 Dec 2011. Current value must be read from `betDelay` in the stream. | [inferred: https://forum.betangel.com/viewtopic.php?t=5164] (fetched, 2011, may be outdated) |
| 2b. Passive delay | A third-party page lists "Tennis, Baseball, NFL, NBA, Darts already at 100% coverage" for passive bets (0 s for orders that cannot match immediately). For a short-horizon trader this removes the delay on resting orders, not on orders that take the price. | [inferred: https://bettingexchange.net/en/betfair/passive-bet-delay] (fetched, secondary, undated in the extract) |
| 2c. Suspension rules | Not found. Whether the market suspends at leg end, at checkout attempts or only on feed events: [unknown]. | [unknown]. Resolve by recording `status` transitions in delayed-key streams, and Betfair darts rules page. |
| 2d. Settlement (walkover, retirement, abandonment) | Not found at Betfair. A bookmaker's rules say abandoned matches void; that is not Betfair's rule. | [unknown]. Resolve at support.betfair.com exchange market rules, darts section (403 for me). |
| 3. Markets per week, seasonality | 2026 PDC: Players Championships 34 events, 9 Feb to 5 Nov, two on most dates. Challenge Tour 24 events on 14 dates, Development Tour 24 events. European Tour 15 events (first time). More than 135 ranked playing days. Majors and World Series spread across the year (list below). Players Championship Finals 27 to 29 Nov 2026. World Championship 11 Dec 2026 to 3 Jan 2027, 128 players. Number of Betfair match markets per week: [unknown]. Betfair coverage of Challenge and Development Tour: [unknown]. | [verified: https://en.wikipedia.org/wiki/2026_PDC_Pro_Tour] (counts and PC dates), [verified: https://dartsnews.com/pdc/pdc-darts-calendar-2026-135-days-of-pdc-ranked-action-with-main-expansion-confirmed-on-two-fronts] (135 days, 15 Euro Tour), [verified: https://en.wikipedia.org/wiki/2027_PDC_World_Darts_Championship] (dates, 128 players). Wikipedia is secondary. The PDC site (pdc.tv) fetch returned a truncated page, so the primary calendar is not confirmed. |
| 4. Volume, depth, spread by tier and time | No Betfair figure found for any tier or time. Only context: a Lakeside affiliate guide says PDC liquidity is "significantly better" than WDF, and another piece says in-play liquidity in top darts markets "roughly doubled", both unsourced. Bookmaker side: Kambi called the 2025 World final its most bet-on darts event. None is an exchange measure. | [inferred] affiliate pages from search result summaries only (https://www.lakesideworlddarts.co.uk/?p=76, https://www.gamblinginsider.com/news/23739/kambi-reports-record-betting-numbers-during-world-darts-championship-final). Spread and depth at 24 h, 6 h, 1 h, 15 min, 5 min, 1 min and in-play thirds: [unknown]. Resolve by Phase 1b recording. |
| 5. Competition | Third-party darts odds APIs claim leg-by-leg live feeds (one vendor claims under 150 ms, unverified vendor figure). Who feeds Betfair darts prices and whether bots use official scoring feeds: [unknown]. | [inferred: https://odds-api.io/sports/darts] (search summary only, not fetched). |
| 6. Commission | See cross-sport row. | [inferred] |
| 7. Structure | Easier: passive orders have 0 s delay in darts (if the third-party page is right), formats are discrete legs with a fixed 3-dart structure. Harder: a 3 s delay on taking orders if the 2011 value still holds, and a 1 to 180 s delayed key means recorded prices are late. In sets format (World Championship, World Grand Prix, World Masters) market state also changes at set boundaries. | [inferred] |

Darts formats confirmed (all [verified] from Wikipedia unless stated):

| Event type | Dates 2026 | Format | Source |
|---|---|---|---|
| World Championship (2026 and 2027) | 11 Dec to 3 Jan | Sets. Best of 5, 5, 7, 7, 9, 11, 13 sets by round. Non-deciding sets best of 5 legs. Deciding set 2-2 tie-break lead by two, sudden-death leg at 5-5. GBP 5,000,000 prize fund. | https://en.wikipedia.org/wiki/2027_PDC_World_Darts_Championship and https://en.wikipedia.org/wiki/2026_PDC_World_Darts_Championship |
| Grand Slam of Darts | 14 to 22 Nov (in progress today) | Legs only. 48 players in 16 groups of 3, top of each group advances. Group scores like 5-2 suggest first to 5 legs, but that is the fetch tool's inference. GBP 1,000,000 prize fund. | https://en.wikipedia.org/wiki/2026_Grand_Slam_of_Darts |
| Players Championship (34 events) | 9 Feb to 5 Nov | Scores such as 8-6 imply first to 8 legs. GBP 150,000 per event, GBP 15,000 to the winner. | https://en.wikipedia.org/wiki/2026_PDC_Pro_Tour |
| Challenge Tour and Development Tour (24 + 24) | various | Scores such as 5-2 imply first to 5 legs. GBP 20,000 per event, GBP 3,000 to the winner. | same |
| Other majors and World Series | see source | Page marks results with (s) sets or (l) legs but does not define it. Reading of the suffix: World Masters 6-5 sets, World Grand Prix 6-4 sets, Premier League 11-10 legs, UK Open 11-7, World Matchplay 18-9, European Championship 11-8, World Series events 8-5 style. Treat as [inferred]. | https://en.wikipedia.org/wiki/2026_in_PDC |

Tournament tiers on the 2026 PDC calendar as listed by Wikipedia: World Championship, World Masters (28 Jan to 1 Feb), Premier League (5 Feb to 28 May, non-ranked), UK Open (6 to 8 Mar), World Cup of Darts (11 to 14 Jun), World Matchplay (18 to 26 Jul), World Series events (Bahrain, Saudi, Nordic, US, New Zealand, Australian Masters and World Series Finals), World Grand Prix (28 Sep to 4 Oct), European Championship (22 to 25 Oct), Grand Slam (14 to 22 Nov), Players Championship Finals (27 to 29 Nov). 2027 announcements: European Open in Salzburg 18 to 20 Jun, World Matchplay 17 to 25 Jul, World Cup in Frankfurt 10 to 13 Jun. [inferred: search summary of dartsnews.com and Sky Sports, not fetched].

### 2. Snooker

| Question | Answer | Evidence |
|---|---|---|
| 1. Event type, markets, in-play | Event type ID and market types: [unknown]. Snooker is a normal in-play exchange sport per general guides (Match Odds, frame betting exist at bookmakers). Specific exchange markets (frame winner, total frames, handicap): [unknown]. | [unknown]. Bookmaker-side frame markets noted at https://www.sportinglife.com/free-bets/guides/sports/snooker-betting-introduction, not stated for Betfair. |
| 2a. Bet delay | 5 s for snooker in general, 3 s for Power Snooker and Snooker Shoot-out, per a Bet Angel post dated 9 Dec 2011. Current value unchecked. | [inferred: https://forum.betangel.com/viewtopic.php?t=5164] |
| 2b. Suspension, settlement | Retirement, walkover, abandonment, and mid-frame suspension rules: not found. | [unknown] |
| 3. Markets per week, seasonality | Not found. WST calendar not fetched. | [unknown]. Resolve with the WST (worldsnooker.com) calendar and Betfair Basic Other Sports files (marketType). |
| 4. Volume, depth, spread | None found. A Sporting Life guide says exchanges have "more liquidity on betting exchanges during the biggest tournaments". A 2026 World Championship preview noted a three-figure price on the exchange for one player (one anecdote, not depth). | [inferred: https://www.sportinglife.com/free-bets/guides/sports/snooker-betting-introduction] |
| 5. Competition | Not found. | [unknown] |
| 6. Commission | See cross-sport. | [inferred] |
| 7. Structure | Discrete frames, long pauses between shots and frames. Both are my reading of the sport and not evidence about the market. Kalshi does not list snooker (brief). | [inferred] |

### 3. Cricket

| Question | Answer | Evidence |
|---|---|---|
| 1. Event type, markets, in-play | Event type ID and market type names: [unknown]. Match Odds in-play and the existence of derivative markets: [unknown] at an official source. The Betfair Stream API has a cricket subscription op (seen in Nautilus Trader client, third party), and a Betfair September 2025 newsletter title says "data fields added to Cricket API stream". The fields themselves are not read. | [inferred: https://nautilustrader.io/docs/rust-api-latest/nautilus_betfair/stream/client/struct.BetfairStreamClient.html], newsletter fetch 403 (https://betting.betfair.com/betfair-announcements/exchange-news/betfair-exchange-september-newsletter-bet-delays-reduced-in-european-football-and-data-fields-added--010925-1392.html) |
| 2a. Bet delay | 5 s in the 2011 Bet Angel post. Current value unchecked. | [inferred: https://forum.betangel.com/viewtopic.php?t=5164] |
| 2b. Passive delay | Cricket not named among sports with passive delay coverage in the one page I read. | [inferred: https://bettingexchange.net/en/betfair/passive-bet-delay] |
| 2c. Suspension, settlement | Betfair rules for ties, no result, abandonment, Duckworth-Lewis, Test draws: not found. Other operators void on no result, which is not Betfair's rule. | [unknown] |
| 3. Markets per week, seasonality | 41,905 Basic market files Jan to Oct 2026, about 960 per week averaged, all market types and formats. Per-month and per-format split not read (tar not opened). Seasonality: [unknown] until the tar is parsed. | [verified: C:\Users\jackt\Exchange\data\raw\betfair_historic\sizes.json] for the total, derived rate is [inferred] |
| 4. Volume, depth, spread | No Betfair figure verified. Lead claims (IPL final about GBP 150m matched, Test day 1 about GBP 20m) came from blog comments and are not confirmed. | [unknown] |
| 5. Competition | Not found. | [unknown] |
| 6. Commission | See cross-sport. | [inferred] |
| 7. Structure | Delay of 5 s (if unchanged) on taking orders. Ball-by-ball state changes are frequent in T20. A Betfair cricket stream with extra data fields may exist, which would help or hurt depending on who can read it (see Unknowns). | [inferred] |

### 4. Short screen: golf, basketball, US sports, table tennis, esports

| Sport | 1. Event type, markets, in-play | 2. Delay and settlement | 3. Markets per week | 4. Volume, depth, spread | 5. Competition | 7. Structure |
|---|---|---|---|---|---|---|
| Golf | Golf appears as a Betfair event type in a sample response with id "3" (third party). Market names not verified. Outrights, top-N and matchups reported by guides. | 5 s in the 2011 post. Settlement: [unknown]. | 6,920 Basic market files Jan to Oct 2026 (about 159 per week averaged). | Masters 2025: SEN reported 46.38 million (dollar currency unspecified) matched on the Masters market and 24.27 million on one player. No spread or depth. | Data Golf forum users trade it (anecdotal). | Many runners per market, multi-day. [inferred] |
| Basketball | Event type and market types: [unknown]. Basketball is in the third-party passive-delay 100% list as "NBA". | Delay seconds: [unknown]. Passive delay 0 s per third party. | [unknown] (inside Other Sports files). | No Betfair figures. A promo guide says NBA/NFL in-play liquidity is "decent" but below football and tennis. A primer says Matchbook has better US-sport liquidity than Betfair. | Not found. | Fast scoring, passive delay removal helps resting orders. [inferred] |
| US sports (NFL, MLB, NHL) | NFL and Baseball named in the passive-delay 100% list. Others: [unknown]. | [unknown] | [unknown] | No figures. | Not found. | [unknown] |
| Table tennis | Not verified that Betfair lists it as an in-play exchange sport. Vendor blog: 647 to 675 finished matches a day across Czech Liga Pro, TT Cup, TT Elite Series (23 to 25 Oct 2026), median match 16 min (bookmaker-data vendor, not Betfair). | Not found. | Not found for Betfair. | None. | Not found. | Very short matches. [inferred] |
| Esports | A 2023 review says Betfair offered little esports on the exchange. Current availability: [unknown]. | [unknown] | [unknown] | None. | Not found. | [unknown] |

Sources for the screen: [inferred: https://betfairsquare.pages.dev/strategies/in-play-trading] (promo), [inferred: https://www.sen.com.au/news/2025/04/14/usd24m-matched-with-betfair-in-mcilroys-dramatic-masters-triumph] (search summary), [inferred: https://oddspapi.io/blog/table-tennis-odds-api/], [inferred: https://www.esports.net/betting/bonus/betfair]. All from search summaries, not fetched.

## Exact fields and operations

| Name | Where it appears | Type | Meaning | Evidence |
|---|---|---|---|---|
| `betDelay` | `marketDefinition` in stream and historic files | number (integer in examples: 0 and 1) | Bet delay in seconds for the market. Value 0 pre-off, 1 or more once in-play, "may be greater than 1 for sport markets". The page does not define units. | [verified: https://betfair-datascientists.github.io/data/historicStreamFiles/] |
| `inPlay` (written `inplay` in prose on the same page) | `marketDefinition` | boolean | Resent as true when market goes in-play. | [verified: same URL] |
| `turnInPlayEnabled` | `marketDefinition` | boolean | "Does the market go inplay?" | [verified: same URL] |
| `status` | market-level and runner-level | string | Market OPEN or SUSPENDED (suspended during BSP reconciliation, then reopened). Runner ACTIVE, REMOVED means SCRATCHED. | [verified: same URL] |
| `betDelayModels` | `listMarketBook` response | not verified | Marks markets with passive bet delay. A third party says the Stream API does not yet expose it. | [inferred: https://bettingexchange.net/en/betfair/passive-bet-delay] |
| `listEventTypes`, `listMarketTypes` | Betting API | operations | `listEventTypes` "Find[s] the sports associated with markets selected by a MarketFilter." No ID list on the page. | [verified: https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages/2687158/Betting+API] for `listEventTypes` only. `listMarketTypes` not read. |

## Known facts re-checked

| Fact from `docs/known-facts.md` | Still holds? | Evidence |
|---|---|---|
| Live app key activation fee GBP 499, delayed key free | yes | [verified: https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages/2687105/Application+Keys] |
| Delayed key: 2 connections, 200 markets, 3 price levels, no total matched by selection, no BSP near/far, delay 1 to 180 s | yes | same page |
| Delayed key for development and functional testing | yes (page says development and testing, plus simulation apps without live betting) | same page |
| Delayed key can place bets on the live exchange | yes per this page's summary ("Both keys can place bets on the live exchange"); phrasing came from the fetch tool, not a quote | same page |
| Market data cap 200 points per request | could not check | not in scope |
| Bet delay models PASSIVE and DYNAMIC exist; darts not checked | partly | Darts now has a secondary source: 3 s in 2011 and passive 100% coverage ([inferred] both). Developer page for PASSIVE/DYNAMIC rendered empty to me, so not re-verified. |
| Minimum bet EUR 1 | could not check | Betfair support pages return 403 |
| Historical data tiers and Basic format | could not check | not in scope; Basic file counts in sizes.json are consistent with the purchases list |
| Commission packages for Ireland Basic 2%, Rewards 5%, Rewards+ 8% (was [inferred]) | still [inferred], now supported by one fetched secondary page that says UK and Irish customers use My Betfair Rewards | https://www.sportinglife.com/free-bets/guides/betfair-exchange-education/how-does-commission-work |
| Whether the delayed key returns traded volume | could not check. The Application Keys page lists "total matched by market" as available and "total matched by selection" as not available on delayed. That is different from `EX_TRADED` per price. | same Application Keys page |

## Costs

- Live key activation GBP 499, debited after activation. Delayed key none. [verified: Application Keys page, 2026-11-15]
- Commission packages 2% / 5% / 8% for UK and Ireland. [inferred: Sporting Life page, undated]
- Passive-delay related, Expert Fee and transaction charge thresholds: [unknown].
- Basic data already purchased. Advanced and Pro prices for these sports: [unknown].

## Impact on the spec

All [inferred].
- Darts, snooker and cricket delays (3 s, 5 s, 5 s in a 2011 post) are inside the 1 to 60 s target horizons; the horizon floor interacts with the delay if the value is unchanged. The delayed key's 1 to 180 s price lag is larger than any of these delays, so recordings on the delayed key cannot tell what a live trader would have seen at second resolution.
- If passive-delay coverage is true for darts, resting-order strategies face no delay and aggressive ones face the standard delay. That changes which fill model rows in spec section 8 matter. It needs reading `betDelayModels` on live markets.
- Basic files cannot show intra-minute behaviour for any sport here (1-minute resolution), so they can only support counts of markets, `marketType` mix, `betDelay`, `inPlay`, `turnInPlayEnabled` and tournament calendars.
- Darts in-play sporting data (spec section 7) has no verified source. Third-party vendor claims only.

## Unknowns

| Unknown | What would resolve it |
|---|---|
| Betfair rules for darts, snooker, cricket, golf: suspension, walkover, retirement, abandonment settlement | A person opens https://support.betfair.com/app/answers/list/exchange-market-rules (403 to me) and reads each sport's section. |
| Current bet delay per sport, and passive-delay coverage | `betDelay` and `betDelayModels` from `listMarketBook` on the delayed key, and the Developer docs Exchange Stream API page in a browser (rendered empty to me). Betfair newsletters at betting.betfair.com (403). |
| Event type IDs and market type names for darts, snooker, cricket, golf, basketball, esports, table tennis | `listEventTypes` and `listMarketTypes` calls on the delayed key, or `marketType` in the Basic files already on disk. |
| Matched volume, depth and spread by time point and tournament tier | Phase 1b recording on the delayed key (3 price levels, prices 1 to 180 s late) and measurement in Phase 1c. Pro samples if bought. |
| Betfair markets per week for darts, snooker, other sports | Parse `marketType` and event IDs from the Basic tar files (cricket and golf are on disk, darts and snooker need the Other Sports download). |
| Commission package and base rate for the user's account | The user's My Betfair Rewards page and the Rules tab of a market. |
| Whether Betfair's cricket stream carries extra fields and who can use them | Read the Betfair newsletter (September 2025) and the Developer docs cricket subscription page in a browser. |
| Who the automated competition is, for any of these sports | No official source. Phase 1c can look at update frequency and queue behaviour only. |
| Primary PDC calendar (pdc.tv) and WST calendar | Open pdc.tv and worldsnooker.com. |

## Archive lead claims: confirmed or not

| Lead claim (archive cricket.md / other.md) | Status this session |
|---|---|
| Delayed key free, 1 to 180 s delayed snapshots | Confirmed [verified: Application Keys]. The lead's "no bet placement" is contradicted: the page says delayed keys can place bets (carried in known-facts). |
| Live key fee GBP 299 vs 499 | Resolved to GBP 499 [verified: Application Keys]. |
| Commission 2/5/8 for UK and Irish customers | Supported by one fetched secondary page, not confirmed at Betfair. |
| Cricket bet delay "substantial" (Gemini input) | Not confirmed. Only the 2011 5 s figure found. |
| IPL final about GBP 150m, Test day 1 about GBP 20m | Not confirmed, not re-found. |
| Basic data is 1-minute, no volume | Not re-read at an official source this session. |
| Expert Fee tiers 0 / 20 / 40% | Not confirmed. |
| Transaction charge 0.2p above 5,000 per hour and exemption | Not confirmed (the cited betfair-datascientists commission URL returned 404). |
| Golf and US politics are the deep segments | Masters 2025 matched figure found in a search summary (currency unspecified). Politics not checked. |
| Stake minimum GBP 2 (third party) | Not confirmed. |
| Basketball and US sports thin and delay-affected | Promo-site claim found, no data. Passive delay claim for NBA and NFL found at one third party. |

## Sources

Fetched successfully (content read):
- https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages/2687105/Application+Keys
- https://betfair-datascientists.github.io/data/historicStreamFiles/
- https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages/2687158/Betting+API (partial)
- https://www.sportinglife.com/free-bets/guides/betfair-exchange-education/how-does-commission-work
- https://www.sportinglife.com/free-bets/guides/sports/snooker-betting-introduction
- https://forum.betangel.com/viewtopic.php?t=5164
- https://www.betangel.com/betfair-passive-bet-delay/
- https://bettingexchange.net/en/betfair/passive-bet-delay
- https://en.wikipedia.org/wiki/2026_PDC_Pro_Tour
- https://en.wikipedia.org/wiki/2026_in_PDC
- https://en.wikipedia.org/wiki/2027_PDC_World_Darts_Championship
- https://en.wikipedia.org/wiki/2026_PDC_World_Darts_Championship
- https://en.wikipedia.org/wiki/2026_Grand_Slam_of_Darts
- https://dartsnews.com/pdc/pdc-darts-calendar-2026-135-days-of-pdc-ranked-action-with-main-expansion-confirmed-on-two-fronts
- Local: C:\Users\jackt\Exchange\data\raw\betfair_historic\sizes.json and my_data.json
- Local leads: archive/football-review-2026-11/research/01-scan/cricket.md and other.md

Fetch failed (403, 404, empty or blocked): support.betfair.com (exchange-market-rules, betfair-charges, a_id/411), betting.betfair.com newsletters (Sep 2025, Nov 2025), betfair-datascientists.github.io/wagering/commission (404), betfair-developer-docs wiki/x/pAEp, tTAp and Ui8p (empty), pdc.tv/node/10930 (truncated), web.archive.org (blocked), historicdata.betfair.com (title only), wiki.krisyotam.com (525), dartshopper.com (429), promo.betfair.com (404), 2026_PDC_season on Wikipedia (404).

Search results used as [inferred] context only (not fetched): odds-api.io darts page, lakesideworlddarts.co.uk, gamblinginsider Kambi item, sen.com.au Masters item, oddspapi.io table tennis blog, esports.net Betfair review, nautilustrader.io Betfair client, betfairsquare.pages.dev in-play trading page.

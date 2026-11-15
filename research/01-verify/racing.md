# Verify: racing (UK and Irish horse racing on the Betfair Exchange)

Date: 2026-11-15
Agent: docs-verifier

## Summary (max 5 lines)

Betfair's own rules, charges and market-list pages were not readable in this session (support.betfair.com returned 403 or redirected to blocked pages; the Rules page gave 403), so the delay, suspension and 2% racing base rate are only confirmed at secondary sources. Confirmed at the Betfair developer page: live key GBP 499 and delayed-key limits; the delayed key does not return `totalMatched` or `EX_ALL_OFFERS` through `listMarketBook`. The only dataset-backed volume figure is a 2014-16 paper (mean traded volume 122,693 at 10 min out, 520,865 at 1 min out). Largest gaps: current official in-running delay, official racing base rate for an Irish account, volume and spread by time point on current data.

## Answers

| Question | Answer | Evidence |
|---|---|---|
| 1. Market types and which go in-play | Win and Place are separate markets. Win keeps trading in-running ("Win In-Running"). Forecast and reverse forecast markets are said to exist for fields of 8+ runners. A "To Be Placed" market is also described. Which of Place, Forecast and To Be Placed go in-play is [unknown]. API `marketType` codes for these (for example WIN, PLACE, OTHER_PLACE) were not confirmed at an official page. The Basic data files hold `marketType` per market, so this can be read from the user's own Horse Racing Basic files. | [inferred] from secondary guides: https://betfairsquare.pages.dev/sports/horse-racing-markets-explained and search summary of https://www.sportinglife.com/free-bets/guides/betfair-exchange-education/placing-a-back-bet (not fetched). [verified: https://arxiv.org/html/2510.16008] only for UK To-Win markets existing and being briefly suspended when they go in-play. Lead file (H4 each-way, forecast): not confirmed. |
| 2a. Pre-off bet delay | No pre-off delay is documented in anything fetched. [unknown]. | [unknown] |
| 2b. In-play bet delay | Secondary sources say 1 second for horse racing (Gruss glossary: "1 second delay", darts "usually 3 seconds", some football up to 8). A search summary also reported 2 seconds from another guide and a 2018 Betfair Community post saying Betfair planned to remove the racing in-running delay (then 1 second); whether that happened is unconfirmed. Trinity Logic says some UK racing markets at certain tracks can have a different delay or "in-play but no delay" (very rare). Current official figure: not obtained. The Gemini-lead "2s delay" is not confirmed; sources say 1s. | [verified: https://www.gruss-software.co.uk/betting-glossary/delays] that Gruss states 1 second. This is a third-party tool vendor, not Betfair, so the delay value is [inferred]. Also https://www.trinitylogic.co.uk/blog/betfair-in-play-automation-latency-execution/ (third party). Official page not readable: https://support.betfair.com/app/answers/list/exchange-market-rules returned 403. |
| 2c. Suspension at the off | Per Betfair rules as quoted in a search summary of support.betfair.com: Betfair aims to turn horse and greyhound markets in-play at the scheduled off but does not guarantee suspension at that time. If the market is not suspended at the off and is later turned in-play, bets matched after the off stand; otherwise they are void. Unmatched bets are no longer automatically cancelled at the off: the bettor chooses "Take SP" (converts to a non-cancellable SP bet at suspension) or "Keep" (persists in-play). The BSP is calculated by balancing SP and exchange bets when the market is suspended at the off, and BSP bets cannot be cancelled once placed. Non-runner rule: reduction factor of at least 2.5% in a win market or 4% in a place market leads to cancelled unmatched lay bets on other runners (except lay "keep" bets, which are reduced instead). | [verified: https://promo.betfair.com/betfairsp/FAQs_SPrules.html] for BSP reconciliation at suspension at the off, SP bets uncancellable, Take SP and Keep options. The rest (no guarantee of suspension, matched-after-off rule, 2.5% and 4% thresholds) is [inferred] from a search summary of https://support.betfair.com/app/answers/detail/exchange-general-rules/ (fetch returned 403). |
| 2d. Suspension in-running (during the race) | Racing has no scoring events, so no event-driven suspensions were documented. A third-party paper says UK markets are briefly suspended as they go in-play. Anything beyond that (stewards, falls, abandonment) is [unknown]. Void races and BHA rule changes exist (Sandown void-race procedure article seen in search results) but were not read. | [verified: https://arxiv.org/html/2510.16008] "briefly suspended when they go in-play" (authors' software description). Otherwise [unknown]. |
| 3a. Markets per day, UK and Ireland | Lead file does not state a figure. Sourced figures: GB 2025 fixture list 1,460 fixtures (1,468 in 2024); 2026 list 1,458 meetings. Races per fixture not obtained. Academic paper (2014-16, UK To-Win) gives 15 to 30 or 15 to 25 daily races in different places, which is internally inconsistent and old. HorseTrader.live (commercial) says it recorded 2,103 GB and Irish win markets cumulatively, with no per-day figure. Irish fixture and race counts not found. Per-day and per-week counts for UK plus Ireland: [unknown]; they can be computed from the user's Horse Racing Basic files (market count per day by `marketType` WIN and country code). | [verified: https://www.britishhorseracing.com/press_releases/bha-publishes-2025-fixture-list/] 1,460 fixtures and 162 premier racedays, races total not stated. 2026 count 1,458 is from a search summary of a Thoroughbred Daily News item, [inferred]. [verified: https://arxiv.org/html/2510.16008]. [verified: https://horsetrader.live/]. BHA monthly data packs (https://media.britishhorseracing.com/bha/Racing_Statistics/Racing_Data_Packs_By_Month_2025/November25.pdf) were fetched but are compressed PDFs the fetch tool could not decode: a person should open them for races per month. |
| 3b. Daily schedule shape | Not obtained from an official source. Substack author (UK win markets, Mar 2022 to Jan 2026) reports per-race pre-off volume about 40% lower on days with over fifty races than on days with two or fewer meetings, an in-play kink at about forty races, payday effects, and Cheltenham Festival over 250% more volume than average. Time-of-day shape (afternoon, evening cards) is [unknown]; computable from `marketTime` in the user's Basic files. | [verified: https://algorithmicsportsbetting.substack.com/p/two-markets-one-race-degeneracy-and] (free preview only; a single practitioner, chart-based figures). |
| 4. Volume, depth, spread by time | (a) Paper, UK To-Win, Sep 2014 to Aug 2016, 14,421 races, sampled 2 frames per second: mean traded volume 122,693 in the 10th minute before the off and 520,865 in the 1st minute (about 4.2x; the table's units are not stated, and whether this is cumulative or per minute is not clear from the extract); mean unmatched bid plus ask liquidity 2,029 vs 6,974 (about 3.4x); volatility (abs ticks per minute) 642 vs 1,052. No spread figure. (b) Trader guide claims 30 to 50% of total matched volume in the final 10 minutes: no dataset, [inferred]. (c) Substack, 2022 to Jan 2026: volumes fell; early 2026 pre-off and in-play below 70% and 60% of 2022 levels. (d) BHA: GB betting turnover on racing fell 4.3% in 2025 and 10.3% since 2023 (bookmaker and tote betting, not exchange). Average GB field Flat 8.9, jumps 7.84; premier Flat 11.02, jumps 9.41. (e) HorseTrader.live publishes money matched at 15, 10, 5 and 1 min per race and a cumulative GBP 311,757,365 matched before the off over 2,103 recorded GB and Irish win markets (about GBP 148k per market on average, computed here; methodology not given). (f) No source gave in-play matched volume, depth or spread by early, middle and late stage, or tick-level spread by time. Figures for 24 h, 6 h and 1 h before the off: [unknown]. Lead file's "about 280k per race quiet weekday, 3 to 8m Saturday televised, ~100k matched 10 min before" is not confirmed by any source here and conflicts with HorseTrader's average. | (a) [verified: https://arxiv.org/html/2510.16008] (dataset is 10 years old, pre-2017). (c) [verified: https://algorithmicsportsbetting.substack.com/p/two-markets-one-race-degeneracy-and] (single author). (d) [verified: https://www.racingpost.com/news/britain/british-racing-report-2025-good-news-on-attendances-and-prize-money-but-betting-on-the-sport-continues-to-fall-agKp79O8Vz66/]. (e) [verified: https://horsetrader.live/] commercial, methodology unseen. Racing Post also reported average traded in British win markets fell every year since 2016: [verified: https://www.racingpost.com/news/britain/betfair-exchange-to-introduce-new-commission-system-for-2025-as-premium-charge-is-dropped-a7wbg0v4GCAJ]. |
| 5. Competition | No source measures the automated share of racing volume. Gambling Commission: bots are most commonly used in in-play betting to detect and bet stale prices, and to spot arbitrage. Substack author infers bot activity dominates in-play from volume patterns, not measured, and calls a link to automated bettors moving to prediction markets "rampant speculation". Gruss and Trinity Logic describe the in-running delay as a measure against split-second data advantage. A forum post (anecdotal, not fetched) says track-side players are about 1.5 seconds ahead of SIS viewers. Pre-off scalper, syndicate and bookmaker-hedger shares: [unknown]. The paper's own agents are research bots, not market participants. | [verified: https://www.gamblingcommission.gov.uk/licensees-and-businesses/guide/in-play-or-in-running-betting]. [verified: https://algorithmicsportsbetting.substack.com/p/two-markets-one-race-degeneracy-and]. Forum anecdote [inferred] from search summary of https://theracingforum.co.uk/forums/topic/betfair-delay/. |
| 6. Commission, Irish account | Sporting Life (a third party): "customers have the choice to pay either 8%, 5% or 2% commission on Exchange winnings"; UK and Irish customers who do not opt into My Betfair Rewards pay up to 5% by default; "all UK and IRE customers will now be using My Betfair Rewards"; discount based on Betfair Points can apply. That page does not mention a market base rate or a racing-specific rate. Several unofficial sites (search summaries) say UK and Irish horse racing carries a 2% market base rate and most other markets 5%; consistent across sources but not official. Expert Fee from 6 Jan 2025 (Racing Post): based on gross profit over a rolling 52 weeks; nothing under GBP 25,000; 20% for GBP 25,000 to 100,000; 40% above GBP 100,000. The Racing Post article does not mention Ireland, so applicability to an Irish account's currency (EUR) is [unknown]. Transaction charge: [unknown] (not found on any fetched page). `marketBaseRate` is in the Historical Data feed per market, so the base rate for racing can be read from the user's Horse Racing Basic files (in the football Basic download it was 5.0; known-facts says this does not show the account's own commission). | [verified: https://www.sportinglife.com/free-bets/guides/betfair-exchange-education/how-does-commission-work] for 8/5/2 choice and default up to 5%. [verified: https://www.racingpost.com/news/britain/betfair-exchange-to-introduce-new-commission-system-for-2025-as-premium-charge-is-dropped-a7wbg0v4GCAJ] for Expert Fee thresholds. 2% racing base rate: [inferred]. Official page https://support.betfair.com/app/answers/detail/betfair-charges returned 403. |
| 7. Structural features | See "Impact on the spec". Facts: in-running delay reported at 1 second (shortest of the sports named by Gruss) [inferred]; racing has no score events but has non-runner rule effects and a BSP auction at the off; one race lasts minutes; many near-identical markets daily; the Win market is documented as the most volatile in-running by a guide [inferred]; volume trend is falling. | As above. |

## Exact fields and operations

Only the items below were confirmed at an official page. Stream `marketDefinition` fields (`betDelay`, `bspMarket`, `inPlay`, `marketType`, `marketBaseRate`) and `listMarketBook` `ExBestOffersOverrides`/price projections were not read: the Exchange Stream API page fetch returned only navigation and a title, and the Additional Information page returned only navigation. Treat them as [unknown] until a person opens the pages.

| Name | Where it appears | Type | Meaning | Evidence |
|---|---|---|---|---|
| `totalMatched` | `listMarketBook` | not stated | Not returned to delayed app keys | [verified: https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages/2687105/Application+Keys] |
| `EX_ALL_OFFERS` | `listMarketBook` price projection | enum value | Not returned to delayed app keys | same page |
| Delay 1 to 180 s, 2 stream connections, 200 markets, 3 price levels | Application Keys comparison table | n/a | Delayed key limits | same page |

## Known facts re-checked

| Fact from `docs/known-facts.md` | Still holds? | Evidence |
|---|---|---|
| Live key GBP 499, KYC; delayed key free | yes for GBP 499 (the lead file's 299 is wrong) | [verified: DEV/2687105/Application+Keys] |
| Delayed key: 2 connections, 200 markets, 3 price levels, delay 1 to 180 s | yes | same page |
| Delayed key "for development and functional testing" | yes (the page adds simulation and practice applications, not live betting) | same page |
| Delayed key returns traded volume? (listed [unknown]) | Partly resolved: `listMarketBook` does not return `totalMatched` or `EX_ALL_OFFERS`. Stream API `trd` on a delayed key still [unknown]. | same page |
| Commission Basic 2%, Rewards 5%, Rewards+ 8% for Ireland | partly: 8/5/2 choice and default up to 5% confirmed at a third party; names of tiers and Irish switching rules not confirmed officially | https://www.sportinglife.com/free-bets/guides/betfair-exchange-education/how-does-commission-work |
| Expert Fee tiers and thresholds | thresholds confirmed at Racing Post (GBP 25k/100k, 20%/40%); currency for Ireland [unknown] | Racing Post link above |
| Minimum bet EUR 1 | could not check | Additional Information page returned no content |
| Historical data tiers and Basic contents; `marketBaseRate` in files | could not check (local spec PDF unreadable here, no PDF renderer) | n/a |
| Transaction charge threshold | still unknown | n/a |

## Costs

| Item | Figure | Source | Date |
|---|---|---|---|
| Live app key activation | GBP 499 | [verified: DEV/2687105/Application+Keys] | fetched 2026-11-15 |
| Commission choice | 8%, 5% or 2% | [verified: Sporting Life page above], third party | fetched 2026-11-15 |
| Racing market base rate | 2% UK and Ireland | [inferred], unofficial sites | 2026 per search summaries |
| Expert Fee | 0 below GBP 25,000, 20% to GBP 100,000, 40% above, gross profit over rolling 52 weeks | [verified: Racing Post article] | effective 6 Jan 2025 |
| Racing-specific extra charges, transaction charge, premium charge | Premium Charge dropped (Racing Post headline); no racing-specific charge found | [unknown] for others | |

## Impact on the spec

All [inferred].

- Racing has many comparable markets per day and a well-defined time axis (minutes to the off), which suits measurement at the 15 min, 5 min and 1 min points. The 24 h and 6 h points may have thin or no trading for many races; this is a measurement question, not found in any source.
- Volume concentration near the off (4.2x between 10 min and 1 min in 2014-16 data) is the only quantitative support that late-pre-off is where order-book signals have material volume. The data is old and the trend since is downward.
- A 1 second in-running delay (unconfirmed officially) would make the delayed key's 1 to 180 s price lag a much larger disadvantage than the exchange delay itself; recordings from the delayed key cannot show what a trader at the live feed saw. Whether stream timestamps `pt` are already shifted is [unknown] (known-facts).
- Delayed key and `listMarketBook` omit traded volume, so volume-based signals from delayed recordings depend on whether the Stream API returns `trd`; this remains [unknown].
- The user's Horse Racing Basic files (1-minute last-traded price, 2020 to 2026) can give market counts, schedule shape, `marketBaseRate` and BSP-related fields, but not depth, spread or volume.
- Commission at 2% for racing (if confirmed) is lowest of the common rates; the Expert Fee would not bind at EUR 500 scale.

## Unknowns

| Unknown | What would resolve it |
|---|---|
| Current official in-running delay for UK and Irish racing, and pre-off delay | A person opens Betfair's Exchange rules (support.betfair.com exchange-market-rules, "Managing markets in-play") or reads `betDelay` in the stream `marketDefinition` of a live recording |
| Official racing market base rate and Irish package names | Betfair charges page in a browser; or `marketBaseRate` in the Horse Racing Basic files |
| Which racing market types go in-play | `marketType` and `inPlay` fields in the Basic files, or `listMarketTypes` call |
| Races per day and week, UK and Ireland, schedule shape | Count markets by day and `marketTime` in Basic files; BHA and HRI fixture data |
| Matched volume by time point (24 h to 1 min, in-play stages), depth and spread | Advanced or Pro samples, or own recordings on a live key; Basic cannot show this |
| Share of volume from bots, scalpers, syndicates | No public source found; not observable from public market data (project rule: public data does not identify traders) |
| Transaction charge threshold | Betfair charges page |
| Whether delayed key Stream API returns `trd` and how `pt` relates to the delay | A short test recording |
| BHA monthly race counts | Open https://media.britishhorseracing.com/bha/Racing_Statistics/Racing_Data_Packs_By_Month_2025/ PDFs |
| Local Historical Data spec PDF contents (not re-read; no PDF renderer in this session) | Re-read with a PDF tool |

## Sources

Fetched and read:
- https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages/2687105/Application+Keys
- https://promo.betfair.com/betfairsp/FAQs_SPrules.html
- https://www.sportinglife.com/free-bets/guides/betfair-exchange-education/how-does-commission-work
- https://www.racingpost.com/news/britain/betfair-exchange-to-introduce-new-commission-system-for-2025-as-premium-charge-is-dropped-a7wbg0v4GCAJ
- https://www.racingpost.com/news/britain/british-racing-report-2025-good-news-on-attendances-and-prize-money-but-betting-on-the-sport-continues-to-fall-agKp79O8Vz66/
- https://arxiv.org/html/2510.16008 (Convolutional Attention in Betting Exchange Markets; extracted by a summarising tool)
- https://algorithmicsportsbetting.substack.com/p/two-markets-one-race-degeneracy-and (free preview)
- https://www.gruss-software.co.uk/betting-glossary/delays (third party)
- https://www.trinitylogic.co.uk/blog/betfair-in-play-automation-latency-execution/ (third party)
- https://horsetrader.live/ (commercial)
- https://www.gamblingcommission.gov.uk/licensees-and-businesses/guide/in-play-or-in-running-betting
- https://www.britishhorseracing.com/press_releases/bha-publishes-2025-fixture-list/

Fetched but unusable: Exchange Stream API and Additional Information developer pages (navigation only); BHA November 2025 data pack and arXiv PDF (compressed); https://www.betfair.com/aboutUs/Betfair.Charges/ redirected to a page that returned 403; support.betfair.com exchange-market-rules and exchange-general-rules returned 403; betfair-datascientists.github.io/wagering/commission returned 404; support.betfair.com a_id/410 returned 403.

Search only (not fetched): betfairsquare.pages.dev pages (low quality), theracingforum.co.uk threads, community.betfair.com thread on removal of IP delay, thestraight.com.au, Thoroughbred Daily News fixture items, BHA 2026 fixture list.

Lead file confirmation status: commission tiers 2/5/8 partly confirmed (third party); 2% racing base rate not officially confirmed; Expert Fee thresholds confirmed at Racing Post; live key 299 contradicted (499 is correct); 2 s delay not confirmed (sources say 1 s); arXiv 2510.16008 checked (it is a UK To-Win study, 2014-16 data, not a WoM microstructure study of current markets); volume figures (280k, 3 to 8m, 100k) not confirmed.

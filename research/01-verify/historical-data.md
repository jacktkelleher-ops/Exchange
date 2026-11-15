# Verify: historical-data

Date: 2026-11-15
Agent: docs-verifier

## Summary (max 5 lines)

Betfair's support page (updated 2026-09-24) gives per-sport monthly and yearly prices for Advanced and Pro, and they differ by sport (Pro: GBP 230/month Horse Racing and Soccer, down to GBP 79 Other Sports). Advanced is 1-second sampled with a shallow ladder (a secondary source says top 3), Pro is full ladder at the 50 ms API tick rate. I could not read the specification PDF (compressed streams, no PDF renderer), so field-level and ladder-depth claims rest on secondary pages plus the earlier known-facts check. Per-sport start dates for paid plans, in-play inclusion by plan, licence wording, the API rate limit and current free samples are not confirmed.

## Answers

| Question | Answer | Evidence |
|---|---|---|
| 1. Plan granularity and fields | Basic: 1-minute intervals, last traded price, no volume. Advanced: 1-second intervals, price ladder "top 3", volume. Pro: "API tick intervals (50ms)", full price ladder, volume. Betfair Hub text: Advanced 1 second, Pro 50 millisecond, both with volume. Pro is intended to match streaming it yourself. Traded volume by price (`trd`) and market `tv` are in the PRO files; cumulative per price, `tv` = backer stake x 2, no runner total. Timestamp precision: `pt` is epoch ms in the stream format (known-facts); the sampling interval is 50 ms for Pro and 1 s for Advanced. Whether Advanced carries `trd` per price is not confirmed by me (known-facts says yes from the spec). Advanced depth: known-facts says "best available to back and lay"; datascientists page says "top 3". These differ. | [verified: https://betfair-datascientists.github.io/data/usingHistoricDataSite] [verified: https://betcode-org.github.io/faq/using-data] [verified: https://support.developer.betfair.com/hc/en-us/articles/360002401937-How-is-traded-available-volume-represented-within-the-PRO-Historical-Data-files] [unknown] for spec text: PDF could not be decoded |
| 2. Coverage by sport and date | Stream data covers Australian and overseas racing, soccer, tennis, cricket, golf and "other sport". The price table lists Advanced and Pro for Horse Racing, Soccer, Tennis, Cricket, Greyhound Racing, Golf, Other Sports. Darts, snooker are not listed separately; they would fall in Other Sports [inferred]. Service data "provided from April 2015" (support) and "from May 2015 global, October 2016 AU/NZ" (spec summary via Scribd); a datascientists page says "since 2016". Per-sport start dates for Advanced and Pro: [unknown]. In-play inclusion by plan: [unknown]; the Pro stream format carries in-play flags in market definition per known-facts, not re-verified here. | [verified: https://support.developer.betfair.com/hc/en-us/articles/360019984158-Are-bulk-purchase-discounts-available] [verified: https://betfair-datascientists.github.io/modelling/dataSources] [verified: https://support.developer.betfair.com/hc/en-us/articles/360002407732-What-data-is-provided-by-the-Historical-Data-service] [inferred: Scribd summary] |
| 3. Price per plan per sport | See Costs. Prices differ by sport. Prices are for the bulk purchase article; whether the same per-month rate applies when buying one month in the portal is not confirmed. | [verified: bulk-purchase URL above] |
| 4. Free samples | The data-scientists page says samples of each tier can be downloaded from the portal help page (historicdata.betfair.com.au/#/help); the page itself is a JS app and was not readable. Betfair Hub and apps.betfair.com say "Free samples available". A Flemington R7 31/12/25 file is linked from a data-scientists page (tier not stated). In 2020 Betfair ran a free offer (Advanced Jan-May 2020, Pro Apr-May 2020, all sports); no end date stated, current status unknown. Sample sport coverage (any non-racing Pro sample): [unknown]. | [verified: https://betfair-datascientists.github.io/data/usingHistoricDataSite] [verified: https://apps.betfair.com/data/betfair-historical-data/] [verified: https://forum.developer.betfair.com/forum/developer-program/historical-data/30893-free-betfair-exchange-historical-data-offer] [verified: https://betfair-datascientists.github.io/data/historicStreamFiles/] |
| 5. Licence terms | Not found in any fetched page. Betcode FAQ (community, not official) says Betfair allows access "for your personal betting activities" and may ask for evidence of betting activity. A search snippet of a Betfair developer page says data is free for personal use and commercial use has other options; I did not fetch that page, so [inferred]. Redistribution: [unknown]. Betfair support has an article "Does Betfair provide historical data for academic research?" that I could not locate. | [inferred: https://betcode-org.github.io/faq/using-data] [unknown] |
| 6. Request rate limits | Betfair support has an article titled "What are the request rate limits on the Historical Data API?" (linked from two fetched support pages) but I could not fetch its content. [unknown]. The 200-point limit in known-facts is for the live Exchange API, not this service. | [verified that the article exists: https://support.developer.betfair.com/hc/en-us/articles/360000402211-How-do-I-download-and-view-Betfair-Historical-Data] |
| 7. Known-facts re-check | See below. | |

## Exact fields and operations

Only items confirmed from fetched pages. Spec field tables not read.

| Name | Where it appears | Type | Meaning | Evidence |
|---|---|---|---|---|
| `atb` / `atl` | Pro files | array of [price, size] | Available to back / lay, absolute sizes; size 0 means none left | [verified: https://support.developer.betfair.com/hc/en-us/articles/360002401937-How-is-traded-available-volume-represented-within-the-PRO-Historical-Data-files] |
| `trd` | Pro files | array of [price, size] | Traded volume at price, cumulative per price; some updates come from FX rate changes and can lower values | same |
| `tv` | Pro files | number | Traded volume = backer stake x 2 | same |
| `ltp` | known-facts only | number | Last traded price | [inferred: known-facts] |
| `pt` | stream file lines | epoch ms | Publish time | [verified: known-facts, own scan] |
| `GetMyData`, `GetAdvBasketDataSize`, `DownloadListOfFiles`, `DownloadFile`, `PreDownload`, `DownloadBasketFiles` | Historical Data API | HTTP | Per known-facts; not re-fetched | [verified: known-facts, own runs] |

## Known facts re-checked

| Fact from `docs/known-facts.md` | Still holds? | Evidence |
|---|---|---|
| Historical data from May 2015 | Partly. Support page says "from April 2015"; spec summary says May 2015 global, October 2016 AU/NZ. Another page says 2016. Treat start as April or May 2015. | URLs in Answer 2 |
| Basic: 1-minute last traded price plus market definition | Yes (1 minute, last traded price, no volume) | datascientists page |
| Advanced: 1-second, best back/lay, traded volume, `trd`, `ltp` | Granularity yes. Depth conflicts: "top 3" on datascientists page. `trd` in Advanced not confirmed. | datascientists page |
| Pro: tick by tick, full ladder, `trd`, `tv`, `ltp`, BSP | Full ladder, volume, 50 ms yes. BSP not confirmed here. | datascientists page; Scribd summary says Pro has "starting prices and full order books" |
| Advanced and Pro prices unknown | Resolved: see Costs | bulk-purchase page |
| Whether darts is covered by each plan | Still unknown. Darts is not a listed sport; probably Other Sports [inferred] | price table |
| Basic is free (inferred) | Supported: "BASIC data is free of charge" via search summary and betcode page "Basic data is free" | [verified: https://betcode-org.github.io/faq/using-data] |
| User purchases all Basic, ranges (Historical API behaviour table) | Not re-checked; local-run facts, outside web scope | |
| Historical Data API endpoints and 405/GET behaviour | Not re-checked | |

## Costs

Source: Betfair support, "Are bulk purchase discounts available?", marked Updated 2026-09-24. Bulk discounts apply to 12 months for one sport; discount percentage not stated; request via Developer Support with sport, plan and months. The yearly figures below are the listed per-year prices.

| Sport | Advanced / month | Advanced / year | Pro / month | Pro / year |
|---|---|---|---|---|
| Horse Racing | GBP 69 | GBP 699 | GBP 230 | GBP 2,299 |
| Soccer | GBP 69 | GBP 699 | GBP 230 | GBP 2,299 |
| Tennis | GBP 49 | GBP 499 | GBP 150 | GBP 1,499 |
| Cricket | GBP 49 | GBP 499 | GBP 150 | GBP 1,499 |
| Greyhound Racing | GBP 49 | GBP 499 | GBP 150 | GBP 1,499 |
| Golf | GBP 39 | GBP 399 | GBP 99 | GBP 999 |
| Other Sports | GBP 39 | GBP 399 | GBP 79 | GBP 799 |

[verified: https://support.developer.betfair.com/hc/en-us/articles/360019984158-Are-bulk-purchase-discounts-available]. Whether a "month" is a calendar month of market dates (as the user's `forDate` purchases suggest) is [inferred]. Whether the portal charges the same for a single month: [unknown]. Basic: free. 2020 forum post listed normal prices of 2615 (Advanced, 5 months) and 2180 (Pro, 2 months), currency unrendered, historic only.

## Impact on the spec

[inferred] Full ladder, `trd` per price and queue inference (spec secs 3, 4, 8) need Pro. A year of Pro for one sport costs GBP 799 to 2,299, so a single sport-year is bounded; multi-year history multiplies this. Advanced at 1 second may support the 1 to 60 second horizons only coarsely and with at most 3 levels, so imbalance at 5 levels needs Pro. Darts, snooker, and similar are cheapest (Other Sports) if included in that bucket.

## Unknowns

| Unknown | What resolves it |
|---|---|
| Spec field tables, Advanced ladder depth, Advanced `trd`, BSP, in-play handling | Open `docs/inputs/official/Betfair-Historical-Data-Feed-Specification.pdf` in a PDF viewer; read the package comparison table (the page the known-facts calls SPEC p1-4) |
| Per-sport start dates for Advanced and Pro, and which sports exist | Log in at historicdata.betfair.com, open the data selection page, pick Advanced or Pro per sport, and read the available date range and quoted price |
| Single-month portal price, and whether it equals the bulk table | Same portal page; the basket shows a total before purchase |
| Current free samples | historicdata.betfair.com (or .com.au) /#/help page |
| Rate limits | Support article "What are the request rate limits on the Historical Data API?" at support.developer.betfair.com |
| Licence and redistribution | Betfair Terms and Conditions linked in the portal footer; support article on academic research; or ask Developer Support |
| Whether the 2020 free offer or similar is current | Developer Program forum, Historical Data section |

## Sources

- https://historicdata.betfair.com/ (empty JS shell)
- https://historicdata.betfair.com/apidocs (empty JS shell)
- https://betfair-datascientists.github.io/data/usingHistoricDataSite
- https://betfair-datascientists.github.io/modelling/dataSources
- https://betfair-datascientists.github.io/data/historicStreamFiles/
- https://betcode-org.github.io/faq/using-data
- https://support.developer.betfair.com/hc/en-us/articles/360019984158-Are-bulk-purchase-discounts-available
- https://support.developer.betfair.com/hc/en-us/articles/360002407732-What-data-is-provided-by-the-Historical-Data-service
- https://support.developer.betfair.com/hc/en-us/articles/360002407712-How-can-I-access-the-Betfair-Historical-Data-service
- https://support.developer.betfair.com/hc/en-us/articles/360002423271-Where-can-I-view-the-data-specification-for-each-historical-data-package
- https://support.developer.betfair.com/hc/en-us/articles/360002401937-How-is-traded-available-volume-represented-within-the-PRO-Historical-Data-files
- https://support.developer.betfair.com/hc/en-us/articles/360000402211-How-do-I-download-and-view-Betfair-Historical-Data
- https://historicdata.betfair.com/files/Betfair-Historical-Data-Feed-Specification.pdf (binary, not decodable)
- https://forum.developer.betfair.com/forum/developer-program/historical-data/30893-free-betfair-exchange-historical-data-offer
- https://apps.betfair.com/data/betfair-historical-data/
- https://www.scribd.com/document/646857169/Betfair-Historical-Data-Feed-Specification (truncated, secondary)
- Web searches only (not fetched): Betfair Hub historical-data-sources page, Acusick1/odds issue 507, apis.io Betfair plans and rate limits

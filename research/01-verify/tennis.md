# Verify: tennis (Betfair Exchange)

Date: 2026-11-15
Agent: docs-verifier

## Summary (max 5 lines)

Betfair's own rules, charges and newsletter pages all returned HTTP 403 to WebFetch in this session, and the Wayback Machine is blocked. So the tennis rules text, the Irish commission rate and the delay announcements are only [inferred] from search summaries. Developer-docs pages did load: the live key fee, delayed key limits, the 1 to 12 s in-play delay range and the tennis Game betting exclusion from historical data are [verified].
No Betfair-sourced figure for matched volume, depth or spread by tour level was found. The only measured sample is an Italian-exchange study (a separate liquidity pool): 64.9% of 6,477 pre-match tennis markets had nothing matched.
Biggest gap: the exact Exchange tennis rule text and Irish tennis commission rate. A person should open support.betfair.com/app/answers/detail/exchange-tennis-rules/ and the commission page in a normal browser.

## Answers

| Question | Answer | Evidence |
|---|---|---|
| 1. Market types and which go in-play | Match Odds is the main market and its code MATCH_ODDS is confirmed as an example code in the docs [verified: https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages/2687465/Betting+Type+Definitions]. Other tennis markets named by a third-party affiliate guide: Set Betting, Set Winner / Set Score, Total Games (often about 22.5), and Game Betting / Set Game Score with very low liquidity [inferred: https://betfairsquare.com/sports/tennis]. Exact marketType codes for these: [unknown]; call listMarketTypes with event type ID 2 (a search summary gave "2" as tennis from a community R example [inferred]). Tennis "Game betting" markets are not in Betfair historical data [verified: https://support.developer.betfair.com/hc/en-us/articles/360017615137-Which-markets-aren-t-available-via-Historical-Data]. Which markets go in-play: the guide implies all of the above do [inferred]; not confirmed by an official page. | see cells |
| 2a. Pre-match and in-play bet delay | Official developer FAQ: "In-play markets usually carry a time delay varying from 1-12 seconds"; the delay applying to placeOrders/replaceOrders is in `betDelay` in listMarketBook, and in the Market Definition on the Stream API [verified: https://support.developer.betfair.com/hc/en-us/articles/360002825652-Why-do-you-have-a-delay-on-placing-bets-on-a-market-that-is-in-play]. A fixed tennis figure is not given officially. Third-party figures conflict: 5 s (affiliate guide [inferred: https://betfairsquare.com/sports/tennis]), 3 s (a Bet Angel forum thread dated 2020-01-29, secondhand report of a Betfair Support remark [verified that the thread says this: https://forum.betangel.com/viewtopic.php?t=20415]; whether it is still true is [unknown]). Pre-match delay is zero for ordinary markets [unknown for tennis; not found]. | see cells |
| 2b. Reduction at set games | Betfair's August 2025 newsletter (search summary only, page 403) says delay on tennis drops to 1 second when the end-of-game or end-of-set signal is received, for games 3, 5, 7, 9, 11 and games that decide a set [inferred: https://betting.betfair.com/betfair-announcements/exchange-news/betfair-exchange-august-newsletter-290725-1392.html]. The January 2026 newsletter says dynamic delay testing restarted on some Challenger events, so it may be a test and not a permanent rollout [inferred: https://betting.betfair.com/betfair-announcements/exchange-news/betfair-exchange-january-newsletter-whats-ahead-for-2026-270126-1392.html]. The developer docs confirm that bet delay models PASSIVE and DYNAMIC exist as a filter value [verified: https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages/2687465/Betting+Type+Definitions]. Per-sport behaviour was not on the fetched pages. | see cells |
| 2c. Passive bets | The August 2025 newsletter reports passive bet delay enabled across 100% of tennis and baseball competitions, so orders that make a price skip the delay [inferred: same August newsletter URL; page 403]. | |
| 2d. Suspension rules | Official rule text not obtained. Developer docs list market statuses but the fetched page was truncated before them [unknown]. A short-delay in-play FAQ states the delay exists "to allow customers to cancel unmatched orders" on a change in market conditions [verified: URL in 2a]. Whether Betfair suspends tennis on each point or only on specific events: [unknown]. | |
| 2e. Retirement and walkover settlement | Search summary of the Exchange tennis rules page: if a player retires or is disqualified the other player is the winner, but if less than one set has been completed all bets on that match are void; a retirement during a game or set voids game and set markets except those already unconditionally determined [inferred: https://support.betfair.com/app/answers/detail/exchange-tennis-rules/]. The Exchange general rules are reported to say match odds bets are void if a match is not completed for any reason [inferred: https://support.betfair.com/app/answers/detail/exchange-general-rules/]; how this fits with the tennis page is unresolved. Walkover treatment on the Exchange: [unknown]; the walkover-void statement in the scan lead was not confirmed. Sportsbook tennis rules (first set cutoff) are separate and do not apply to Exchange bets [inferred: same search summary]. | |
| 3. Markets per day and week by tour level | Event counts found, not market counts. ATP Challenger 2026: 263 tournaments (6 C175, 39 C125, 33 C100, 104 C75, 81 C50) [verified: https://en.wikipedia.org/wiki/2026_ATP_Challenger_Tour]. ATP Tour 2026: 59 tournaments, 9 Masters 1000, 16 ATP 500, 29 ATP 250 (the other 5 include the ATP Finals and Next Gen Finals) [verified: https://www.atptour.com/en/news/2026-atp-tour-calendar-announced]. WTA 2026: over 50 tournaments, 10 WTA 1000, 17 WTA 500, 22 WTA 250, plus four Grand Slams [verified: https://www.wtatennis.com/news/4377748/wta-announces-2026-tour-calendar]. ITF World Tennis Tour 2025: 634 men's and 627 women's tournaments in 77 countries [verified: https://tennistourtalk.com/128923/itf-world-tennis-tour-2025-in-review, a news site quoting the ITF; the ITF original was not fetched]. Matches per day and week per tier, and how many have a Betfair market: [unknown]. A search summary said lower-tier matches often have no Exchange market at all [inferred: affiliate and blog sources]. Seasonality: Grand Slam fortnights, Masters 12-day formats (seven of the ten WTA 1000 use a 12-day format [verified: WTA URL above]). Month-by-month counts: [unknown]. | see cells |
| 4. Matched volume, depth and spread by tour level and time | No Betfair UK/Irish exchange measurement found. Anecdotal, unsourced figures from affiliate guides: Grand Slam round 1 top-30 matches £500K to £2m; Wimbledon men's QF £8m to £15m; 1000-level round of 16 £200K+; Match Odds 70 to 80% of a match's volume; £200 to £500 stakes in majors do not move the price [inferred: https://betfairsquare.com/sports/tennis, affiliate]. Another search summary gave £150K to £500K on Set Betting in a Slam QF, which is not consistent with the above [inferred]. Only measured sample: Betfair Italian exchange, 11,073 pre-match Match Odds markets (6,477 tennis), 31 Jul to 19 Oct 2026, four snapshots a day: 64.9% of tennis markets had zero traded, 14.5% over EUR 100, 3.3% over EUR 1,000, 1.0% over EUR 3,000, 0.3% over EUR 10,000, median EUR 0 (ATP/WTA main-tour median market EUR 6 traded, said by the article; Challenger "three in four" and ITF "nearly nine in ten" had nothing matched) [verified that the article says this: https://theoddslab.com/articoli/tennis-trading-betfair/]. The Italian exchange is a separate, ring-fenced liquidity pool, so these numbers do not describe the pool a UK or Irish account sees [inferred]. The study gives no spreads, no in-play data and no time-before-start profile. Spread by tier and time: [unknown]. | see cells |
| 5. Competition, latency | Evidence is vendor or anonymous. UK Gambling Commission: courtsiding is "using or transmitting information from a live sporting event for the purpose of gambling" and may breach event entry terms; operator delay varies with strategy and the latency of its data source [verified: https://www.gamblingcommission.gov.uk/licensees-and-businesses/guide/in-play-or-in-running-betting]. A Bet Angel thread (2020) reports that traders worried courtsiders gain from a short delay and that market making is fragile because courtsiders can take leftover stakes [verified that the thread says this: https://forum.betangel.com/viewtopic.php?t=20415; opinions, not data]. A 2026-11-03 Substack post claims human scouts add 3 to 7 s, TV buffer 5 to 15 s, court-side radio 150 to 400 ms, and that official feeds to sportsbooks have largely closed the gap; it never mentions Betfair and cites no source [inferred: https://sharpbetsclub.substack.com/p/court-siding-rf-transmission-nodes]. A bot-vendor blog (affiliate) says tennis point data needs a paid feed (Live Tennis API about $10, $30 or $100 a month by plan; only the top plan has WebSocket), and shows a median score latency of about 105 ms from one 45-second probe on one match [inferred: https://botblog.co.uk/live-tennis-api-exchange-bots/]. The affiliate guide says Bet Angel is used by most full-time tennis traders [inferred: https://betfairsquare.com/sports/tennis]. Identity and volume share of automated traders on Betfair tennis: [unknown]. The official Betfair in-play data feed for tennis and its latency: [unknown]. | see cells |
| 6. Commission for an Irish account on tennis | Formula: Net Winnings x Market Base Rate x (100% minus Discount Rate); base rate depends on country; My Betfair Rewards package sets it for opted-in users (search summary of the support page [inferred: https://support.betfair.com/app/answers/detail/413-exchange-what-is-commission-and-how-is-it-calculated/], page 403). Third-party sources put the Irish base rate at 5% and tennis at 5% standard, with one saying 3% on Grand Slams [inferred: https://betfairsquare.com/guides/betfair-commission-explained and others via search, unconfirmed]. Basic 2%, Rewards 5%, Rewards+ 8% from the scan lead: not confirmed, and it is not consistent with the 5% base figures [unknown]. Historical Basic soccer files carried `marketBaseRate` 5.0 [verified: docs/known-facts.md, from a real download]. Tennis `marketBaseRate` can be read from the user's Basic tennis files, which are already downloaded [inferred; not done, tools limited to Read/Write/Glob/web]. The user's account-level rate can only be read in the account's own commission display. | see cells |
| 7. Structural factors | See "Impact on the spec". | |

## Exact fields and operations

| Name | Where it appears | Type | Meaning | Evidence |
|---|---|---|---|---|
| `betDelay` | listMarketBook response; Market Definition on the Exchange Stream API | not stated on fetched page | delay in seconds applied to placeOrders/replaceOrders for that market | [verified: https://support.developer.betfair.com/hc/en-us/articles/360002825652-Why-do-you-have-a-delay-on-placing-bets-on-a-market-that-is-in-play] |
| `betDelayModels` | market filter | list of strings, e.g. PASSIVE, DYNAMIC | restricts to markets with those delay models | [verified: https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages/2687465/Betting+Type+Definitions] |
| `marketTypeCodes` | market filter | list of strings, e.g. MATCH_ODDS | restricts by market type; full list via listMarketTypes | [verified: same page] |
| `inPlayOnly` | market filter | boolean | restrict to markets currently in play (or not) | [verified: same page] |

Tennis marketType codes other than MATCH_ODDS: [unknown].

## Known facts re-checked

| Fact from `docs/known-facts.md` | Still holds? | Evidence |
|---|---|---|
| Live app key activation fee GBP 499, KYC required; delayed key free | yes for fee and delayed key free (KYC not on the fetched text) | [verified: https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages/2687105/Application+Keys] |
| Delayed key: Stream API 2 connections, 200 markets, 3 price levels, no total matched by selection, no BSP near/far, prices 1 to 180 s delayed | yes | same page |
| Delayed key for development and testing; read-only allowed on delayed key, restricted on live key | yes | same page |
| Delayed key can place bets on live exchange | yes | same page |
| Bet delay models PASSIVE and DYNAMIC exist | yes (as a filter value); per-sport behaviour not on the page fetched | [verified: Betting Type Definitions URL above] |
| Minimum bet EUR 1 | could not check (page truncated) | https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages/2686993/Additional+Information |
| Market data request cap 200 points | could not check | not fetched |
| Historical data plans, Basic content, coverage dates | could not check, apart from tennis Game betting being excluded (yes) | [verified: https://support.developer.betfair.com/hc/en-us/articles/360017615137-Which-markets-aren-t-available-via-Historical-Data] |
| Commission packages Basic 2%, Rewards 5%, Rewards+ 8% | could not confirm | support page 403 |
| Expert Fee and transaction charge details | could not check | support pages 403 |

## Costs

- Live app key GBP 499 activation, debited from the Betfair account [verified: Application Keys URL above, 2026-11-15]. Delayed key free.
- Commission: formula verified only via search summary; Irish tennis rate not confirmed (see Answer 6).
- Tennis data feeds for point-by-point scores, vendor pricing: about $10, $30, $100 a month (Live Tennis API plans) [inferred: https://botblog.co.uk/live-tennis-api-exchange-bots/, affiliate, 2026].
- Historical Advanced and Pro prices: not checked in this session.

## Impact on the spec

All [inferred].
- Harder: matched volume is concentrated. The only measured sample shows most tennis Match Odds markets with nothing traded pre-match, so short-horizon order-book work likely only has data on a small share of matches (main tour, later rounds, Slams). Share on the main UK/IE exchange is unmeasured.
- Harder: in-play delay of 1 to 12 s (tennis figure unconfirmed, possibly 1 s at game ends) plus a delayed key whose prices are 1 to 180 s late means in-play recordings from the delayed key cannot show 1 to 60 s dynamics reliably.
- Possibly easier: passive orders reportedly skip the delay on all tennis, so resting orders are the less penalised style; cancel and join queue behaviour could be studied. Unconfirmed because the newsletter was not fetched.
- Harder: in-play moves are driven by point and game events from feeds the retail trader does not have; competitors with court-side or fast feeds are reported by vendor sources only.
- Tennis Game betting markets are absent from Betfair history, so game-level order-flow work needs own recordings.
- Settlement risk: retirement after one set settles as a result, producing full losses on positions on the retiring player; ITF and lower tiers have more retirements (not measured).
- Spec section 7 in-play reaction work needs timestamped point data aligned to exchange time; no verified free source.

## Unknowns

| Unknown | What resolves it |
|---|---|
| Exact Exchange tennis rule text (retirement, walkover, suspension, game markets) | Open https://support.betfair.com/app/answers/detail/exchange-tennis-rules/ and exchange-general-rules in a browser (WebFetch got 403) |
| Irish tennis commission rate and whether Rewards discount applies | Account commission display; the commission support page; `marketBaseRate` in the user's tennis Basic files |
| Current tennis bet delay and dynamic delay status | Read `betDelay` and `betDelayModels` from live markets with the delayed key; Betfair newsletters in a browser |
| Tennis marketType codes | listMarketTypes for event type ID 2 |
| Matched volume, depth, spread by tier and time | Own recordings, Basic history (1-minute last price, market definition), or Advanced/Pro samples |
| Markets per day per tier that have a Betfair market | Count markets from the user's 2026 Basic tennis files |
| Courtsider and bot share, official feed latency | No public source found; own measurement of reaction time after score events with a paid feed |
| Seasonality by month | Count markets per month in the user's Basic tennis data |

## Claims from the scan lead (archive/football-review-2026-11/research/01-scan/tennis.md)

| Lead claim | Status |
|---|---|
| Live key GBP 499 | confirmed (Application Keys page) |
| Delayed key 1 to 180 s snapshots | confirmed |
| Betfair in-play delay 1 to 12 s, `betDelay` field | confirmed |
| Game betting not in historical data | confirmed (tennis Game betting) |
| Passive bets no delay on tennis; dynamic delay to 1 s at game end; Challenger tests Jan 2026 | not confirmed at source; reconfirmed only by search summary quoting the newsletters (pages 403) |
| Retirement voids if less than one set; game and set markets void | not confirmed at source; same search summary of the rules page |
| Walkover void; Match Odds void if not completed for any reason | not confirmed |
| Commission Basic 2%, Rewards 5%, Rewards+ 8%; tennis 5% | not confirmed; third-party sources say 5% base and tennis 5%, so the 2% basic claim is doubtful |
| Liquidity figures from affiliate guide | still affiliate, unsourced; one figure (1000 round of 16 £200K+) repeated |
| ITF and Challenger thin | supported only by Italian-exchange sample and guides |
| Expert Fee, transaction charges, historical prices | not checked this session |

## Sources

Fetched successfully:
- https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages/2687105/Application+Keys
- https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages/2687465/Betting+Type+Definitions
- https://support.developer.betfair.com/hc/en-us/articles/360002825652-Why-do-you-have-a-delay-on-placing-bets-on-a-market-that-is-in-play
- https://support.developer.betfair.com/hc/en-us/articles/360017615137-Which-markets-aren-t-available-via-Historical-Data
- https://en.wikipedia.org/wiki/2026_ATP_Challenger_Tour
- https://www.atptour.com/en/news/2026-atp-tour-calendar-announced
- https://www.wtatennis.com/news/4377748/wta-announces-2026-tour-calendar
- https://tennistourtalk.com/128923/itf-world-tennis-tour-2025-in-review
- https://www.gamblingcommission.gov.uk/licensees-and-businesses/guide/in-play-or-in-running-betting
- https://forum.betangel.com/viewtopic.php?t=20415
- https://theoddslab.com/articoli/tennis-trading-betfair/ (blog, context)
- https://botblog.co.uk/live-tennis-api-exchange-bots/ (affiliate, context)
- https://betfairsquare.com/sports/tennis (affiliate, context)
- https://sharpbetsclub.substack.com/p/court-siding-rf-transmission-nodes (unsourced Substack, context)
- https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages/2686993/Additional+Information (truncated, nothing usable)
- https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages/2687396/Exchange+Stream+API (truncated, nothing usable)

Blocked (HTTP 403 or fetch refused), used only through search summaries:
- https://support.betfair.com/app/answers/detail/exchange-tennis-rules/
- https://support.betfair.com/app/answers/detail/413-exchange-what-is-commission-and-how-is-it-calculated/
- https://support.betfair.com/app/answers/detail/betfair-charges
- https://support.betfair.com/app/answers/list/exchange-market-rules
- https://betting.betfair.com/betfair-announcements/exchange-news/betfair-exchange-august-newsletter-290725-1392.html
- https://betting.betfair.com/betfair-announcements/exchange-news/betfair-exchange-january-newsletter-whats-ahead-for-2026-270126-1392.html
- https://caanberry.com/betfair-exchange-in-play-delay-explained/
- https://www.gambling.com/news/betfair-introduce-new-rule-changes-to-tennis-betting-markets-774200 (body truncated)
- web.archive.org (blocked by the tool)

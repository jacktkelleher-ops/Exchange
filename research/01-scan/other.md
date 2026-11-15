# Findings: Other (golf, basketball, US sports, esports, politics and specials)

Date: 2026-11-15
Agent: market-scanner

## Summary (max 5 lines)

Betfair official hosts (betfair.com, support.betfair.com, developer.betfair.com, historicdata.betfair.com, the Betfair developer docs and Betfair data scientists sites) did not resolve in this session, so no fee or data cost is [verified]. All figures below are third-party or from the Gemini input and are tagged [inferred] or [unknown].
Golf outrights and the US politics winner market are the only segments in this family with evidence of deep liquidity (third-party). Basketball and US sports are described as thin and delay-affected. Esports and specials: no evidence found.
Main risk for a EUR 500 bankroll: thin books outside golf and politics, long-dated capital lock-up in outrights and politics, and unconfirmed costs (live API key, paid historical tiers).

## Markets reviewed

| Market | Typical liquidity | Typical spread | Likely counterparties | Data available | Edge hypothesis | Evidence |
|---|---|---|---|---|---|---|
| Golf outright winner (majors and tour events) | High on majors and favourites, thin on longshots. No measured figures found | [unknown] | Recreational backers of favourites, golf-model bettors (DataGolf forum users trade it) | Historical data lists golf as a sport; tier prices unconfirmed. DataGolf is a model source (paid, not checked) | Longshot overround and favourite-longshot bias; model-vs-exchange value | [inferred] Sporting Life https://www.sportinglife.com/free-bets/guides/sports/golf-guide and DataGolf forum https://forum.datagolf.com/t/betfair-exchange-prices/252 (anecdotal) |
| Golf top 5/10/20, make cut, matchups | [unknown] | [unknown] | [unknown] | As above | Same as outrights; separate markets less efficiently priced is a guess | [unknown] |
| Golf in-play outright trading | [unknown] for Betfair. Supplier note says outrights are not actively managed in-play by operators | [unknown] | Other traders reacting to leaderboard moves | Stream API in-play data needs live key (cost unconfirmed) | Lag between leaderboard events and price update | [inferred] https://geniussports.atlassian.net/wiki/x/_NceAg (supplier note, not Betfair) |
| Basketball (NBA etc.) match odds, handicap, totals | Described as decent in-play but harder for UK traders; Gemini says shallow versus Kalshi/Pinnacle. No volume figures | [unknown] | Sharp bookmakers' prices feed the market; casual US-sport bettors | Basketball not named in historical data sports list; may sit under other sports | Slow reaction to scoring runs; undermined by fast scoring and bet delay | [inferred] https://betfairsquare.pages.dev/strategies/in-play-trading (strategy blog); Gemini input line 770 (not confirmed) |
| US sports (NFL, MLB, NHL) | Gemini says Medium to Low on Betfair. Not confirmed | [unknown] | Same as above | [unknown] | None identified; Pinnacle closing line is the benchmark and is sharper | [inferred] Gemini input only, unconfirmed |
| Esports | [unknown] | [unknown] | [unknown] | [unknown] | None identified | [unknown] |
| Politics: US election winner and other political markets | Very high on US presidential winner (about GBP 317m on 2024 US election markets, about GBP 250m on winner; GBP 400m+ in 2020). Other political markets [unknown] | [unknown] | Informed political bettors, media-driven flow, large position holders | Historical tiers cover other sports; coverage of politics [unknown] | Long-dated pricing bias; cross-event correlation; narrow event calendar | [inferred] https://www.oddschecker.com/insight/industry/20241106-over-300-million-matched-on-2024-us-election-markets-on-betfair-exchange and https://www.racingpost.com/news/latest/world-waits-on-next-president-with-over-400-million-matched-on-betfair-market/457615 |
| Specials (TV, entertainment, novelty) | [unknown] | [unknown] | [unknown] | [unknown] | None identified | [unknown] |

## Edge hypotheses

1. Golf outright model value
- Claim: Exchange prices on mid-priced golfers deviate from a strokes-gained model price, mainly on longshots and favourites.
- Why it might persist: Recreational flow concentrates on well-known names; outrights have many runners, so the overround and bias are structural.
- Why it might not: Model bettors (the DataGolf community) already trade it; one forum user says outrights are easy to beat with patience, which is anecdote only. Lay-side liabilities on longshots are large for a EUR 500 bankroll.
- How to test: Collect exchange prices at tournament start and close, compare with a free or self-built model, measure against Betfair closing price or BSP where available. Needs many tournaments for a sample (about 40 per season).
- Evidence: [inferred] https://forum.datagolf.com/t/betfair-exchange-prices/252 (anecdotal)

2. Golf in-play outright lag
- Claim: Outright prices lag leaderboard changes during rounds.
- Why it might persist: Many runners and markets updated by manual traders.
- Why it might not: Bots already read live scoring; bet delay and data latency penalise a retail stack.
- How to test: Record Stream API prices against a live score feed. Requires a live key (cost [unknown]) and a free scoring feed [unknown].
- Evidence: [unknown]

3. Politics long-dated favourite-longshot bias
- Claim: Longshot candidates are overpriced in long-dated political markets.
- Why it might persist: Capital lock-up deters arbitrageurs.
- Why it might not: Capital lock-up also hits a EUR 500 bankroll hard; the event calendar is sparse, giving few independent bets. Many events resolve once per cycle.
- How to test: Needs historical political price data; availability [unknown].
- Evidence: [inferred] liquidity only, no bias evidence found

4. Basketball in-play reaction
- Claim: Exchange prices underreact to scoring runs or lineup news.
- Why it might persist: Thin books.
- Why it might not: Fast scoring plus bet delay; bookmakers and bots price faster. A trade-based strategy also faces thin books.
- How to test: Stream data with score feed; needs live key.
- Evidence: [inferred] https://betfairsquare.pages.dev/strategies/in-play-trading (blog); not confirmed

No hypothesis is offered for esports or specials because no evidence was found.

## Costs

- Commission: Gemini input says Basic 2%, Rewards 5%, Rewards+ 8% for Ireland, and a legacy Market Base Rate of 5% on most sports including golf and basketball. Third-party Sporting Life says the same tiers (https://www.sportinglife.com/free-bets/guides/betfair-exchange-education/how-does-commission-work). Not confirmed at an official Betfair page. [inferred] (input claim 1 plus third-party; unconfirmed)
- Other charges that apply to profitable accounts: Expert Fee, reported by Racing Post as 0% under GBP 25,000 rolling 52-week gross profit, 20% for GBP 25,000 to 100,000, 40% above (https://www.racingpost.com/news/britain/betfair-exchange-to-introduce-new-commission-system-for-2025-as-premium-charge-is-dropped-a7wbg0v4GCAJ). Not confirmed officially. [inferred] (input claim 2 plus third-party). At EUR 500 bankroll the 25,000 threshold is not realistic to reach, so it is likely irrelevant. Transaction charges (input claim 3, 5,000 per hour threshold): [unknown], not checked.
- Data costs: Delayed API key reported free, no betting, 1 to 180 second delayed snapshots; live key one-off activation fee reported as GBP 299 in Betfair developer docs, with third-party directories saying about 499 (search summary of betfair-developer-docs.atlassian.net pages; page itself not fetched). Resolves input claim 4 only provisionally. [inferred]. Historical Basic tier reported free (one-minute last traded price, no volume); Advanced and Pro are paid, prices for golf and other sports [unknown]. Gemini input lists Advanced GBP 39 (Golf) / 39 (Other?) and Pro GBP 99 (Golf) / 79 (Other), with a garbled table; [inferred], unconfirmed.

Small bankroll and zero data budget limits:
- A live key (about GBP 299, unconfirmed) is about 60% of the EUR 500 bankroll, so live API automation conflicts with the zero data budget until a go decision. [inferred]
- Delayed key allows research but no betting, so only manual betting or Basic data until then. [inferred]
- Advanced and Pro historical tiers are out of the zero budget. Basic (free, one-minute, no volume) cannot support in-play or queue modelling. [inferred]
- Minimum stake and market-making exemption sizes (input says back 10 or more, lay liability 100 or more): [unknown], not checked. If lay liability must be 100 or more, longshot lays in golf outrights would consume a large share of a 150 EUR drawdown limit. [inferred]

## Data and access

- Historical data: Three tiers reported (Basic free, Advanced 1 second, Pro 50 ms). Golf and "other sport" named as covered; basketball, esports and politics coverage [unknown]. Prices [unknown] officially. [inferred] Source: web search summary of Betfair data-scientists pages; page not fetched.
- Live data and API: Delayed key free, live key requires approval plus fee, commercial use needs Betfair approval. [inferred] same source as above.

Cross-venue prediction market arbitrage (Kalshi, Polymarket): out of scope per brief, not assessed.

## Unknowns

- All official fee and data figures: need access to betfair.com, support.betfair.com, developer.betfair.com, historicdata.betfair.com and betfair-developer-docs.atlassian.net, which were not reachable from this session network. Allowing these hosts resolves it.
- Matched volume, spread and bet delay for golf, basketball, esports and specials: resolve by sampling the Betfair Exchange site or the delayed API key.
- Whether historical data covers basketball, esports and politics: historicdata.betfair.com or data@betfair.com.au.
- Stake minimum, transaction charge exemption terms: Betfair support pages.
- Any evidence of edge in golf, politics, esports or specials beyond forum anecdote.

## Sources

Official Betfair pages: none reachable this session.
Third party (all [inferred] context):
- https://www.sportinglife.com/free-bets/guides/golf-guide (as https://sportinglife.com/free-bets/guides/sports/golf-guide)
- https://forum.datagolf.com/t/betfair-exchange-prices/252
- https://geniussports.atlassian.net/wiki/x/_NceAg
- https://betfairsquare.pages.dev/strategies/in-play-trading
- https://www.oddschecker.com/insight/industry/20241106-over-300-million-matched-on-2024-us-election-markets-on-betfair-exchange
- https://www.racingpost.com/news/latest/world-waits-on-next-president-with-over-400-million-matched-on-betfair-market/457615
- https://www.racingpost.com/news/britain/betfair-exchange-to-introduce-new-commission-system-for-2025-as-premium-charge-is-dropped-a7wbg0v4GCAJ
- https://www.sportinglife.com/free-bets/guides/betfair-exchange-education/how-does-commission-work
- https://apis.io/plans/betfair/betfair-plans-pricing/ and Betfair developer docs pages surfaced by search (betfair-developer-docs.atlassian.net/wiki/x/URAp and others, not fetched)
- Input file docs/inputs/gemini-research.md (lines 90 to 105, 765 to 780, 895 to 935, 1100 to 1135), unverified lead

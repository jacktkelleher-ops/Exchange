# Findings: Football

Date: 2026-11-15
Agent: market-scanner

## Summary (max 5 lines)

The best-documented lead is in-play behavioural mispricing after a goal, mainly a late surprise goal by a pre-match longshot, plus lower-tier and women's markets for pre-match modelling. The main risk is cost verification: the fetch tool could not reach any Betfair host in this session, so no fee or data price here is verified at an official page. The EUR 0 data budget conflicts with a paid Live API key (reported at GBP 299, unconfirmed), which blocks live automation until the budget changes. Delayed-key and Basic data access were not confirmed either.

## Markets reviewed

| Market | Typical liquidity | Typical spread | Likely counterparties | Data available | Edge hypothesis | Evidence |
|---|---|---|---|---|---|---|
| Match Odds, top-tier leagues (e.g. EPL) | Deepest in football. Gemini quotes GBP 500K+ for EPL | [unknown] | Sharp traders, bots, market makers, recreational flow | Historical tiers exist. Prices unverified | In-play post-goal reaction bias, late-game longshot effects | Liquidity figure from input only, [inferred]. Bias evidence: [verified: https://econpapers.repec.org/RePEc:eee:intfor:v:38:y:2022:i:1:p:282-299] for existence of the paper only |
| Over/Under goals | Medium to high in top leagues, [inferred] | [unknown] | Same as Match Odds, plus model-driven traders | Same | Structural pricing with Dixon-Coles or xG models, cross-market partition arbitrage | Input only, [inferred] |
| Correct Score | Thin to medium, [inferred] | Wide, [inferred] | Recreational backers, some arbitrageurs | Same | Partition arbitrage with Win-to-Nil and Total Goals at low commission | Input claim, not confirmed, [inferred] |
| First Goalscorer | Thin, [inferred] | Wide, [inferred] | Recreational backers | Same | Player-level scoring models in a low-efficiency market | No evidence found, [unknown] |
| Lower leagues, women's football (all above markets) | Thin to medium. Gemini says under GBP 20K to 100K | Wide, [inferred] | Fewer sharps, [inferred] | Basic/Advanced data coverage of these leagues [unknown] | Lower efficiency, so a simple model might beat the close | Input claim 13, [inferred], not confirmed |

## Edge hypotheses

### H1: Underreaction to surprise goals by longshots
- Claim: after a pre-match longshot scores, especially late, the exchange underestimates its win probability. Gemini cites roughly 50% gross ROI in 2019/20 EPL.
- Why it might persist: it is a behavioural bias in crowd pricing, not a speed edge. It does not depend on beating betDelay because the goal is already priced when the market reopens.
- Why it might not: the sample is one season and gross of commission and liquidity limits. Others may have traded it since publication. Input claim 10 reports the opposite bias (favourite-longshot) in late in-play trading.
- How to test: Advanced or Pro tier data (paid) with goal timestamps, then check returns net of 5% or lower commission against the closing price. Benchmark is the closing price, per CLAUDE.md.
- Evidence: the paper exists and studies Betfair football: [verified: https://econpapers.repec.org/RePEc:eee:intfor:v:38:y:2022:i:1:p:282-299]. The 50% ROI figure, sample and the MPRA 126351 counter-finding came from the input file and were not confirmed. [inferred]

### H2: Structural score-grid models in thin derivative markets
- Claim: Dixon-Coles or shot-level xG convolution mispriced Draw, Correct Score, Totals in thin markets.
- Why it might persist: thin books, retail flow, and fewer model-driven participants.
- Why it might not: thin books mean stake limits and slippage; bookmaker prices are a sharper benchmark than Betfair in many leagues.
- How to test: free match-result and odds data (not yet sourced, see Unknowns), model closing-line value against a devigged sharp benchmark.
- Evidence: [inferred]. Source is the input file only.

### H3: Cross-market partition arbitrage
- Claim: Correct Score, Win-to-Nil and Total Goals can occasionally sum to a net positive after commission.
- Why it might persist: separate order books are only partly cross-matched.
- Why it might not: opportunities are small and short-lived, and bots with faster access likely take them. Legs of different sizes at stake minimums limit the small bankroll.
- How to test: stream or snapshot data across linked markets, count sub-1 booksums.
- Evidence: [inferred]. Input file only, not confirmed.

### H4: Late-game equaliser and half-time cusp effects
- Claim: probability shifts toward the Draw after late equalisers. Input also cites Croxson and Reade (2014).
- Why it might persist: slow adjustment in behavioural pricing.
- Why it might not: academic publication invites competition.
- How to test: same as H1.
- Evidence: [inferred]. Papers exist per the search above but figures not checked. [verified: https://econpapers.repec.org/RePEc:eee:intfor:v:38:y:2022:i:1:p:282-299] mentions Croxson and Reade only as prior work.

## Costs

Fetch failed with DNS errors for www.betfair.com, support.betfair.com, historicdata.betfair.com, betfair-developer-docs.atlassian.net and betfair-datascientists.github.io. No figure below is verified at an official page. Search summaries are the best available and are labelled [inferred].

- Commission: input claims Basic 2%, Rewards 5%, Rewards+ 8% for Ireland, and a 5% market base rate for football. A search summary of Sporting Life says UK and Ireland customers pay a maximum of 5% by default. Betfair's own page was not reached. [inferred] Conflicts: the claim that football uses a 5% base rate and that Basic is 2% are both unconfirmed. [unknown] Resolve at https://www.betfair.com/aboutUs/Betfair.Charges/ once the host is allowed.
- Other charges that apply to profitable accounts: Expert Fee, 0% below 25,000, 20% from 25,000 to 100,000, 40% above, rolling 52 weeks of gross profit, from 6 Jan 2025. Source is Racing Post reporting [inferred: https://www.racingpost.com/news/britain/betfair-exchange-to-introduce-new-commission-system-for-2025-as-premium-charge-is-dropped-a7wbg0v4GCAJ]. Currency is GBP, applicability to Irish accounts unconfirmed. Not relevant at EUR 500 bankroll unless profits scale 50 times. Transaction charges: a search summary attributes a 5,000 transactions per hour threshold to a Betfair data science page and Bet Angel help; older documents cite 1,000 bets per hour. [inferred] The input's stake 10 / liability 100 exemption was not found anywhere. [unknown] At 5 hours a week of mostly manual or modest bot activity, 5,000 per hour is unlikely to bind. Data Request Charges on heavy polling: [unknown].
- Data costs: Live API key reported as a one-off GBP 299 with a free Delayed key (search summary of Betfair developer docs, not fetched) [inferred]. A third-party page lists about GBP 499 for vendor or commercial use [inferred]. Input says GBP 299 vs 499 conflict. Historical data: Basic is free with last-traded price at 1-minute resolution; Advanced adds best prices and volume at 1 second; Pro is 50ms tick data with full ladder [inferred: search summary, https://betfair-datascientists.github.io/data/usingHistoricDataSite not fetched]. Soccer prices for Advanced (GBP 69) and Pro (GBP 230) come from the input only. [inferred]

Small-bankroll and zero-budget limits:
- A Live key at GBP 299 is about 60% of the EUR 500 bankroll, and is not affordable under the EUR 0 budget. [inferred]
- Delayed key is reportedly free but its data is delayed, which rules out in-play reaction strategies (H1, H4) even if it works for pre-match capture. [inferred]
- Basic historical data (free) has last-traded price only at 1-minute resolution, too coarse for in-play goal-reaction tests or queue and fill simulation. [inferred] Advanced at GBP 69 per input would need a budget change.
- Minimum stake on the Exchange: [unknown]. Needs the Betfair minimum bet page. At low stakes, thin Correct Score and First Goalscorer books may not fill meaningfully, and spreads can be a large share of an edge.
- Max drawdown EUR 150 limits in-play exposure on a single match. Lay liabilities on longshots tie up bankroll quickly. [inferred]

## Data and access

- Historical data: Betfair Historical Data service with Basic (free), Advanced and Pro tiers. Pricing and coverage unconfirmed at the official site. Free alternatives for results and bookmaker odds (football-data.co.uk or similar) were not searched in this session. [unknown]
- Live data and API: Exchange API with Live and Delayed application keys, one of each per account, Live key said to cost a one-off GBP 299 and reported to start inactive [inferred: search summary of Betfair developer docs]. Stream API availability on the Delayed key: [unknown]. Football bet delay: input says 5 to 8 seconds by league tier; sources agree on a 1 to 12 second range overall and say the value is exposed in the betDelay field. Not verified. [inferred] VAR rules from input (cancelled red card voids later bets) not found in any source. [unknown]

## Unknowns

- Official commission rate for football on an Irish account. Resolve: allow www.betfair.com and fetch the charges page.
- Whether Expert Fee and transaction charge figures apply in EUR and to Ireland. Resolve: same.
- Current Live key fee and whether the Delayed key supports Stream API. Resolve: Betfair developer docs, allow betfair-developer-docs.atlassian.net.
- Historical data prices and soccer league coverage, including women's and lower leagues. Resolve: historicdata.betfair.com.
- Exchange minimum stake, and liquidity or spread figures per market type. Resolve: Betfair rules page and free Basic data sample.
- Replication and sample size of the 50% ROI longshot-goal result, and the MPRA 126351 counter-finding. Resolve: read the Reading manuscript and the MPRA paper.
- Free results/odds sources for lower leagues and women's football.

## Sources

- https://econpapers.repec.org/RePEc:eee:intfor:v:38:y:2022:i:1:p:282-299 (paper existence confirmed by search only, full text not read)
- https://www.racingpost.com/news/britain/betfair-exchange-to-introduce-new-commission-system-for-2025-as-premium-charge-is-dropped-a7wbg0v4GCAJ (via search summary)
- https://betfair-developer-docs.atlassian.net/wiki/x/J4DS (listed in search, not fetched)
- https://betfair-datascientists.github.io/api/apiappkey/ (listed in search, not fetched)
- https://betfair-datascientists.github.io/wagering/commission (listed in search, not fetched)
- https://betfair-datascientists.github.io/data/usingHistoricDataSite (listed in search, not fetched)
- https://www.sportinglife.com/free-bets/guides/betfair-exchange-education/how-does-commission-work (via search summary)
- Input: /home/user/Exchange/docs/inputs/gemini-research.md

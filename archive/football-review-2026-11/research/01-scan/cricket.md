# Findings: Cricket

Date: 2026-11-15
Agent: market-scanner

## Summary (max 5 lines)

Most promising structure: in-play match odds and limited-overs derivatives (IPL and other T20 leagues, ODIs), where a ball-by-ball model could be run against a live feed. [inferred]
Main risk: no official Betfair page could be fetched this session (betfair.com, historicdata.betfair.com, support.betfair.com and the developer docs host did not resolve), so no fee, data or API claim below is [verified].
Second risk: a EUR 500 bankroll and EUR 0 data budget collide with a live API key fee reported at GBP 299 and with paid historical tiers. [inferred]
Liquidity, spread and bet delay figures for cricket have no official source. [unknown]

## Access note

WebFetch failed with "host not resolved" for www.betfair.com, historicdata.betfair.com, support.betfair.com, betfair-developer-docs.atlassian.net and betfair-datascientists.github.io. These hosts need to be allowed in the session network settings before the official checks required by CLAUDE.md can be done. All figures below come from web search summaries of secondary pages. They are tagged [inferred] with the URL they came from, never [verified]. Re-run the cost checks once the hosts are allowed.

## Markets reviewed

| Market | Typical liquidity | Typical spread | Likely counterparties | Data available | Edge hypothesis | Evidence |
|---|---|---|---|---|---|---|
| Match Odds, T20 franchise leagues (IPL etc.) | Very high for major IPL matches. One blog comment cites 150m GBP traded on an IPL final and 260m GBP on a qualifier. [inferred: https://mannersoncricket.substack.com/p/rabada-shines-in-home-test/comments] Gemini input also rates IPL "Very High". Input only, unconfirmed. | [unknown] | Recreational and Indian-market flow, other traders and bots [inferred] | Free Basic historical tier is 1 minute odds, no volume. [inferred: https://betcode-org.github.io/faq/using-data] Ball-by-ball results from free public sources were not checked. [unknown] | In-play overreaction to wickets and phase changes, plus ball-by-ball models | [inferred] |
| Match Odds, ODI and international T20 | Lower than IPL, size [unknown] | [unknown] | Same as above, plus country-specific flow [inferred] | Same as above | Phase models (overs 1-30 vs 31-50) suggested by Gemini input. Unconfirmed. | [inferred] |
| Match Odds, Test (3 outcomes incl. draw) | One blog comment: about 20m GBP on a Test day 1 "pretty good". [inferred: https://mannersoncricket.substack.com/p/rabada-shines-in-home-test/comments] Unsourced thesis claims many more tradeable pockets per Test than per T20. [inferred: https://forsyt-docs-pages.pages.dev/Hannibal/INPLAY_SPORTS_TRADING_THESIS] | [unknown] | Specialist traders, draw-market punters [inferred] | Same as above | Slow-moving market, weather and draw pricing may be less efficient. | [inferred] |
| Innings runs, session runs, top batsman, other derivatives | [unknown] for Betfair. No official source found. | [unknown] | Likely thin, mostly traders [inferred] | [unknown] | Lower efficiency in thin derivatives. Nothing found to support it for Betfair. | [unknown] |

## Edge hypotheses

### H1: In-play wicket and phase reaction in T20 match odds
- Claim: the market over or under reacts after wickets and at phase boundaries, and a ball-by-ball model can price the gap.
- Why it might persist: large retail flow in IPL, emotional trading around wickets. [inferred]
- Why it might not: Gemini input says substantial in-play delay applies, sharp traders and bots already price this, and an automated feed would need to beat the bet delay. Delay size is [unknown].
- How to test: collect free or Basic-tier price history, align with free ball-by-ball outcome data, test post-wicket price drift against a model benchmarked to the closing price. Basic tier has no volume and 1 minute resolution, which is too coarse for in-play work. [inferred: https://betcode-org.github.io/faq/using-data]
- Evidence: Gemini input lines 741 and 889 to 904 (input only, not confirmed). [inferred]

### H2: Test match draw and weather pricing
- Claim: draw probability is mispriced when weather or pitch information is slow to update.
- Why it might persist: slow market, multi-day exposure. [inferred]
- Why it might not: weather data is public and informed traders watch it.
- How to test: needs historical Test price series and weather logs. Availability at free tier [unknown].
- Evidence: [inferred]

### H3: Thin derivative markets are less efficient
- Claim: innings and session runs markets have wider spreads and slower repricing.
- Why it might persist: low attention.
- Why it might not: wide spreads and low liquidity cancel the edge. A EUR 500 bankroll would also be cramped by thin books.
- How to test: observe live books with a free delayed key (see Data and access).
- Evidence: [unknown]

## Costs

- Commission: search summaries report Basic 2%, Rewards 5%, Rewards+ 8% for UK and Irish customers, switchable once per month. [inferred: https://www.sportinglife.com/free-bets/guides/betfair-exchange-education/how-does-commission-work] Gemini input claim 1 matches, but it is not confirmed at an official page. Market base rate for cricket as 5% of net winnings also comes from Gemini input only. [inferred]
- Other charges that apply to profitable accounts: Expert Fee replaced the Premium Charge on 6 Jan 2025, based on rolling 52-week gross profit. [inferred: https://www.racingpost.com/news/britain/betfair-exchange-to-introduce-new-commission-system-for-2025-as-premium-charge-is-dropped-a7wbg0v4GCAJ] Tier figures (0% under 25k, 20% to 100k, 40% above) conflict across secondary sources. [unknown] Likely irrelevant at EUR 500 bankroll. [inferred]
- Transaction charge: search summary reports a charge of 0.2p per transaction above 5,000 in a clock hour, failed attempts included. [inferred: https://betfair-datascientists.github.io/wagering/commission] No source found for the market-making exemption (back stake 10 or more, lay liability 100 or more) from Gemini claim 3. [unknown] Impact: a EUR 500 bankroll rarely produces anything near 5,000 transactions per hour, but a quoting bot could. Exemption sizes of 10 and 100 would be large relative to a EUR 500 bankroll, so if the exemption exists, small quotes would not qualify. [inferred]
- Data costs: Basic historical tier free. Advanced and Pro prices not confirmed. Gemini input says Advanced 69 and Pro 230 for racing and soccer, which would not cover cricket. [inferred: input only]. Live API key one-off fee GBP 299 per search summary of the developer docs. [inferred: https://betfair-developer-docs.atlassian.net/wiki/x/TyQp] An aggregator lists about 499. [inferred: https://apis.io/plans/betfair/betfair-plans-pricing/] Conflict unresolved. [unknown]

## Data and access

- Historical data: Basic is free, 1 minute odds, no volume. Advanced is 1 second with volume, Pro is 50 ms. [inferred: https://betcode-org.github.io/faq/using-data] Cricket coverage in each tier [unknown]. Price of paid tiers [unknown]. Check historicdata.betfair.com once reachable.
- Live data and API: delayed application key is free, with 1 to 180 second delayed snapshots and no bet placement. Live key needs a one-off fee reported at GBP 299 and is applied for after testing on the delayed key. [inferred: https://betfair-developer-docs.atlassian.net/wiki/x/TyQp] At EUR 500 bankroll the fee is about 60% of the bankroll if paid in full, so an automated live strategy conflicts with the EUR 0 budget until a go decision. [inferred]
- Stake limits: one third-party guide reports a GBP 2 minimum back stake. [inferred: https://betfairsquare.pages.dev/blog/betfair-minimum-maximum-bet-size-limits] Betfair official minimum, and Euro equivalent for an Irish account, [unknown]. At EUR 500 bankroll and 30% drawdown (EUR 150), liability on lays at long odds consumes bankroll quickly. [inferred]
- Bet delay for cricket in-play: [unknown]. Gemini input says "substantial". Unconfirmed.

## Unknowns

- Official commission, Expert Fee and transaction charge figures. Resolve by allowing betfair.com and support.betfair.com hosts and fetching the charges page.
- Live key fee (299 vs 499). Resolve at the Betfair Developer portal.
- Historical data price and cricket coverage. Resolve at historicdata.betfair.com.
- Cricket in-play bet delay, minimum stake and market spreads. Resolve via the Betfair rules pages and live book observation on a delayed key.
- Whether free ball-by-ball outcome data (for example public scorecard archives) can be joined to Betfair price history. Not searched.
- Gemini claims 1, 2, 3, 4, 5, 7 touched here remain unconfirmed at an official source.

## Sources

- https://www.sportinglife.com/free-bets/guides/betfair-exchange-education/how-does-commission-work
- https://www.racingpost.com/news/britain/betfair-exchange-to-introduce-new-commission-system-for-2025-as-premium-charge-is-dropped-a7wbg0v4GCAJ
- https://betfair-datascientists.github.io/wagering/commission
- https://betfair-developer-docs.atlassian.net/wiki/x/TyQp
- https://apis.io/plans/betfair/betfair-plans-pricing/
- https://betcode-org.github.io/faq/using-data
- https://betfairsquare.pages.dev/blog/betfair-minimum-maximum-bet-size-limits
- https://mannersoncricket.substack.com/p/rabada-shines-in-home-test/comments
- https://forsyt-docs-pages.pages.dev/Hannibal/INPLAY_SPORTS_TRADING_THESIS
- /home/user/Exchange/docs/inputs/gemini-research.md (input file, unverified)

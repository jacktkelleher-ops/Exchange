# Findings: Horse racing (UK and Irish primary)

Date: 2026-11-15
Agent: market-scanner

## Summary (max 5 lines)

The most promising area is pre-off UK and Irish Win market microstructure and BSP-related trading, because it is the deepest racing liquidity and has the lowest claimed base commission. [inferred] The main risk is that this session could not fetch any official Betfair page (www.betfair.com and historicdata.betfair.com failed DNS resolution), so no fee or data cost is `[verified]`. Fee and data figures below come from search summaries and the Gemini lead file and are tagged `[inferred]`. The EUR 0 data budget limits testing to free Basic data (1-minute, no volume) until a go decision. [inferred] The live API key reportedly costs a one-off GBP 299, which is over half the EUR 500 bankroll. [inferred]

Access note: the hosts www.betfair.com and historicdata.betfair.com need to be added to the session network allowlist for official checks. Re-run the cost checks once allowed.

## Markets reviewed

| Market | Typical liquidity | Typical spread | Likely counterparties | Data available | Edge hypothesis | Evidence |
|---|---|---|---|---|---|---|
| UK/IE Win (pre-off) | Wide range: one low-quality source says about GBP 280k per race on a quiet weekday card, GBP 3-8m on Saturday televised races, and about 100k matched 10 minutes before the off with most volume later. Sources conflict by 10x. | [unknown] Likely 1 tick on favourites and wider on outsiders. [inferred] | Syndicates, bots and scalpers, bookmaker hedgers, retail. Share of bots [unknown]. | Basic free (1 min, no volume); Advanced/Pro paid [inferred] | Microstructure (weight of money) and BSP near/far price divergence | Gemini lead, unconfirmed; liquidity from https://betfairsquare.pages.dev/blog/betfair-horse-racing-trading-mastery-guide-2026 (low quality) [inferred] |
| UK/IE Win (in-play) | Heavy in-running volume at big races [inferred] | [unknown] | Trackside-informed traders, bots; 2s delay claimed in Gemini file | Advanced/Pro paid | In-running overreaction and post-race mispricing; not confirmed | Gemini lead, unconfirmed [inferred] |
| UK/IE Place | Lower than Win [inferred] | Wider than Win [inferred] | Retail, each-way hedgers [inferred] | As above | Win-to-place price inconsistency (cross-market) | [inferred] |
| Each-Way | Thin [inferred] | [unknown] | Retail [inferred] | As above | None identified | [unknown] |
| Forecast / reverse forecast / other racing specials | Thin [inferred] | [unknown] | Retail [inferred] | [unknown] | Thin books may be mispriced; liquidity probably too low for EUR 500 | [unknown] |
| BSP (Betfair Starting Price) auction | Single auction at the off; depth only at the jump [inferred] | Not applicable | SP-only bettors and resting orders converted to SP | Pro tier needed for BSP depth per Gemini file; free BSP result files exist but not checked | Model must beat BSP; BSP-based reconciliation | Gemini lead, unconfirmed; project rule that models are benchmarked to BSP (CLAUDE.md) |
| Other jurisdictions (AU/NZ, US, South Africa) | AU is large per Gemini lead; AU/NZ data starts Oct 2016 per Gemini lead | [unknown] | [unknown] | Pro-level AU data may need Betfair contact [inferred] | Not scanned in depth | Gemini lead, unconfirmed. AU/NZ markets may not be available to an Irish account [unknown] |

## Edge hypotheses

### H1: Pre-off weight-of-money and order-book signals

- Claim: short-horizon price moves in UK/IE Win markets partly follow order-book imbalance and matched-volume changes, so a rule can predict a tick or two.
- Why it might persist: informed money (syndicates) arrives gradually and leaves footprints. [inferred]
- Why it might not: well-funded bots already trade these signals, and a EUR 500 account cannot beat their queue priority or speed. [inferred]
- How to test: free Basic data has no volume or depth, so a real test needs Advanced (reported GBP 69 for racing) or Pro (reported GBP 230). Both are outside the EUR 0 budget. [inferred]
- Evidence: Gemini file cites arXiv:2510.16008v1 on WoM; not fetched or confirmed. [inferred]

### H2: Passive market making on UK/IE Win markets

- Claim: quoting both sides near the touch earns the spread, with commission only on net market profit.
- Why it might persist: low base commission (reported 2% for racing) and many small markets. [inferred]
- Why it might not: adverse selection when informed runners move, FIFO queue priority held by bots, and a EUR 500 bankroll with minimum stake limits. [inferred]
- How to test: needs queue-level data (Pro tier) or paper trading via the delayed API key. The delayed key reportedly lacks traded volume. [inferred]
- Evidence: Gemini lead; delayed key limits from https://betfair-datascientists.github.io/api/apiappkey/ (search summary only). [inferred]

### H3: BSP versus late exchange price

- Claim: BSP and the final traded price diverge systematically for some runner types (outsiders, thin markets).
- Why it might persist: BSP clears only against liquidity present at the jump, so thin markets can settle away from projections. [inferred, Gemini lead]
- Why it might not: BSP participants and bots already arbitrage the near/far price, and any model must beat BSP, a strong benchmark. [inferred]
- How to test: free BSP results and Basic last-traded-price data may allow a first pass. Whether free BSP files cover the needed history is [unknown].
- Evidence: Gemini lead, unconfirmed. [inferred]

### H4: Win versus place cross-market inconsistency

- Claim: place prices lag Win moves because the place market is thinner.
- Why it might persist: thin books update slowly. [inferred]
- Why it might not: place liquidity is low, so tradable size at EUR 500 scale is tiny and bots likely scan this. [inferred]
- How to test: needs Advanced-level price and volume data for Win and Place together. [inferred]
- Evidence: [inferred]

### H5: Own-odds model for flat or jumps racing versus BSP

- Claim: a form-based model can find runners where BSP is too long or too short.
- Why it might persist: racing has rich public data. [inferred]
- Why it might not: BSP embeds the same public data and syndicate information. [inferred]
- How to test: needs race result and form data. Free sources exist but were not researched here. [unknown]
- Evidence: [unknown]

## Costs

- Commission: Gemini file claims Irish tiers Basic 2%, Rewards 5%, Rewards+ 8%, switchable monthly, and a 2% market base rate on UK/IE Win and Each-Way. A search summary of third-party pages repeats the tiers, but one source (Timeform) says the default is up to 5% unless you opt in. Betfair official page not fetched. [inferred] Unconfirmed sources: https://www.timeform.com/betting/betfair-exchange-education/how-does-commission-work ; https://www.racingpost.com/news/britain/betfair-exchange-to-introduce-new-commission-system-for-2025-as-premium-charge-is-dropped-a7wbg0v4GCAJ
- Other charges that apply to profitable accounts: Expert Fee from 6 Jan 2025, described as based on gross profit over a rolling 52 weeks (Gemini file: 0% under 25k, 20% for 25-100k, 40% above). The Racing Post headline confirms the replacement of the Premium Charge, but the thresholds are not confirmed, and another site describes the rules differently. Not `[verified]`. [inferred] At a EUR 500 bankroll this is very unlikely to bind. [inferred] Transaction charges: Gemini file says a hourly threshold of 5,000 bets with exemptions (back stake 10 or more, lay liability 100 or more). A search summary of an old Levy Board paper gave 1,000 bets per hour. The current figure is [unknown]. Transaction charges are reportedly offset against commission. [inferred] From https://betfair-datascientists.github.io/wagering/commission (search summary). Note an automated strategy placing many small orders could hit the threshold while a EUR 500 bankroll cannot meet the exemption sizes (10 back stake, 100 lay liability). [inferred]
- Data costs: Gemini file claims Basic free, Advanced GBP 69 (Racing, Soccer), Pro GBP 230 (Racing, Soccer). A search summary confirms the tier structure and the free Basic tier but not the prices. An unofficial source estimates about GBP 300 per year for UK/IE racing Win. Not `[verified]`. [inferred]

Cost drag against bankroll: a live key at GBP 299 reportedly costs about 60% of the EUR 500 bankroll. [inferred] The delayed key is reportedly free but gives delayed prices (sources say 1-60 or 1-180 seconds) with no traded volume. [inferred] So until a go decision, API automation is limited to delayed, observation-only work. [inferred]

Stake minimums: sources say the UK/IE minimum is GBP 2 on back stakes and on the backer's stake on lays. The euro minimum for an Irish betfair.com account is [unknown]. SP bets reportedly need a GBP 10 minimum lay liability (Gemini file, unconfirmed). With EUR 500 and a 30% (EUR 150) drawdown limit, stakes of 2-10 per bet leave limited room for a sized strategy. [inferred]

## Data and access

- Historical data: Betfair Historic Data. Tiers Basic (free, 1-minute prices, no volume), Advanced (1 second, with volume), Pro (50 ms). Racing coverage reportedly from April/May 2015. Prices not confirmed. Sources: https://betfair-datascientists.github.io/data/usingHistoricDataSite (search summary, not fetched), Gemini file. [inferred]
- Live data and API: delayed key free, live key one-off GBP 299 activation, account must be KYC verified, personal use only unless Betfair approves commercial use. Source: https://betfair-developer-docs.atlassian.net/wiki/x/7yMp and https://betfair-datascientists.github.io/api/apiappkey/ (search summaries, not fetched). Gemini file flagged 299 versus 499 and the search suggests 299. Currency for an Irish account (GBP or EUR) is [unknown]. [inferred]
- Other free sources for racing (results, form, BSP files) were not researched. [unknown]

## Unknowns

- All official Betfair fees: commission by market and tier, Expert Fee thresholds, transaction charge threshold. Resolve: allow www.betfair.com in the network settings and fetch the Betfair charges page.
- Historic data prices and what the free tier covers for racing. Resolve: allow historicdata.betfair.com.
- Live key fee and currency for Irish accounts. Resolve: developer portal (betfair-developer-docs.atlassian.net page fetch).
- Euro minimum stake and BSP minimum for an Irish account. Resolve: Betfair rules pages.
- Real spreads, depth and bot share of volume in UK/IE racing. Resolve: Advanced or Pro sample data.
- Whether Betfair limits or restricts winning accounts (Gemini claim 8). Not checked.
- Whether AU/NZ or other jurisdictions' racing is open to an Irish betfair.com account.

## Sources

- /home/user/Exchange/docs/inputs/gemini-research.md (unverified lead file; lines 1-30 and racing sections)
- https://www.timeform.com/betting/betfair-exchange-education/how-does-commission-work (search result only)
- https://www.racingpost.com/news/britain/betfair-exchange-to-introduce-new-commission-system-for-2025-as-premium-charge-is-dropped-a7wbg0v4GCAJ (search result only)
- https://betfair-datascientists.github.io/api/apiappkey/ (search result only)
- https://betfair-developer-docs.atlassian.net/wiki/x/7yMp (search result only)
- https://betfair-datascientists.github.io/wagering/commission (search result only)
- https://betfair-datascientists.github.io/data/usingHistoricDataSite (search result only)
- https://betfairsquare.pages.dev/blog/betfair-horse-racing-trading-mastery-guide-2026 (low quality, liquidity figures)
- https://www.betfair.com/aboutUs/Betfair.Charges/ and https://historicdata.betfair.com/ (fetch attempted, host not resolvable in session)

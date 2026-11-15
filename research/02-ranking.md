# Ranking: Betfair Exchange market types

Date: 2026-11-15
Agent: ranker
Inputs read: docs/rubric.md, docs/brief.md, CLAUDE.md, research/00-verify/input-claims.md, all five files in research/01-scan/.

## Result in brief

No market type clears the shortlist gates. The shortlist is empty.

- The best total is 57 out of 100 (football over/under goals, own-odds model). The gate is 60.
- Every market fails the Data access gate (3 or higher). No free history with traded volume or ladders is confirmed anywhere. The free delayed key lacks total matched and shows only 3 price levels `[verified: DEV/2687105/Application+Keys]`. Free Basic history is reported as 1 minute last traded price with no volume, but that is only `[inferred]`.
- Four market types are marked needs-more-data because their totals would reach 60 or more if the specific unknowns listed below resolve in their favour.

## Basis for scoring

Scale: criterion score 1 to 5, times weight, summed, divided by 5. Total is out of 100.

Verified facts used (from research/00-verify/input-claims.md):

- Live API key costs GBP 499, debited after activation, KYC needed `[verified: DEV/2687105/Application+Keys]`. This is about EUR 590 at an assumed rate `[inferred]`, so it is unaffordable on a EUR 500 bankroll and EUR 0 data budget.
- The free delayed key can place live bets, includes the Stream API (2 connections, 200 markets), shows 3 price levels, has no total matched by selection and no BSP near/far price, and delays prices by 1 to 180 seconds `[verified: DEV/2687105/Application+Keys]`.
- Passive in-play orders that cannot match immediately skip the bet delay. Tennis dynamic delay drops to 1 second at set games. Football dynamic events have no delay at half time `[verified: DEV/2687396/Exchange+Stream+API]`.
- Transaction charges apply to both key types, but the threshold and exemption could not be read `[verified: DEV/2687105/Application+Keys]`.
- Mapping files exist for soccer, tennis, cricket, golf and other sports, 2018 to 2025 `[verified: DEV/2686993/Additional+Information]`. These are not price data.
- Reading paper (Angelini, De Angelis, Singleton 2022) on in-play football: mispricing after surprise late goals by longshots `[verified: Reading page]`. The 50% ROI figure is `[unknown]`.
- MPRA 126351: pre-match and early in-play, makers earn more than takers. Late in-play, longshot bets lose even for makers and takers on favourites profit `[verified: https://mpra.ub.uni-muenchen.de/126351/]`. The note does not state the sport mix.
- Everything else (commission rates, Expert Fee, historical data tiers and prices, liquidity, spreads, per-sport delay values, winning-account limits) is `[inferred]` or `[unknown]`. Scores resting only on these are capped at 3.

Scanner disagreements with the verification file (the verification file is used, the scanner view is noted):

- Live key fee: cricket, football, racing and other scanners said GBP 299 or an unresolved 299 vs 499. Tennis said 499. Verified is 499.
- Delayed key betting: cricket and other scanners said the delayed key cannot place bets. Verified says it can.
- Delayed key Stream API: football scanner marked it `[unknown]`. Verified says it is included.
- Fixed per-sport bet delays: the input said fixed figures. The football and tennis scanners did not support fixed values. Verified shows dynamic and passive rules, with fixed figures `[unknown]`.

Disagreements between scanners that stay unresolved (both reported, neither picked):

- Commission: Basic 2%, Rewards 5%, Rewards+ 8% (input, several scanners) against "up to 5% by default" (Timeform, Sporting Life summaries). Racing scanner also cites a 2% base rate on racing Win, while other scanners cite 5% base rates for football, tennis, golf and basketball.
- Transaction charge threshold: 5,000 per hour (most scanners) against 1,000 per hour (older Levy Board paper, racing scanner). Market-making exemption sizes (back 10, lay liability 100): not found by any scanner.
- Expert Fee tiers: consistent in Racing Post and tennis summaries, flagged as conflicting across sources by the cricket scanner. Irrelevant at this bankroll in either case `[inferred]`.
- Historical data prices: input says Advanced 69 and Pro 230 (racing, soccer). Tennis scanner says Advanced GBP 499 per year and Pro GBP 1,499 per year. Other scanner reports Advanced 39 and Pro 99 or 79 for golf and other. Unresolved.
- Racing liquidity: sources differ by about 10 times per race.
- Football post-goal bias direction: Reading paper (longshot goals underpriced) against MPRA (late longshot bets lose). They may be consistent because they condition differently, but this is `[inferred]` and untested.

Model type assumed per row is stated in the Model column. OM means own-odds model benchmarked to the closing price or BSP. MS means market-structure or behavioural strategy.

Common notes, referred to in the table:

- Cost note (CN): commission 2% to 8% depending on package or base rate `[inferred]`, Expert Fee not binding at this bankroll `[inferred]`, transaction charge unlikely to bind at brief volumes `[inferred]`, slippage not measured `[unknown]`. Scored 3 (cap) where books are medium or deep, 2 where books are thin or spreads wide.
- Capital note (KN): fits brief means back-style or small-stake use inside the EUR 150 drawdown limit `[verified: brief]`. Minimum stake is reported as about EUR 1 `[inferred]` or GBP 2 `[inferred]`, so minimums do not bind. Scored 4 for back-biased pre-play, 3 where lay liability or lock-up is material, 2 where capital is locked for long periods.
- Operational note (ON): the only affordable key is delayed, so any strategy needing a current price view is hurt `[verified]`. Whether Betfair restricts winning accounts is `[unknown]` (input claim 8), so no row scores 4 or 5 on operational risk.
- Data note (DN): Basic free history is `[inferred]` 1 minute last traded price without volume. Forward capture on the delayed key is free `[verified]` but gives delayed prices with 3 levels. Model-side inputs (results, form, ratings, point feeds) were not sourced by any scanner `[unknown]`. For these reasons no row scores Data access above 2.

## Full score table

Columns: L liquidity (20), E edge (25), D data (15), C cost (15), K capital (10), T time to first test (10), O operations (5).

### Summary

| Rank | Market type | Model | L | E | D | C | K | T | O | Total | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Football over/under goals and totals | OM | 3 | 3 | 2 | 3 | 4 | 2 | 3 | 57 | needs-more-data |
| 2 | Football in-play after surprise goals | MS (behavioural) | 3 | 3 | 2 | 3 | 4 | 2 | 2 | 56 | needs-more-data |
| 2 | Cross-sport pre-play passive resting orders (maker side) | MS | 3 | 3 | 2 | 3 | 4 | 2 | 2 | 56 | needs-more-data |
| 4 | Golf outright winner | OM | 3 | 3 | 2 | 3 | 3 | 2 | 3 | 55 | needs-more-data |
| 5 | Football Match Odds, top tier, pre-match | OM | 3 | 2 | 2 | 3 | 4 | 2 | 3 | 52 | reject |
| 5 | Tennis Match Odds, ATP/WTA 250 and above, pre-match | OM | 3 | 2 | 2 | 3 | 4 | 2 | 3 | 52 | reject |
| 5 | Cricket Match Odds pre-match (T20, ODI, Test) | OM | 3 | 2 | 2 | 3 | 4 | 2 | 3 | 52 | reject |
| 5 | Horse racing Win vs BSP, pre-off | OM | 3 | 2 | 2 | 3 | 4 | 2 | 3 | 52 | reject |
| 9 | Horse racing BSP vs late exchange price | MS | 2 | 2 | 2 | 3 | 4 | 3 | 3 | 50 | reject |
| 9 | Football lower leagues and women's football | OM | 2 | 3 | 2 | 2 | 4 | 2 | 3 | 50 | needs-more-data (lower priority) |
| 11 | Basketball (NBA etc.) | OM / MS | 2 | 2 | 2 | 3 | 4 | 2 | 2 | 47 | reject |
| 12 | Football Correct Score | OM | 2 | 2 | 2 | 2 | 4 | 2 | 3 | 45 | reject |
| 13 | Cricket T20 Match Odds in-play | MS / OM | 3 | 2 | 1 | 3 | 3 | 1 | 2 | 44 | reject |
| 14 | Tennis Match Odds in-play reaction | MS | 3 | 2 | 1 | 3 | 3 | 1 | 1 | 43 | reject |
| 14 | Horse racing Win in-play | MS | 3 | 2 | 1 | 3 | 3 | 1 | 1 | 43 | reject |
| 14 | Horse racing Place | OM / MS | 2 | 2 | 2 | 2 | 3 | 2 | 3 | 43 | reject |
| 14 | Politics, US election winner and long-dated markets | OM | 3 | 1 | 2 | 3 | 2 | 2 | 3 | 43 | reject |
| 18 | Football First Goalscorer | OM | 2 | 1 | 2 | 2 | 4 | 2 | 3 | 40 | needs-more-data (low priority) |
| 18 | US sports (NFL, MLB, NHL) | OM | 2 | 1 | 1 | 3 | 4 | 2 | 3 | 40 | reject |
| 20 | Tennis derived markets (set betting, totals, handicap) | OM / MS | 2 | 2 | 1 | 2 | 3 | 2 | 2 | 39 | reject |
| 21 | Football Match Odds in-play quoting or scalping | MS | 3 | 1 | 1 | 3 | 3 | 1 | 1 | 38 | reject |
| 21 | Horse racing Win pre-off weight of money, scalping, market making | MS | 3 | 1 | 1 | 3 | 3 | 1 | 1 | 38 | reject |
| 21 | Tennis Challenger and ITF Match Odds | OM | 1 | 2 | 2 | 2 | 3 | 2 | 2 | 38 | reject |
| 24 | Football cross-market partition arbitrage | MS | 2 | 1 | 2 | 2 | 3 | 2 | 2 | 37 | reject |
| 25 | Horse racing Each-Way, forecasts, specials | OM | 2 | 1 | 1 | 1 | 3 | 1 | 3 | 30 | needs-more-data (low priority) |
| 25 | Golf in-play outright | MS | 1 | 1 | 1 | 3 | 3 | 1 | 1 | 30 | reject |
| 27 | Golf top 5/10/20, make cut, matchups | OM | 1 | 1 | 1 | 2 | 3 | 1 | 3 | 29 | needs-more-data (low priority) |
| 28 | Esports | n/a | 1 | 1 | 1 | 1 | 3 | 1 | 3 | 26 | needs-more-data (low priority) |
| 28 | Specials (TV, entertainment, novelty) | n/a | 1 | 1 | 1 | 1 | 3 | 1 | 3 | 26 | needs-more-data (low priority) |
| 30 | Cricket innings, session and top batsman derivatives | OM | 1 | 1 | 1 | 1 | 2 | 1 | 2 | 23 | needs-more-data (low priority) |
| n/s | Horse racing in other jurisdictions (AU/NZ, US, South Africa) | n/a | not scored | | | | | | | n/s | needs-more-data (low priority) |

Rows with a 1 given only because the evidence is `[unknown]` are provisional floors, not findings. Their totals are not comparable with evidence-backed rows. Ties are broken by time to first test, then left in listed order.

### Reasons and evidence for each score

Each cell gives the score, the evidence tag and a one line reason. "CN", "KN", "ON" and "DN" refer to the common notes above.

**1. Football over/under goals and totals, OM (57)**

- L3 `[inferred]`: medium to high in top leagues, from the football scanner. No measured depth.
- E3 `[inferred]`: named source is a Dixon-Coles or xG model against retail-flow pricing in derivative markets. Input only, capped at 3.
- D2 `[inferred]`: DN. Whether over/under markets are in free Basic history is not shown.
- C3 `[inferred]`: CN.
- K4 `[verified: brief]`: KN. Back-style stakes fit.
- T2 `[inferred]`: no free results source was identified by the scanner, so a first backtest is not days away.
- O3 `[unknown]` basis for restriction risk: ON. Pre-play is not hurt by price delay as much as in-play.

**2. Football in-play after surprise goals, MS behavioural (56)**

- L3 `[inferred]`: EPL match odds deepest in football, GBP 500K+ from the input only.
- E3 `[verified: Reading page and MPRA]` existence of mispricing, directions conflict, 50% ROI is `[unknown]`, one season, not tested on delayed data.
- D2 `[inferred]`: a real test needs Advanced or Pro data with goal timestamps. Delayed key timing is too loose `[verified]`.
- C3 `[inferred]`: CN.
- K4 `[verified: brief]`: back longshots at small stakes. Lay liability would not fit.
- T2 `[inferred]`: blocked on paid data or a data sample.
- O2 `[verified]`: prices seen are delayed 1 to 180 seconds, so the entry price is uncertain. Passive orders skip the bet delay `[verified]`.

**3. Cross-sport pre-play passive resting orders, MS (56)**

- L3 `[inferred]`: assumed on liquid pre-play markets only.
- E3 `[verified: https://mpra.ub.uni-muenchen.de/126351/]`: makers earn more than takers pre-match. This is an average across all makers, net of commission and for a retail size not shown, so held at 3.
- D2 `[verified]`: testing queue and fill needs order-level data. Delayed key has no volume.
- C3 `[inferred]`: CN. Makers pay commission only on net market profit `[inferred]`.
- K4 `[verified: brief]`: KN.
- T2 `[inferred]`: needs data that is not free.
- O2 `[verified]`: ON. You rest orders against a stale view, so adverse selection risk is higher than the paper's average.

**4. Golf outright winner, OM (55)**

- L3 `[inferred]`: high on majors and favourites, thin on longshots. No measured figures.
- E3 `[inferred]`: longshot overround and model against exchange value. Anecdotal (forum), capped. DataGolf community already trades it.
- D2 `[inferred]`: DN. Golf mapping files exist `[verified]`, price history coverage not confirmed, model data unsourced. Delay is irrelevant for slow outright pricing `[inferred]`.
- C3 `[inferred]`: CN.
- K3 `[inferred]`: capital is tied up for days to weeks, and longshot lays would be large.
- T2 `[inferred]`: about 40 events per season means a slow sample.
- O3 `[unknown]`: ON.

**5. Football Match Odds, top tier, pre-match, OM (52)**

- L3 `[inferred]`: deepest football market.
- E2 `[inferred]`: this is the most heavily traded football market, sharps and bots present, and the benchmark is the close.
- D2 `[inferred]`: DN.
- C3 `[inferred]`: CN.
- K4 `[verified: brief]`: KN.
- T2 `[inferred]`: model data unsourced.
- O3 `[unknown]`: ON.

**6. Tennis Match Odds, ATP/WTA 250 and above, pre-match, OM (52)**

- L3 `[inferred]`: GBP 200K+ at round of 16 of 1000 level per an affiliate guide.
- E2 `[inferred]`: Pinnacle-referencing traders keep the book aligned. The devig lead is practitioner-sourced and `[unknown]`.
- D2 `[inferred]`: Betfair tennis history appears paid only (Advanced GBP 499 per year per one summary). Pinnacle closes are not free.
- C3 `[inferred]`: CN.
- K4 `[verified: brief]`: KN.
- T2 `[inferred]`: history must be bought or collected forward.
- O3 `[unknown]`: ON. Retirement after the first set stands as a normal result `[inferred]`.

**7. Cricket Match Odds pre-match, OM (52)**

- L3 `[inferred]`: very high IPL, one Test day "pretty good". ODI and international size is `[unknown]`.
- E2 `[inferred]`: Test draw and weather pricing is public information. No supporting evidence found.
- D2 `[inferred]`: Basic tier cricket coverage `[unknown]`. Cricket mapping files exist `[verified]`.
- C3 `[inferred]`: CN.
- K4 `[verified: brief]`: KN.
- T2 `[inferred]`: no free ball-by-ball source searched.
- O3 `[unknown]`: ON.

**8. Horse racing Win vs BSP, pre-off, OM (52)**

- L3 `[inferred]`: deepest racing market. Sources differ by 10 times.
- E2 `[inferred]`: BSP embeds public form and syndicate information. Edge evidence is `[unknown]` in the scan.
- D2 `[inferred]`: Basic racing prices free, BSP files exist but were not checked, form data not researched.
- C3 `[inferred]`: CN. Racing base rate reported as 2% by the input and "up to 5%" by Timeform.
- K4 `[verified: brief]`: KN.
- T2 `[inferred]`: form model must be built.
- O3 `[unknown]`: ON.

**9. Horse racing BSP vs late exchange price, MS (50)**

- L2 `[inferred]`: BSP depth exists only at the jump, thin markets settle away from projections.
- E2 `[inferred]`: BSP participants and bots already trade near and far price. Delayed key has no BSP near/far price `[verified]`.
- D2 `[unknown]` for free BSP history coverage, `[inferred]` for Basic last traded price.
- C3 `[inferred]`: CN.
- K4 `[verified: brief]`: KN. BSP minimum liability reported as GBP 10 `[inferred]`.
- T3 `[inferred]`: a first pass on free BSP files and Basic prices might take days if coverage exists.
- O3 `[unknown]`: ON.

**10. Football lower leagues and women's football, OM (50)**

- L2 `[inferred]`: thin to medium, input says under GBP 20K to 100K.
- E3 `[inferred]`: fewer sharps. Input claim 13 only, no Betfair evidence, capped.
- D2 `[unknown]` coverage of these leagues in Basic or Advanced.
- C2 `[inferred]`: wide spreads and slippage raise cost drag beyond CN.
- K4 `[verified: brief]`: small stakes suit thin books.
- T2 `[inferred]`: coverage and free results not checked.
- O3 `[unknown]`: ON.

**11. Basketball, OM and MS (47)**

- L2 `[inferred]`: shallow against Kalshi and Pinnacle per input, decent in-play per a strategy blog.
- E2 `[inferred]`: fast scoring plus bet delay and sharp bookmaker feeds.
- D2 `[unknown]`: basketball is not named in the historical sports list.
- C3 `[inferred]`: CN.
- K4 `[verified: brief]`: KN.
- T2 `[inferred]`: needs a score feed.
- O2 `[verified]`: bet delay and stale delayed-key prices hurt in-play use.

**12. Football Correct Score, OM (45)**

- L2 `[inferred]`: thin to medium.
- E2 `[inferred]`: wide spreads, arbitrageurs already active.
- D2 `[inferred]`: DN.
- C2 `[inferred]`: wide spreads.
- K4 `[verified: brief]`: KN.
- T2 `[inferred]`: DN.
- O3 `[unknown]`: ON.

**13. Cricket T20 Match Odds in-play, MS and OM (44)**

- L3 `[inferred]`: IPL very high (blog comment).
- E2 `[inferred]`: bots and sharp traders already price wickets. Cricket in-play delay is `[unknown]`.
- D1 `[inferred]`: Basic is 1 minute with no volume, too coarse. Ball-by-ball feed unsourced.
- C3 `[inferred]`: CN.
- K3 `[inferred]`: KN, in-play exposure.
- T1 `[inferred]`: needs a ball feed and tick data.
- O2 `[verified]`: ON.

**14. Tennis Match Odds in-play reaction, MS (43)**

- L3 `[inferred]`: as row 6.
- E2 `[inferred]`: bots and court-side feeds exist. A free retail stack has no point feed. Passive orders skip delay `[verified]` but are picked off.
- D1 `[verified]`: delayed key prices are 1 to 180 seconds late, tick history is paid.
- C3 `[inferred]`: CN.
- K3 `[inferred]`: a retirement after the first set loses fully.
- T1 `[inferred]`: months to a valid test.
- O1 `[verified]`: latency risk is severe on a delayed key.

**15. Horse racing Win in-play, MS (43)**

- L3 `[inferred]`: heavy in-running volume at big races.
- E2 `[inferred]`: trackside traders and bots. A 2 second delay claim is input only.
- D1 `[inferred]`: Advanced or Pro paid.
- C3 `[inferred]`: CN.
- K3 `[inferred]`: KN.
- T1 `[inferred]`: no free data.
- O1 `[verified]`: ON.

**16. Horse racing Place, OM and MS (43)**

- L2 `[inferred]`: lower than Win.
- E2 `[inferred]`: Win-to-place lag exists in theory, but thin books and bots.
- D2 `[inferred]`: DN. Needs Win and Place together with volume for a real test.
- C2 `[inferred]`: wider spreads than Win.
- K3 `[inferred]`: tiny tradable size.
- T2 `[inferred]`: DN.
- O3 `[unknown]`: ON.

**17. Politics, US election winner and long-dated markets, OM (43)**

- L3 `[inferred]`: about GBP 317m on 2024 US election markets (secondary reports).
- E1 `[unknown]`: scanner found liquidity only, no bias evidence.
- D2 `[unknown]`: coverage of politics in history `[unknown]`. Forward capture is free `[verified]`.
- C3 `[inferred]`: CN.
- K2 `[inferred]`: capital locked for long periods.
- T2 `[inferred]`: sparse event calendar gives few independent bets.
- O3 `[unknown]`: ON.

**18. Football First Goalscorer, OM (40, provisional)**

- L2 `[inferred]`: thin.
- E1 `[unknown]`: no evidence found. This is the reason it is not a plain reject.
- D2 `[inferred]`: DN.
- C2 `[inferred]`: wide spreads.
- K4 `[verified: brief]`: KN.
- T2 `[inferred]`: no player-level data sourced.
- O3 `[unknown]`: ON.

**19. US sports (NFL, MLB, NHL), OM (40)**

- L2 `[inferred]`: Medium to Low per input only.
- E1 `[inferred]`: none identified. Pinnacle close is sharper than Betfair.
- D1 `[unknown]`: coverage `[unknown]`.
- C3 `[inferred]`: CN.
- K4 `[verified: brief]`: KN.
- T2 `[inferred]`: no data source.
- O3 `[unknown]`: ON.

**20. Tennis derived markets, OM and MS (39)**

- L2 `[inferred]`: thin.
- E2 `[inferred]`: bots already model it. Retirement voids create unhedged risk.
- D1 `[inferred]`: Game Betting markets reportedly not in historical data.
- C2 `[inferred]`: wide spreads.
- K3 `[inferred]`: KN.
- T2 `[inferred]`: no historical derived prices.
- O2 `[inferred]`: retirement and void rules.

**21. Football Match Odds in-play quoting or scalping, MS (38)**

- L3 `[inferred]`: as row 5.
- E1 `[verified]`: needs a current queue view. Delayed key is 1 to 180 seconds late and has no total matched.
- D1 `[verified]`: ON and delayed key limits.
- C3 `[inferred]`: CN. Exemption sizes `[unknown]`.
- K3 `[inferred]`: KN.
- T1 `[inferred]`: no free tick data.
- O1 `[verified]`: ON.

**22. Horse racing Win pre-off weight of money, scalping, market making, MS (38)**

- L3 `[inferred]`: as row 8.
- E1 `[verified]`: bots hold queue priority `[inferred]`. Delayed key lacks volume, so weight of money cannot be built `[verified]`.
- D1 `[verified]`: Advanced or Pro paid, delayed key has no volume.
- C3 `[inferred]`: CN.
- K3 `[inferred]`: KN.
- T1 `[inferred]`: no data.
- O1 `[verified]`: ON.

**23. Tennis Challenger and ITF Match Odds, OM (38)**

- L1 `[inferred]`: too thin to trade meaningfully per a guide, some ITF matches have no counterparty.
- E2 `[inferred]`: low liquidity deters large players, but a EUR 500 stake moves the price.
- D2 `[inferred]`: DN.
- C2 `[inferred]`: wide spreads.
- K3 `[inferred]`: KN.
- T2 `[inferred]`: DN.
- O2 `[inferred]`: retirement rules and data-feed risk.

**24. Football cross-market partition arbitrage, MS (37)**

- L2 `[inferred]`: legs sit in thin markets.
- E1 `[verified]`: opportunities are small and short lived, stale delayed-key prices defeat the strategy.
- D2 `[inferred]`: DN.
- C2 `[inferred]`: several legs, each paying spread.
- K3 `[inferred]`: stake minimums limit leg sizing.
- T2 `[inferred]`: DN.
- O2 `[verified]`: ON.

**25. Horse racing Each-Way, forecasts, specials, OM (30, provisional)**

- L2 `[inferred]`: thin. Scanner says likely too low for EUR 500.
- E1 `[unknown]`: no edge identified.
- D1 `[unknown]`: DN.
- C1 `[unknown]`: spreads unknown.
- K3 `[inferred]`: KN.
- T1 `[unknown]`: nothing to test with.
- O3 `[unknown]`: ON.

**26. Golf in-play outright, MS (30, provisional)**

- L1 `[unknown]`: Betfair liquidity not found.
- E1 `[unknown]`: lag edge depends on a current view, which the delayed key cannot give `[verified]`.
- D1 `[verified]`: live stream data needs the GBP 499 key.
- C3 `[inferred]`: CN.
- K3 `[inferred]`: KN.
- T1 `[inferred]`: no free scoring feed identified.
- O1 `[verified]`: ON.

**27. Golf top 5/10/20, make cut, matchups, OM (29, provisional)**

- L1 `[unknown]`.
- E1 `[unknown]`: the scanner states "less efficiently priced" is only a guess.
- D1 `[unknown]`.
- C2 `[unknown]`: assumed thin books.
- K3 `[inferred]`: KN.
- T1 `[unknown]`.
- O3 `[unknown]`: ON.

**28. Esports (26, provisional) and 29. Specials (26, provisional)**

- L1, E1, D1, C1 all `[unknown]`: scanner found no evidence at all for either.
- K3 `[inferred]`: KN. T1 `[unknown]`. O3 `[unknown]`: ON.

**30. Cricket innings, session and top batsman derivatives, OM (23, provisional)**

- L1 `[unknown]`, E1 `[unknown]`, D1 `[unknown]`, C1 `[unknown]`: no official or measured evidence.
- K2 `[inferred]`: thin books cramp a small bankroll.
- T1 `[unknown]`. O2 `[inferred]`.

**31. Horse racing in other jurisdictions**

- Not scored. The racing scanner did not scan these in depth, and availability to an Irish betfair.com account is `[unknown]`.

## Gates applied

| Gate | Result |
|---|---|
| Total 60 or higher | No market passes. Highest is 57. |
| Edge plausibility 3 or higher | Passed by rows 1 to 4 and row 10 only. All rest on `[inferred]` support except rows 2 and 3, which also have `[verified]` papers. |
| Data access 3 or higher | No market passes. Highest Data score is 2. |
| No criterion on `[unknown]` evidence alone | Rows 18, 25, 27, 28, 29, 30 and 31 fail this. They are marked needs-more-data. |

## Shortlist

Empty. No market type meets all four gates.

Closest candidates, none shortlisted, with the gate each fails:

| Candidate | Total | Gates failed | Main risk |
|---|---|---|---|
| Football over/under goals, OM | 57 | total below 60, Data below 3 | Edge rests on the input file only. Free data coverage and results source unconfirmed. |
| Football in-play after surprise goals, MS | 56 | total below 60, Data below 3 | Needs paid tick data, and the delayed key cannot time the entry. Papers disagree on direction. |
| Cross-sport passive resting orders, MS | 56 | total below 60, Data below 3 | Paper is an average over makers. Retail size, net of commission and stale prices are untested. |
| Golf outright winner, OM | 55 | total below 60, Data below 3 | Anecdotal edge. Few events per year gives a slow sample. |

## Needs-more-data

Items 1 to 4 would reach 60 or more if their listed unknowns resolve favourably. Totals shown are best case, with Data Access moving from 2 to 3 and Time to first test from 2 to 3 where stated, and no other score changed.

| # | Market | What is missing | What would resolve it | Best case total |
|---|---|---|---|---|
| 1 | Football over/under goals, OM | Whether over/under markets are in free Basic history. A free results source for a goals model. Any evidence of mispricing in these markets. | A person opens historicdata.betfair.com and the Basic file list, or supplies the page text. Pull one season of football results from a free source and run a closing price calibration. | 62 |
| 2 | Football in-play after surprise goals, MS | Price of soccer Advanced data (input says GBP 69, unverified, and the tennis figures were far higher). Reading paper sample size, ROI and net-of-commission result. Whether the effect survives the MPRA late in-play finding. | Read the Reading manuscript and MPRA 126351 in full. Check the Advanced price for soccer on the official page. Test on one season only if the budget owner approves a purchase. | 61 |
| 3 | Cross-sport passive resting orders, MS | Sport mix and sample of MPRA 126351, whether maker profit is net of commission, and whether it holds at EUR 1 to 10 stake sizes with delayed prices. | Read the full paper. Paper trade passive orders on the delayed key for a few weeks, logging fills against the later close. | 61 |
| 4 | Golf outright winner, OM | Basic history coverage for golf. A free source of strokes-gained or similar model inputs. Matched volume and spread on outrights. | Official Basic file list for golf. Sample outright books on the delayed key across two tournaments. Search for a free player rating source. | 60 |
| 5 | Football lower leagues and women's football, OM (lower priority) | Depth, spread and coverage of these leagues in history. Input claim 13 has no Betfair evidence. Totals would need liquidity, cost and data all to resolve favourably. | Record books on the delayed key for several weeks. Check history coverage for these competitions. | 62 if three unknowns all resolve well |
| 6 | Low priority group: Football First Goalscorer, Horse racing Each-Way and forecasts, Golf top-N and matchups, Esports, Specials, Cricket derivatives, Horse racing other jurisdictions | No evidence on liquidity, edge or data. Scanners stated no edge hypothesis for esports and specials, and thin books for the others. | Sample live books on the delayed key. For other racing jurisdictions, confirm whether an Irish betfair.com account can trade them. Treat as optional, only if capacity remains. | Not meaningful |

Across all items, these unknowns also remain open and affect every row:

- Official commission table for an Irish account (claim 1), transaction charge threshold and exemption (claim 3), and the Expert Fee terms (claim 2). Resolve by a person reading the official charges page or pasting its text. Those pages answered the session with a Cloudflare challenge.
- Whether Betfair limits winning accounts (claim 8). No official statement was found.
- Historical data tier prices and per-sport coverage (claim 5), where scanner and input figures conflict.
- Euro minimum stake for an Irish account. One scan found EUR 1, others quote GBP 2.

## Rejects

| Market | Total | Reason |
|---|---|---|
| Football Match Odds top tier pre-match, OM | 52 | Edge 2 in the most efficient football market, benchmark is the close. |
| Tennis Match Odds pre-match, OM | 52 | Edge 2, paid tennis history, Pinnacle closes not free. |
| Cricket Match Odds pre-match, OM | 52 | Edge 2, no evidence of mispricing. |
| Horse racing Win vs BSP, OM | 52 | Edge 2, BSP embeds the public information. |
| Horse racing BSP vs late price, MS | 50 | Edge 2, delayed key has no BSP near/far price. Cheap to retest if free BSP files turn out to cover it. |
| Basketball | 47 | Edge 2, fast scoring and bet delay. |
| Football Correct Score, OM | 45 | Thin, wide spreads, edge 2. |
| Cricket T20 in-play | 44 | Data 1 and latency risk on a delayed key. |
| Tennis in-play reaction | 43 | Delayed key and no point feed. Latency and retirement risk. |
| Horse racing in-play | 43 | Delayed key, paid data, bots. |
| Horse racing Place | 43 | Thin, wide spreads, edge 2. |
| Politics | 43 | No bias evidence, sparse calendar, capital locked. Even edge 3 would give 53. |
| US sports | 40 | No edge found, Pinnacle sharper. |
| Tennis derived markets | 39 | Not in history, thin, retirement void risk. |
| Football Match Odds in-play quoting or scalping | 38 | Needs a live key (GBP 499). Verified unaffordable. |
| Horse racing weight of money, scalping, market making | 38 | Needs volume and live queue view. Delayed key has neither. |
| Tennis Challenger and ITF | 38 | Too thin, a EUR 500 stake moves the price. |
| Football partition arbitrage | 37 | Stale delayed-key prices defeat a short-lived arbitrage. |
| Golf in-play outright | 30 | Needs a live stream and a scoring feed. Its unknown liquidity and edge are secondary to the verified key constraint. |

## Notes for the next phase

- If the user approves any data spend, the top four candidates all move up together, because Data access and Time to first test are the criteria holding them under 60. Stating the amount first is a decision for the user. The soccer Advanced price is not verified.
- The delayed key allows real bets, so pre-play work and slow strategies can be paper traded at no data cost. This is the cheapest way to resolve items 3 and 4.
- Net conclusion on the brief: a EUR 0 data budget plus the GBP 499 live key rules out latency-sensitive in-play and queue-based strategies. What remains is slow pre-play modelling, and its edge evidence is inferred or from papers only.

# Verify: viability-literature

Date: 2026-11-15
Agent: docs-verifier

## Summary (max 5 lines)

Peer-reviewed work gives few published numbers for Betfair spreads, depth, update rates or maker/taker returns by sport. Most full texts were PDFs that WebFetch could not decode, so many values are only in abstracts or search summaries and are tagged [inferred]. The hard numbers found: the horse-racing pre-off liquidity and volume profile (arXiv 2510.16008), the Flepp et al. liquidity cut-offs (GBP 23,400 cumulative volume, spread 0.044; [inferred]), Betfair in-play delay of 1 to 9 s with up to 12 s (Bet Angel quoting Betfair), Expert Fee tiers (Racing Post), and Kyle's lambda ranges for Polymarket. Biggest gap: no published Betfair spread-in-ticks by sport, no published Betfair update rate by time to off, no published rule of thumb for minimum liquidity for automated trading, and no net-of-commission test of scalping on Betfair tick data. The orchestrator will have to build these from the survey data.

## Answers

Evidence tags: V = `[verified: URL]` means the fetched page text stated it. I = `[inferred]` means a search summary or a page that did not show the number.

| Question | Answer | Evidence |
|---|---|---|
| 1a. Spread and depth on Betfair, by sport | No peer-reviewed value for quoted spread in ticks by sport was found. Whelan's model says thick markets have high match rates and narrow spreads, thin markets have wide spreads and less liquidity (abstract-level only). Horse racing (UK win, pre-off) is described as high liquidity and high volatility; liquidity defined as unmatched amounts at best bid and ask. | Whelan: [verified: https://mpra.ub.uni-muenchen.de/126351/] for maker/taker model; thick/thin text [inferred: web search summary of https://www.karlwhelan.com/Papers/Betfair.pdf]. Horse racing: [verified: https://arxiv.org/html/2510.16008v1] data section; the "high liquidity and volatility" wording [inferred: search summary]. |
| 1b. Published liquidity values | UK horse racing "to win", 2014-09 to 2016-08, 14,421 races, last 10 minutes: mean volume 520,865 in minute 1 before the start vs 122,693 in minute 10; mean liquidity 6,974 vs 2,029; mean volatility 1,052 vs 642 absolute ticks per minute. Units are as in the paper's Table 2; currency and unit not confirmed. | [verified: https://arxiv.org/html/2510.16008v1] |
| 1c. Liquidity threshold from literature | Flepp, Nuesch and Franck (Quarterly Review of Economics and Finance 2017): across 17,410 soccer matches, bookmakers beat Betfair for bettors when exchange cumulative trading volume is below GBP 23,400 and/or average quoted spread is above 0.044 (index 1-11 in the source). The abstract page fetched does not show these two numbers. | Matches and finding: [verified: https://ideas.repec.org/p/zrh/wpaper/342.html]. Thresholds GBP 23,400 and 0.044: [inferred: web search summary; full text at https://unifr.ch/tim/en/assets/public/uploads/Publication list/2017/Flepp_Nüesch_Franck_2017.pdf not decoded]. Spread unit ("index 1-11", 0.044) is not defined in what was read. |
| 1d. Kyle's lambda | No Betfair estimate found. Comparable venues: Polymarket 2024 US election market, lambda from regressing hourly change in log-odds on hourly net signed flow in USD millions over a rolling 30-day window: 0.518 early or in news shocks, about 0.04 after Sept 2024, about 0.01 by October. At p=0.5, 0.518 implies USD 1m net buy moves implied probability about 13 points; 0.01 implies about 0.25 points. Regression of daily lambda on 30-day average daily volume: coefficient -0.073, R2 0.278, n 277. | [verified: https://arxiv.org/html/2603.03136v1] |
| 1e. Lambda and trade direction reliability | On Polymarket order-book data, trade direction inferred from the public feed matched on-chain truth in about 59% of buckets (panel mean 0.615, CI 0.58 to 0.65), versus about 80% for Lee-Ready on Nasdaq. Kyle's lambda changed sign in 60% and 43% of markets in two windows when feed-based direction replaced on-chain direction. Relevant to any Betfair lambda built from inferred aggressor side. | [verified: https://arxiv.org/abs/2604.24366] |
| 1f. Kalshi price impact and maker returns | Bartlett and O'Hara, 41.6 million Kalshi trades: single-name markets show greater informed price impact than broad-based markets; effective spreads only modestly wider; makers earn about twice as much per contract; VPIN-style one-sided flow predicts maker losses in single-name markets. A secondary write-up gives 1.91 cents vs 0.82 cents per contract (unverified). | Abstract: [verified: https://law.stanford.edu/publications/adverse-selection-in-prediction-markets-evidence-from-kalshi/]. Cents figures [inferred: search summary]. Kalshi is not Betfair. |
| 1g. Amihud illiquidity | No Betfair or betting-exchange Amihud estimate found. | [unknown]. Resolve by computing from survey data. |
| 1h. Resilience | No published resilience measure for Betfair found. | [unknown]. |
| 1i. Matched volume rate | No peer-reviewed matched volume per market by sport. Practitioner estimates conflict by an order of magnitude (for example GBP 280k per weekday UK race, GBP 200k to 800k range; Premier League win market average GBP 3.2m; minor tennis under GBP 100k) and come from affiliate sites, so treat as context only. | [inferred: search summary of betfairsquare.pages.dev and comparison sites, practitioner, low reliability, not fetched]. |
| 2. Update and trade frequency, vs time to start and in-play | Horse racing: volume per minute rises 4.2 times, liquidity 3.4 times and volatility 1.6 times from minute 10 to minute 1 before the race. The data were recorded at 2 frames per second. No published update-per-second counts by sport or in-play phase. Betfair's default stream conflation is not stated in any source read; NautilusTrader docs say unset conflateMs leaves Betfair's own default, and 0 gives no conflation. | Racing: [verified: https://arxiv.org/html/2510.16008v1]. Conflation: [inferred: search summary of https://nautilustrader.io/docs/python-api-latest/adapters/betfair.html]. Rest [unknown]. |
| 3. Short-horizon predictability from imbalance or flow | Non-Betfair LOB: Cont, Kukanov and Stoikov (50 US stocks): short-interval price change is mostly linear in order flow imbalance at best bid and ask, slope inversely proportional to depth. Gould and Bonart (10 Nasdaq stocks): queue imbalance has a strongly significant link to next mid-price direction, strong improvement over null for large-tick stocks, modest for small-tick stocks. Lipton et al. model the link between top-of-book queue imbalance and trade arrivals. A search summary of another LOB study says the expected move is typically below the spread even at high imbalance (study not identified). Betfair: Goncalves et al. (arXiv 2025) classify the final 2 minutes of price movement in UK horse racing win markets from the preceding ~4.5 minutes of depth data; best model accuracy 30.92% (mean 30.05%) on five classes, about 11 points above baseline; per-class recall: strong down 46.4%, strong up 44.7%, weak and neutral classes 10 to 28%. Sample trade P&L GBP 0.35 profit or GBP 0.28 loss on a GBP 3 stake; 30-day test P&L and commission are not given in the part read. Dzalbs and Kalganova (2018) report 83% ROI in a one-month simulated validation, not net of live costs. | Cont: [verified: https://arxiv.org/abs/1011.6402]. Gould: [verified: https://arxiv.org/abs/1512.03492]. Lipton: [verified: https://arxiv.org/abs/1312.0514] (abstract only). Goncalves: [verified: https://arxiv.org/html/2510.16008v1] (first 100,000 characters). Dzalbs: [verified: https://gpbib.cs.ucl.ac.uk/gp-html/DZALBS_2018_BDR.html]. "Below spread" statement: [inferred: search summary]. |
| 4a. Efficiency, favourite-longshot bias | Tennis exchange (Abinzano, Muga, Santamaria 2019): mispricing rises with trading volume; lower where institutional bettors are present; FLB grows with uncertainty; information absorbed faster in the market that attracts more attention. Tennis exchange FLB stronger for lower-ranked players, later rounds and high-profile tournaments (Applied Economics Letters 2016). Football in-play (Angelini, De Angelis, Singleton, Int. J. Forecasting 2022): mispricing before kickoff and in play, described as reverse FLB (favourites overvalued per the Reading page; the search summary says undervalued, so direction is unresolved), larger after surprising news such as a late goal by a longshot. Whelan (soccer, 2022 to 2024, over 200,000 matches): pre-match and early in-play fit the maker/taker model; later in the match longshots lose heavily even for makers, and takers backing favourites profit. | Abinzano 2019: [verified: https://ideas.repec.org/a/sae/jospec/v20y2019i2p261-285.html]. 2016 paper: [inferred: search summary of https://academica-e.unavarra.es/entities/publication/ba8b15b0-d50b-4e1e-8344-f86ed89bc9ca]. Angelini: [verified: https://research.reading.ac.uk/football-research/new-journal-article-informational-efficiency-and-behaviour-within-in-play-prediction-markets/]. Whelan: [verified: https://ideas.repec.org/p/cpr/ceprdp/20633.html]. Horse racing FLB on Betfair: Finnish thesis found by search, results not read [unknown]. |
| 4b. In-play reaction to events | Brown (Economic Journal 2014): Wimbledon 2011 and 2012 Betfair data, information arriving in each match creates substantial mispricing between two equivalent assets, partly linked to different update frequency of each price; temporary. Brown (Applied Economics 2012) title: "Evidence of in-play insider trading on a UK betting exchange" (abstract not obtained). Brown and Yang (Review of Finance 2017): 9,562 UK horse races 2013 and 2014, trade volume predicts fundamentals, but much of the effect occurs during the race when the outcome is revealed within seconds anyway. Croxson and Reade (Economic Journal 2014, soccer goals): prices do not drift after a goal before half-time, per later citing papers (search summary). Franck, Verbeek, Nuesch (Int. J. Forecasting 2010, 5,478 matches): Betfair predicts outcomes better than 8 bookmakers; betting where bookmaker odds exceed exchange-implied probability gave above-average and sometimes positive returns (not net of live execution). Croxson and Reade 11-19: some support that the exchange leads price discovery over bookmakers. Brown and Yang (IJF 2019): tennis prices become significantly less informative when participation is reduced. Bundesliga fixed-odds study (arXiv 2505.21275, a bookmaker not an exchange): no anticipation of the first goal. | Brown 2014: [verified: https://ueaeprints.uea.ac.uk/id/eprint/44399/]. Brown 2012: [verified: https://ueaeprints.uea.ac.uk/id/eprint/45783/] (title only). Brown and Yang 2017: [verified: https://ueaeprints.uea.ac.uk/58626/]. Croxson and Reade 2014: [inferred: search summary]. Franck: [inferred: search summary of https://ideas.repec.org:443/a/eee/intfor/v26yi3p448-459.html]. Croxson and Reade 11-19: [verified: https://ideas.repec.org/p/bir/birmec/11-19.html]. IJF 2019: [verified: https://ueaeprints.uea.ac.uk/67342/]. arXiv 2505.21275: [verified: https://arxiv.org/html/2505.21275v1]. |
| 5a. Competition, automation | Dumitrescu et al. (Imperial, tennis score inference) state most liquidity on Betfair tennis is provided by automated systems; no share given. The BBE simulator paper says a single LOB snapshot has enough information for short-term predictions under imbalance, a simulation claim. No published share of automated volume, no published latency tables. Betfair applies a transaction charge to accounts placing more than 5,000 bets per hour (Betfair Data Scientists text, as quoted in search results). | Dumitrescu: [inferred: search summary of https://www.doc.ic.ac.uk/~wjk/publications/DumitrescuHuangKnottenbeltSpaniasWozniak.pdf, PDF not decoded]. BBE: [inferred: search summary of https://ar5iv.arxiv.org/html/2105.08310; fetched page had no Betfair numbers]. 5,000 per hour: [inferred: search result quoting https://betfair-datascientists.github.io/wagering/commission, page returned 404 when fetched]. |
| 5b. Bet delay and latency | In-play orders are held a delay before entering the market. Bet Angel's support article, quoting Betfair, gives 1 to 9 seconds as the usual range and up to 12 seconds depending on market and sport. Betfair's developer docs define a per-market betDelay and delay models (PASSIVE, DYNAMIC) per known-facts, but the official pages did not render in WebFetch, so field text is not quoted. Courtsiding and round-trip claims of 12 to 20 s are practitioner claims. | [verified: https://betangel.freshdesk.com/support/solutions/articles/80001073155-why-is-there-a-delay-when-placing-bets-] (practitioner vendor quoting Betfair). Official: [unknown] for per-sport table; open the Betfair Developer Program "Betting Type Definitions" and "Exchange Stream API" pages in a browser. |
| 5c. Who wins and loses (maker vs taker) | Whelan (soccer, transaction-level Betfair data supplied by Betfair, over 200,000 matches 2022 to 2024): model predicts makers earn higher returns than takers and takers' losses grow as win probability falls; empirically pre-match and early in-play fit; later in play longshot bets lose heavily even for makers and takers backing favourites profit. Per-bucket return numbers were not readable (PDF). Kalshi: makers earn about twice as much per contract in single-name markets (see 1f). Franck et al. suggest exchange prices are at least as good as bookmaker prices. | Whelan: [verified: https://ideas.repec.org/p/cpr/ceprdp/20633.html]; dataset size [inferred: search summary of https://www.karlwhelan.com/sports-betting-how-betting-exchanges-work/ (fetched page states "over 200,000 soccer matches")]. Return numbers: [unknown]; resolve by reading https://www.karlwhelan.com/Papers/Betfair.pdf locally. |
| 6. Cost hurdles | Commission is on net market winnings at the market base rate (Betfair Data Scientists and practitioner sites say 2% UK and Irish horse racing, 5% most other markets, with a discount rate; sources conflict on discount details). Betfair dropped the Premium Charge and introduced an Expert Fee from 6 January 2025: based on gross profit over a rolling 52 weeks, no fee under GBP 25,000, 20% from GBP 25,000 to 100,000, 40% above. No published minimum edge calculation for Betfair scalping. Cost in ticks depends on tick size: one tick is 0.01 at prices 1.01 to 2.00 under the ladder in the search summary. | Expert Fee: [verified: https://www.racingpost.com/news/britain/betfair-exchange-to-introduce-new-commission-system-for-2025-as-premium-charge-is-dropped-a7wbg0v4GCAJ] (press). Base rates and discount: [inferred: search summaries, conflicting]. Tick ladder: [inferred: search summary; official page https://betfair-developer-docs.atlassian.net/wiki/x/ZCwp returned empty]. Official charges page not retrievable (support.betfair.com returned 403) so [unknown]; open Betfair's Charges page in a browser. |
| 7. Minimum liquidity rule of thumb for automated trading | None found in peer-reviewed or Betfair sources. Closest: Flepp et al. cut-offs (1c) which describe where bookmakers beat the exchange for bettors, not trading viability. Practitioner guide says minor tennis and League Two under GBP 100k is "too thin for most active trading". | Flepp: see 1c. Practitioner: [inferred: search summary, low reliability]. |

## Metrics and published values

| Metric | Definition as published | Published value | Venue and sample | Evidence |
|---|---|---|---|---|
| Cumulative exchange volume, liquidity cut-off | Cumulative trading volume on the exchange for a match | GBP 23,400 | Betfair soccer, 17,410 matches, 1.8m odds pairs | [inferred: search summary] |
| Average quoted spread cut-off | Average quoted spread at the exchange (unit not given in what was read) | 0.044 | same | [inferred: search summary] |
| Liquidity (horse racing) | Unmatched amounts at best bid and ask | 6,974 (minute 1) to 2,029 (minute 10) mean | UK win, 14,421 races | [verified: https://arxiv.org/html/2510.16008v1] |
| Volume (horse racing) | Per paper Table 2 | 520,865 (minute 1) to 122,693 (minute 10) mean | same | [verified: same] |
| Volatility (horse racing) | Absolute number of tick variations per minute | 1,052 (minute 1) to 642 (minute 10) | same | [verified: same] |
| Sampling rate | Frames per second of recorded depth | 2 per second | same | [verified: same] |
| Depth levels used | Best 2, 3 or 4 price levels around transacted price, by price level | 2 to 4 | same | [verified: same] |
| Kyle's lambda (log-odds form) | Slope of hourly change in log-odds on hourly net signed flow in USD m, 720-hour rolling | 0.518, 0.04, 0.01 | Polymarket 2024 election | [verified: https://arxiv.org/html/2603.03136v1] |
| Volume effect on lambda | Daily lambda regressed on 30-day average daily volume | -0.073 per USD 1m (t -10.29, R2 0.278, n 277) | same | [verified: same] |
| Self-trade share | Share of volume with same counterparty | median 1%, upper tail 22% | Polymarket, 600 markets | [verified: https://arxiv.org/abs/2604.24366] |
| Trade direction accuracy | Feed-inferred vs on-chain direction | 59% of buckets (mean 0.615) | Polymarket | [verified: same] |
| Order flow imbalance | Net supply minus demand changes at best bid and ask | Linear price change; slope inverse to depth | 50 US stocks | [verified: https://arxiv.org/abs/1011.6402] (no R2 on the page) |
| Queue imbalance | Bid vs ask queue at the top predicts next mid move | Significant; stronger for large-tick stocks | 10 Nasdaq stocks | [verified: https://arxiv.org/abs/1512.03492] |
| Forecast accuracy, depth data | Five-class price move over final 2 minutes | 30.92% best, about 11 points above baseline | Betfair UK win, pre-live | [verified: https://arxiv.org/html/2510.16008v1] |
| Bet delay | Seconds an in-play order is held before entering the market | 1 to 9 usual, up to 12 | Betfair, per market and sport | [verified: Bet Angel page above] (quoting Betfair) |
| Expert Fee | Rolling 52-week gross profit | 0% under GBP 25k; 20% GBP 25k to 100k; 40% above | Betfair Exchange from 2025-01-06 | [verified: Racing Post URL above] |
| Maker advantage | Maker vs taker return | Makers higher, takers' losses rise as win probability falls; no numbers read | Betfair soccer | [verified: https://ideas.repec.org/p/cpr/ceprdp/20633.html] |
| Maker per-contract profit | Cents per contract | 1.91 vs 0.82 (single-name vs broad) | Kalshi | [inferred: secondary write-up] |

## Exact fields and operations

Not an API topic. Betfair field betDelay and delay models PASSIVE and DYNAMIC were not re-verified: official pages (betfair-developer-docs.atlassian.net) returned no text through WebFetch. A person should open the Betting Type Definitions and Exchange Stream API pages in a browser.

## Known facts re-checked

| Fact from `docs/known-facts.md` | Still holds? | Evidence |
|---|---|---|
| Bet delay models PASSIVE and DYNAMIC exist | could not check | Official page returned empty. Bet Angel confirms an in-play delay of 1 to 9 s, up to 12 s: [verified: https://betangel.freshdesk.com/support/solutions/articles/80001073155-why-is-there-a-delay-when-placing-bets-] |
| Commission packages Ireland: Basic 2%, Rewards 5%, Rewards+ 8% | could not check | Official charges page not retrievable. Sources found describe market base rate (2% UK and Irish racing, 5% other) and a discount rate; they conflict with this row. |
| Expert Fee tiers and thresholds | partly | Press report gives GBP 25k and 100k at 20% and 40%, rolling 52 weeks of gross profit, from 6 Jan 2025: [verified: Racing Post URL] |
| Transaction charge threshold | partly | 5,000 bets per hour per search result quoting Betfair Data Scientists page: [inferred] |
| Delayed key conflation, `trd` | could not check | Not covered by literature. |

## Costs

| Item | Value | Source and date |
|---|---|---|
| Expert Fee | 0% below GBP 25,000 gross profit over 52 weeks; 20% to GBP 100,000; 40% above | Racing Post, effective 2025-01-06 [verified] |
| Market base rate | 2% UK and Irish horse racing, 5% most others (practitioner) | [inferred] |
| Transaction charge | Applies above 5,000 bets per hour | [inferred] |
| Live key | GBP 499 | known-facts, not re-checked here |

## Impact on the spec

All [inferred]:
- Published evidence supports order-flow and queue imbalance as a modest predictor in liquid LOBs, usually below the spread; Betfair evidence is one pre-off horse-racing paper with about 31% five-class accuracy and no cost-adjusted live result.
- Thresholds on spread, depth, lambda and volume cannot be taken from Betfair literature. The Flepp et al. cut-offs are the only published Betfair liquidity numbers and apply to bettors vs bookmakers.
- Horse racing pre-off shows the largest published liquidity and activity ramp over the last 10 minutes, which supports the 15, 5 and 1 minute time points.
- Delayed-key data (1 to 180 s late) is a different scale from the 1 to 12 s in-play bet delay and the 2 frames per second used in published work, so published results do not transfer directly.

## Unknowns

| Item | What would resolve it |
|---|---|
| Whelan's spreads, match rates and maker/taker return numbers | Read https://www.karlwhelan.com/Papers/Betfair.pdf locally (PDF not decodable by WebFetch). |
| Flepp et al. exact cut-offs and spread unit | Read the published paper (doi 10.1016/j.qref.2016.07.016). |
| Official Betfair charges, discount rate, base rate for Ireland | Open the Betfair Exchange charges page in a browser. |
| Official bet delay table by sport and the betDelay field text | Open Developer Program docs pages in a browser. |
| Full results of the 2025 arXiv horse racing paper (30-day test P&L) | Read arXiv 2510.16008 beyond the first 100,000 characters. |
| Brown 2012 abstract, Croxson and Reade 2014 abstract, Franck et al. numbers, Dumitrescu et al. text | Fetch abstract pages on a publisher site or read PDFs locally. |
| Share of automated volume, update rates by sport, Betfair Amihud, resilience | Measure from the survey recordings. |

## Sources

Fetched with readable text:
- https://arxiv.org/html/2510.16008v1
- https://arxiv.org/abs/2510.16008v1
- https://arxiv.org/abs/1312.0514
- https://arxiv.org/abs/1011.6402
- https://arxiv.org/abs/1512.03492
- https://arxiv.org/html/2603.03136v1
- https://arxiv.org/abs/2604.24366
- https://arxiv.org/html/2505.21275v1
- https://ar5iv.arxiv.org/html/2105.08310
- https://mpra.ub.uni-muenchen.de/126351/
- https://ideas.repec.org/p/cpr/ceprdp/20633.html
- https://www.karlwhelan.com/sports-betting-how-betting-exchanges-work/
- https://ideas.repec.org/p/zrh/wpaper/342.html
- https://econpapers.repec.org/RePEc:eee:quaeco:v:64:y:2017:i:c:p:306-317
- https://ideas.repec.org/p/bir/birmec/11-19.html
- https://ideas.repec.org/a/sae/jospec/v20y2019i2p261-285.html
- https://ueaeprints.uea.ac.uk/id/eprint/44399/
- https://ueaeprints.uea.ac.uk/id/eprint/45783/
- https://ueaeprints.uea.ac.uk/58626/
- https://ueaeprints.uea.ac.uk/67342/
- https://research.reading.ac.uk/football-research/new-journal-article-informational-efficiency-and-behaviour-within-in-play-prediction-markets/
- https://gpbib.cs.ucl.ac.uk/gp-html/DZALBS_2018_BDR.html
- https://law.stanford.edu/publications/adverse-selection-in-prediction-markets-evidence-from-kalshi/
- https://www.racingpost.com/news/britain/betfair-exchange-to-introduce-new-commission-system-for-2025-as-premium-charge-is-dropped-a7wbg0v4GCAJ
- https://betangel.freshdesk.com/support/solutions/articles/80001073155-why-is-there-a-delay-when-placing-bets-

Fetched but unreadable or empty (PDF binary, JS pages, 403 or 404): karlwhelan.com/Papers/Betfair.pdf, mpra PDF 126351, doc.ic.ac.uk Dumitrescu PDF, markrbest.github.io thesis PDF, cerge-ei.cz Wp545 PDF, conference.nber.org f243677 PDF, arxiv.org/pdf/1312.0514, centaur.reading.ac.uk/34884, betfair-developer-docs.atlassian.net pages (x/cA0p, x/6QEp, x/ZCwp, Exchange+Stream+API), support.betfair.com, betfair-datascientists.github.io/wagering/commission, academic.oup.com Brown EJ.

Search-only (not fetched, all [inferred]): Franck, Verbeek, Nuesch IJoF 2010; Croxson and Reade EJ 2014; Abinzano et al. 2016; NautilusTrader Betfair adapter docs; practitioner sites betfairsquare.pages.dev and comparison sites.

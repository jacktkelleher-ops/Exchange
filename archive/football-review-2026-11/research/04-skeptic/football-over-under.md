# Skeptic review: Football over/under goals (Phase 3)

Date: 2026-11-15
Agent: skeptic
Files reviewed (not edited):
- research/03-viability/football-over-under/costs-constraints.md (COSTS)
- research/03-viability/football-over-under/odds-model.md (ODDS)
- research/03-viability/football-over-under/market-structure.md (MS)

Also read: research/00-verify/input-claims.md (with both addenda), docs/inputs/gemini-research.md (claims list and relevant report text), docs/brief.md, docs/rubric.md, research/02-ranking.md, docs/inputs/official/Betfair-Historical-Data-Feed-Specification.pdf (SPEC, pages 1 to 4 read directly).

## Access note

In this session WebFetch failed at DNS for betfair-developer-docs.atlassian.net (including the Confluence REST API route), mpra.ub.uni-muenchen.de, research.reading.ac.uk, the-odds-api.com and betfairsquare.pages.dev. These hosts must be allowed in the session network settings before the DEV citations and paper pages can be re-fetched. I did not touch the Betfair consumer sites (Cloudflare). Consequences:

- DEV-tagged claims could not be re-fetched. They are marked `not re-fetched` below and checked only for consistency with input-claims.md.
- SPEC claims were checked directly against the PDF.
- A few claims were checked through WebSearch summaries. Those checks are weaker than a fetch and are labelled as such.

## 1. Input-derived claims (checked first)

| Input claim | Where used | Status | Reason |
|---|---|---|---|
| 1. Ireland Basic 2%, Rewards 5%, Rewards+ 8% | COSTS s1, ODDS s5, MS constants | weakened as used | Still `[inferred]` (search summaries only, official page not read). The Phase 3 files then treat 5% as the planning case. The input itself (gemini-research.md lines 87 to 92) says that in Rewards jurisdictions, including Ireland, the package rate replaces the market base rate. If Basic 2% applies to all exchange markets, the operator can simply choose 2%, and the 5% planning case is a pessimistic choice, not a constraint. A WebSearch this session found summaries saying the package sets the exchange rate, with Basic at 2%, but none confirmed football specifically. Unverified either way. |
| 2. Expert Fee tiers | COSTS s2 | confirmed as irrelevant | Inferred tiers; the non-binding conclusion at EUR 500 holds under any of the reported bases. |
| 3. Transaction charges | COSTS s2 | survived | Threshold unknown, but a pre-play model placing tens of bets a day is far below 1,000 or 5,000 an hour. |
| 4. Live key GBP 499 | COSTS s3, MS D | not re-fetched | Consistent with input-claims.md row 4 (`[verified: DEV/2687105]`). Could not re-open the page. |
| 4a. Delayed key facts (bets on live exchange, 3 levels, no total matched, 1 to 180 s delay, 2 connections and 200 markets) | all three files | not re-fetched | Consistent with input-claims.md row 4a and its addendum. |
| 5. Historical tiers and prices | COSTS s4, ODDS s2/s3 | partly confirmed | SPEC confirms BASIC = ltp plus marketDefinition at 1-minute intervals, ADVANCED = best offers, traded volume and trd at 1 second, PRO = full ladder tick by tick (SPEC p3 to p4). SPEC does not say Basic is free (p1 says the service provides data "for purchase"). Prices remain `[unknown]`. Market coverage is not in SPEC. |
| 7. Bet delays | MS D | not re-fetched | Passive and dynamic rules consistent with input-claims row 7. SPEC p2 confirms the betDelayModels field exists from 17/08/2026. |
| 8. No winner limits on Betfair | COSTS s5, MS open items | unknown | Correctly left `[unknown]` in all three files. |
| 9. Reading paper | MS D | not re-fetched | Host blocked. Consistent with input-claims row 9. |
| 10. MPRA 126351 | MS A, D | confirmed by search summary only | WebSearch summaries (RePEc, IDEAS, the author's blog) agree: Karl Whelan, soccer data from Betfair, pre-match and early in-play fit the model, late in-play longshots lose even for makers. One summary says makers "generally break even" pre-match. That supports, rather than weakens, the no-go on Strategy A. |
| 13. Women's and lower-league football less efficient | not used | unknown | None of the three files relies on it. |
| Input: cross-matching runs across linked markets (Match Odds and Under/Over), gemini-research.md lines 341 to 343 | MS B | unknown, and the MS file is right not to adopt it | MS says it found no evidence of matching between separate markets. SPEC p2 only shows a per-market crossMatching flag. The input claim is unverified and should not be relied on. |
| Input: partition arbitrage "occasionally positive at 2% commission" (lines 688 to 698) | MS B | unknown | No evidence. MS spread arithmetic (below) is the better guide. |

## 2. Claim checks, Phase 3 files

### SPEC claims (checked directly against the PDF)

| Claim | File | Result |
|---|---|---|
| Data from May 2015, AUS/NZ from Oct 2016, JSON in tar.bz2 | ODDS, MS addendum | confirmed (SPEC p1). Note: the May 2015 start is for the service, not stated per plan. |
| marketDefinition in all plans carries marketType, marketBaseRate, inPlay, betDelay, crossMatching, status, discountAllowed | ODDS s2, MS addendum | confirmed (SPEC p1 to p2, "Data Returned - All Pricing Plans") |
| Runner status WINNER/LOSER and runner bsp in all plans | ODDS s2 | confirmed (SPEC p2, RunnerDefinition) |
| BASIC: ltp only, 1-minute intervals, no volume, no ladder | ODDS s2, MS addendum | confirmed (SPEC p3 table and p4 subscription table) |
| ADVANCED: batb/batl, tv by market and runner, trd, 1 second | MS addendum | confirmed (SPEC p3 to p4) |
| PRO: full ladder, trd, tv, BSP near/far, tick by tick | MS addendum | confirmed, with a detail: runner-level tv is marked N for PRO (SPEC p3). Market tv and trd are Y. |
| "The spec is field-level only", no market coverage list | ODDS s2 | confirmed |
| "Free Betfair close and labels if covered `[verified: SPEC]`" | ODDS s9 summary | contradicted as tagged. SPEC does not say Basic is free. "Free" is `[inferred]` from community sources. The data table row in ODDS s3 limits the tag to fields, but the summary row does not. |

### DEV claims (could not re-fetch; consistency only)

| Claim | File | Result |
|---|---|---|
| marketBaseRate and discountAllowed exist in the API | COSTS s1, ODDS s5, MS | not re-fetched. The same fields are confirmed in SPEC p1 to p2. |
| Min bet EUR 1 | ODDS s7, MS | not re-fetched; consistent with input-claims addendum. COSTS body says EUR 2; its own addendum overrides it. The body text was not corrected. |
| Ladder steps (0.01 below 2, 0.02 from 2 to 3, etc.) | ODDS s5, MS | not re-fetched; consistent with input-claims addendum and with input report. |
| 200 point request cap, EX_BEST_OFFERS weight 5, about 40 markets per call | COSTS s3, MS B | cap not re-fetched (consistent with addendum). Weight 5 remains `[inferred]`. 200 / 5 = 40 is correct. |
| Passive in-play orders skip the delay; football dynamic no delay at half time | COSTS s3, MS D | not re-fetched; consistent with input-claims row 7. |

### Other sources

| Claim | File | Result |
|---|---|---|
| The Odds API Starter: 500 credits a month free | MS C, F | Tagged `[verified: https://the-odds-api.com/, as summarized in search]`. That is a search summary, not a fetch, so the tag is wrong. Content is consistent with a WebSearch this session (500 credits, cost = markets x regions, historical 10x). Re-tag as `[inferred]`. |
| O/U 2.5 most traded line; typical prices 1.85 to 2.10 | MS constants | not re-fetched (host blocked). Correctly tagged `[inferred]`. |
| Top-5 leagues about 1,750 matches a year | ODDS s4 | confirmed by arithmetic: 380 x 3 + 306 x 2 = 1,752 (Bundesliga and Ligue 1 at 18 teams). "About 38 matches a team" is wrong for those two leagues (34). Immaterial. |

## 3. Inferences presented as facts

1. ODDS s9: "Free ... `[verified: SPEC]`". Free is not in SPEC (see above).
2. MS C and F: The Odds API facts tagged `[verified]` from a search summary.
3. COSTS s1 "How to resolve", ODDS s5 and "What would change the call", MS open items: all three treat `marketBaseRate` as the account's commission rate. For an Irish account under My Betfair Rewards, the input says the package rate (2/5/8) applies instead of market base rate times discount. If that is right, `marketBaseRate` on a football market will likely read 5% even for a Basic-package account paying 2%. The proposed test ("marketBaseRate reading 2% rather than 5%") would then give the wrong answer, and any backtest that charges history `marketBaseRate` would overstate costs for a Basic account. This is `[inferred]` from the input, but no file flags the risk.
4. ODDS s6: "175 to 260 bets a year" is presented as the operator's capacity at 5 hours a week. An automated pre-play model's bet count is set by the filter and the league list, not by hours. The figure is a choice (top five leagues, 10 to 15% flagged).
5. ODDS s6 CLV route: "sd about 3%" per bet is an invented number. The input cites sigma_CLV about 0.10. At 10% the sample is (2 x 10 / 1)^2 = 400 bets, not 36.
6. MS A: "half of orders fill both legs", "move of 2 to 5 ticks". Invented parameters; correctly tagged `[inferred]`, but the resulting range of -1.0% to +0.5% is no more than the assumptions put in.
7. MS B: per-leg prices (0-0 at 12.5, etc.) are illustrative, not observed. Tagged as illustrative. Acceptable.
8. ODDS s5: "Pre-match O/U markets typically move by less than that between a 3.5 hour snapshot and the close" is tagged `[unknown]` yet used in the argument.

## 4. Arithmetic re-done

COSTS cost table: recomputed every row. c(o-1)/o and p* - 1/o match to rounding (for example o = 2.00: 1.00% and 0.505 pp at 2%; 2.50% and 1.282 pp at 5%; o = 1.70 at 5%: 2.06% and 1.236 pp). Matches the input's 0.505 and 1.282 pp. Lay cost c/o per unit liability is correct. Confirmed.

ODDS s5 required edge with one tick: p* at o = 1.98 is 1/(1 + 0.98 x 0.98) = 0.5101 (1.01 pp) at 2% and 1/(1 + 0.98 x 0.95) = 0.5179 (1.79 pp) at 5%. Confirmed as arithmetic. Two problems with the inputs to it:

- Slippage is likely double counted. A full tick is charged on top of a benchmark that is the ltp, which sits on one side of the spread or the other. Against a mid-like benchmark the cost of crossing a one-tick spread is half a tick. Also, MS reports O/U 2.5 prices of 1.85 to 2.10, so many bets sit below 2.00 where the tick is 0.01, not 0.02. Half a tick at 1.90 is 0.005 / 1.90 = 0.26% of stake. Realistic slippage is 0.25% to 1.0%, not a flat 1.0%.
- Re-done hurdle at 2% commission with 0.25% to 0.5% slippage: about 1.25% to 1.5% EV, about 0.6 to 0.75 pp. At 5%: about 2.75% to 3.0% EV.

ODDS s6 sample size: the logic is wrong. The table sets "edge to show" equal to the cost hurdle (2.0% or 3.5%) and gets 10,000 and 3,265 bets. That tests whether gross ROI differs from zero. If the gross edge equals the hurdle, the net edge is zero and no sample proves net profit. It also produces the absurd result that 5% commission needs fewer bets than 2%. The correct quantity is the net edge after costs. At z = 2 and sd = 1: net 2% needs 10,000 bets, net 1% needs 40,000. With 80% power one-sided (z total 2.487) net 2% needs 15,457 (matches the input report). So the file's numbers understate the sample needed. This error makes the no-go look less severe, not more.

ODDS s6 log loss: 0.0175^2 / (2 x 0.25) = 0.00061 nats; per-match sd about 0.035; n = (2 x 0.035 / 0.0006)^2 = 13,611. Confirmed. It assumes the model is better by 1.75 pp on every match, which is generous.

ODDS s6 backtest SE: 1 / sqrt(2,000) = 2.24%. Confirmed.

ODDS s7 ruin: exp(-6) = 0.25%, exp(-3) = 5.0%, exp(-2) = 13.5%, exp(-1.2) = 30.1%. Confirmed. Caveat: the formula is loss from the start. If the brief's 30% means peak-to-trough drawdown, the risk is higher over a long horizon. At EUR 1 to 2 stakes and a few hundred bets a year it does not bind. Kelly 2% of bankroll at EV 2% and o = 2 is correct.

ODDS s7 income: 200 x 2 x 0.02 = 8; 200 x 3 x 0.035 = 21. Arithmetic correct, but the EUR 21 case applies 3.5% as a net edge when 3.5% was defined as the hurdle. Even a generous re-run (1,000 bets a year across more leagues, EUR 5 stakes, 2% net) gives EUR 100 a year.

MS A round trip: L = 2.04/2.02 S = 1.0099 S; locked 0.0099 S; net after 5% on profit 0.94%. Confirmed. Adverse selection line: 0.47% + 0.5 x (-1% to -2.5%) = -0.03% to -0.78%. Confirmed.

MS B tick widths: 0.32, 0.25, 0.41, 0.47, 0.41, 0.15 pp, sum 2.02 pp, plus 0.5 pp for Under 2.5. Confirmed. Over 1.5 plus Under 2.5 = 1 + P(exactly 2 goals). Confirmed by definition.

MS C: L = S ob / (ol - c) derived from equal profit in both states. Break-even 2.116 at 5% and 2.082 at 2% for ol = 2.06. Examples +3.3% and -0.75%. Ratios 1.0105 and 1.027. All confirmed.

## 5. Leakage, bias, fills, restrictions

- Leakage in the proposed liquidity filter (ODDS s2): "filter out markets whose ltp did not update in the final minutes" uses information from after the 3.5-hour bet time. Fine for the benchmark, not fine for choosing which bets enter the backtest. The filter must be applied at the bet timestamp.
- Leakage via marketDefinition: Basic files carry the final runner status and settled market status in the same stream. A parser that reads the last marketDefinition for features (not just labels) leaks the result. The file warns about inPlay ticks but not this.
- Fill optimism: the backtest entry price is a Basic ltp at 3.5 hours, which may be a lay-side trade and may be stale in a thin line. There is no record of what was available to back at that moment. One tick of slippage partly covers this. Depth is `[unknown]`, so fill at stake is assumed, though at EUR 1 to 5 that is reasonable for top-league O/U 2.5.
- Survivorship: the backtest universe is markets that exist in Basic and leagues that football-data.co.uk carries. Not a large bias for top leagues, larger for lower leagues.
- Multiple testing: noted in ODDS. Correct.
- Account restrictions: Betfair winner limits `[unknown]` in all files. The delayed key "for development purposes and any functional testing" wording is flagged in all three files. Fair.
- Commission basis: ODDS backtest plan charges history `marketBaseRate`. See item 3 in section 3: that may overstate cost for a Basic-package account.

## 6. Who is on the other side

Pre-play O/U 2.5 on Betfair in top leagues: bookmaker hedgers, arbitrage bots referencing Pinnacle, syndicates, and recreational money that tends to back Overs. A results-only Poisson model uses the same public inputs as all of them and none of the late information (line-ups, money). There is no named reason a sharp participant would leave a 1 to 3% edge in a liquid top-league O/U line. The only argument for persistence is capacity: at EUR 1 to 5 stakes, the operator could exploit edges too small or too thin for syndicates to bother with, which points to lower leagues. None of the files tested lower leagues, and the input claim 13 on their inefficiency is unsupported. The "close is efficient" risk named in ODDS is the right one.

## 7. Verdicts per call

### ODDS: "no-go for trading this bankroll; optional backtest only"

Verdict: weakened.

- The direction (do not stake money now) holds. No evidence of O/U mispricing exists in the review, and the other side is well informed.
- The reasons given are partly wrong or off-brief:
  - The brief's objective is "a positive expected return after costs". It sets no income threshold. The main stated reason (EUR 4 to 21 a year) is an income test the brief does not ask for. Low absolute income at a EUR 500 bankroll is true of every market in the review and cannot by itself justify no-go for this one.
  - The sample-size section measures the wrong quantity (gross edge equal to the hurdle instead of net edge). Correct numbers are larger, so this does not rescue the strategy, but the cited "3,000 to 10,000 bets" is not a valid figure.
  - The cost hurdle is likely too pessimistic: 5% commission as planning case when the operator can probably choose Basic 2% (unverified), and a full tick of slippage where half a tick at 0.01 steps is more likely below odds 2.00. A re-done hurdle is about 1.25% to 1.5% EV (0.6 to 0.75 pp) at 2%.
  - The CLV route sample (36 bets) uses an invented sd; at the input's sd 0.10 it is about 400 bets, which is still reachable in one to two seasons of automated betting across more leagues. The file dismisses CLV, but the input's own design rule is to judge pre-game edges by CLV.
  - The proposed commission check via `marketBaseRate` may not show the rate this account pays.
- The decisive test the file names (one Basic soccer month to check O/U coverage, then a 4 to 5 week free backtest against the close) is cheap and within the EUR 0 budget. Under the brief, that makes the honest label needs-more-data (backtest first, no live staking), not no-go. ODDS also conflicts with MS Strategy F, which rates the same underlying edge (beating a sharp close pre-play) as needs-more-data.

### MS: A. Passive quoting on O/U 2.5

Verdict: survived. Stale 1 to 180 s view and no queue or volume on the delayed key (consistent with verified input) are sufficient. MPRA summaries say makers roughly break even pre-match before commission, which supports the call. The numeric range is assumption-driven.

### MS: A2. Passive entry as tactic

Verdict: survived. Arithmetic correct (0.5% at 1.95, 1.0% at 2.04). The 0 to +0.5% net figure is assumed.

### MS: B. Cross-market consistency

Verdict: survived. Partition arithmetic and tick widths check out; the 2.5 pp one-tick cost across seven legs exceeds any documented gap. The input's cross-market cross-matching claim is unverified and was rightly not used.

### MS: C. Bookmaker vs exchange arbitrage

Verdict: survived. All formulas and examples recomputed correctly. Bookmaker account restriction is `[inferred]` but widely reported. The Odds API tag must change from `[verified]` to `[inferred]`.

### MS: D. In-play reaction

Verdict: survived. Free-key price lag and the GBP 499 live key are consistent with verified input. Paper findings could not be re-fetched.

### MS: E. Order flow and ladder signals

Verdict: survived. Hurdle 1.5% to 3.5% (at 2% to 5% commission plus 0.5% to 1.0% tick) is consistent; 3 levels and no volume on the delayed key.

### MS: F. Sharp-book reference

Verdict: survived as needs-more-data. Same edge as ODDS; the label is the more defensible of the two. The 2% to 5% commission caveat and the `marketBaseRate` issue apply here too.

### COSTS: claims (no go/no-go call in the file)

| Claim | Verdict | Reason |
|---|---|---|
| Cost table arithmetic | survived (confirmed) | Recomputed all rows. |
| 5% as planning case | weakened | Too pessimistic if Basic 2% applies to football for an Irish account; unverified both ways. |
| Rate readable from `marketBaseRate` | weakened | Likely shows the market base rate, not the Rewards package rate. |
| Min stake EUR 2 (body) | refuted | Own addendum and input addendum give EUR 1; body not corrected. |
| Delayed key facts | survived | Consistent with input-claims; not re-fetched this session. |
| Basic tiers content (s4, `[inferred]`) | survived, now confirmed for content | SPEC confirms BASIC/ADVANCED/PRO content. "Pro at 50 ms" from community FAQ is not what SPEC says (SPEC: tick by tick). Prices `[unknown]`. |
| Expert Fee and transaction charges not binding | survived | Holds under any reported basis at this scale. |
| Irish tax | unverified | Rests on a 2012 parliamentary reply seen only in a search summary. Not tax advice. |
| Top constraint 1 (data) | survived, partly resolved | SPEC removes the field-content question; O/U coverage in Basic still `[unknown]`. |
| Top constraint 2 (commission) | survived | Correctly named; the resolution path is flawed (see `marketBaseRate`). |

## 8. What would settle the open points

1. Allow betfair-developer-docs.atlassian.net, mpra.ub.uni-muenchen.de, research.reading.ac.uk and the-odds-api.com, then re-fetch the DEV pages and papers.
2. A person reads the My Betfair Rewards terms: does Basic 2% apply to football O/U for an Irish account, and is the charged rate independent of `marketBaseRate`?
3. Download one free Basic soccer month and confirm O/U market types are present and the file is free.
4. If 3 holds, run the ODDS backtest with: net-edge sample sizes, liquidity filter applied at bet time, labels only from final marketDefinition, commission at the package rate, half-tick slippage sensitivity, and CLV against the close with measured sd.

Sources:
- docs/inputs/official/Betfair-Historical-Data-Feed-Specification.pdf (pages 1 to 4, read directly)
- [RePEc MPRA 126351](https://econpapers.repec.org/RePEc:pra:mprapa:126351) and [Karl Whelan blog](https://www.karlwhelan.com/sports-betting-how-betting-exchanges-work/) (WebSearch summaries only)
- [The Odds API](https://the-odds-api.com/) and [OddsPapi on the free tier](https://oddspapi.io/blog/the-odds-api-free-tier-limits) (WebSearch summaries only)
- [Sporting Life commission guide](https://www.sportinglife.com/free-bets/guides/betfair-exchange-education/how-does-commission-work) and [Timeform commission guide](https://www.timeform.com/betting/betfair-exchange-education/how-does-commission-work) (WebSearch summaries only)

# Skeptic review: pre-play passive resting orders (maker side)

Date: 2026-11-15
Agent: skeptic
Files reviewed (not edited):
- research/03-viability/passive-resting-orders/costs-constraints.md (COSTS)
- research/03-viability/passive-resting-orders/odds-model.md (ODDS)
- research/03-viability/passive-resting-orders/market-structure.md (MS)
Also read: research/00-verify/input-claims.md (both addenda), docs/inputs/gemini-research.md claims list, docs/brief.md, docs/inputs/official/Betfair-Historical-Data-Feed-Specification.pdf (SPEC, pages 1 to 4 read directly).

## Access in this session

- mpra.ub.uni-muenchen.de, ideas.repec.org, econpapers.repec.org, nautilustrader.io and betfair-developer-docs.atlassian.net (including the Confluence REST API path) did not resolve (DNS failure, outside the session allow list). These hosts must be allowed before a re-fetch. No Cloudflare challenge was bypassed.
- I could therefore not re-read the dev-doc pages DEV/2687105, DEV/2686993, DEV/2687396 or the MPRA paper body. Claims resting on them are marked "not re-verified" below. They were recorded as read by the orchestrator earlier on 2026-11-15.
- The SPEC PDF was read directly, pages 1 to 4.
- WebSearch summaries were used for the MPRA abstract. That is a summary of the abstract and the author's site, not the paper body.

## 1. Input-derived claims checked first

### 1a. MPRA 126351 (Gemini claim 10, input-claims row 10)

| Claim as used in Phase 3 | Status | Finding |
|---|---|---|
| Paper exists: Whelan, "Agreeing to Disagree: The Economics of Betting Exchanges", MPRA 126351, also CEPR DP 20633, revised Jan 2026 | confirmed (search summary) | Search results list MPRA 126351, CEPR DP 20633 and a January 2026 revision on karlwhelan.com. |
| Pre-match and early in-play, makers earn more than takers | confirmed, but incomplete | The search summary of the abstract says: pre-match and early in-play, "Takers lose more and more heavily on longshots, while Makers generally break even." The "makers earn more" claim is relative. In absolute terms makers are about break-even. |
| "Evidence that makers can win" (ODDS 5c) | contradicted | The source summary says makers break even on average. That is evidence that the average maker does not win. ODDS presents the paper as weak support for a maker edge. It is the opposite. |
| Paper covers soccer only, not racing (MS) | confirmed (search summary) | "Betfair transaction data covering over 200,000 soccer matches." |
| Whether returns are net of commission | still unknown | Not in any summary seen. If the break-even figure is before commission, the average pre-match maker loses after commission. If it is after commission, the average maker earns about zero. Either way no positive absolute maker return is shown. |
| Late in-play longshot losses even for makers | confirmed (search summary) | "longshot bets lose an increasing amount of money as the game nears its end, even for Makers." |
| research/02-ranking.md line 124 says the MPRA result is "net of commission" | not found at source | Outside the reviewed folder, but the orchestrator should not carry it into the decision memo. No source seen states commission treatment. |

Consequence. The interpretation risk that MS lists as the biggest risk to strategy 1 ("the paper may show makers positive after commission") is largely answered by the abstract summary: makers break even. This strengthens the no-go on strategy 1 and on any uninformed resting-order strategy. It undercuts the ODDS framing.

### 1b. Other input-derived claims used in this folder

| Claim (source) | Phase 3 use | Status |
|---|---|---|
| Ireland commission Basic 2% / Rewards 5% / Rewards+ 8% (Gemini 1) | Both 2% and 5% modelled | still `[inferred]`. Not re-verifiable. Note: if the 2% Basic package exists and is selectable, the user would choose it, and every 5% scenario in the folder is a pessimistic branch, not a co-equal case. |
| UK/IE racing Win MBR 2% (Gemini text) | COSTS: unresolved | still `[inferred]`. Note that under a Rewards package the account rate may override marketBaseRate, so reading marketBaseRate from Basic files does not settle the account's rate. ODDS section 8 lists "marketBaseRate shows 2%" as a call-changer. That is an inference, not a resolution. |
| TX charge exemption for makers at back 10+ / lay liability 100+ (Gemini 3) | COSTS: unknown | unknown, correctly tagged. |
| CLV standard deviation about 0.10 (Gemini section 5, "How Pros Bet") | Not cited. ODDS uses 3% and 6%, MS uses 4% | Phase 3 values are lower than the only input figure and are not sourced. See section 3. |
| Min stake GBP 1 to 2, BSP min liability GBP 10 (Gemini) | Addendum: EUR 1 min | Not re-verified this session (DEV host unreachable). |
| Ladder increments (Gemini) | Used throughout | Matches orchestrator addendum. Not re-verified this session. |

## 2. Phase 3 claims checked

Status key: confirmed (re-checked at source this session), survived (not re-checkable, no contrary evidence found), weakened (partly wrong, overstated, or mis-tagged), refuted (contradicted).

### 2a. Claims checked against SPEC (read directly)

| Claim | File | Status | Note |
|---|---|---|---|
| Basic is 1-minute LTP plus marketDefinition, no volume, no ladder, no traded-at-price | ODDS, MS, COSTS | confirmed | SPEC p3 table and p4: BASIC = EX_LTP and EX_MARKET_DEF at 1 minute. tv, batb, batl, trd are N/A for BASIC. |
| marketBaseRate, inPlay, betDelay, runner status, bsp, adjustmentFactor in every plan | ODDS, MS | confirmed | SPEC p1 to p2 "Data Returned - All Pricing Plans". |
| Advanced: 1 s, best back/lay, traded volume, traded price-volume | ODDS, MS | confirmed | SPEC p3 to p4. |
| Pro: tick by tick, full ladder, BSP near and far | ODDS, MS | confirmed | SPEC p3 to p4. |
| Basic is free | ODDS data table "Cost: Free ... [verified: SPEC p1-4]"; ODDS section 2 "free Basic [verified: SPEC p1-2]" | weakened (mis-tagged) | SPEC p1 says the service "provides time stamped Betfair Exchange data for purchase." It does not say Basic is free. Free Basic is a secondary-source claim. Tag should be `[inferred]`. The whole EUR 0 offline drift study depends on it. |
| Basic runs from May 2015 | ODDS | weakened (minor) | SPEC says the data service starts May 2015. It does not say per plan. |
| Advanced shows only "top levels" | ODDS, MS | survived | SPEC says batb/batl are "keyed by level" with no level count. The number of levels is not stated. |
| "Queue simulation needs Pro" | MS strategy 2 tags it `[verified: SPEC p3-4]`; ODDS and MS elsewhere tag `[inferred from SPEC]` | weakened (inference tagged verified in MS strategy 2) | SPEC lists fields, not what a simulation needs. Advanced has trd (traded volume by price) and best-level sizes at 1 s. A standard approximation for orders at the touch (queue ahead = displayed size at join, decremented by traded volume at that price) is possible with Advanced. It is cruder than Pro but not impossible. Both are paid, so the EUR 0 conclusion holds, but the "Pro only" claim is overstated. |
| Football close = last 1-minute LTP before the off | ODDS, MS | confirmed for field, inference for quality | LTP is a last trade, not a mid. It can be stale in quiet periods and carries bid-ask bounce. See section 4 on leakage. |

### 2b. Claims checked against dev docs (not re-verifiable this session)

| Claim | Status | Note |
|---|---|---|
| Delayed key can place bets on the live exchange (v144, 2026-11-02) | survived, not re-verified | DEV host unreachable. A fresh search summary still surfaces official-page snippets saying the delayed key "does not allow betting transactions" and that "the Stream API is only available via the Live Application Key". The orchestrator reports a newer page version that overrides these. I cannot confirm which is current. |
| Delay 1 to 180 s | survived, not re-verified | Search snippets show both 1-180 s and 1-60 s official wording. A third-party summary (NautilusTrader docs, not fetched) describes delayed stream data as conflated to about 3-minute intervals. If true, staleness is near the upper bound most of the time, which makes the no-go calls more robust, not less. |
| Delayed key: Stream API 2 connections, 200 markets, 3 levels, no total matched | survived, not re-verified | As above. Conflicts with an older snippet saying stream is live-key only. |
| "Development purposes and any functional testing" wording | survived, not re-verified | |
| Min bet EUR 1, ladder table | survived, not re-verified | |
| "Passive in-play orders that cannot match immediately skip the bet delay" | survived as a fact, weakened as applied | input-claims row 7 records the verified scope: PASSIVE betDelayModel, plain LIMIT, LAPSE only. SPEC p2 shows betDelayModels exist only on markets published since 17/08/2026 and can be absent. COSTS section 4 and ODDS section 1 use it as the reason PERSIST "must not be used". That is a non sequitur. The feature concerns orders placed in-play under a PASSIVE model. It says nothing about pre-play PERSIST orders. PERSIST is still a bad idea for a pre-play test, but for a different reason: a resting order carried into play is exposed to in-play informed flow. |

### 2c. Other claims

| Claim | File | Status | Note |
|---|---|---|---|
| Real bets are out of scope | ODDS, MS | confirmed | docs/brief.md "Out of scope: Placing real bets." |
| Commission on net market winnings, not per bet | COSTS, MS | survived `[inferred]` | Consistent with Gemini text. Not official. |
| Matching is price then time | MS | survived `[inferred]` | Gemini claims Betfair confirmed price, then direct over cross-match, then FIFO. Not verified. Note that cross-matching can place virtual liquidity ahead of or alongside the queue. MS ignores it. |
| "A delayed-key quoter is the slowest quoter in the book by construction" `[verified: DEV/2687105]` | MS | weakened (inference tagged verified) | The page verifies a data delay. It does not rank participants. Manual web users and slow API users also quote. The statement is plausible for the queue front but is inference. |
| "A view 1 to 180 s old is stale by an amount comparable to the edge sought" `[verified]` | ODDS 5c | weakened (inference tagged verified) | Only the delay range is from the source. "Comparable to the edge" is an unmeasured inference. |
| "Separating moving flow from non-moving flow needs volume, queue and tape" `[verified: DEV; SPEC]` | ODDS 5c | weakened (inference tagged verified) | The sources verify what data is absent. The "needs" is inference. |
| Live key GBP 499 | all | survived, not re-verified | |

## 3. Arithmetic re-done

| Item | File | Result |
|---|---|---|
| Round-trip gross = tick / p1, table values 0.667%, 1.000%, 1.667%, 2.000% | COSTS 8 | confirmed. Derivation checked: back S at p2, lay S x p2/p1 at p1, profit S(p2 - p1)/p1 either way. |
| Break-even completion, one-tick stop, q = 1/(2 - c): 50.51% at 2%, 51.28% at 5% | COSTS 8, MS S2 | confirmed. |
| Break-even completion, two-tick stop: 66.4% at 2%, 67.2% at 5% | COSTS 8, MS S2 | refuted (wrong numbers). q(1 - c) = 2(1 - q) gives q = 2/(3 - c) = 67.11% at 2% and 67.80% at 5%. Error is about 0.7 points and does not change any call. |
| MS S2 table per-attempt EV: -0.41%, -0.01%, +0.19%, -1.11%, -0.51%, -0.21% | MS | confirmed at 2% commission. |
| Commission hurdle c(1 - 1/p): 0.67/1.00/1.33/1.60% at 2%, 1.67/2.50/3.33/4.00% at 5% | ODDS 5a | confirmed as arithmetic, weakened as applied. It assumes the filled position is held to settlement. See section 5. |
| "EV = 0.5 x 2.01 - 1 = +0.5%" for resting one tick better than mid at 2.0 | MS cross-cutting, S1 | weakened. 2.01 is not a valid price. The ladder steps 0.02 above 2.00 (2.00, 2.02). The intent (half a 1% tick versus mid) is right, but "quoting one tick better than the touch" in a one-tick market would cross the spread, so the setup is internally inconsistent. |
| MS S1 commission drag 0.02 x 0.5 x 1.01 = 1.0%; 0.05 x 0.5 x 1.01 = 2.5% | MS | confirmed as arithmetic, same hold-to-settlement caveat. |
| ODDS 6a n = (2 sigma / mu)^2: 21, 144, 400, 85, 576 | ODDS | confirmed as arithmetic. But t = 2 with no power term gives about 50% power. MS uses 2.8 (80% power). The two files are inconsistent. At 80% power ODDS's "400 fills" case becomes (2.8 x 3 / 0.3)^2 = 784. |
| CLV sigma assumptions: 3% football, 6% racing (ODDS), 4% (MS) | ODDS, MS | weakened. Unsourced, and the only figure in the inputs is about 10% (Gemini, How Pros Bet). Racing early price to BSP is likely more volatile than 6% `[inferred]`. At sigma = 10% and mu = 0.5%, 80% power needs (2.8 x 10 / 0.5)^2 = 3,136 fills. Sample sizes in both files are optimistic, not pessimistic. Sigma is measurable for free from Basic if Basic is free and covers these markets. |
| ODDS 6b: 40,000 and 160,000 bets, 1,333 weeks | ODDS | confirmed. |
| ODDS 6c ruin probabilities 0.86 and 0.74 | ODDS | confirmed as arithmetic (exp(-0.15) = 0.861, exp(-0.30) = 0.741; MS used variance 1,225 instead of 1,250, immaterial). Weakened as applied: per-fill SD of 1.0 assumes holding to settlement. If fills are hedged at the close, per-fill SD falls to the CLV SD (3% to 10%) and drawdown risk becomes small. |
| MS section 9: n = (2.8 x 4 / 0.5)^2 = 502; 313,600; 1,700 orders; 13 to 25 weeks; EUR 10 expected cost | MS | confirmed as arithmetic. |
| MS section 9: "15 open orders of EUR 2, so under EUR 30 exposure" | MS | weakened. Exposure on a lay is liability, not stake (EUR 2 lay at 5.0 is EUR 8 liability). Matched bets held to settlement are no longer open orders but are still exposure. The cap does not bound exposure as written. |

## 4. Leakage, bias and optimistic assumptions

1. LTP bid-ask bounce (ODDS section 4 drift study). Basic LTP alternates between back and lay sides. A rule fitted on "price at T versus LTP at the off" will find spurious mean reversion from bounce alone. That would show an apparent drift edge that is not tradeable. ODDS does not mention it. This is the one place where the free test is biased in favour of the strategy.
2. Stale LTP. In quiet early pre-play periods the 1-minute LTP may be hours old. Using it as "price at T" mixes times. ODDS rates look-ahead risk "Low" for Basic. For this use the risk is bias, not look-ahead, but it is not low.
3. Fill simulation from LTP. ODDS correctly says touch-equals-fill overstates fills. Survived.
4. Closing benchmark. The 1-minute LTP before the off can be up to 60 s early (MS notes this). For football this misses the last minute but is minor. Survived.
5. Counterfactual logging of unfilled orders (ODDS, MS selection test). Good design. Survived.
6. Survivorship. Not a material issue in this folder. Markets that were voided or had non-runners need handling (adjustmentFactor is in SPEC), which neither file details for racing. Minor.
7. Account restrictions. Winning-account limits are correctly `[unknown]`. The bigger restriction is the dev-key intended-use wording, which both files flag. Survived.
8. Slippage. Not applicable to resting orders except at the stop-out. The stop-out in COSTS and MS assumes a one-tick exit. In a moving market the exit is often two or more ticks. This makes the scalping case worse, so the no-go is not weakened by it.

## 5. Are the no-go calls too pessimistic?

Where the folder is too pessimistic:

1. Hold versus hedge. ODDS (main reason) and MS strategy 1 charge commission as if every fill is held to settlement: c x (1 - 1/p), which is 1.0% at 2.0 and 2.5% at 5%. A filled order with positive CLV can instead be hedged near the close. Cost: crossing about half a tick (about 0.5% at 2.0) plus commission on the small net, about c x CLV. At 5% commission this is roughly 0.5% instead of 2.5%. At 2% it is roughly 0.5% instead of 1.0%. Neither file considers it. The "1% tick equals the 2% hurdle and is below the 5% hurdle" argument therefore overstates the hurdle by a factor of about 2 to 5.
2. Commission branch. If the Basic 2% package exists for Irish accounts (input claim, unverified), the user would choose it. The 5% scenarios should not weigh on the calls.
3. Completion rate. MS's "30% to 50% likelier than 60%" is an unsupported judgement. Break-even is a coin flip (50.5%). Nothing in the folder bounds q.
4. Adverse selection ranges. ODDS (pi 10 to 30%, m = 3%) and MS (0 to -1.0%) are assumptions with no source.
5. ODDS's no-go is partly a testability verdict. "Cannot be tested honestly at EUR 0" is a reason for needs-more-data or not-testable-within-brief, not evidence of negative EV.

Where the folder is not pessimistic enough, or where independent evidence now supports the call:

1. MPRA abstract summary: pre-match makers on average "generally break even". This is the only empirical evidence in the folder, and it says the average maker has about zero edge before any retail-specific handicap. A delayed-key retail maker is worse placed than the average maker (stale view, late queue). This supports no-go on uninformed resting strategies more strongly than either file's assumed numbers.
2. Sample sizes are optimistic (sigma too low, no power term in ODDS). Test durations would be longer than stated.
3. Delayed data may be conflated near 3 minutes (unverified third-party claim), which worsens adverse selection.
4. Absolute euros. Even the best case in MS S2 (+0.2% per attempt at EUR 10) is about EUR 2 a week. With hedging, the ODDS case at EUR 10 stakes and a 0.5% net edge on 30 fills a week is about EUR 1.50 a week. Correcting the hold-versus-hedge error removes the drawdown objection but not the "not worth 5 h/week" objection.

Net: the pessimism errors (hold-only commission, 5% branch, asserted q and pi) are real and change the size of the hurdle. They do not produce a positive expected edge, because the folder has no positive edge evidence and the one empirical source says makers break even. The no-go calls survive on substance, with corrected reasoning.

## 6. Who is on the other side, and why would the edge persist?

- Counterparties to a resting order are takers. Some pay for immediacy (recreational, hedgers, traders exiting). Some are informed (team news, sharp bookmaker moves, racing money). The paper's model says makers are compensated for non-execution risk, and its data says that compensation nets to about zero on average pre-match.
- Competing makers are bots with live data that cancel on news. They hold the queue front and leave stale orders exposed to informed takers. A delayed-key maker gets the residual flow, which is skewed to informed fills.
- Why an edge would persist: only as payment for waiting and non-execution, which is competed down to the cost of capital and technology. Nothing in the folder identifies a reason a delayed-key participant would earn more than the average maker. Persistence of a premium for this participant is not supported.

## 7. Verdict per call

### costs-constraints.md (no go/no-go call; top constraints treated as calls)

| Item | Verdict | Reason |
|---|---|---|
| Constraint 1: delayed key bet placement and latency | survived | Orchestrator addendum resolves placement from v144. Not re-verifiable this session, and fresh search snippets still show older contrary wording. Placement latency and order-status delay remain unknown. The suggested EUR 2 test is a real bet and out of scope. |
| Constraint 2: no free data measures queue, fill rate or traded volume | survived | Confirmed by SPEC. Wording that queue work needs Pro specifically is overstated in sibling files. |
| Constraint 3: TX threshold, winning-account limits, Irish tax, commission rate unconfirmed | survived | Correctly tagged unknown. |
| Section 8 break-even table | weakened | Two-tick stop numbers are wrong (67.1% and 67.8%, not 66.4% and 67.2%). One-tick numbers correct. |
| Section 4 reason for avoiding PERSIST | weakened | Misapplies the passive-delay rule. Conclusion is fine, reason is not. |

### odds-model.md

| Call | Verdict | Reason |
|---|---|---|
| no-go | survived (main reason weakened) | The stated main reason, that one maker tick roughly equals the commission hurdle, assumes hold-to-settlement and overstates the hurdle by 2 to 5 times. "Basic is free" is tagged verified but SPEC says "for purchase". The MPRA paper is misread as evidence makers can win. Sample sizes are optimistic. The call still holds because the only empirical source says average pre-match makers break even, the model has no information beyond the close by the file's own admission, and absolute returns are a few euros a week. Recommend relabelling the reason: "no evidence of a positive maker edge, and not testable within the brief", not "commission exceeds the tick". |

### market-structure.md

| # | Call | Verdict | Reason |
|---|---|---|---|
| 1 | Single-sided resting held to settlement: no-go | survived | MPRA abstract summary (makers break even) supports it and largely answers the file's own biggest risk. Arithmetic uses an invalid price (2.01) and ignores the hedge option, which would cut the commission drag, but without an edge source the hedge only reduces the loss. |
| 2 | Two-sided scalping, football MO: no-go | survived | Completion-rate range is asserted, not evidenced, and break-even is a coin flip, so the sign of the edge is unknown. The call survives on stale-feed adverse selection, the impossibility of competitive re-quoting on a delayed key, and the tiny absolute euros (best case about EUR 2 a week). Two-tick break-even numbers are slightly wrong. |
| 3 | Two-sided scalping, racing Win: no-go | survived | No racing evidence either way. The paper is soccer only (confirmed by search summary). Racing volatility likely makes the CLV sigma higher than assumed, which strengthens the call. |
| 4 | Passive execution overlay: needs-more-data | survived | Correct framing. Depends on a model that does not exist yet. "Missed bets cost 1.2%" mixes opportunity cost with P&L and should be compared against crossing the spread on every bet. |
| 5 | Stink bids: needs-more-data (low priority) | survived | No evidence either way, correctly labelled. |
| 9 | Measurement design | weakened | Out of scope per brief (real bets). Exposure cap of EUR 30 does not bound lay liability or matched positions held to settlement. Sigma of 4% is unsourced and likely low, so 502 fills is a floor. |

## 8. Items tagged [verified] that are only inferred

1. ODDS section 2 and section 3 table: Basic is "Free" `[verified: SPEC]`. SPEC says data is "for purchase". Inferred.
2. MS strategy 2: "Queue simulation needs Pro `[verified: SPEC p3-4]`". Inferred, and overstated.
3. MS: "A delayed-key quoter is the slowest quoter in the book by construction `[verified: DEV/2687105]`". Inferred.
4. ODDS 5c: "stale by an amount comparable to the edge sought `[verified]`". Inferred.
5. ODDS 5c: "Separating moving flow ... needs volume, queue and tape `[verified]`". Inferred.
6. ODDS 1 and COSTS 4: passive-delay rule `[verified]` used as the reason PERSIST must not be used. The rule is verified; its application is a non sequitur.
7. ODDS 5c and MS: MPRA "makers earn more than takers" `[verified]`. True as a relative statement. Using it as evidence of a maker edge is contradicted by the abstract summary that makers break even.
8. All `[verified: DEV/...]` tags: could not be re-verified in this session (host unreachable). They rest on the orchestrator's reading.

## Sources

- [MPRA paper 126351 PDF](https://mpra.ub.uni-muenchen.de/126351/1/MPRA_paper_126351.pdf) (search result, not fetched)
- [MPRA 126351 landing page](https://mpra.ub.uni-muenchen.de/126351/) (fetch failed, DNS)
- [IDEAS 126351](https://ideas.repec.org/p/pra/mprapa/126351.html) (fetch failed, DNS)
- [CEPR DP 20633 on IDEAS](https://ideas.repec.org/p/cpr/ceprdp/20633.html) (search result)
- [Karl Whelan, Agreeing to Disagree](https://www.karlwhelan.com/sports-betting-how-betting-exchanges-work/) (search result)
- [Betfair dev docs Best Practice](https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages/2687730/Best+Practice) (search result, not fetched)
- [NautilusTrader Betfair integration](https://nautilustrader.io/docs/latest/integrations/betfair/) (search result, fetch failed)
- docs/inputs/official/Betfair-Historical-Data-Feed-Specification.pdf (read directly, pages 1 to 4)

# Odds-model viability: pre-play passive resting orders, maker side

Date: 2026-11-15
Agent: odds-model-assessor
Scope: football Match Odds and UK/Irish horse racing Win, pre-play only. Angle: can a simple fair-price model decide where to rest orders so that fills have positive expected value against the close or BSP, instead of relying on spread capture?
Inputs read: CLAUDE.md, research/02-ranking.md, costs-constraints.md (including the orchestrator addendum), research/00-verify/input-claims.md (including Addendum 2, the official Historical Data Feed Specification, cited as SPEC), docs/brief.md.
Fetching: no new pages were fetched this session. Betfair consumer sites are behind a Cloudflare challenge and were not bypassed. Anything not carried over from the files above is `[inferred]`.
DEV = https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages

## Call

no-go. Main reason: the fair-price model cannot be tested honestly at EUR 0. Free history now confirmed to have no volume or ladder, so fills, queue and adverse selection can only be measured with real orders, which the brief puts out of scope. Single biggest risk: adverse selection (fills arrive when the market is moving against you) is not measurable offline, and plausible values of it wipe out the one-tick edge a maker earns.

## 1. Target

- Outcome predicted: the fair price at the close, not the match result. The model gives a fair value v for each selection at the close (racing: BSP; football: last traded price at kick-off, or devigged Pinnacle close). `[inferred]`
- Decision: rest a back order at price p above v, or a lay order below v, so that each fill has expected closing line value (CLV) greater than zero after commission. `[inferred]`
- Time: place 1 to 6 hours before the off, persistence LAPSE so it cancels at the turn in-play `[inferred: persistence types from costs file, page not read]`. Passive in-play orders skip the bet delay `[verified: DEV/2687396/Exchange+Stream+API]`, so PERSIST must not be used.
- The model's own win probability is not the target. If v is a devigged sharp close, the model has no information beyond the close. Its only job is to predict where the close will land so your fill price beats it.

## 2. Benchmark

- Racing: BSP. Per-runner bsp is in every plan including free Basic `[verified: SPEC p1-2]`, and Basic runs from May 2015 `[verified: SPEC p1]`. So the racing benchmark is free and has a long history. Whether racing Win markets are in the Basic file set is `[unknown]` (SPEC is field-level only).
- Football: last traded price at the off. Basic gives the last 1-minute ltp before the off `[verified: SPEC p3-4]`, which is a near-close, not the exact close `[inferred]`. Football Match Odds has no BSP in general `[inferred]`.
- Primary metric: mean CLV per fill. Back fill at p: CLV = p / v_close - 1. Lay fill: CLV = 1 - p / v_close (approximate). v_close is the devigged close.
- Secondary metric: log loss of model v against the outcome, compared with the close. Labels (runner WINNER or LOSER) are free in Basic `[verified: SPEC p1-2]`. A devigged sharp-book model should tie the close, so this cannot be the source of edge.
- Comparison unit: fills, not orders. Unfilled orders must be logged with counterfactual CLV, or fill selection hides the bias (section 5).
- Realised P&L is not used for skill testing at this size (section 6).

## 3. Data

| Item | Source | Cost | History | Look-ahead risk | Tag |
|---|---|---|---|---|---|
| Last traded price per runner, 1 minute, plus marketDefinition (marketBaseRate, betDelay, inPlay, runner status, bsp) | Basic historical data | Free | From May 2015 | Low. No volume, no ladder, no traded-at-price | `[verified: SPEC p1-4]` |
| Commission base rate per market, historic | marketDefinition in every plan | Free | Same | None | `[verified: SPEC p1-2]` |
| Best back and lay, traded volume, 1 second | Advanced | Paid, price `[unknown]` | From 2015 `[inferred]` | Low. Only best offers, so no queue | `[verified: SPEC p3-4]` for content |
| Full ladder, tick by tick, BSP near and far | Pro | Paid, price `[unknown]` | `[inferred]` | Low. Needed for any queue simulation | `[verified: SPEC p3-4]` for content |
| Live stream, 3 levels, delayed 1 to 180 s, no total matched | Delayed key | Free | Forward only | High. You rest against a view up to 3 minutes old | `[verified: DEV/2687105/Application+Keys]` |
| Own order fills | listCurrentOrders or order stream | Free | Forward only | None. Only fill ground truth at EUR 0 | `[inferred]` |
| Sharp bookmaker odds for devig | Free archive CSVs for closing odds exist for major leagues, live feed cost `[unknown]` | Archive free | Many seasons | Archive is closing only. Using it to time an earlier order is look-ahead | `[inferred]`, not fetched |
| Racing sharp reference | None free. BSP is the benchmark, so it cannot also be a feature for an earlier order | n/a | n/a | High if misused | `[inferred]` |

Notes.
- Which sports and market types Basic covers (Match Odds, Win) is `[unknown]`. Resolve by downloading one free Basic month `[unknown]` per input-claims Addendum 2.
- Free history cannot give fill probability or adverse selection. It gives only the 1-minute price path to the close. It can test one thing: how far the price drifts from time T to the close, and whether a simple rule predicts that drift (section 4).
- The delayed key is documented as for "development purposes and any functional testing" `[verified: DEV/2687105/Application+Keys]`. Enforcement `[unknown]`.
- For racing there is no free sharp live reference, so a fair-value input would be Betfair's own delayed price, which is circular.

## 4. Method

Realistic class: a rule, not a trained model.

1. Fair value v_now = devigged live reference (football: sharp bookmaker if a free live feed exists, otherwise Betfair mid with overround removed).
2. Optional drift term: expected close minus current price, a shrunken regression on time to off, price bucket and favourite-longshot bucket, with 3 to 5 parameters at most. This part can be fitted offline on free Basic data: price at T minus 1 to 6 hours against ltp at the off, and for racing against bsp `[verified: SPEC p1-4]` for the fields.
3. Placement: back at v_now + d, lay at v_now - d, with d chosen on the live fill sample (0.5, 1, 2 ticks).
4. Cancel at a fixed time before the off. No re-quoting, to keep transaction counts low `[inferred]`.

Do not propose queue-position models, order-flow imbalance or tick-level machine learning. Data cannot support them: free history has no volume or ladder `[verified: SPEC p3-4]`, Advanced has only best offers at 1 second so queue simulation needs Pro `[inferred from SPEC]`, and the live free feed is delayed with 3 levels `[verified: DEV/2687105/Application+Keys]`.

The fair-price model only picks a side of the mid. If v is within a tick of the mid, which is usual in liquid pre-play markets `[inferred]`, the gain is the drift prediction, which is small and noisy.

## 5. Required accuracy (arithmetic)

### 5a. Commission hurdle

Expected commission on a back bet at a fair price p with win probability 1/p, charged only if the market nets a profit: c x P(win) x (p - 1) = c x (1 - 1/p). Gross CLV needed to break even:

| Odds p | 1 - 1/p | Required CLV at c = 2% | Required CLV at c = 5% |
|---|---|---|---|
| 1.5 | 0.333 | 0.67% | 1.67% |
| 2.0 | 0.500 | 1.00% | 2.50% |
| 3.0 | 0.667 | 1.33% | 3.33% |
| 5.0 | 0.800 | 1.60% | 4.00% |

The Irish rate is `[inferred]` (2% vs up to 5% unresolved). The per-market rate is in marketDefinition in the free Basic files `[verified: SPEC p1-2]`, so a person can read the actual historic rate for football and racing Win from one free download. Netting across a market lowers the hurdle slightly `[inferred]`. Expert Fee and transaction charge are not binding `[inferred]`.

### 5b. What one tick is worth

One tick at p = 2.0 is 0.02 / 2.0 = 1.0%. At p = 3.0 it is 0.05 / 3.0 = 1.67%. At p = 1.5 it is 0.01 / 1.5 = 0.67% (ladder `[verified: DEV/2686993/Additional+Information]`). One tick inside the mid therefore earns about the 2% commission hurdle and 40% of the 5% hurdle, before adverse selection. This matches the costs file break-even completion rate of 50.5% at 2% and 51.3% at 5%.

### 5c. Adverse selection (Glosten-Milgrom style)

Let d be your price improvement over fair, pi the share of takers who know more than you, m the average move of the close against your fill when they do. Expected CLV given a fill is about d - pi x m.

Scenario at p = 2.0, d = 1 tick = 1.0%, m = 3% (assumed) `[inferred, no measurement]`:

| Informed share pi | Adverse cost pi x m | CLV per fill | Clears 2% hurdle (1.0%)? | Clears 5% hurdle (2.5%)? |
|---|---|---|---|---|
| 10% | 0.3% | 0.7% | No | No |
| 20% | 0.6% | 0.4% | No | No |
| 30% | 0.9% | 0.1% | No | No |

To clear the 2% hurdle at pi = 20% you need d = 1.0% + 0.6% = 1.6%, about 1.6 ticks. At 5% commission you need 2.5% + 0.6% = 3.1%, about 3 ticks at p = 2.0. Orders that far from the mid fill less often, and fill rate is `[unknown]` and not measurable from free data.

Why a fair-price model does not fix this. A fill happens because someone trades at your price. If v equals the close, a fill that arrives while the market moves is conditional on the move. Separating moving flow from non-moving flow needs volume, queue and tape, which neither the delayed key nor Basic history has `[verified: DEV/2687105/Application+Keys; SPEC p3-4]`. A view 1 to 180 seconds old is stale by an amount comparable to the edge sought `[verified: DEV/2687105/Application+Keys]`.

Evidence that makers can win: MPRA 126351 says makers earn more than takers pre-match and early in-play `[verified: https://mpra.ub.uni-muenchen.de/126351/]`. It is an average over makers, with sport mix, commission treatment and stake size not seen `[unknown]`. It does not show a delayed-key retail maker earns it.

Required accuracy, summary: mean CLV per fill of 1.0% to 1.3% at 2% commission, or 2.5% to 3.3% at 5% commission, at odds 2 to 3, after adverse selection. Add 0.3% for model error, so target about 1.3% to 1.6% at 2% commission. `[inferred]`

## 6. Sample size (arithmetic)

### 6a. Testing CLV (feasible)

Per-fill CLV standard deviation: assumed 3% football pre-match, 6% racing early price to BSP `[inferred, not measured]`. Both can be measured from free Basic data for the drift part `[verified: SPEC p1-4]` for fields. n for t = 2 is (2 x sigma / mu)^2.

| Sport | sigma | True mean CLV mu | n |
|---|---|---|---|
| Football | 3% | 1.3% | (6 / 1.3)^2 = 21 |
| Football | 3% | 0.5% | (6 / 0.5)^2 = 144 |
| Football | 3% | 0.3% | (6 / 0.3)^2 = 400 |
| Racing | 6% | 1.3% | (12 / 1.3)^2 = 85 |
| Racing | 6% | 0.5% | (12 / 0.5)^2 = 576 |

Plan on 400 fills per sport, with unfilled-order counterfactuals logged. Throughput, assuming 100 resting orders per week and a 30% fill rate `[unknown]`: 30 fills per week, so 400 fills take about 13 weeks per sport, about 7 weeks pooled `[inferred]`.

### 6b. Testing realised profit (not feasible)

Per-bet P&L standard deviation per unit stake is about 1.0 at p = 2. For net edge e at t = 2, n = (2 / e)^2: e = 1.0% gives 40,000 bets, e = 0.5% gives 160,000. At 30 fills per week, 40,000 fills take 1,333 weeks. Skill can only be judged on CLV.

### 6c. Drawdown and economics

Stake EUR 10, 100 fills per week, net edge 0.5% (optimistic). Weekly mean = 100 x 10 x 0.005 = EUR 5. Weekly standard deviation = sqrt(100) x 10 x 1.0 = EUR 100. Chance of ever hitting the EUR 150 drawdown limit, Brownian approximation exp(-2 x mu x D / sigma^2) = exp(-2 x 5 x 150 / 10,000) = 0.86. At EUR 5 stakes and 50 fills per week: mu = 1.25, sigma = 35, exp(-2 x 1.25 x 150 / 1,225) = 0.74. A breach of the 30% limit is more likely than not before skill shows in P&L. At EUR 1 stakes the drawdown risk is small but expected profit is about EUR 0.25 per week at 0.5% edge on 50 fills, not worth 5 hours per week. Min bet is EUR 1 `[verified: DEV/2686993/Additional+Information]`. All other inputs `[inferred]`.

## 7. Build effort

| Task | Hours |
|---|---|
| Stream capture on delayed key, market selection, logging | 8 to 10 |
| Order placement, LAPSE, cancel at fixed time, fill logging | 8 to 10 |
| Fair-value input, CLV calculation, results join | 6 to 8 |
| Offline drift study on free Basic data | 4 to 6 |

Total about 26 to 34 hours, or 5 to 7 weeks at 5 hours per week `[inferred]`.

What a free first backtest can and cannot do. With Basic from May 2015 `[verified: SPEC p1]`, a drift and benchmark study (price at T minus h against close or BSP, by price bucket, with labels and marketBaseRate) is feasible in about 1 to 2 weeks, if football Match Odds and racing Win are in the free file set `[unknown]`. It answers one question: does a simple rule predict the close better than the current price. It cannot test fills, queue or adverse selection, because Basic has no volume, ladder or traded-at-price `[verified: SPEC p3-4]`, and Advanced shows only best offers so queue simulation needs Pro `[inferred from SPEC]`. Simulating fills from 1 minute last traded prices would assume a fill whenever price touches your level, which overstates fills and is biased in favour of the strategy. A fill-honest test needs real orders: 5 to 7 weeks of build plus about 13 weeks of collection, roughly 5 months. Real orders are out of scope in the brief `[verified: docs/brief.md]`.

## 8. Call

| Field | Value |
|---|---|
| Call | no-go |
| Main reason | The fair-price model has no information beyond the close, so the edge is the maker's tick, about 1% at odds 2.0. That roughly equals the 2% commission hurdle (1.0%) and is below the 5% hurdle (2.5%). Adverse selection of 0.3% to 0.9% removes it. The free data confirmed to date cannot measure it. |
| Single biggest risk | Adverse selection on a 1 to 180 second stale view with no volume data. Fills cluster when the market moves against the resting order. |
| What would change the call to needs-more-data | (1) Free Basic month shows football Match Odds and racing Win coverage and the offline drift study finds a rule predicting close or BSP by more than 1.3%. (2) marketBaseRate read from a free Basic file shows 2% for these markets. (3) User approval for EUR 1 live orders for a fill study, or an affordable Pro sample. |
| Fallback | If micro stakes are approved, run a CLV-only study at EUR 1 with a stop of 400 fills or EUR 30 loss. Treat any result as exploratory. |

Open items for a person: commission rate, transaction charge threshold, winning-account limits, delayed key intended-use wording, Basic coverage by market type, Advanced and Pro prices.

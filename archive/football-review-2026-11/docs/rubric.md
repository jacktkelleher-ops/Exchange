# Scoring rubric

Used by the `ranker`. Score each criterion 1 to 5, multiply by weight, total out of 100 after scaling (sum of weights x 5 = 500, divide by 5).

| Criterion | Weight | 1 (poor) | 5 (strong) |
|---|---|---|---|
| Liquidity and depth | 20 | Thin books, wide spreads, hard to fill a meaningful stake | Deep books, tight spreads, stake fills without moving price |
| Edge plausibility | 25 | Efficient, dominated by sharp money and automated players, no clear mispricing source | A named, testable source of mispricing with a reason it persists |
| Data access | 15 | No usable history or order-book data | Affordable historical and live data, including traded volume and price ladders |
| Cost drag | 15 | Commission and other charges remove most plausible edge | Costs small relative to plausible edge |
| Capital and scale fit | 10 | Needs capital or stake size outside the brief | Fits the brief bankroll with room to scale |
| Time to first test | 10 | Months of build before any backtest | A backtest possible within days |
| Operational risk | 5 | Account restriction, latency or rule risk is severe | Low risk |

## Gates

A market goes to the shortlist only if all hold:

- Total score is 60 or higher.
- Edge plausibility is 3 or higher.
- Data access is 3 or higher.
- No criterion is scored on `[unknown]` evidence alone. If it is, mark the market `needs-more-data` and list what is missing.

## Scoring rules

- Each score needs a one line reason and an evidence tag.
- Scores with only `[inferred]` support are capped at 3.
- Break ties by time to first test.

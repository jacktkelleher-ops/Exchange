# Decision log

The orchestrator adds an entry after every `principal-engineer` consult. The advisor never edits this file. Newest entry at the bottom. Entries are not edited after the user decides; a reversal is a new entry that names the one it replaces.

## Entry format

```
## <YYYY-MM-DD> <short title>

- Phase / gate: <e.g. Gate 1>
- Question: <the exact question sent to the advisor>
- Advisor answer: <summary of the Answer and Reasoning>
- Files the advisor relied on: <paths>
- What would change the answer: <from the advisor>
- User decision: <what the user decided, in their words where possible, or "pending">
- Follow-up: <files or tasks changed as a result>
```

## Entries

## 2026-11-15 Gate 1a: are the viability criteria sound?

- Phase / gate: Gate 1a
- Advisor model: `claude-fable-5-2` (confirmed from headless run modelUsage)
- Question: "Are the gates, scored metrics and thresholds in docs/viability-criteria.md sound for choosing which Betfair sport, market type and time point to pursue for 1 to 60 second order-book trading, given what free data can and cannot measure (survey-plan.md sections 1 and 2)? Name the single threshold or metric most likely to mislead the selection and why, and anything material that is missing."
- Advisor answer: Sound as a liquidity and access screen, not as a selection rule. G2 (0.044 spread in raw odds) is the most misleading: tick size grows with price, so long-priced runners fail mechanically and racing would be wrongly excluded; the runner set is undefined. The Flepp and Whelan figures were tagged "read in full" but no file recorded that read. G1 is a bettor-versus-bookmaker floor measured at the off, wrong for in-play cells. The unweighted sum is a liquidity ranking on free data (S1, S3, S7 co-move; S5 unmeasured), so use it to shortlist only. Missing: a queue-turnover metric for the maker side, a fixed-cost break-even test (live key GBP 499, Pro GBP 79 to 230 per month, EUR 500 bankroll), anchoring time points to the actual off, excluding suspended snapshots, intervals on medians, the racing in-play blind spot at 180 s cadence, and a stated choice of ladder fields for spread. S5 as a median is likely zero at 1 to 5 s; use the share of windows where the move exceeds cost.
- Files the advisor relied on: docs/viability-criteria.md, research/01-verify/survey-plan.md, research/01-verify/viability-literature.md, docs/brief.md, docs/spec.md, docs/gates.md, docs/known-facts.md
- What would change the answer: Flepp's spread unit confirmed as relative to price; official tick ladder showing no surveyed runner where one tick exceeds 0.044; Whelan figures confirmed or contradicted; Pro or live-key data on shortlisted cells; a user decision to pursue taker strategies only; in-play sports turning out to trade mostly before the off.
- User decision: pending (Gate 1a)
- Follow-up: orchestrator revised docs/viability-criteria.md and survey-plan.md and recorded the paper reads in research/01-verify/literature-reads.md (same day). The revisions are proposals for the user's approval.

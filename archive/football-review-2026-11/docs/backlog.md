# Backlog

Ideas and follow-ups that are not part of the current review phase.

## Data

- **Train models on Kalshi and Polymarket data alongside Betfair** (added 2026-11-15, user request).
  - Sources: Kalshi 1-minute candles (bid, ask, volume) and Polymarket price history, both free and unauthenticated. See `research/00-verify/prediction-markets.md`.
  - Main use (user view): fill in prices at times when Betfair Basic has none for free. Basic only records a last traded price when a trade happens, so quiet minutes, including the model's bet time, can be blank.
  - Other gains: a free bid/ask spread (Kalshi) and a second view of the close.
  - Caveat: for matches all three venues list, this adds price observations, not independent outcomes. Outcome sample size only grows with matches that Betfair does not cover, or with more seasons [inferred].
  - Caveat: neither venue can be traded from Ireland, so they are data sources only.
  - Check before use: Kalshi Developer Agreement terms for research use; how far back Kalshi candles go.

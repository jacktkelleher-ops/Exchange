# Survey plan (Phase 1b and 1c)

Date: 2026-11-15. Author: orchestrator. Status: draft for Gate 1a.

Inputs: `docs/brief.md` (survey settings), `docs/viability-criteria.md`, the nine Phase 1a files in this folder, and two read-only probes of the user's delayed key run on 2026-11-15 (`scripts/probe/`).

## 1. What the delayed key actually delivers (measured)

Two probes, run 23:35 to 23:50 UTC on 2026-11-15 on in-play and near-off soccer, tennis, basketball, American football, cricket and US racing markets.

| Route | Finding | Evidence |
|---|---|---|
| Stream API, 25 markets, 8 min | Exactly one update per market every 180 s (all 45 gaps 180.0 s); `conflateMs` 180000 on every message; 44 market changes flagged `con=true`. | [verified: data/raw/probe/20261115T233458Z.jsonl, scripts/probe/analyse_probe.py] |
| Stream API, fields | Full ladders `atb`/`atl` present (up to 94 back and 141 lay price levels), plus `batb`/`batl` (10 levels as requested), `trd`, runner `tv`, market `tv`, `ltp`, `marketDefinition`. This contradicts the "3 price levels" in known-facts and the Application Keys page. | [verified: same] |
| Stream API, timing | `pt` is about 0.8 s before local receive time, so `pt` is when the conflated snapshot was sent, not when its contents were current. | [verified: same, n 3 non-heartbeat messages] |
| listMarketBook polling, 3 in-play markets, every 5 s for 120 s | The response changed on 22 to 23 of 23 polls, and `totalMatched` was returned. The REST route is not held to the 180 s conflation. | [verified: data/raw/probe/*_poll.jsonl, scripts/probe/delayed_poll_probe.py] |
| listMarketBook, staleness | Poll time minus reported `lastMatchTime`, on continuously traded NFL and NBA markets: min 5 to 33 s, median 108 to 136 s, max 185 to 239 s. The data is a variable 5 to 240 s old. | [verified: same] |

Consequence [inferred from the above]: free Betfair data gives accurate depth, spread and matched volume snapshots at a resolution of about 3 minutes, with an unknown 5 to 240 s lag. It cannot measure anything on a 1 to 60 s scale.

## 2. What each source can measure against the criteria

| Criterion | Delayed-key stream (free) | Basic history (held) | Kalshi public REST (free) | Pro history (paid) |
|---|---|---|---|---|
| G1 cumulative matched volume | yes (`tv`, `trd`) | no (no `tv` in Basic) [verified: spec PDF p3] | Kalshi only | yes |
| G2 quoted spread | yes, 3-min snapshots | no | Kalshi only | yes |
| G3 depth at best | yes | no | Kalshi only | yes |
| G4 trade events per minute | no, only volume per 3 min | proxy: `ltp` changes per minute | Kalshi only, exact | yes |
| G5 `betDelay` | yes (`marketDefinition`) | yes | n/a | yes |
| S1 liquidity | yes | no | Kalshi only | yes |
| S2 spread in ticks | yes | no | Kalshi only | yes |
| S3 depth top 3 | yes, full ladder | no | Kalshi only | yes |
| S4 activity per minute | no | proxy only | Kalshi only | yes |
| S5 move over 1 to 60 s versus cost | no | no (1-min `ltp` only) | Kalshi only | yes |
| S6 resilience | no | no | Kalshi only, at poll resolution | yes |
| S7 capacity | yes | yes, years of history | Kalshi only | yes |
| S8 suspension burden | yes | yes | n/a | yes |
| Time points 24 h, 6 h, 1 h, 15 min | yes | `ltp` only | Kalshi only | yes |
| Time points 5 min, 1 min | no, the 3-min cadence and lag blur them | `ltp` only | Kalshi only | yes |

The free survey can rank sports and markets on liquidity, depth, spread, capacity, bet delay and suspensions. It cannot test whether the 1 to 60 s dynamics clear costs (G4, S4, S5, S6) for any Betfair market. That needs Pro data or the live key.

## 3. Recording design

### 3a. Betfair stream (delayed key)

- Two connections of up to 200 markets each [verified: research/01-verify/api-access.md].
- Subscribe each selected market from 20 minutes before its scheduled start to its close. A new subscription replaces the old one on the same connection, so the recorder re-subscribes as markets enter and leave the window [verified: api-access.md].
- Fields: EX_ALL_OFFERS, EX_TRADED, EX_TRADED_VOL, EX_LTP, EX_MARKET_DEF. Write every raw line unchanged with local receive time.
- Market types: MATCH_ODDS (soccer, tennis, darts, snooker, cricket), WIN (UK and Irish racing).

### 3b. Betfair pre-off snapshots (delayed key, REST)

- For every selected market, one listMarketBook call at 24 h, 6 h and 1 h before the scheduled start (EX_BEST_OFFERS, EX_TRADED), recording `lastMatchTime` so staleness is visible. These points are too early for the stream window and cheap to poll.

### 3c. Kalshi (public REST, no key)

- For each Kalshi market matching a selected Betfair event (soccer, tennis, cricket, darts; Kalshi has no racing or snooker [verified: research/01-verify/kalshi.md]), poll the order book and new trades every 10 s from 20 minutes before start to settlement, plus snapshots at 24 h, 6 h and 1 h.
- Kalshi Basic tier allows 200 reads per second at 10 tokens per request [verified: kalshi.md]. At 10 s polling, 50 markets is 5 requests per second, well inside that.
- The WebSocket needs signed key headers even for public channels [verified: kalshi.md], so REST polling is used. No private key is needed.

### 3d. Market selection and quotas

Concurrency sets the limit: up to 400 markets at once on Betfair. Long in-play markets (soccer about 2 h, tennis 1.5 to 3 h, T20 cricket about 3.5 h) use slots for longest.

| Sport | Markets recorded | Basis |
|---|---|---|
| UK and Irish racing, WIN | all | short in-play, few slots needed |
| Soccer, MATCH_ODDS | top-tier leagues plus a random sample of lower tiers, capped so soccer never holds more than 200 slots at once | [reasoning] weekend 15:00 peaks would otherwise fill both connections |
| Tennis, MATCH_ODDS | all Grand Slam, ATP, WTA and Challenger matches; ITF sampled | [reasoning] tier coverage for S1 comparisons |
| Darts, snooker, MATCH_ODDS | all | small volume, central to the original brief |
| Cricket, MATCH_ODDS | international and major T20 only; Test matches excluded | [reasoning] multi-day markets would hold slots for days |

Target: at least 30 markets per cell (sport x market type x time point) so each median rests on a usable sample [reasoning]. Cells that fall short are reported as such, not dropped.

### 3e. Recording period

14 days, starting when the recorder passes its smoke test.

Reasoning: two full weekends capture the soccer and racing weekend peaks; the ATP Challenger and late-season tennis events still run in the second half of November; darts and snooker have events in late November [inferred: research/01-verify/other-sports.md calendar]. Two weeks is also short enough to make the Pro-data decision before December, when tennis thins out [inferred].

Disk: full-ladder snapshots every 3 minutes for up to 400 markets, gzip-compressed, are estimated at roughly 1 to 3 GB over 14 days [inferred, to be checked against the smoke test]. Free space after the historical download is about 12 GB.

The laptop must stay on, awake and online for the 14 days. Gaps are logged and counted in the data audit.

## 4. Basic history (held, already downloaded)

Use for: market counts per week by sport and tier (S7), suspension and in-play duration statistics (S8), `betDelay` by sport (G5), and per-minute `ltp` change frequency as an activity proxy. Years of history make these far more reliable than 14 days of recording. Archives are read in place without extracting.

No task for the user: the user's purchases are already downloaded by `scripts/historic/download.py`.

## 5. Decision needed at Gate 1a: a Pro sample

The free survey cannot answer the core question for any Betfair market: do 1 to 60 s dynamics clear costs (G4, S4, S5, S6)? Two options:

| Option | What it buys | Cost |
|---|---|---|
| A. Free survey only, decide on Pro at Gate 1 | Ranking on liquidity, depth, spread, capacity, bet delay, suspensions. Short-horizon question still open at Gate 1. | EUR 0, 14 days |
| B. Free survey plus one Pro month for the leading candidates now, analysed in Phase 1c alongside the recording | The same ranking plus a direct test of G4, S4, S5, S6 on real tick data for those sports. | Pro per month: Other Sports (darts, snooker) GBP 79; Tennis, Cricket, Greyhounds GBP 150; Horse Racing, Soccer GBP 230 [verified per historical-data.md, Betfair support page updated 2026-09-24] |

The brief sets the data budget to EUR 0 until Gate 1, so option B needs the user's decision.

## 6. Changes after the Gate 1a advisor consult (revision 2)

See `docs/decisions.md` (2026-11-15) and `docs/viability-criteria.md` revision 2.

- In section 2, old G1 and G2 are now context metrics C1 and C2. New metric S10 (queue turnover) is roughly measurable from the stream's `trd` deltas. New gate G7 (fixed-cost break-even) needs no recording.
- Time points are anchored to the actual off, defined in the criteria from `marketDefinition` `inPlay` and status, not to `marketTime`. The recorder therefore keeps every `marketDefinition` change. The 24 h, 6 h and 1 h REST snapshots in 3b are timed from `marketTime`. Their offset from the actual off is recomputed afterwards and reported.
- Snapshots with market status other than `OPEN` are excluded from depth, spread and activity statistics but kept for S8.
- Racing in-play is effectively blind at a 180 s cadence: races last minutes. It is reported as unmeasured on free data, not as weak.
- Every median is reported with a bootstrap 95% interval and its n.
- The currency of ladder sizes on this account is checked in the smoke test.

## 7. Smoke test before the full run (Phase 1b step 2)

Record for at least one hour covering at least one live market of each sport available at the time. The data auditor checks: 180 s cadence per market, fields present, subscription rotation working, Kalshi polling within limits, file sizes against the disk estimate.

# Exchange: Betfair quantitative trading research

Research platform for finding which Betfair Exchange sports and markets can support short-horizon trading driven by order-book behaviour, order flow and liquidity dynamics, and then testing whether a repeatable, cost-adjusted edge exists in the selected market.

Status: setup. No trading code. Read-only data collection and research only; no orders are placed without explicit approval at the execution gate.

## How it works

The work runs as a gated multi-agent pipeline in Claude Code. The main session orchestrates specialist subagents and stops for approval at the end of each phase.

| Phase | Output |
|---|---|
| 0 Brief | Constraints and access decisions |
| 1a, 1b, 1c Market survey | Desk research and viability criteria, a free recording survey across sports, then measurement and market selection |
| 2 Design | Architecture, storage schema, development plan |
| 3 Ingest | Market data ingestion for the selected market with tests and a data quality report |
| 4 First look | Streamlit dashboard, order-book imbalance notebook, install guide |
| 5 Status | Memo and plan for features, regimes, prediction and backtesting |

Run a phase with `/run-phase <n>` in Claude Code from this folder.

## Key files

- `docs/spec.md` requirements
- `docs/brief.md` constraints
- `docs/gates.md` pass criteria per phase
- `docs/known-facts.md` verified facts carried over, and where the spec conflicts with current data access
- `CLAUDE.md` rules every agent follows
- `.claude/agents/` subagent definitions

## Credentials

Copy `.env.example` to `.env` and fill it in. `.env`, certificates and all data are git-ignored. Never commit them.

Installation and run instructions arrive in Phase 4.

## History

An earlier cross-sport opportunity review lives in `archive/football-review-2026-11/` and at the git tag `football-review-2026-11`.

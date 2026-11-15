# Spec: Betfair Darts Quantitative Trading Research Platform

Source: the user's starting prompt, 2026-11-15. This file is the authoritative statement of requirements. Do not edit it to match what was built. Record deviations in the phase memo instead. Constraints such as budget and data access live in `docs/brief.md`.

---

Act as a senior quantitative developer, financial markets researcher and Python engineer.

I want to develop a quantitative trading algorithm for Betfair Exchange, initially focusing exclusively on professional darts markets.

The objective is to identify profitable trading opportunities by modelling market microstructure, game theory and participant behaviour.

This is a research-first project. Do not immediately build an autonomous betting bot. First establish a robust data collection, analysis and backtesting infrastructure that can demonstrate whether a genuine, repeatable trading edge exists.

I have a background in financial mathematics, commercial analytics, SQL, Python, statistical modelling and Betfair liquidity analysis. I am comfortable with quantitative concepts but want the code to be modular, well-documented and maintainable.

## 1. Overall objectives

Build a system capable of:

1. Collecting historical and live Betfair Exchange market data.
2. Reconstructing order-book movements over time.
3. Identifying patterns in market participant behaviour.
4. Measuring liquidity, order flow, price movements and market inefficiencies.
5. Developing predictive models for short-term price movements.
6. Simulating realistic trading strategies.
7. Measuring profitability after commission, slippage and execution constraints.
8. Eventually executing trades automatically through the Betfair API, subject to separate approval.

The initial scope is darts only.

Focus on:
- Match Odds markets.
- Pre-match and in-play markets.
- Individual player prices.
- Available back and lay liquidity.
- Traded volume at individual prices.

Design the system so other sports can be introduced later.

## 2. Technology stack

Use:

- Python 3.12+
- Pandas and NumPy
- Polars where beneficial for larger datasets
- Scikit-learn
- XGBoost or LightGBM
- Statsmodels
- DuckDB
- Parquet for historical data storage
- Plotly
- Streamlit for dashboards
- Pytest for testing

Use a modular architecture with clear separation between:
- Data ingestion
- Data storage
- Feature engineering
- Statistical modelling
- Backtesting
- Strategy evaluation
- Visualisation

Avoid unnecessary infrastructure. The system must initially run locally on a standard laptop.

## 3. Betfair data infrastructure

Integrate with the official Betfair Exchange API.

Prioritise:
- Betfair Historical Data API.
- Betfair Exchange Stream API.
- Betfair market catalogue.
- Betfair market book.
- Betfair order management API, but only when we reach the execution stage.

Investigate the available historical data packages and their actual granularity before implementing the ingestion pipeline.

Capture the following wherever available:

Market-level:
- Market ID
- Event ID
- Event name
- Market name
- Market status
- Market start time
- In-play status
- Total matched volume

Runner-level:
- Selection ID
- Runner name
- Best available back price
- Best available lay price
- Full available back ladder
- Full available lay ladder
- Last traded price
- Traded volume at individual prices

Time-series:
- Timestamp
- Price changes
- Volume changes
- Order-book additions and removals
- Market suspension and resumption events

Use the Betfair Stream API where possible rather than repeatedly polling the REST API.

Preserve raw data separately from transformed data.

Every record must have a reliable timestamp and market identifier.

IMPORTANT: Do not assume that public market data identifies individual traders. Model aggregate market behaviour using observable price, volume and liquidity changes.

## 4. Market microstructure research

Develop a feature engineering framework covering:

### Order-book imbalance

Calculate liquidity imbalance at:
- Best available price.
- Top three price levels.
- Top five price levels.
- Full available ladder.

### Order flow

Calculate:
- Aggressive buying and selling proxies.
- Traded volume imbalance.
- Price-level depletion.
- Liquidity replenishment.
- Liquidity cancellation.
- Changes in available liquidity.
- Spread compression and expansion.

### Price behaviour

Calculate:
- Price returns.
- Short-term volatility.
- Price momentum.
- Mean reversion.
- Price acceleration.
- Price movement relative to traded volume.
- Time spent at individual price levels.

### Market resilience

Investigate:
- How quickly liquidity replenishes after being matched.
- How much traded volume is required to move the price.
- Whether liquidity disappears before significant price movements.
- Whether particular price levels act as resistance or support.

Be careful to distinguish actual matched volume from changes in displayed liquidity.

Do not assume that disappeared liquidity was cancelled: it may have been matched or otherwise changed.

## 5. Game theory and participant behaviour

This is a central part of the project.

Investigate whether recurring market behaviours can be identified from aggregate order-book data.

Potential behavioural regimes:

1. Aggressive buying.
2. Aggressive selling.
3. Passive liquidity provision.
4. Liquidity withdrawal.
5. Herding and momentum following.
6. Price anchoring.
7. Temporary liquidity imbalances.
8. Market uncertainty following sporting events.

Develop a regime-classification framework.

Initially investigate:
- K-means clustering.
- Gaussian mixture models.
- Hidden Markov Models.

Compare the usefulness of each approach.

The objective is to identify market states that have different conditional probabilities of subsequent price movements.

Do not claim that these regimes correspond to identifiable individual traders. They are inferred aggregate market states.

## 6. Predictive modelling

Build models that estimate the probability of short-term price movements.

Test prediction horizons of:

- 1 second
- 5 seconds
- 15 seconds
- 30 seconds
- 60 seconds

Predict:
- Probability of price shortening.
- Probability of price drifting.
- Expected magnitude of movement.
- Expected time until movement.
- Probability of obtaining a matched order.

Use:
- Logistic regression as a baseline.
- Random Forest as a benchmark.
- Gradient boosting using LightGBM or XGBoost.
- Hidden Markov Models for market regimes.

Avoid introducing deep learning or reinforcement learning until simpler models have demonstrated a measurable edge.

Prevent data leakage by using chronological train, validation and test splits.

## 7. Darts-specific research

Investigate the characteristics of darts markets.

Distinguish:
- Pre-match markets.
- In-play markets.
- Different match formats.
- Different tournament structures.

For in-play markets, investigate whether price movements and liquidity patterns behave differently around:
- Individual legs.
- Breaks of throw.
- Sets.
- Checkout opportunities.
- Missed doubles.
- Match darts.
- Changes in player momentum.

Where available, incorporate sporting information such as:
- Current score.
- Leg score.
- Player throwing order.
- Match format.
- Average score.
- Checkout percentage.

Do not invent or infer sporting data that has not been reliably sourced.

Initially, use market data alone. Sporting-state integration should be a separate module.

## 8. Backtesting framework

Build an event-driven backtesting engine.

It must simulate:
- Order submission.
- Order matching.
- Partial fills.
- Unmatched orders.
- Queue position.
- Price movement during execution.
- Commission.
- Slippage.
- Position management.
- Market suspension.

Never assume an order gets filled simply because the market subsequently trades at that price.

Implement three execution scenarios:
1. Optimistic.
2. Realistic.
3. Conservative.

Calculate:
- Gross P&L.
- Net P&L.
- Return on capital.
- Sharpe ratio.
- Maximum drawdown.
- Win rate.
- Average winning trade.
- Average losing trade.
- Profit factor.
- Number of trades.
- Average holding period.
- Expected value per trade.

Include comparisons against:
- Random entry benchmarks.
- Simple momentum strategies.
- Simple mean-reversion strategies.
- Passive spread capture.

## 9. Strategy development

Do not assume the strategy will be profitable.

The first strategy to investigate should be:

**Short-term price movement prediction using order-book behaviour and liquidity dynamics.**

The algorithm should identify when:
- Liquidity imbalance suggests a likely price movement.
- Aggressive trading is depleting available liquidity.
- Liquidity replenishment indicates resistance.
- A behavioural regime change suggests a possible opportunity.

The strategy should calculate expected value after execution costs.

Only generate a trading signal when the estimated expected value exceeds a configurable minimum threshold.

## 10. Dashboard

Build a Streamlit dashboard with:

1. Live market overview.
2. Current order-book visualisation.
3. Historical price charts.
4. Traded volume at individual prices.
5. Liquidity imbalance over time.
6. Behavioural regime classification.
7. Predictive model output.
8. Backtesting performance.
9. Strategy-level P&L.
10. Model diagnostics.

Allow selection of individual darts events and markets.

## 11. Development and safety requirements

Build incrementally.

Before writing substantial code:

1. Inspect the existing project directory.
2. Propose the architecture.
3. Identify missing credentials and API access.
4. Identify the available data sources.
5. Create a development plan.
6. Explain any technical limitations.

Never invent API endpoints or assume data fields exist without checking the official documentation.

Use environment variables for credentials and a .env file excluded from version control.

Never commit API keys.

Initially implement read-only data collection and research.

Do not place real-money bets, submit live orders or enable autonomous execution without my explicit approval.

Include unit tests for all critical calculations.

Document assumptions and limitations.

## 12. First deliverable

Do not attempt to build the entire platform immediately.

Start by delivering:

A. A proposed project architecture.

B. A complete list of required Betfair API access and data requirements.

C. A proposed database schema.

D. A data ingestion implementation capable of collecting darts market data.

E. A simple initial dashboard displaying:
- Market prices.
- Available liquidity.
- Traded volume.
- Price movements over time.

F. A short research notebook demonstrating initial order-book imbalance calculations.

G. A README explaining how to install, configure and run the project.

Once these are working, we can progress to behavioural modelling, predictive modelling and backtesting.

Prioritise data quality, reproducibility and demonstrable statistical edge over code complexity.

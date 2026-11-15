# Literature reads by the orchestrator

Date: 2026-11-15. Agent: orchestrator. Purpose: record the full-text reads behind figures used in `docs/viability-criteria.md`, which the docs-verifier could not decode (PDFs). Method: downloaded each public PDF with curl to the session scratchpad, extracted text with pypdf 6 in the project venv, and searched the text. PDFs are not committed (copyright); URLs below.

## Flepp, Nuesch and Franck (2017)

"The liquidity advantage of the quote-driven market: Evidence from the betting industry", Quarterly Review of Economics and Finance 64, 306-317. PDF: https://unifr.ch/tim/en/assets/public/uploads/Publication list/2017/Flepp_Nüesch_Franck_2017.pdf (12 pages).

Quotes from the extracted text:
- Abstract: "Bettors obtain higher odds and returns when using the quote-driven bookmaker market if the cumulative trading volume at the betting exchange is less than £ 23,400 and/or if the quoted spread at the betting exchange is higher than 0.044 on average."
- Results: "If the quoted spread is 0.044 and the cumulative trading volume is £ 23,438 at the betting exchange, both markets offer the same prices on average."
- Definition: "The quoted spread is the difference between the lowest ask price and the highest bid price (Chordia, Roll, & Subrahmanyam, 2008)."

Not established from the text searched: whether "price" here is decimal odds or implied probability, and the runner set the average is taken over. The "index 1-11" note in `viability-literature.md` was not checked. Status: GBP 23,400 and 0.044 are [verified: this read]; the spread unit is [unknown].

## Whelan (2026)

"Agreeing to Disagree: The Economics of Betting Exchanges", Karl Whelan, University College Dublin, January 26, 2026. PDF: https://www.karlwhelan.com/Papers/Betfair.pdf (45 pages). Data supplied by Betfair; the paper states "the exchange we have data for has a 2% commission".

Quotes from the extracted text:
- Match odds: "This produced 902,568 bets ... For these 902,568 bets, the average return for Takers was -2.5% while the average return for Makers was 0.6%. The t-statistic for the difference between these means is 11.8". Context: "a dataset of 152,102 matches in which we could identify the side taken by the Maker and Taker on all six possible options", final pre-play trades, Figure 14 "Average post-fee returns ... Final pre-play trades on home, away or draw in soccer (2022-24)".
- Total goals: "we identified 2,088,032 bets across the different markets (from 0.5 goals up to 5.5 goals) ... The average return on bets placed by Takers was -2.2% while the average return for Makers was 2%."
- Spread effect: "there is evidence of bigger losses for Takers and bigger losses for Makers for those bets with larger bid-ask spreads, particularly for longshot bets."

Status: these figures are [verified: this read]. They are post-fee at 2% commission, soccer only, final pre-play trades.

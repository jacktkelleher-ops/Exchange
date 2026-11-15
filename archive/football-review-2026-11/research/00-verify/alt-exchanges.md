# Alternative exchanges: Matchbook and Betdaq data availability

Date: 2026-11-15
Agent: orchestrator (main session)

MB = https://developers.matchbook.com

## Summary

Neither exchange offers a historical market data product comparable to Betfair Historical Data, as far as can be checked. Matchbook's live API is free to start with no activation fee, which Betfair's live key does not offer. Liquidity on both is much thinner than Betfair [inferred], which matters more for a model benchmarked to the close than for data access. Matchbook bought the Betdaq brand in October 2026 [inferred], so Betdaq's future as a separate venue is uncertain.

## Comparison

| Item | Betfair | Matchbook | Betdaq |
|---|---|---|---|
| Historical market data product | Basic (free, 1-min ltp), Advanced, Pro, from May 2015 [verified: SPEC p1-4]; Basic free [verified: https://betfair-datascientists.github.io/modelling/dataSources/] | None in the developer docs index; no "historic" endpoint [verified: MB/llms.txt, searched 2026-11-15]. A vendor says Matchbook "doesn't sell a historical product directly" [inferred: https://oddspapi.io/blog/?p=2848] | None found [unknown]. API help pages blocked (HTTP 403) |
| Live API access | Delayed key free; live key GBP 499 [verified: DEV/2687105] | Any registered customer can use the API immediately with standard login [verified: MB/docs/faq] | One-off API access fee of GBP 250 after full verification [inferred: https://betdaq.zendesk.com/hc/en-gb/articles/360020067139-API-access, via search summary; page returned 403] |
| API usage cost | Transaction charges above a threshold [unknown figure] | API plan: GBP 100 per 1 million GET requests a month; write requests free at reasonable frequency [verified: MB/docs/pricing] | [unknown] |
| Default rate limits | 200 points per data request [verified: DEV/2687478] | Account 300/min, Events 700/min, Navigation 100/min, Reports 40/min, Betting write 3000/min [verified: MB/docs/faq] | [unknown] |
| Price data delay on free access | 1 to 180 s on delayed key [verified] | None stated in docs [unknown] | [unknown] |
| Commission, Irish customer | 2% / 5% / 8% packages [inferred] | 2% on net profits for UK, IoM, Channel Islands and Ireland; 4% elsewhere [inferred: search summaries of Matchbook terms; official page is JS-rendered and not readable here] | "UK's lowest commission" claim on homepage [verified: https://www.betdaq.com/]; rate [unknown] |
| Irish licence | n/a | [unknown] | Licensed by the Gambling Regulatory Authority of Ireland, GRAI-0313-RBI-26-0001 [verified: https://www.betdaq.com/] |
| Ownership news | n/a | Acquired the Betdaq brand and domains, 14 Oct 2026; Betdaq accounts do not transfer [inferred: https://europeangaming.eu/portal/latest-news/2026/10/15/216005/matchbook-acquires-betdaq-brand/] | Same |
| Fair use restriction worth noting | n/a | API may not be used "for benchmarking or competitive purposes" [verified: MB/docs/fair-usage-policy s3.5d] | [unknown] |

## Implications for the review

- For historical data, Betfair Basic remains the only free official source found. The alternative exchanges do not replace it.
- Matchbook could replace Betfair's delayed key as a free, possibly undelayed live feed and execution venue. This could reopen strategies rejected only because of the 1 to 180 s delay, subject to Matchbook's thinner books [inferred] and its fair use policy.
- Matchbook at 2% commission [inferred] gives the same break-even as Betfair Basic package.
- A third-party aggregator (OddsPapi) claims free Matchbook price history at 250 requests a month [inferred, vendor claim]. Unverified and outside official sources.

## Unknowns and how to resolve

| Item | Resolve by |
|---|---|
| Matchbook price delay and order book depth via API | Register and call Get Prices on a live O/U 2.5 market |
| Matchbook commission for Irish accounts | Read commission page in a browser or account settings |
| Betdaq API status after the Matchbook acquisition | Email Betdaq support or check the help centre in a browser |
| Liquidity on Matchbook and Betdaq O/U 2.5 vs Betfair | Log books side by side for two weeks |

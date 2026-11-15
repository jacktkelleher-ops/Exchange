# Findings: Tennis

Date: 2026-11-15
Agent: market-scanner

## Summary (max 5 lines)

Evidence is limited: every Betfair host (www.betfair.com, support.betfair.com, historicdata.betfair.com, the developer docs) failed to resolve when fetched in this session. Official-page content below comes only from web search summaries that cite those URLs, so it is tagged [inferred] with the page named, not [verified].
Match Odds on ATP/WTA 250 and above is the deepest tennis market. Set betting, total games and game handicap are thinner. Challenger and ITF are reported thin and carry the most settlement risk.
Main risks: the live API key (one-off 499 GBP per the search summary) conflicts with the EUR 0 budget, and Betfair tennis historical data for tennis is paid (Advanced and Pro), with no Basic tennis price found.

## Markets reviewed

| Market | Typical liquidity | Typical spread | Likely counterparties | Data available | Edge hypothesis | Evidence |
|---|---|---|---|---|---|---|
| Match Odds, ATP/WTA 1000 and Slams | High. A third-party guide says round of 16 at 1000 level reaches 200K+ GBP matched [inferred: affiliate guide, uncited, https://betfairsquare.pages.dev/sports/tennis] | [unknown] one tick at favourites is likely, not measured | Pinnacle-referencing traders, in-play bots, retail [inferred] | Historical Advanced 49 GBP/month or 499 GBP/year, Pro 150 GBP/month or 1,499 GBP/year, per bulk page summary [inferred: https://support.developer.betfair.com/hc/en-us/articles/360019984158-Are-bulk-purchase-discounts-available]; live stream via API needs live key | Reaction lag after point or break events (H1); pricing vs devigged Pinnacle close (H2) | Mixed, see sources |
| Match Odds, ATP/WTA 250/500 | Adequate from quarter-finals, thin earlier [inferred: same affiliate guide] | [unknown] | Same as above, fewer sharp participants [inferred] | Same | Slower repricing in thin early rounds (H3) | [inferred] |
| Match Odds, Challenger | Guide says too thin to trade meaningfully [inferred: affiliate guide] | [unknown] | Retail and few bots [inferred] | Same Betfair data; delay tests were running on some Challenger events in Jan 2026 [inferred: https://betting.betfair.com/betfair-announcements/exchange-news/betfair-exchange-january-newsletter-whats-ahead-for-2026-270126-1392.html] | Less efficient pricing but stake moves price (H3) | [inferred] |
| Match Odds, ITF | Very thin, some matches have no counterparty [inferred: forum report via search summary] | [unknown] | Retail [inferred] | Same; one older report says ITF had different delay [inferred: community thread] | Same as Challenger, retirement and data-feed risk | [inferred] |
| Set Betting (set score) | Lower than Match Odds [inferred] | [unknown] | Retail, model traders [inferred] | In historical data [inferred: https://support.developer.betfair.com/hc/en-us/articles/360017615137-Which-markets-aren-t-available-via-Historical-Data] | Match-score model priced from point-win probability (H4) | [inferred] |
| Total Games and Game Handicap | Thin; one guide says very low liquidity, used by automated models [inferred: affiliate guide] | [unknown] | Bots [inferred] | A search summary says tennis Game Betting markets are not in historical data [inferred: same Betfair support page above]; unclear if that covers totals and handicap | Serve-hold model priced against totals line (H4) | [inferred] |
| Game-by-game and point markets in-play | Very low [inferred] | [unknown] | Bots [inferred] | Not in historical data per summary above | Markov point-level models (H1) | [inferred] |

## Edge hypotheses

H1. In-play reaction after point, game or set events
- Claim: Match Odds reprices slowly for a few seconds after a break of serve or injury signs. A fast, automated trader could be the first to move or to offer into the move.
- Why it might persist: Bet delay varies and is changing; Betfair is testing dynamic delay (down to 1 second at end of game or set) and has removed delay for passive bets across tennis [inferred: https://betting.betfair.com/betfair-announcements/exchange-news/betfair-exchange-august-newsletter-290725-1392.html]. Passive orders let a small trader rest orders without delay.
- Why it might not: Established bots with court-side or low-latency feeds already trade this. A retail trader on free data has no point-level feed. Passive orders can be picked off by faster participants.
- How to test: Needs tick-level Betfair data with in-play timestamps and a point-by-point feed. Neither is free. Test on delayed key data first only to check the pipeline, not the edge.
- Evidence: [inferred] 

H2. Pre-match mispricing against devigged sharp closing line
- Claim: Betfair Match Odds pre-match deviates from a devigged Pinnacle close often enough, in some tournaments, to leave positive expected value after commission.
- Why it might persist: Thin early-round and Challenger books lag the sharp market [inferred].
- Why it might not: Pinnacle-referencing traders keep the books aligned. Commission and wide spreads in thin markets remove small deviations.
- How to test: Needs Pinnacle closing prices (not freely available here) and Betfair last-traded or BSP-style close. Per CLAUDE.md, benchmark against Betfair close, not 50/50.
- Evidence: Lead from `docs/inputs/gemini-research.md` (Power-method devig on 77,500 mostly Pinnacle tennis markets, sharp books lambda 2.1). Not confirmed; source is a practitioner post per the input's own note. [unknown]

H3. Lower-tier inefficiency (Challenger, ITF, early rounds)
- Claim: Lower tiers are priced with less information and fewer sharp participants.
- Why it might persist: Low liquidity deters large players.
- Why it might not: The same low liquidity means a EUR 500 bankroll still moves the price, spreads are wide, and settlement risk is higher (see retirement rules below). A guide says to avoid these tiers.
- How to test: Collect close prices and results for a sample of lower-tier matches; compare calibration against the last traded price.
- Evidence: [inferred]

H4. Derived markets (set betting, total games, game handicap) priced from a match model
- Claim: A hold-probability model gives consistent prices across Match Odds, set score and total games. Inconsistencies between them are tradable.
- Why it might persist: Derived markets are thin and may be priced independently by retail.
- Why it might not: Bots already do this per one guide. Derived markets void on retirement unless already settled, which creates unhedged risk if the hedge leg is Match Odds.
- How to test: Build the consistency check offline from free results data. Needs historical derived-market prices, which may not exist in Betfair data.
- Evidence: [inferred]

## Retirement and void rules (Exchange)

Direct fetch of https://support.betfair.com/app/answers/detail/exchange-tennis-rules/ failed (host not resolvable in this session). What a search summary reported about that page:
- Retirement or disqualification: the player who advances is the winner, except where less than one set has been completed, in which case all bets on that match are void [inferred: https://support.betfair.com/app/answers/detail/exchange-tennis-rules/].
- Retirement or disqualification during a game or set voids game and set markets, unless the outcome was already settled [inferred: same URL].
- Walkover, where a competitor takes no part: match bets are void [inferred: https://support.betfair.com/app/answers/detail/exchange-general-rules/].
- Match not completed for any reason: Match Odds void, per the search summary [inferred: same general rules URL]. This sits oddly with the retirement rule above and needs a read of the page.

Input check: `docs/inputs/gemini-research.md` says Exchange Match Odds void on retirement before the end of the first set, and that ITF, UTR and exhibition matches void on any retirement. The first part matches the search summary. The ITF/UTR part appears to come from the Betfair Sportsbook tennis page, not the Exchange page [inferred: https://support.betfair.com/app/answers/detail/tennis-rules/]. So the input's ITF/UTR statement is probably a Sportsbook rule misapplied to the Exchange. Not confirmed on the Exchange page itself. Input also gave a dead heat rule; not relevant to tennis match markets and not checked.

Cost of retirement risk for a small bankroll: after the first set, a retirement settles as a normal win or loss, so a position held on the retiring player loses fully. Not hedged by voids. [inferred]

## Costs

- Commission: Charged on net winnings per market; rate depends on My Betfair Rewards package or country Market Base Rate [inferred: https://www.betfair.com/aboutUs/Betfair.Charges/ and https://support.betfair.com/app/answers/detail/413-exchange-what-is-commission-and-how-is-it-calculated/]. A 2% Basic package was cited only as an example, not as the Irish rate. The Irish rate table could not be read: only a Portuguese-language Irish page was returned. Input claim 1 (Basic 2%, Rewards 5%, Rewards+ 8%) is [unknown] until confirmed. The input's statement of 5% on tennis market base rate is also unconfirmed.
- Other charges that apply to profitable accounts: Expert Fee, weekly, on rolling 52 active weeks gross profit: 0% below 25,000, 20% from 25,000 to 100,000, 40% above 100,000, and only if the account has bet in more than 100 markets. Commission Generated = (Commission Paid + Implied Commission) divided by 2, Implied Commission = Market Losses x 2.5% [inferred: https://support.betfair.com/app/answers/detail/expert-fee-faqs]. Figures were in GBP in the summary; EUR thresholds [unknown]. A EUR 500 bankroll is far below the 25,000 threshold. Transaction charges: apply to more than 5,000 bets in an hour, offset by commission already paid [inferred: https://support.betfair.com/app/answers/detail/betfair-charges]. The market-making exemption sizes from the input (back stake 10 or more, lay liability 100 or more) were not found. Irrelevant at this bankroll since 5,000 bets an hour is far above any plausible volume. The input's claim that Betfair does not limit winning accounts was not checked.
- Data costs: See below.

Bankroll limits found:
- EUR minimum bet size 1, minimum deposit 15, minimum BSP liability 10, minimum payout 20 [inferred: https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Additional+Information; page marked about 990 days old by the summary]. A EUR 1 minimum is compatible with a EUR 500 bankroll; thin tennis markets are limited by depth, not by minimums.
- 30% drawdown is EUR 150. With in-play positions that can lose fully on a retirement, stake sizing must keep a single-match loss well inside that.

## Data and access

- Historical data: Three plans, Basic, Advanced and Pro, differ in frequency and content; Pro adds starting price and full-ladder fields [inferred: https://historicdata.betfair.com/files/Betfair-Historical-Data-Feed-Specification.pdf]. Tennis 12-month bulk prices: Advanced 499 GBP per year (49 per month), Pro 1,499 GBP per year (150 per month) [inferred: https://support.developer.betfair.com/hc/en-us/articles/360019984158-Are-bulk-purchase-discounts-available]. No Basic price or Basic tennis content found. Coverage from May 2015 on one page, April 2015 on another [inferred: https://support.developer.betfair.com/hc/en-us/articles/360002407732-What-data-is-provided-by-the-Historical-Data-service]. Game Betting markets not included [inferred: https://support.developer.betfair.com/hc/en-us/articles/360017615137-Which-markets-aren-t-available-via-Historical-Data]. Input claim 5 (Advanced 69, Pro 230, racing and soccer) does not match these tennis figures; the differences may be per-sport or per-currency. Unresolved. Anything above Basic breaks the EUR 0 data budget.
- Live data and API: Delayed key is free for development, with delayed price data of 1 to 180 second snapshots [inferred: https://support.developer.betfair.com/hc/en-us/articles/115003864531-Are-there-any-costs-associated-with-API-access]. Live key: one-off 499 GBP per current support pages, 299 GBP on older material; non-refundable; read-only use not permitted; account must be KYC verified and funded [inferred: https://support.developer.betfair.com/hc/en-us/articles/115003860331-How-do-I-activate-my-Live-App-Key and the first URL]. Input claim 4 conflict (299 vs 499): current evidence points to 499 GBP, still unconfirmed on the page itself and not converted to EUR. A live key at 499 GBP exceeds the whole EUR 500 bankroll and the EUR 0 data budget, so automated live trading is blocked until the budget changes. [inferred]
- Bet delay: Developer FAQ says in-play delays are usually 1 to 12 seconds, shown per market as betDelay in listMarketBook [inferred: https://support.developer.betfair.com/hc/en-us/articles/360002825652-Why-do-you-have-a-delay-on-placing-bets-on-a-market-that-is-in-play]. Passive bets skip delay for all tennis competitions since 2025; dynamic delay tests ran on some Challenger events in Jan 2026 [inferred: Betfair newsletters above]. Input said 5 seconds for tennis; that is not supported as a fixed figure.
- Free outside data: not researched in depth. Tennis results and point-by-point data from free sources were not assessed here.

## Unknowns

- Exact current Betfair Exchange tennis rules text, including Match Odds vs "not completed for any reason". Resolve by reading https://support.betfair.com/app/answers/detail/exchange-tennis-rules/ directly; the host must be reachable from the session.
- Irish commission rate and package table. Resolve at the Irish Betfair Charges page in English.
- EUR conversion and current price of the live key; whether Irish accounts pay in EUR. Resolve in the developer portal.
- Basic historical data tennis content and whether it is free. Resolve at https://historicdata.betfair.com/.
- Whether Total Games and Game Handicap are in historical data (summary says Game Betting is not).
- Actual spreads and matched volume per tier. Needs sampled order book snapshots from the delayed key, or paid history.
- Transaction charge exemption sizes (not found; not material at this bankroll).
- Whether Betfair limits winning accounts (input claim 8, not checked).

## Sources

Fetched or queried, all via web search summaries; no Betfair page could be opened (DNS failure for www.betfair.com, support.betfair.com, historicdata.betfair.com, betfair-developer-docs.atlassian.net):
- /home/user/Exchange/docs/inputs/gemini-research.md (unverified input, first 30 lines plus grep on tennis)
- https://support.betfair.com/app/answers/detail/exchange-tennis-rules/
- https://support.betfair.com/app/answers/detail/tennis-rules/
- https://support.betfair.com/app/answers/detail/exchange-general-rules/
- https://support.betfair.com/app/answers/detail/betfair-charges
- https://www.betfair.com/aboutUs/Betfair.Charges/
- https://support.betfair.com/app/answers/detail/expert-fee-faqs
- https://support.betfair.com/app/answers/detail/413-exchange-what-is-commission-and-how-is-it-calculated/
- https://support.developer.betfair.com/hc/en-us/articles/115003864531-Are-there-any-costs-associated-with-API-access
- https://support.developer.betfair.com/hc/en-us/articles/115003860331-How-do-I-activate-my-Live-App-Key
- https://support.developer.betfair.com/hc/en-us/articles/360019984158-Are-bulk-purchase-discounts-available
- https://support.developer.betfair.com/hc/en-us/articles/360002407732-What-data-is-provided-by-the-Historical-Data-service
- https://support.developer.betfair.com/hc/en-us/articles/360017615137-Which-markets-aren-t-available-via-Historical-Data
- https://support.developer.betfair.com/hc/en-us/articles/360002825652-Why-do-you-have-a-delay-on-placing-bets-on-a-market-that-is-in-play
- https://historicdata.betfair.com/files/Betfair-Historical-Data-Feed-Specification.pdf
- https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Additional+Information
- https://betting.betfair.com/betfair-announcements/exchange-news/betfair-exchange-august-newsletter-290725-1392.html
- https://betting.betfair.com/betfair-announcements/exchange-news/betfair-exchange-january-newsletter-whats-ahead-for-2026-270126-1392.html
- https://betfairsquare.pages.dev/sports/tennis (affiliate guide, context only)

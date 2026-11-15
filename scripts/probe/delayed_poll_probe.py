"""Read-only probe: does polling listMarketBook on the delayed key refresh faster than the stream's 180 s conflation?

Usage: .venv/Scripts/python -I scripts/probe/delayed_poll_probe.py <repo root> [seconds] [interval_s] [n_markets]

Polls listMarketBook (EX_BEST_OFFERS, EX_TRADED) for the most-traded in-play or
soon-to-start MATCH_ODDS / WIN markets and records, per poll, a fingerprint of each
market's best prices, traded volume and last traded price, plus the market's
lastMatchTime and totalMatched if returned. Prints how often each fingerprint changed.
No order operations. Credentials never printed.
"""
import datetime as dt
import json
import pathlib
import sys
import time

import betfairlightweight
from betfairlightweight import filters
from dotenv import dotenv_values

root = pathlib.Path(sys.argv[1]).resolve()
secs = int(sys.argv[2]) if len(sys.argv) > 2 else 120
step = float(sys.argv[3]) if len(sys.argv) > 3 else 5
n = int(sys.argv[4]) if len(sys.argv) > 4 else 3
env = dotenv_values(root / ".env")
out_dir = root / "data" / "raw" / "probe"
out_dir.mkdir(parents=True, exist_ok=True)
stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")

client = betfairlightweight.APIClient(
    username=env["BETFAIR_USERNAME"], password=env["BETFAIR_PASSWORD"], app_key=env["BETFAIR_APP_KEY"]
)
client.login_interactive()
now = dt.datetime.now(dt.timezone.utc)
cat = client.betting.list_market_catalogue(
    filter=filters.market_filter(
        market_type_codes=["MATCH_ODDS", "WIN"],
        market_start_time={"from": (now - dt.timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%SZ"),
                           "to": (now + dt.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")},
    ),
    market_projection=["EVENT_TYPE", "EVENT"],
    sort="MAXIMUM_TRADED",
    max_results=n,
)
ids = [m.market_id for m in cat]
for m in cat:
    print(f"market {m.market_id}: {m.event_type.name} | {m.event.name}")

rows, last_fp, changes, polls = [], {}, {i: 0 for i in ids}, 0
t_end = time.time() + secs
while time.time() < t_end:
    t0 = time.time()
    books = client.betting.list_market_book(
        market_ids=ids,
        price_projection=filters.price_projection(price_data=["EX_BEST_OFFERS", "EX_TRADED"]),
        lightweight=True,
    )
    polls += 1
    for b in books:
        fp = json.dumps([[r.get("selectionId"), r.get("lastPriceTraded"), r.get("totalMatched"),
                          (r.get("ex") or {}).get("availableToBack", [])[:1],
                          (r.get("ex") or {}).get("availableToLay", [])[:1],
                          len((r.get("ex") or {}).get("tradedVolume", []))] for r in b.get("runners", [])],
                        sort_keys=True)
        mid = b["marketId"]
        if mid in last_fp and fp != last_fp[mid]:
            changes[mid] += 1
        last_fp[mid] = fp
        rows.append({"recv_ms": int(t0 * 1000), "marketId": mid, "inplay": b.get("inplay"),
                     "status": b.get("status"), "totalMatched": b.get("totalMatched"),
                     "lastMatchTime": b.get("lastMatchTime"), "fingerprint": fp})
    time.sleep(max(0.0, step - (time.time() - t0)))
(out_dir / f"{stamp}_poll.jsonl").write_text("\n".join(json.dumps(r) for r in rows), encoding="utf-8")
print(f"polls: {polls} every {step}s over {secs}s")
for mid in ids:
    lmt = sorted({r['lastMatchTime'] for r in rows if r['marketId'] == mid and r['lastMatchTime']})
    print(f"  {mid}: fingerprint changed {changes[mid]} times; distinct lastMatchTime values {len(lmt)}; "
          f"totalMatched returned: {any(r['totalMatched'] for r in rows if r['marketId'] == mid)}")
try:
    client.logout()
except Exception:
    pass

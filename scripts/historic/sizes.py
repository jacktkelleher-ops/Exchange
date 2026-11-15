"""Report file count and size of purchased Betfair historical data (read-only).

Usage: .venv/Scripts/python -I scripts/historic/sizes.py <repo root>

Reads data/raw/betfair_historic/my_data.json (from my_data.py), groups items
by sport and plan, and calls GetAdvBasketDataSize for each group's full date
range. Writes data/raw/betfair_historic/sizes.json. No files downloaded.

Request shape follows the historicdata.betfair.com portal bundle (2026-11-15):
integer day/month/year fields and the three collection arrays always present.
betfairlightweight 2.24.0 sends strings and omits empty arrays, which now
returns HTTP 400 [verified: run on 2026-11-15].
"""
import calendar
import json
import pathlib
import sys
import time
from collections import defaultdict

import betfairlightweight
from dotenv import dotenv_values

BASE = "https://historicdata.betfair.com/api/"


def body(sport, plan, lo, hi, mt=(), co=(), ft=()):
    y1, m1 = int(lo[:4]), int(lo[5:7])
    y2, m2 = int(hi[:4]), int(hi[5:7])
    return {
        "sport": sport, "plan": plan,
        "fromDay": 1, "fromMonth": m1, "fromYear": y1,
        "toDay": calendar.monthrange(y2, m2)[1], "toMonth": m2, "toYear": y2,
        "marketTypesCollection": list(mt), "countriesCollection": list(co), "fileTypeCollection": list(ft),
    }


def post(client, method, payload):
    r = client.session.post(BASE + method, json=payload, headers=client.historic.headers, timeout=(10, 120))
    return r.status_code, (r.json() if r.headers.get("content-type", "").startswith("application/json") else r.text[:300])


root = pathlib.Path(sys.argv[1]).resolve()
out = root / "data" / "raw" / "betfair_historic"
env = dotenv_values(root / ".env")
items = json.loads((out / "my_data.json").read_text(encoding="utf-8"))
groups = defaultdict(list)
for it in items:
    groups[(it["sport"], it["plan"])].append(it["forDate"][:10])

client = betfairlightweight.APIClient(
    username=env["BETFAIR_USERNAME"], password=env["BETFAIR_PASSWORD"], app_key=env["BETFAIR_APP_KEY"]
)
client.login_interactive()
results = []
try:
    for (sport, plan), dates in sorted(groups.items()):
        lo, hi = min(dates), max(dates)
        b = body(sport, plan, lo, hi)
        code, size = post(client, "GetAdvBasketDataSize", b)
        if code != 200:
            # Fall back: fill the collections with every option the API offers.
            c2, opts = post(client, "GetCollectionOptions", b)
            if c2 == 200:
                ids = lambda k: [o["name"] for o in opts.get(k, [])]
                b = body(sport, plan, lo, hi, ids("marketTypesCollection"), ids("countriesCollection"), ids("fileTypeCollection"))
                code, size = post(client, "GetAdvBasketDataSize", b)
            else:
                size = {"error": f"GetCollectionOptions {c2}: {opts}"}
        results.append({"sport": sport, "plan": plan, "from": lo, "to": hi, "status": code, "size": size})
        print(f"{sport} | {plan} | {lo} -> {hi} | HTTP {code} | {json.dumps(size)[:200]}")
        time.sleep(1)
finally:
    try:
        client.logout()
    except Exception:
        pass
(out / "sizes.json").write_text(json.dumps(results, indent=2), encoding="utf-8")

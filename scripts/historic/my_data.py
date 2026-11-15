"""List the Betfair historical data the user has purchased (read-only).

Usage: .venv/Scripts/python -I scripts/historic/my_data.py <repo root>

Logs in with the interactive (no certificate) login using credentials from
<repo root>/.env, calls the Historical Data API GetMyData, saves the raw
response to data/raw/betfair_historic/my_data.json and prints a summary.
Credentials and the session token are never printed or written.

Source for the call sequence: betfairlightweight 2.24.0 endpoints/historic.py
(base URL https://historicdata.betfair.com/api/, ssoid header) [inferred:
library source, Betfair's own API docs page did not render].
"""
import json
import pathlib
import sys
from collections import defaultdict

import betfairlightweight
from dotenv import dotenv_values

root = pathlib.Path(sys.argv[1]).resolve()
env = dotenv_values(root / ".env")
client = betfairlightweight.APIClient(
    username=env["BETFAIR_USERNAME"],
    password=env["BETFAIR_PASSWORD"],
    app_key=env["BETFAIR_APP_KEY"],
)
client.login_interactive()
try:
    # GetMyData now only allows GET (OPTIONS on 2026-11-15 returned
    # "Allow: GET,HEAD,OPTIONS"; betfairlightweight 2.24.0 still POSTs and gets 405).
    r = client.session.get(
        client.historic.url + "GetMyData", headers=client.historic.headers, timeout=(10, 60)
    )
    r.raise_for_status()
    data = r.json()
finally:
    try:
        client.logout()
    except Exception:
        pass

out = root / "data" / "raw" / "betfair_historic"
out.mkdir(parents=True, exist_ok=True)
(out / "my_data.json").write_text(json.dumps(data, indent=2), encoding="utf-8")

print(f"purchased items: {len(data)}")
if data:
    print("fields:", sorted(data[0].keys()))
groups = defaultdict(list)
for item in data:
    groups[(item.get("sport"), item.get("plan"))].append(item.get("forDate", "")[:10])
for (sport, plan), dates in sorted(groups.items(), key=lambda kv: (str(kv[0][0]), str(kv[0][1]))):
    dates = sorted(dates)
    print(f"{sport} | {plan} | {len(dates)} month(s) | {dates[0]} -> {dates[-1]}")

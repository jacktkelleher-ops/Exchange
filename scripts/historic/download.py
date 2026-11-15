"""Download purchased Betfair historical data as one archive per sport, plan and year.

Usage: .venv/Scripts/python -I scripts/historic/download.py <repo root> [sport ...]

Reads data/raw/betfair_historic/my_data.json (from my_data.py). For each
(sport, plan, year) it asks the API for a download key (POST api/PreDownload
with a JSON array of basket items) and streams GET api/DownloadBasketFiles?key=
to data/raw/betfair_historic/<sport>/<plan>/<year>.tar. This is the flow the
historicdata.betfair.com portal uses (portal bundle read on 2026-11-15); the
per-file DownloadFile route would need one request per market file.

Resumable: a finished archive is skipped; downloads go to .part and are renamed
when complete. Stops if free disk space would fall below MIN_FREE_GB.
Most recent years first. Credentials and tokens are never printed.
"""
import calendar
import json
import pathlib
import shutil
import sys
import time
from collections import defaultdict

import betfairlightweight
from dotenv import dotenv_values

BASE = "https://historicdata.betfair.com/api/"
MIN_FREE_GB = 5  # operational safety margin, not a research threshold


def item(sport, plan, year, months):
    m1, m2 = min(months), max(months)
    return {
        "sport": sport, "plan": plan,
        "fromYear": year, "fromMonth": m1, "fromDay": 1,
        "toYear": year, "toMonth": m2, "toDay": calendar.monthrange(year, m2)[1],
        "eventId": None, "eventName": None,
        "marketTypesCollection": [], "countriesCollection": [], "fileTypeCollection": [],
    }


def slug(s):
    return s.lower().replace(" ", "-")


root = pathlib.Path(sys.argv[1]).resolve()
only = {s.lower() for s in sys.argv[2:]}
out = root / "data" / "raw" / "betfair_historic"
env = dotenv_values(root / ".env")
items = json.loads((out / "my_data.json").read_text(encoding="utf-8"))
log_path = out / "download_log.jsonl"

jobs = defaultdict(set)
for it in items:
    if only and it["sport"].lower() not in only:
        continue
    y, m = int(it["forDate"][:4]), int(it["forDate"][5:7])
    jobs[(it["sport"], it["plan"], y)].add(m)
order = sorted(jobs, key=lambda k: (-k[2], k[0]))

client = betfairlightweight.APIClient(
    username=env["BETFAIR_USERNAME"], password=env["BETFAIR_PASSWORD"], app_key=env["BETFAIR_APP_KEY"]
)
client.login_interactive()
headers = client.historic.headers
try:
    for sport, plan, year in order:
        dest = out / slug(sport) / slug(plan) / f"{year}.tar"
        if dest.exists():
            print(f"skip  {dest.relative_to(root)} (exists)")
            continue
        free_gb = shutil.disk_usage(out).free / 1e9
        if free_gb < MIN_FREE_GB:
            print(f"STOP  free disk {free_gb:.1f} GB < {MIN_FREE_GB} GB")
            break
        dest.parent.mkdir(parents=True, exist_ok=True)
        body = [item(sport, plan, year, jobs[(sport, plan, year)])]
        r = client.session.post(BASE + "PreDownload", json=body, headers=headers, timeout=(10, 300))
        if r.status_code != 200:
            print(f"FAIL  PreDownload {sport} {plan} {year}: HTTP {r.status_code} {r.text[:200]}")
            continue
        key = r.json().get("key")
        part = dest.with_suffix(".tar.part")
        t0, n = time.time(), 0
        with client.session.get(BASE + "DownloadBasketFiles", params={"key": key}, headers=headers,
                                stream=True, timeout=(10, 600)) as d:
            if d.status_code != 200:
                print(f"FAIL  DownloadBasketFiles {sport} {plan} {year}: HTTP {d.status_code} {d.text[:200]}")
                continue
            ctype = d.headers.get("content-type", "")
            with open(part, "wb") as f:
                for chunk in d.iter_content(chunk_size=1 << 20):
                    f.write(chunk)
                    n += len(chunk)
        part.replace(dest)
        secs = time.time() - t0
        rec = {"sport": sport, "plan": plan, "year": year, "months": sorted(jobs[(sport, plan, year)]),
               "bytes": n, "seconds": round(secs, 1), "content_type": ctype, "path": str(dest.relative_to(root))}
        with open(log_path, "a", encoding="utf-8") as lf:
            lf.write(json.dumps(rec) + "\n")
        print(f"done  {dest.relative_to(root)}  {n/1e6:.0f} MB in {secs:.0f}s  ({ctype})")
finally:
    try:
        client.logout()
    except Exception:
        pass

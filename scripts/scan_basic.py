"""Stream a Betfair Basic historical tar and summarise markets without extracting to disk.

Usage: python -I scan_basic.py <tar path> <out dir>
Writes:
  summary_types.csv   counts by eventTypeId x marketType
  soccer_markets.csv  one row per runner for selected soccer market types
"""
import bz2, csv, json, os, sys, tarfile, collections
from datetime import datetime, timezone

TAR, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
KEEP = {"MATCH_ODDS", "OVER_UNDER_05", "OVER_UNDER_15", "OVER_UNDER_25", "OVER_UNDER_35",
        "OVER_UNDER_45", "BOTH_TEAMS_TO_SCORE", "CORRECT_SCORE"}
OFFSETS_MIN = [1440, 360, 180, 60, 15]  # minutes before scheduled start


def iso_ms(s):
    return int(datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp() * 1000)


types = collections.Counter()
errors = 0
fields = ["marketId", "eventId", "eventName", "countryCode", "marketType", "marketName",
          "marketTime", "marketBaseRate", "turnInPlayEnabled", "selectionId", "runnerName",
          "status", "n_ltp_preoff", "ltp_first", *[f"ltp_m{m}" for m in OFFSETS_MIN],
          "ltp_close", "first_inplay_pt"]
fout = open(os.path.join(OUT, "soccer_markets.csv"), "w", newline="", encoding="utf-8")
w = csv.DictWriter(fout, fieldnames=fields)
w.writeheader()

with tarfile.open(TAR, "r:") as tf:
    for n, m in enumerate(tf):
        if not m.isfile() or not m.name.endswith(".bz2"):
            continue
        try:
            raw = bz2.decompress(tf.extractfile(m).read())
        except Exception:
            errors += 1
            continue
        md = None
        runners_hist = collections.defaultdict(list)  # selId -> [(pt, ltp)]
        first_inplay = None
        mid = None
        for line in raw.splitlines():
            try:
                msg = json.loads(line)
            except Exception:
                continue
            pt = msg.get("pt")
            for mc in msg.get("mc", []):
                mid = mc.get("id", mid)
                if "marketDefinition" in mc:
                    md = mc["marketDefinition"]
                    if md.get("inPlay") and first_inplay is None:
                        first_inplay = pt
                for rc in mc.get("rc", []):
                    if "ltp" in rc:
                        runners_hist[rc["id"]].append((pt, rc["ltp"]))
        if md is None:
            errors += 1
            continue
        et, mt = md.get("eventTypeId"), md.get("marketType")
        types[(et, mt)] += 1
        if et != "1" or mt not in KEEP:
            continue
        try:
            mtime = iso_ms(md["marketTime"])
        except Exception:
            mtime = None
        cutoff = first_inplay if first_inplay else mtime
        for r in md.get("runners", []):
            hist = runners_hist.get(r["id"], [])
            pre = [(p, v) for p, v in hist if cutoff is None or p < cutoff]
            row = {"marketId": mid, "eventId": md.get("eventId"), "eventName": md.get("eventName"),
                   "countryCode": md.get("countryCode"), "marketType": mt, "marketName": md.get("name"),
                   "marketTime": md.get("marketTime"), "marketBaseRate": md.get("marketBaseRate"),
                   "turnInPlayEnabled": md.get("turnInPlayEnabled"), "selectionId": r["id"],
                   "runnerName": r.get("name"), "status": r.get("status"), "n_ltp_preoff": len(pre),
                   "ltp_first": pre[0][1] if pre else None,
                   "ltp_close": pre[-1][1] if pre else None, "first_inplay_pt": first_inplay}
            for off in OFFSETS_MIN:
                val = None
                if mtime:
                    t = mtime - off * 60000
                    for p, v in pre:
                        if p <= t:
                            val = v
                        else:
                            break
                row[f"ltp_m{off}"] = val
            w.writerow(row)
        if n % 20000 == 0:
            print(n, "members", flush=True)

fout.close()
with open(os.path.join(OUT, "summary_types.csv"), "w", newline="") as f:
    cw = csv.writer(f)
    cw.writerow(["eventTypeId", "marketType", "markets"])
    for (et, mt), c in types.most_common():
        cw.writerow([et, mt, c])
print("done; errors", errors)

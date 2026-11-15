"""Summarise a delayed-key stream probe file written by delayed_stream_probe.py.

Usage: python -I scripts/probe/analyse_probe.py <probe .jsonl>

Reports: message ops and change types, conflateMs and status/error messages,
per-market update counts and intervals (from pt), runner-change fields seen,
ladder depth seen, con flags, and receive time minus pt.
"""
import json
import statistics as st
import sys
from collections import Counter, defaultdict

path = sys.argv[1]
ops, cts, statuses, conflate = Counter(), Counter(), [], set()
market_pts = defaultdict(list)
fields = Counter()
mc_keys = Counter()
levels = defaultdict(int)
con_true = 0
lags = []
for line in open(path, encoding="utf-8"):
    rec = json.loads(line)
    msg = json.loads(rec["raw"]) if isinstance(rec["raw"], str) else rec["raw"]
    op = msg.get("op")
    ops[op] += 1
    if op == "status":
        statuses.append({k: msg.get(k) for k in ("statusCode", "errorCode", "errorMessage", "connectionClosed")})
    if op != "mcm":
        continue
    cts[msg.get("ct", "UPDATE")] += 1
    if "conflateMs" in msg:
        conflate.add(msg["conflateMs"])
    pt = msg.get("pt")
    if pt and msg.get("ct") != "HEARTBEAT":
        lags.append(rec["recv_ms"] - pt)
    for mc in msg.get("mc", []):
        mc_keys.update(k for k in mc if k not in ("id", "rc"))
        if mc.get("con"):
            con_true += 1
        if mc.get("rc") or "marketDefinition" in mc:
            market_pts[mc["id"]].append(pt)
        for rc in mc.get("rc", []):
            for k, v in rc.items():
                if k == "id":
                    continue
                fields[k] += 1
                if k in ("batb", "batl", "bdatb", "bdatl") and v:
                    levels[k] = max(levels[k], max(x[0] for x in v) + 1)
                if k in ("atb", "atl") and v:
                    levels[k] = max(levels[k], len(v))

print("ops:", dict(ops))
print("change types:", dict(cts))
print("conflateMs seen:", sorted(conflate))
print("status messages:", statuses[:5])
print("market-change keys:", dict(mc_keys))
print("runner-change fields (count of runner changes containing each):", dict(fields))
print("max ladder levels seen:", dict(levels))
print("market changes flagged con=true:", con_true)
if lags:
    lags.sort()
    print(f"recv - pt (ms): median {lags[len(lags)//2]}, min {lags[0]}, p90 {lags[int(len(lags)*.9)]}, max {lags[-1]}, n {len(lags)}")
print(f"markets with updates: {len(market_pts)}")
gaps = []
rows = []
for mid, pts in market_pts.items():
    pts = sorted(p for p in pts if p)
    g = [(b - a) / 1000 for a, b in zip(pts, pts[1:]) if b > a]
    gaps += g
    rows.append((len(pts), mid, round(st.median(g), 1) if g else None))
for n, mid, med in sorted(rows, reverse=True)[:10]:
    print(f"  {mid}: {n} updates, median gap {med} s")
if gaps:
    gaps.sort()
    print(f"all update gaps (s): median {gaps[len(gaps)//2]:.1f}, p10 {gaps[int(len(gaps)*.1)]:.1f}, p90 {gaps[int(len(gaps)*.9)]:.1f}, min {gaps[0]:.1f}, n {len(gaps)}")

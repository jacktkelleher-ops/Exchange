"""Read-only probe of what the Betfair delayed app key actually streams.

Usage: .venv/Scripts/python -I scripts/probe/delayed_stream_probe.py <repo root> [seconds] [n_markets]

Picks the most-traded MATCH_ODDS / WIN markets that are in-play or start within
the next hour (listMarketCatalogue), subscribes to them on the Exchange Stream
API asking for every price field, and writes each raw stream line with a local
receive time to data/raw/probe/<UTC timestamp>.jsonl. Prints nothing secret.
Uses only login, listMarketCatalogue and the Stream API. No order operations.

Purpose (Phase 1a): settle what docs could not, per research/01-verify/api-access.md:
real update interval under the delayed key's documented 180000 ms conflation,
whether trd / tv / ltp / full atb-atl ladders arrive, ladder depth, and whether
pt is delayed relative to receive time.
"""
import datetime as dt
import json
import pathlib
import sys
import threading
import time

import betfairlightweight
from betfairlightweight import filters
import queue

from betfairlightweight.streaming import StreamListener
from dotenv import dotenv_values

root = pathlib.Path(sys.argv[1]).resolve()
secs = int(sys.argv[2]) if len(sys.argv) > 2 else 360
n = int(sys.argv[3]) if len(sys.argv) > 3 else 25
env = dotenv_values(root / ".env")
out_dir = root / "data" / "raw" / "probe"
out_dir.mkdir(parents=True, exist_ok=True)
stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
out = out_dir / f"{stamp}.jsonl"


class RawRecorder(StreamListener):
    """Writes every raw stream line unchanged, with a local receive time, then lets
    betfairlightweight's StreamListener process it as usual (it keeps clk/heartbeat
    bookkeeping the stream needs). The cache output queue is not read."""

    def __init__(self, fh):
        super().__init__(output_queue=queue.Queue())
        self.fh = fh
        self.lines = 0

    def on_data(self, raw_data):
        self.fh.write(json.dumps({"recv_ms": int(time.time() * 1000), "raw": raw_data}) + "\n")
        self.lines += 1
        return super().on_data(raw_data)


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
    market_projection=["EVENT_TYPE", "EVENT", "MARKET_START_TIME"],
    sort="MAXIMUM_TRADED",
    max_results=n,
)
meta = [{"marketId": m.market_id, "eventType": m.event_type.name, "event": m.event.name,
         "marketName": m.market_name, "start": m.market_start_time.isoformat(),
         "totalMatched_catalogue": m.total_matched} for m in cat]
(out_dir / f"{stamp}_markets.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
print(f"markets: {len(meta)}")
for m in meta:
    print(f"  {m['eventType']:<16} {m['start'][:16]}  {m['event'][:40]} | {m['marketName']}")

with open(out, "w", encoding="utf-8") as fh:
    listener = RawRecorder(fh)
    stream = client.streaming.create_stream(listener=listener)
    stream.subscribe_to_markets(
        market_filter=filters.streaming_market_filter(market_ids=[m["marketId"] for m in meta]),
        market_data_filter=filters.streaming_market_data_filter(
            fields=["EX_ALL_OFFERS", "EX_BEST_OFFERS", "EX_TRADED", "EX_TRADED_VOL", "EX_LTP", "EX_MARKET_DEF"],
            ladder_levels=10,
        ),
    )
    t = threading.Thread(target=stream.start, daemon=True)
    t.start()
    time.sleep(secs)
    stream.stop()
    print(f"stream lines written: {listener.lines} -> {out.relative_to(root)}")
try:
    client.logout()
except Exception:
    pass

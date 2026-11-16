"""Read every downloaded historical tar end to end and count its .bz2 market files.

Usage: python -I scripts/historic/verify_tars.py data/raw/betfair_historic
Assumes the layout <root>/<sport>/<plan>/<year>.tar written by download.py.
"""
import sys, tarfile, glob, json, os
root = sys.argv[1]
out = []
for p in sorted(glob.glob(os.path.join(root, "*", "*", "*.tar"))):
    n = 0; bz = 0; err = None
    try:
        with tarfile.open(p, "r:") as t:
            for m in t:
                if m.isfile():
                    n += 1
                    if m.name.endswith(".bz2"): bz += 1
    except Exception as e:
        err = repr(e)
    r = {"tar": os.path.relpath(p, root), "files": n, "bz2": bz, "error": err}
    out.append(r); print(json.dumps(r), flush=True)
print("TOTAL files", sum(r["files"] for r in out), "errors", sum(1 for r in out if r["error"]))

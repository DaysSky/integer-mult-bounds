"""[E1 VARIANT of PR #545's adapted PR #493 discovery/host_select.py (the eleven-stage hosting nominator); one listed change.]
The vendored nominator asserts that every helper starts at frame zero (residual width 8).  Here the residual widths are
read from the word's start frames (width = 8 - rank of the start frame), and the availability of each width is
R_w * T per stage; every residual is still forced onto an idle child (no banks).  The schedule, windows and the
integer programme (PR #442's hosting_core.solve, DaysSky) are the vendored ones, imported from the adapted copy.
usage: host11_e1.py AD545_DIR WORD.json.gz OUT_hosting.json"""
import gzip, json, sys
from collections import Counter
from pathlib import Path
import numpy as np

ad = Path(sys.argv[1]).resolve(); sys.path.insert(0, str(ad))
import host_select as HS          # the adapted vendored nominator: schedule(), constants, hosting_core
HC = HS.HC
w = json.loads(gzip.decompress(Path(sys.argv[2]).read_bytes()))
R, V = w['R'], w['v']
Lm = np.array(w['lines'], dtype=float)
dim = lambda f: int(np.linalg.matrix_rank(Lm[w['frames'][f]])) if w['frames'][f] else 0
widths = [HS.H - dim(w['start'][2 * V + i]) for i in range(R)]
win = {i: x for i, x in HC.windows(HS.schedule()).items() if x[1] and x[2]}
avail = Counter()
for s in range(HS.L):
    for wd in widths: avail[s, wd] += HS.T
ys, zs, val = HC.solve(win, 2 * V * HS.T, dict(avail), HS.M, pad_value=0.0, group={wd: 10 ** 9 for wd in set(widths)})
used = Counter()
for (i, wd, s), n in zs.items(): used[s, wd] += n
assert all(used[k] == a for k, a in avail.items()), "not every residual hosted"
out = Path(sys.argv[3])
if out.exists(): out.unlink()
HC.save_selection(out, 'bit', ys, zs, val)
print("selection saved:", out, "windows", len(win), "widths", dict(Counter(widths)), "proxy saving", val)

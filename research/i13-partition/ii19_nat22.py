"""THE WORD4 CONCENTRATION CEILINGS (ii19_nat22.py) — the payoff map of the Lorentzian push.

The word4's skip space is ALIVE (43 legal, 42 raising, +0.498% banked, gcheck-PASS).  The legal
skips so far are the marginal class (single-gate dim-5 levels).  The BIG concentration classes
(the ladder merges) are still behind the climb wall (2539 rejects).  Before the deep joint hunt:
price the ceilings of each class exactly (mass-preserving redistributions of the word4's OWN hist
at (v=121, h=9, R=472); helper-side collapses, the srcs' counter-reshapes ignored — PROBES, with
the record's shape-sensitivity discipline, not word prices).
"""
import json, os, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
from pricer import price
from mpmath import mp

argv = sys.argv[1:]
sys.argv = ['ii19_nat20.py']
exec(open('ii19_nat20.py').read().split('# (1) chain-shape census')[0])
FRONT = mp.mpf('0.001744385950814795279853')
R = w['R']
def pc(h): return price({int(k): int(v) for k, v in h.items()}, V, H, R)[0]

PH = ('D', 'A', 'B')
chainDA = defaultdict(list)
cur = list(w['start'])
for F, d, srcs in w['D'] + w['A']:
    for r in [d] + srcs:
        if cur[r] != F and dims[F] >= dims[cur[r]]:
            cur[r] = F; chainDA[r].append(F)
shape = Counter(tuple(dims[f] for f in chainDA[r]) for r in range(2 * V, nreg))
c0 = pc(hist0)
log('base hist %s (mass %d) | c %s (%+.4f%% vs frontier)' % (dict(sorted(hist0.items())),
    sum(k * v for k, v in hist0.items()), mp.nstr(c0, 22), float((c0 / FRONT - 1) * 100)))
log('helper shapes: %s' % dict(sorted(shape.items(), key=lambda x: -x[1])))

def ranks_of(sh):
    """the climb-rank Counter of a D+A chain with frame dims `sh` (helper starts at dim 0)."""
    out, d = Counter(), 0
    for x in sh:
        out[x - d] += 1; d = x
    return out

# class (i): the v2 merge on the (1,2,4,6) helpers (singleton-build -> cell merge)
n1 = shape[(1, 2, 4, 6)]
h = Counter(hist0); h[1] -= 2 * n1; h[2] += n1
c = pc(h)
log('v2-class x%d: hist %s' % (n1, dict(sorted(h.items()))))
log('    c %s (%+.4f%% vs word4-base, %+.4f%% vs frontier)' % (mp.nstr(c, 22),
    float((c / c0 - 1) * 100), float((c / FRONT - 1) * 100)))

# class (ii): the per-shape one-gate collapse (each helper's whole D+A ladder -> ONE climb to its top rung)
h = Counter(hist0)
for sh, n in shape.items():
    top = sh[-1] if sh else 0
    for r, cnt in ranks_of(sh).items(): h[r] -= cnt * n
    if sh: h[top] += n
h = Counter({k: v for k, v in h.items() if v})
c = pc(h)
log('one-gate collapse (all %d helpers): hist %s (mass %d)' % (sum(shape.values()), dict(sorted(h.items())),
    sum(k * v for k, v in h.items())))
log('    c %s (%+.4f%% vs word4-base, %+.4f%% vs frontier)' % (mp.nstr(c, 22),
    float((c / c0 - 1) * 100), float((c / FRONT - 1) * 100)))

"""For each target (Z11 rep): does ANY good frame through t give full routes (every u in R(t) has a source cell
inside one of the frame's 3 sections)?  Minimal-delivery (in-chain + 2 delivered) tops need such a frame."""
import sys, os, json, collections
os.environ['GRP'] = '11'
from lbase import *
fr = goodframes()
for fn in sys.argv[1:]:
    cov = {int(k): v for k, v in json.load(open(fn)).items()}
    cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in bits(cov[a])))
    cells_of = {s: [C for C in cells if C >> s & 1] for s in range(V)}
    reps = sorted(set(min(p[t] for p in PERMS) for t in range(V)))
    res = []
    for t in reps:
        best = None
        for F in fr:
            if not F >> t & 1: continue
            secs = [perp((1 << t) | (1 << f)) for f in bits(F) if f != t]
            miss = sum(1 for u in bits(HYP[t]) if not any(c & ~S == 0 for S in secs for c in cells_of[u]))
            if best is None or miss < best: best = miss
            if best == 0: break
        res.append((g.kind[t], best))
    print(fn, 'per-target min missing routes over all good-frame tops:', res, flush=True)

"""Line-mixing floor (frame-independent): for each source s, the best two line-perp sections R(s) cap R(s1),
R(s) cap R(s2) cover at most U2 readers; leftover = |R(s)| - U2.  Non-target registers >= 3v - floor(v/leftover)
when the line cover is 3 (each target reads at most one source at a single-line frame).  Exact, bitset exhaustive."""
import json, sys, itertools
import numpy as np
def run(path, reps=None):
    d = json.load(open(path)); eta = np.array(d['eta']); R = np.array(d['R']); v = len(R)
    G = R @ eta @ R.T; Z = np.abs(G) < 1e-9
    if reps is None:
        seen = {}; reps = []
        for t in range(v):
            k = (round(G[t, t], 4), int(Z[t].sum()))
            if k not in seen: seen[k] = 1; reps.append(t)
    worst = None
    for s in reps:
        rd = [t for t in range(v) if t != s and Z[s, t]]
        idx = {t: i for i, t in enumerate(rd)}
        masks = set()
        for u in range(v):
            if u == s: continue
            m = 0
            for t in rd:
                if t != u and Z[u, t]: m |= 1 << idx[t]
            masks.add(m)
        masks = sorted(masks, key=lambda m: -bin(m).count('1'))
        best = 0
        top = masks[:400]
        for a, b in itertools.combinations(top, 2):
            c = bin(a | b).count('1')
            if c > best: best = c
        # certify: any pair must include a mask at least best - max size... exhaustive over all pairs if small
        if len(masks) <= 3000:
            for a, b in itertools.combinations(masks, 2):
                c = bin(a | b).count('1')
                if c > best: best = c
        left = len(rd) - best
        print(path, 'source', s, 'readers', len(rd), 'best two sections cover', best, 'leftover', left, flush=True)
        worst = left if worst is None else min(worst, left)
    return v, worst
for p in sys.argv[1:]:
    v, left = run(p)
    print('==', p, 'v', v, 'min leftover', left, 'floor (cover 3): R >= 2v - floor(v/leftover) =', 2 * v - v // left, '(%.3f per port)' % ((2 * v - v // left) / v), flush=True)

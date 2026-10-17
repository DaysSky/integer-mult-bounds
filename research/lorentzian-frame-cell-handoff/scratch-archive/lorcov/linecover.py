"""Exact LINE cover numbers (the frame model's level-2 crossing): branch frames are flats <s,u> spanned by lines, so a
branch reaches readers in u^perp only.  cover(s) = min #lines u (u != s) with R(s) subset union of u^perp.
Exhaustive over pairs (cover 2) and triples (cover 3) with bitsets."""
import json, sys, collections, itertools
import numpy as np

def analyse(path, max_cover=3):
    d0 = json.load(open(path)); eta = np.array(d0['eta']); R = np.array(d0['R'])
    Gf = R @ eta @ R.T; v = len(R)
    Z = np.abs(Gf) < 1e-9
    G = np.rint(Gf * 1000).astype(np.int64)
    res = collections.Counter(); per = collections.defaultdict(collections.Counter)
    for s in range(v):
        rd = [t for t in range(v) if t != s and Z[s, t]]
        idx = {t: i for i, t in enumerate(rd)}
        full = (1 << len(rd)) - 1
        masks = {}
        for u in range(v):
            if u == s: continue
            m = 0
            for t in rd:
                if Z[u, t] and t != u: m |= 1 << idx[t]
            # a branch frame containing u must also allow u itself? u is not a reader target of its own frame unless
            # u in R(s) -- u in frame means u's own target (u perp u fails for norm != 0), so u is excluded (t != u)
            masks[u] = m
        ms = sorted(set(masks.values()), key=lambda m: -bin(m).count('1'))
        # remove dominated masks
        keep = []
        for m in ms:
            if not any((m | k) == k for k in keep): keep.append(m)
        c = None
        if any(m == full for m in keep): c = 1
        if c is None:
            for a, b in itertools.combinations(keep, 2):
                if a | b == full: c = 2; break
        if c is None and max_cover >= 3:
            for a, b in itertools.combinations(keep, 2):
                need = full & ~(a | b)
                if any((need & ~k) == 0 for k in keep): c = 3; break
        c = c if c is not None else '>3'
        key = (round(float(Gf[s, s]), 4), len(rd))
        res[c] += 1; per[key][c] += 1
    print(path, 'v', v, 'line cover', dict(res), flush=True)
    for k, cc in sorted(per.items()):
        print('   source (norm %s, readers %d):' % k, dict(cc), flush=True)

for p in sys.argv[1:]:
    analyse(p)

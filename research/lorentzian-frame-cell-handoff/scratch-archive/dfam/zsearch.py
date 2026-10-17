"""Z11-invariant decoder families on I_{11,1} from orbits of structured flats (flats.pkl).  Cost of a flat = its rank
(rank + 1 if its span is degenerate).  Family cost = 11 * sum of orbit costs.  Exact F2 span test per target-orbit rep."""
import pickle, itertools, sys, numpy as np
from dfam import LINES, IDX, NO, n, v
from flats import shift
flats = pickle.load(open('flats.pkl', 'rb'))
cost = [f[0] + (0 if f[2] else 1) for f in flats]
# target orbit reps under Z11
seen = set(); reps = []
for t in range(v):
    if t in seen: continue
    reps.append(t)
    typ, pts, _ = LINES[t]
    for a in range(n): seen.add(IDX[(typ, tuple(sorted((p + a) % n for p in pts)))])
Npos = []
for t in reps:
    Np = [t] + list(np.nonzero(NO[t])[0]); Npos.append({s: i for i, s in enumerate(Np)})
# per flat orbit: masks per target rep (11 pieces)
orbit_masks = []
for f in flats:
    pcs = [shift(f[1], a) for a in range(n)]
    pcs = list({tuple(sorted(p)): p for p in pcs}.values())
    per_t = []
    for pos in Npos:
        ms = []
        for p in pcs:
            m = 0
            for s in p:
                i = pos.get(s)
                if i is not None: m |= 1 << i
            if m: ms.append(m)
        per_t.append(ms)
    orbit_masks.append(per_t)
def served(orbs):
    for ti in range(len(reps)):
        basis = []
        for o in orbs:
            for m in orbit_masks[o][ti]:
                for b in basis:
                    m = min(m, m ^ b)
                if m: basis.append(m); basis.sort(reverse=True)
        x = 1
        for b in basis: x = min(x, x ^ b)
        if x: return False, ti
    return True, None
if __name__ == '__main__':
    budget = int(sys.argv[1]) if len(sys.argv) > 1 else 9
    kmax = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    idx = sorted(range(len(flats)), key=lambda i: cost[i])
    hits = 0; tested = 0
    for k in range(2, kmax + 1):
        for combo in itertools.combinations(idx, k):
            if sum(cost[i] for i in combo) > budget: continue
            tested += 1
            ok, _ = served(combo)
            if ok:
                hits += 1
                print('HIT cost', 11*sum(cost[i] for i in combo), [(flats[i][0], len(flats[i][1])) for i in combo], combo, flush=True)
            if tested % 20000 == 0: print('tested', tested, flush=True)
    print('done k<=%d budget %d: tested %d, hits %d' % (kmax, budget, tested, hits))

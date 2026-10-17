# For every target: find 3 LEGAL (closed, nondegenerate, rank 9, inside t-perp) hyperplane frames such that every
# partition cell of R(t) lies wholly inside one of them and every single line in one.  Sampling; a hit certifies.
import sys, pickle, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, bits, V, nondegenerate, closure, dim
L = g.L.astype(float)
part = pickle.load(open(sys.argv[1], 'rb')); TR = int(sys.argv[2])
frames = [tuple(f) for b in part[0] for f in b]
frame_of = {u: f for f in frames for u in f}
rng = np.random.default_rng(7)
out = {}
for t in range(V):
    R = bits(g.HYP[t]); Rs = set(R)
    X = L[R]; B = np.linalg.svd(X)[2][:10]
    C = {u: B @ L[u] for u in R}
    cells, singles, seen = [], [], set()
    for u in R:
        if u in seen: continue
        mates = [v for v in frame_of.get(u, ()) if v != u and v in Rs and v not in seen]
        if mates: cells.append((u, mates[0])); seen |= {u, mates[0]}
        else: singles.append(u); seen.add(u)
    units = [np.array([C[u], C[v]]) for u, v in cells] + [np.array([C[u]]) for u in singles]
    nU = len(units)
    def legal(n):
        Hl = sum(1 << u for u in R if abs(C[u] @ n) < 1e-8)
        cl = closure(Hl)
        return dim(cl) == 9 and nondegenerate(cl) and cl & ~g.HYP[t] == 0
    def inside(n, idx): return [i for i in idx if np.abs(units[i] @ n).max() < 1e-8]
    def hyper(idx):
        M = np.vstack([units[i] for i in idx])
        if np.linalg.matrix_rank(M) != 9: return None
        n = np.linalg.svd(M)[2][-1]
        return n if legal(n) else None
    found = None
    allu = list(range(nU))
    for trial in range(TR):
        n1 = hyper(rng.choice(nU, 6, replace=False))
        if n1 is None: continue
        r1 = [i for i in allu if i not in inside(n1, allu)]
        for t2 in range(20):
            if len(r1) < 6: break
            n2 = hyper(rng.choice(r1, 6, replace=False))
            if n2 is None: continue
            r2 = [i for i in r1 if i not in inside(n2, r1)]
            M = np.vstack([units[i] for i in r2]) if r2 else np.zeros((0, 10))
            rk = np.linalg.matrix_rank(M) if len(M) else 0
            if rk <= 9:
                # extend the rest to a legal hyperplane: try completing with extra units inside
                cand = [n for n in (np.linalg.svd(M)[2][-1],) ] if rk == 9 else []
                if rk < 9:
                    for t3 in range(50):
                        extra = rng.choice(nU, 9 - rk + 2, replace=False)
                        MM = np.vstack([M] + [units[i] for i in extra])
                        if np.linalg.matrix_rank(MM) == 9: cand.append(np.linalg.svd(MM)[2][-1])
                for n3 in cand:
                    if legal(n3) and len(inside(n3, r2)) == len(r2):
                        found = (nU - len(r1), len(r1) - len(r2), len(r2)); break
            if found: break
        if found: break
    out[t] = found
    if t % 20 == 0: print(t, g.kind[t], found, flush=True)
ok = sum(1 for v in out.values() if v)
print('targets with a legal cell-aligned 3-cover found:', ok, 'of', V, '| missing kinds', [g.kind[t] for t, v in out.items() if not v][:20])
pickle.dump(out, open('/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/blk/legalcover_out.pkl', 'wb'))

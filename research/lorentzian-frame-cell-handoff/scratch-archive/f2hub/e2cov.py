# For rank-9 E-sets: search hyperplanes H1 (span of 8 lines of E) such that E \ H1 has rank <= 8 (2-cover).
import sys, pickle, itertools, collections, random, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, bits, V, nondegenerate, closure
HYP = g.HYP
def pm(m):
    r = g.FULL
    for s in bits(m): r &= HYP[s]
    return r
B2 = lambda x, y: (1 << x) | (1 << y)
L = g.L.astype(float)
rnd = random.Random(1)
frames, pun = pickle.load(open('/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/goodframe/goodpart.pkl', 'rb'))
reps = {}
for q in frames: reps.setdefault(''.join(sorted(g.kind[x] for x in q)), q)
def hyper_cover(E, r, tries=4000):
    Eb = bits(E); X = L[Eb]
    U, S, Vt = np.linalg.svd(X); B = Vt[:r]; C = X @ B.T          # coordinates in span
    best = None; seen = set()
    for _ in range(tries):
        idx = rnd.sample(range(len(Eb)), r - 1)
        M = C[idx]
        if np.linalg.matrix_rank(M) < r - 1: continue
        _, s, vt = np.linalg.svd(M); n = vt[-1]
        on = np.abs(C @ n) < 1e-9
        key = tuple(on)
        if key in seen: continue
        seen.add(key)
        rest = C[~on]
        rr = np.linalg.matrix_rank(rest) if len(rest) else 0
        H1 = sum(1 << Eb[i] for i in range(len(Eb)) if on[i]); H2 = E & ~H1
        cand = (rr, -int(on.sum()))
        if best is None or cand < best[0]: best = (cand, H1, H2)
    return best, len(seen)
for key, q in reps.items():
    t, a, b, c = q
    U = B2(t, a) | B2(b, c); Q = pm(U)
    for x, y in itertools.combinations(q, 2):
        Exy = pm(B2(x, y)) & ~Q & ~U
        r = np.linalg.matrix_rank(L[bits(Exy)])
        if r < 9: print(key, g.kind[x] + g.kind[y], 'E rank', r, '(single sub-frame)'); continue
        (cand, H1, H2), ns = hyper_cover(Exy, r)
        print(key, g.kind[x] + g.kind[y], '|E|', bin(Exy).count('1'), 'hyperplanes seen', ns, 'best: rest rank', cand[0], '|H1 n E|', -cand[1],
              'nd(cl H1)', nondegenerate(closure(H1)), 'nd(cl rest)', nondegenerate(closure(H2)) if H2 else None)

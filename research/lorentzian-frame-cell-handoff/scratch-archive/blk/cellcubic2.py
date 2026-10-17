# For target t and a frame partition: cells of R(t) (pairs from one partition frame, both in R(t)) and singles.
# Do 3 hyperplanes of t-perp contain every cell wholly?  Necessary: a nonzero cubic form on t-perp vanishing on
# every cell plane and single line.  Report the rank of the vanishing conditions (220 = dim Sym^3 of a 10-dim space).
import sys, pickle, itertools, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, bits, V
L = g.L.astype(float)
part = pickle.load(open(sys.argv[1], 'rb'))
frames = [tuple(f) for b in part[0] for f in (b if isinstance(b[0], (tuple, list)) else [b])]
frame_of = {u: f for f in frames for u in f}
rng = np.random.default_rng(1)
mons = list(itertools.combinations_with_replacement(range(10), 3))
def cubic_row(x):
    return np.array([x[i] * x[j] * x[k] for (i, j, k) in mons])
for t in [int(a) for a in sys.argv[2:]]:
    R = bits(g.HYP[t]); Rs = set(R)
    X = L[R]; U, S, Vt = np.linalg.svd(X); B = Vt[:10]
    coord = lambda u: B @ L[u]
    cells, singles = [], []
    seen = set()
    for u in R:
        if u in seen: continue
        f = frame_of.get(u)
        mates = [v for v in (f or []) if v != u and v in Rs and v not in seen]
        if mates:
            v = mates[0]; cells.append((u, v)); seen |= {u, v}
        else:
            singles.append(u); seen.add(u)
    rows = []
    for (u, v) in cells:
        cu, cv = coord(u), coord(v)
        for a, b in ((1, 0), (0, 1), (1, 1), (1, -1)):         # 4 points determine a binary cubic
            rows.append(cubic_row(a * cu + b * cv))
    for u in singles: rows.append(cubic_row(coord(u)))
    M = np.array(rows)
    print('t', t, g.kind[t], '| cells', len(cells), 'singles', len(singles), '| conditions', len(rows), '| rank', np.linalg.matrix_rank(M), 'of', len(mons))
# ---- search: H1 = hyperplane spanned by cells (sampled); remaining cells+singles: is there a nonzero quadratic form
# vanishing on all their planes/lines (necessary for a 2-hyperplane cover of the rest)?
mons2 = list(itertools.combinations_with_replacement(range(10), 2))
def quad_row(x): return np.array([x[i] * x[j] for (i, j) in mons2])
for t in [int(a) for a in sys.argv[2:]]:
    R = bits(g.HYP[t]); Rs = set(R)
    X = L[R]; U, S, Vt = np.linalg.svd(X); B = Vt[:10]
    coord = lambda u: B @ L[u]
    cells, singles = [], []; seen = set()
    for u in R:
        if u in seen: continue
        f = frame_of.get(u)
        mates = [v for v in (f or []) if v != u and v in Rs and v not in seen]
        if mates: v = mates[0]; cells.append((u, v)); seen |= {u, v}
        else: singles.append(u); seen.add(u)
    P = [np.array([coord(u), coord(v)]) for (u, v) in cells]
    best = []
    for trial in range(3000):
        idx = rng.choice(len(cells), 5, replace=False)
        M = np.vstack([P[i] for i in idx])
        if np.linalg.matrix_rank(M) != 9: continue
        n = np.linalg.svd(M)[2][-1]
        inside = [i for i in range(len(cells)) if np.abs(P[i] @ n).max() < 1e-8]
        sin = [u for u in singles if abs(coord(u) @ n) < 1e-8]
        best.append((len(inside), tuple(inside), tuple(sin)))
    best = sorted(set(best), reverse=True)[:40]
    ok2 = 0
    for (k, inside, sin) in best:
        rest = [i for i in range(len(cells)) if i not in inside]
        rows = []
        for i in rest:
            cu, cv = P[i]
            for a, b in ((1, 0), (0, 1), (1, 1)): rows.append(quad_row(a * cu + b * cv))
        for u in singles:
            if u not in sin: rows.append(quad_row(coord(u)))
        rk = np.linalg.matrix_rank(np.array(rows)) if rows else 0
        if rk < len(mons2): ok2 += 1
    print('t', t, g.kind[t], '| best H1 holds', best[0][0], 'of', len(cells), 'cells | candidates with a quadratic form vanishing on the rest:', ok2, 'of', len(best))
# ---- direct 3-cover search: H1 (top candidates), H2 sampled, H3 = span of the rest (needs rank <= 9)
print('--- direct 3-hyperplane cell covers')
def planes_rank(idxs, sing, P, coord):
    rows = [P[i][0] for i in idxs] + [P[i][1] for i in idxs] + [coord(u) for u in sing]
    return np.linalg.matrix_rank(np.array(rows)) if rows else 0
for t in [int(a) for a in sys.argv[2:]]:
    R = bits(g.HYP[t]); Rs = set(R)
    X = L[R]; U, S, Vt = np.linalg.svd(X); B = Vt[:10]
    coord = lambda u: B @ L[u]
    cells, singles = [], []; seen = set()
    for u in R:
        if u in seen: continue
        f = frame_of.get(u)
        mates = [v for v in (f or []) if v != u and v in Rs and v not in seen]
        if mates: v = mates[0]; cells.append((u, v)); seen |= {u, v}
        else: singles.append(u); seen.add(u)
    P = [np.array([coord(u), coord(v)]) for (u, v) in cells]
    def hyper_from(idxs):
        M = np.vstack([P[i] for i in idxs])
        if np.linalg.matrix_rank(M) != 9: return None
        return np.linalg.svd(M)[2][-1]
    def inside(n, idxs): return [i for i in idxs if np.abs(P[i] @ n).max() < 1e-8]
    found = None; tries = 0
    allc = list(range(len(cells)))
    for trial in range(4000):
        n1 = hyper_from(rng.choice(len(cells), 5, replace=False))
        if n1 is None: continue
        r1 = [i for i in allc if i not in inside(n1, allc)]
        s1 = [u for u in singles if abs(coord(u) @ n1) > 1e-8]
        if len(r1) < 5: 
            if planes_rank(r1, s1, P, coord) <= 9: found = (len(allc) - len(r1), len(r1), 0); break
            continue
        for t2 in range(30):
            n2 = hyper_from(rng.choice(r1, 5, replace=False))
            if n2 is None: continue
            r2 = [i for i in r1 if i not in inside(n2, r1)]
            s2 = [u for u in s1 if abs(coord(u) @ n2) > 1e-8]
            tries += 1
            if planes_rank(r2, s2, P, coord) <= 9:
                # third hyperplane normal from the rest; check the three line frames
                rows = [P[i][0] for i in r2] + [P[i][1] for i in r2] + [coord(u) for u in s2]
                M = np.array(rows)
                if np.linalg.matrix_rank(M) < 9:
                    extra = [P[i][0] for i in allc] ; M = np.vstack([M] + [P[i] for i in allc])
                n3 = np.linalg.svd(np.array(rows))[2][-1] if len(rows) else None
                chk = []
                for n in (n1, n2, n3):
                    Hl = sum(1 << u for u in R if abs(coord(u) @ n) < 1e-8)
                    from lw import nondegenerate, closure, dim
                    cl = closure(Hl)
                    chk.append((bin(Hl).count('1'), dim(cl), nondegenerate(cl), cl & ~g.HYP[t] == 0))
                found = (len(allc) - len(r1), len(r1) - len(r2), len(r2), chk); break
        if found: break
    print('t', t, g.kind[t], '| cells', len(cells), '| 3-cover found:', found, '| H2 tries', tries)

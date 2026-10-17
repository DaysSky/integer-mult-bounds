# Local search for I_{11,1} decoder codes: pieces from structured low-rank families; state = independent piece list.
# Objective = cost + MU * load (infeasible = some target without a valid row: big penalty per target).
import sys, itertools, random, time, numpy as np, pickle
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V, bits, closure, dim, nondegenerate
from codescore import System
MU = float(sys.argv[1]); T = float(sys.argv[2]); seed = int(sys.argv[3]); KMAX = int(sys.argv[4]) if len(sys.argv) > 4 else 16
S = System(g.G); rnd = random.Random(seed)
P = g.P; Tl = g.T; pts = range(11)
def mask(ls): return sum(1 << u for u in ls)
fam = {}
def add(m):
    if m == 0 or m in fam: return
    F = closure(m); r = dim(F)
    fam[m] = r if nondegenerate(F) else r + 1
lab = np.array([[(g.binlabel(t) >> i) & 1 for i in range(11)] for t in range(V)])
D10 = [mask([t for t in range(V) if lab[t, i]]) for i in pts]
for m in D10: add(m)
for i, j in itertools.combinations(pts, 2): add(D10[i] & D10[j])
for h in pts:
    others = [j for j in pts if j != h]
    for k in (8, 9):
        for Sx in itertools.combinations(others, k):
            add(mask([P(a, b) for a, b in itertools.combinations(Sx, 2)] + [Tl(h, a, b) for a, b in itertools.combinations(Sx, 2)]))
for k in (8, 10):
    for Sx in itertools.combinations(pts, k):
        add(mask([P(a, b) for a, b in itertools.combinations(Sx, 2)] + [Tl(a, b, c) for a, b, c in itertools.combinations(Sx, 3)]))
for a, b in itertools.combinations(pts, 2):
    add((1 << P(a, b)) | mask([Tl(a, b, m) for m in pts if m not in (a, b)]))
for i, j, k in itertools.combinations(pts, 3):
    add(mask([Tl(i, j, k), P(i, j), P(i, k), P(j, k)]))
for t in range(V):
    for u in range(t + 1, V):
        if g.G[t, u] == 0 and rnd.random() < 0.15: add(g.HYP[t] & g.HYP[u])
FAM = list(fam.items()); print('family', len(FAM), flush=True)
def evaluate(pcs):
    basis = []; piv = {}
    for m in pcs:
        x = m
        while x:
            hb = x.bit_length() - 1
            if hb in piv: x ^= piv[hb]
            else: piv[hb] = x; break
        if x: basis.append(m)
        else: return None                      # dependent: reject
    rows = S.rows(basis)
    miss = sum(1 for r in rows if r is None)
    load = sum(r - 1 for r in rows if r is not None)
    cost = sum(fam[m] for m in pcs)
    return cost, miss, load
def obj(e): return e[0] + MU * e[2] + 1000 * e[1]
cur = list(D10); ce = evaluate(cur); co = obj(ce); best = (co, ce, list(cur)); t0 = time.time(); it = 0
print('start', ce, flush=True)
while time.time() - t0 < T:
    it += 1
    new = list(cur); r = rnd.random()
    if r < 0.4 and len(new) < KMAX: new.append(rnd.choice(FAM)[0])
    elif r < 0.6 and len(new) > 1: new.pop(rnd.randrange(len(new)))
    else: new[rnd.randrange(len(new))] = rnd.choice(FAM)[0]
    e = evaluate(new)
    if e is None: continue
    o = obj(e)
    if o <= co or rnd.random() < np.exp((co - o) / 20.0):
        cur, ce, co = new, e, o
        if e[1] == 0 and o < best[0]:
            best = (o, e, list(new)); print('it', it, 'best: cost %d load %d k %d' % (e[0], e[2], len(new)), '%.0fs' % (time.time() - t0), flush=True)
print('FINAL', best[1], 'pieces', len(best[2]))
pickle.dump(best, open('i11_pareto_mu%s_s%d.pkl' % (MU, seed), 'wb'))

"""Simulated annealing over good-frame systems (each line s picks a good 4-frame F_s containing it; mates M(s)) for
WEAK union-top routability: an orthogonal pair (t,u) is routable iff some e in M(t), f in M(u) satisfy
e _|_ u, f _|_ t, e _|_ f (cell {u,f} inside section {t,e}-perp, equivalently cell {t,e} inside {u,f}-perp).
Objective: U = #unroutable unordered orthogonal pairs + LAM * #non-reciprocal mate incidences.
usage: lroute_a3.py seed iters LAM OPTS(good|all) -> lroutea3_best_<seed>.json
Structured variant: lines of the 27 packed A3 blocks (a3part_11.json) must take a cover containing their A3-opposite
(so the A3-perp node is shared by the 3 opposite-pair sections of the block); other lines are free."""
import sys, json, random, time, itertools
import numpy as np
from lgeo import *
seed = int(sys.argv[1]); ITERS = int(sys.argv[2]); LAM = float(sys.argv[3]); OPTS = sys.argv[4]; INIT = sys.argv[5] if len(sys.argv) > 5 else None
random.seed(seed); np.random.seed(seed)
t0 = time.time()
O = (np.array(G) == 0); np.fill_diagonal(O, False)
orth = [np.nonzero(O[s])[0] for s in range(V)]
import pickle
cov = pickle.load(open('covers3.pkl', 'rb'))
fr_of = [[(t,) + ms for ms, gd in cov[t] if gd or OPTS == 'all'] for t in range(V)]
blocks = json.load(open('a3part_11.json'))
oppo = {}
for X in blocks:
    for t in X:
        o = [e for e in X if e != t and G[t][e] == 0]
        assert len(o) == 1; oppo[t] = o[0]
for t, o in oppo.items():
    fr_of[t] = [f for f in fr_of[t] if o in f]
    assert fr_of[t], ('no cover with opposite', t)
print('block lines', len(oppo), 'options per line', sorted(set(len(x) for x in fr_of)), flush=True)
M = np.zeros((V, 3), dtype=np.int64)
if INIT:
    d = {int(k): v for k, v in json.load(open(INIT)).items()}
    for s in range(V):
        ms = [x for x in bits(d[s]) if x != s]; M[s] = ms
else:
    for s in range(V):
        f = random.choice(fr_of[s]); M[s] = list(f[1:])
def route_row(s, Ms):
    """routable(s,u) for all u, given mates Ms of s (array 3) and current M for others"""
    r = np.zeros(V, dtype=bool)
    for e in Ms:
        oe = O[e]                       # e _|_ u
        for j in range(3):
            fj = M[:, j]                # mate j of each u
            r |= oe & O[fj, s] & O[e, fj]
    return r & O[s]
R = np.zeros((V, V), dtype=bool)
for s in range(V): R[s] = route_row(s, M[s])
R = R & R.T | (R & R.T)                 # symmetric by construction; keep consistent
def unr_count(): return int((O & ~R).sum() // 2)
def nonrec():
    c = 0
    for s in range(V):
        for e in M[s]:
            if s not in M[e]: c += 1
    return c
U = unr_count(); NR = nonrec(); cur = U + LAM * NR
best = cur; bestM = M.copy()
print('init U', U, 'nonrec', NR, flush=True)
T0 = 3.0; T1 = 0.05
for it in range(ITERS):
    T = T0 * (T1 / T0) ** (it / ITERS)
    s = random.randrange(V)
    f = random.choice(fr_of[s]); Ms = np.array(f[1:])
    if set(Ms.tolist()) == set(M[s].tolist()): continue
    old = M[s].copy()
    rnew = route_row(s, Ms)
    # change in symmetric routability: pairs (s,u) recomputed from s's side; but route(s,u) also equals route(u,s)
    # computed from u's side with M[s] as u's partner mates -> same condition, so row s is exact.
    dU = int((O[s] & ~rnew).sum()) - int((O[s] & ~R[s]).sum())
    # reciprocity delta
    dNR = 0
    for e in old:
        if s not in M[e]: dNR -= 1
        if e in M[s] and False: pass
    for e in Ms:
        if s not in M[e]: dNR += 1
    oldset, newset = set(old.tolist()), set(Ms.tolist())
    for x in range(V):
        pass
    # mates of others pointing at s: x with s in M[x]: reciprocal iff x in M[s]
    pts = np.nonzero((M == s).any(axis=1))[0]
    for x in pts:
        dNR += (0 if x in newset else 1) - (0 if x in oldset else 1)
    dcost = dU + LAM * dNR
    if dcost <= 0 or random.random() < np.exp(-dcost / T):
        M[s] = Ms; R[s] = rnew; R[:, s] = rnew
        U += dU; NR += dNR; cur += dcost
        if cur < best:
            best = cur; bestM = M.copy()
    if it % 20000 == 0:
        print('[%5.0fs] it %d T %.3f U %d nonrec %d cost %.1f best %.1f' % (time.time() - t0, it, T, U, NR, cur, best), flush=True)
M = bestM
for s in range(V): R[s] = route_row(s, M[s])
print('final best: U', unr_count(), 'nonrec', nonrec(), flush=True)
json.dump({s: sum(1 << int(x) for x in list(M[s]) + [s]) for s in range(V)}, open('lroutea3_best_%d_%s.json' % (seed, OPTS), 'w'))

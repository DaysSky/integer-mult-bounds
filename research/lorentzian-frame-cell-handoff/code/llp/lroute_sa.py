"""Simulated annealing over good-frame systems (each line s picks a good 4-frame F_s containing it; mates M(s)) for
WEAK union-top routability: an orthogonal pair (t,u) is routable iff some e in M(t), f in M(u) satisfy
e _|_ u, f _|_ t, e _|_ f (cell {u,f} inside section {t,e}-perp, equivalently cell {t,e} inside {u,f}-perp).
Objective: U = #unroutable unordered orthogonal pairs + LAM * #non-reciprocal mate incidences.
usage: lroute_sa.py seed iters LAM [init.json] -> lroute_best_<seed>.json"""
import sys, json, random, time, itertools
import numpy as np
from lgeo import *
seed = int(sys.argv[1]); ITERS = int(sys.argv[2]); LAM = float(sys.argv[3]); INIT = sys.argv[4] if len(sys.argv) > 4 else None
random.seed(seed); np.random.seed(seed)
t0 = time.time()
O = (np.array(G) == 0); np.fill_diagonal(O, False)
orth = [np.nonzero(O[s])[0] for s in range(V)]
# good frames through each line
def goodframes():
    fr = set()
    for a in range(V):
        for b in orth[a]:
            if b <= a: continue
            for c in orth[a]:
                if c <= b or not O[b, c]: continue
                for d in orth[a]:
                    if d <= c or not (O[b, d] and O[c, d]): continue
                    s_ = g.L[[a, b, c, d]].sum(axis=0)
                    if all(int(x) % 2 == 0 for x in s_): fr.add((a, b, c, d))
    return sorted(fr)
GF = goodframes()
fr_of = [[] for _ in range(V)]
for f in GF:
    for s in f: fr_of[s].append(f)
print('good frames', len(GF), 'per line', sorted(set(len(x) for x in fr_of)), flush=True)
M = np.zeros((V, 3), dtype=np.int64)
if INIT:
    d = {int(k): v for k, v in json.load(open(INIT)).items()}
    for s in range(V):
        ms = [x for x in bits(d[s]) if x != s]; M[s] = ms
else:
    for s in range(V):
        f = random.choice(fr_of[s]); M[s] = [x for x in f if x != s]
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
    f = random.choice(fr_of[s]); Ms = np.array([x for x in f if x != s])
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
json.dump({s: sum(1 << int(x) for x in list(M[s]) + [s]) for s in range(V)}, open('lroute_best_%d.json' % seed, 'w'))

"""Z11-symmetric weak-routability anneal: each of the 20 line orbits picks a cover (good frame or any exact union
cover) for its representative; images by rotation.  Objective U + LAM * nonrec as lroute_sa.py.
usage: lroute_z11.py seed iters LAM OPTS(good|all) -> lroutez_best_<seed>_<OPTS>.json"""
import sys, json, random, time, pickle
import numpy as np
from lgeo import *
seed = int(sys.argv[1]); ITERS = int(sys.argv[2]); LAM = float(sys.argv[3]); OPTS = sys.argv[4]
random.seed(seed); np.random.seed(seed)
t0 = time.time()
O = (np.array(G) == 0); np.fill_diagonal(O, False)
cov = pickle.load(open('covers3.pkl', 'rb'))
opts = [[ms for ms, gd in cov[t] if gd or OPTS == 'all'] for t in range(V)]
rot = [img_line(s, [(i + 1) % n for i in range(n)]) for s in range(V)]
orb = {}; reps = []
for s in range(V):
    if s in orb: continue
    o = len(reps); reps.append(s); x = s
    for k in range(n): orb[x] = (o, k); x = rot[x]
def rotk(x, k):
    for _ in range(k % n): x = rot[x]
    return x
M = np.zeros((V, 3), dtype=np.int64)
choice = [random.randrange(len(opts[r])) for r in reps]
def apply(o):
    r = reps[o]; ms = opts[r][choice[o]]
    for k in range(n): M[rotk(r, k)] = [rotk(e, k) for e in ms]
for o in range(len(reps)): apply(o)
def route_row(s):
    r = np.zeros(V, dtype=bool)
    for e in M[s]:
        oe = O[e]
        for j in range(3):
            fj = M[:, j]; r |= oe & O[fj, s] & O[e, fj]
    return r & O[s]
def full_U():
    R = np.zeros((V, V), dtype=bool)
    for s in range(V): R[s] = route_row(s)
    R = R | R.T
    return int((O & ~R).sum() // 2)
def nonrec():
    return sum(1 for s in range(V) for e in M[s] if s not in M[e])
U = full_U(); NR = nonrec(); cur = U + LAM * NR; best = cur; bestc = list(choice)
print('init U', U, 'nonrec', NR, flush=True)
T0, T1 = 3.0, 0.05
for it in range(ITERS):
    T = T0 * (T1 / T0) ** (it / ITERS)
    o = random.randrange(len(reps)); old = choice[o]
    choice[o] = random.randrange(len(opts[reps[o]]))
    if choice[o] == old: continue
    apply(o)
    U2 = full_U(); NR2 = nonrec(); c2 = U2 + LAM * NR2
    if c2 <= cur or random.random() < np.exp(-(c2 - cur) / T):
        U, NR, cur = U2, NR2, c2
        if cur < best: best = cur; bestc = list(choice)
    else:
        choice[o] = old; apply(o)
    if it % 200 == 0: print('[%5.0fs] it %d T %.3f U %d nonrec %d best %.1f' % (time.time() - t0, it, T, U, NR, best), flush=True)
choice = bestc
for o in range(len(reps)): apply(o)
print('final U', full_U(), 'nonrec', nonrec(), flush=True)
json.dump({s: sum(1 << int(x) for x in list(M[s]) + [s]) for s in range(V)}, open('lroutez_best_%d_%s.json' % (seed, OPTS), 'w'))

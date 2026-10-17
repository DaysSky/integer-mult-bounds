"""Multi-level extension data: for every node orbit rep N0 (side.pkl), enumerate concrete closed N' strictly inside N0,
group by the orbit of (N0, N'), record W1 keys (N0, N'_r, {u}), Z keys (N'_r, {u}), node key of N'_r, counts, and for
each u in N0 the multiplicity of W1 keys among concrete N' containing u.  -> nodesub.pkl"""
import pickle, time, collections
from lgeo import *
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
side = pickle.load(open('side.pkl', 'rb'))
def inv(p):
    q = [0] * n
    for a, b in enumerate(p): q[b] = a
    return q
out = {}
tot = 0
for k, (nk, d) in enumerate(sorted(side['nodes'].items(), key=lambda kv: kv[1]['size'])):
    N0 = d['N0']
    seen = set(); fr = []
    for u in bits(N0):
        N = pp(1 << u)
        if N != N0 and N not in seen: seen.add(N); fr.append(N)
    while fr:
        nf = []
        for N in fr:
            P = pm(N); done = set()
            for y in bits(N0 & ~N):
                P2 = P & HYP[y]
                if P2 in done: continue
                done.add(P2); N2 = pm(P2)
                if N2 != N0 and N2 not in seen: seen.add(N2); nf.append(N2)
        fr = nf
    reps = {}; mult = collections.defaultdict(collections.Counter)
    for N in seen:
        key, perm = canon((N0, N))
        r = reps.get(key)
        if r is None:
            r = dict(N=N, iperm=inv(perm), count=0, nkey=canon((N,))[0],
                     wkeys={u: canon((N0, N, 1 << u))[0] for u in bits(N)},
                     zkeys={u: canon((N, 1 << u))[0] for u in bits(N)})
            reps[key] = r
        r['count'] += 1
        tau = [r['iperm'][perm[p]] for p in range(n)]
        for u in bits(N): mult[u][r['wkeys'][img_line(u, tau)]] += 1
    for r in reps.values(): del r['iperm']
    out[nk] = dict(reps=reps, mult={u: dict(c) for u, c in mult.items()})
    tot += len(seen)
    if k % 20 == 0: log('node', k, 'rank', d['rank'], 'size', d['size'], 'subsets', len(seen), 'orbits', len(reps), 'total', tot)
pickle.dump(out, open('nodesub.pkl', 'wb'))
log('saved; total concrete subsets', tot)

"""Section side of the one-level LP.  For plane orbit rep pi0 (index i into planes.pkl): enumerate every concrete closed
line set N inside S0 = pm(pi0); group by the S11-orbit of the pair (pi0, N) (key = canonical form); for each group rep
compute the orbit keys of (pi0, N_r, {u}) [W], (N_r, {u}) [Z], (N_r) [node] and lambda (3 if N_r contains an A2 plane,
else 2); and for every u in S0 the multiplicity of each W-key among concrete N containing u.
usage: lsecside.py i  -> sec_i.pkl"""
import sys, pickle, time, collections
from lgeo import *
i = int(sys.argv[1])
planes = pickle.load(open('planes.pkl', 'rb'))
pi0 = planes[i]
assert canon((pi0,))[0][0] == pi0
S0 = pm(pi0)
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
# concrete closed sets inside S0
seen = set(); fr = []
for u in bits(S0):
    N = pp(1 << u)
    if N not in seen: seen.add(N); fr.append(N)
while fr:
    nf = []
    for N in fr:
        P = pm(N); done = set()
        for y in bits(S0 & ~N):
            P2 = P & HYP[y]
            if P2 in done: continue
            done.add(P2); N2 = pm(P2)
            if N2 not in seen: seen.add(N2); nf.append(N2)
    fr = nf
log('section', pc(pi0), pc(S0), 'closed sets', len(seen))
def inv(p):
    q = [0] * n
    for a, b in enumerate(p): q[b] = a
    return q
def has_a2(N):
    b = bits(N)
    for x in range(len(b)):
        for y in range(x + 1, len(b)):
            if abs(int(G[b[x]][b[y]])) == 1:
                for z in b[y + 1:]:
                    if abs(int(G[b[x]][z])) == 1 and abs(int(G[b[y]][z])) == 1 and rank((1 << b[x]) | (1 << b[y]) | (1 << z)) == 2:
                        return True
    return False
reps = {}          # Ykey -> dict(N, perm, count, wkeys{u: key}, zkeys{u: key}, nkey, lam)
mult = collections.defaultdict(collections.Counter)   # u -> Counter(Wkey)
for k, N in enumerate(seen):
    key, perm = canon((pi0, N))
    r = reps.get(key)
    if r is None:
        wk = {u: canon((pi0, N, 1 << u))[0] for u in bits(N)}
        zk = {u: canon((N, 1 << u))[0] for u in bits(N)}
        r = dict(N=N, perm=perm, count=0, wkeys=wk, zkeys=zk, nkey=canon((N,))[0], lam=3 if has_a2(N) else 2,
                 rank=rank(N), size=pc(N), perp=pc(pm(N)))
        r['iperm'] = inv(perm)
        reps[key] = r
    r['count'] += 1
    # map lines of N to rep lines: tau = rep_perm^-1 o perm
    ip = r['iperm']
    tau = [ip[perm[p]] for p in range(n)]
    for u in bits(N):
        ur = img_line(u, tau)
        mult[u][r['wkeys'][ur]] += 1
    if k % 20000 == 0: log(k, 'groups', len(reps))
for r in reps.values(): del r['iperm']; del r['perm']
log('groups (N,pi) orbits:', len(reps), 'W keys:', len(set(k for r in reps.values() for k in r['wkeys'].values())))
pickle.dump(dict(pi0=pi0, S0=S0, reps=reps, mult={u: dict(c) for u, c in mult.items()}), open('sec_%d.pkl' % i, 'wb'))
log('saved')

"""Symmetric SAT search for cheap Eisenstein decoders: B = sum_{h in H} sum_j h.(R_j x A_j), cost-bounded reps."""
import pickle, sys, time, itertools, numpy as np
from pysat.solvers import Cadical153
from pysat.formula import IDPool
d = pickle.load(open('eis.pkl','rb'))
n = 40; nonorth = d['nonorth']; fl = d['flat_list']; C = d['cost'].astype(int); nf = len(fl)
elems = np.load('eis_elems.npy').astype(np.int64)
def order(g):
    x = np.arange(n); k = 0
    while True:
        x = g[x]; k += 1
        if np.array_equal(x, np.arange(n)): return k
def cyclic(g):
    H = [np.arange(n)]; x = g.copy()
    while not np.array_equal(x, np.arange(n)):
        H.append(x.copy()); x = g[x]
    return H
def solve(H, costs, timeout=120, inv_costs=()):
    pool = IDPool(); cl = []
    q = len(costs) + len(inv_costs)
    kinds = ['orb'] * len(costs) + ['inv'] * len(inv_costs)
    costs = list(costs) + list(inv_costs)
    a = [[pool.id(('a', j, t)) for t in range(n)] for j in range(q)]
    b = [[pool.id(('b', j, t)) for t in range(n)] for j in range(q)]
    for j, cj in enumerate(costs):
        sF = [pool.id(('F', j, k)) for k in range(nf)]; sG = [pool.id(('G', j, k)) for k in range(nf)]
        cl.append(sF); cl.append(sG)
        for k in range(nf):
            for t in range(n):
                if not (fl[k] >> t) & 1:
                    cl.append([-sF[k], -a[j][t]]); cl.append([-sG[k], -b[j][t]])
        for x, y in np.argwhere(C > cj):
            cl.append([-sF[int(x)], -sG[int(y)]])
        cl.append(a[j]); cl.append(b[j])   # nonempty
        if kinds[j] == 'inv':
            for h in H:
                for t in range(n):
                    ht = int(h[t])
                    if ht != t:
                        cl.append([-a[j][t], a[j][ht]]); cl.append([-b[j][t], b[j][ht]])
    Hinv = [np.argsort(h) for h in H]
    def xor_eq(lits, val):
        if not lits:
            if val: cl.append([])   # infeasible
            return
        acc = lits[0]
        for x in lits[1:]:
            y = pool.id(); cl.extend([[-y, acc, x], [-y, -acc, -x], [y, -acc, x], [y, acc, -x]]); acc = y
        cl.append([acc] if val else [-acc])
    andc = {}
    def and_(x, y):
        k = (x, y)
        if k not in andc:
            z = pool.id(); cl.extend([[-z, x], [-z, y], [z, -x, -y]]); andc[k] = z
        return andc[k]
    seen = set()
    cons = [(t, t, 1) for t in range(n)] + [(t, s, 0) for t in range(n) for s in range(n) if (nonorth[t] >> s) & 1]
    for t, s, v in cons:
        if (t, s) in seen: continue
        for h in H: seen.add((int(h[t]), int(h[s])))
        lits = [and_(a[j][int(hi[t])], b[j][int(hi[s])]) for j in range(q) if kinds[j] == 'orb' for hi in Hinv]
        lits += [and_(a[j][t], b[j][s]) for j in range(q) if kinds[j] == 'inv']
        xor_eq(lits, v)
    S = Cadical153(bootstrap_with=cl)
    t0 = time.time()
    # time-limited solve via interrupt
    import threading
    timer = threading.Timer(timeout, lambda: S.interrupt()); timer.start()
    ok = S.solve_limited(expect_interrupt=True)
    timer.cancel()
    res = None
    if ok:
        m = set(x for x in S.get_model() if x > 0)
        R = [[t for t in range(n) if a[j][t] in m] for j in range(q)]
        A = [[t for t in range(n) if b[j][t] in m] for j in range(q)]
        res = (R, A, kinds)
    return ok, res, time.time() - t0
def verify(H, R, A, kinds=None):
    B = np.zeros((n, n), dtype=np.uint8); rects = []
    kinds = kinds or ['orb'] * len(R)
    for Rj, Aj, kd in zip(R, A, kinds):
        if kd == 'inv':
            rects.append((list(Rj), list(Aj)))
            for t in Rj:
                for s in Aj: B[t, s] ^= 1
    for h in H:
        for Rj, Aj, kd in zip(R, A, kinds):
            if kd == 'inv': continue
            Rh = [int(h[t]) for t in Rj]; Ah = [int(h[t]) for t in Aj]
            rects.append((Rh, Ah))
            for t in Rh:
                for s in Ah: B[t, s] ^= 1
    ok = all(B[t, t] for t in range(n)) and not any(B[t, s] for t in range(n) for s in range(n) if (nonorth[t] >> s) & 1)
    table = d['table']
    def clo(S):
        f = 0
        for t in S: f = table[f][t]
        return f
    uniq = {}
    for Rh, Ah in rects:
        uniq[(tuple(sorted(Rh)), tuple(sorted(Ah)))] = uniq.get((tuple(sorted(Rh)), tuple(sorted(Ah))), 0) + 1
    cost = sum(int(C[clo(r), clo(a_)]) for (r, a_), mult in uniq.items() if mult % 2 == 1)
    return ok, cost, len(uniq)
if __name__ == '__main__':
    # pick one element of each order (first found) as cyclic group generator
    reps = {}
    for g in elems:
        o = order(g)
        reps.setdefault(o, []).append(g)
    orders = sorted(reps)
    print('element orders', {o: len(reps[o]) for o in orders}, flush=True)
    configs = eval(sys.argv[1]) if len(sys.argv) > 1 else None
    tlim = float(sys.argv[2]) if len(sys.argv) > 2 else 120
    for o, costs, nsamp in configs:
        gens = reps[o]
        rng = np.random.default_rng(o)
        idx = rng.choice(len(gens), size=min(nsamp, len(gens)), replace=False)
        for ii in idx:
            H = cyclic(gens[ii])
            ok, res, dt = solve(H, costs, tlim)
            line = 'order %d costs %s -> %s %.1fs' % (o, costs, {True: 'SAT', False: 'UNSAT', None: 'TIMEOUT'}[ok], dt)
            if ok:
                okv, cost, nu = verify(H, *res)
                line += ' verify %s true cost %d distinct rects %d' % (okv, cost, nu)
                pickle.dump((o, costs, [list(map(int, h)) for h in H], res), open('symsol_%d_%s_%d.pkl' % (o, '-'.join(map(str, costs)), ii), 'wb'))
            print(line, flush=True)

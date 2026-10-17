"""Symmetric (cyclic H) decoder search with a global weighted cost budget; finds min symmetric cost <= start."""
import pickle, sys, time, threading, numpy as np
from pysat.solvers import Cadical153
from pysat.formula import IDPool
from pysat.card import ITotalizer
d = pickle.load(open('eis.pkl','rb'))
n = 40; nonorth = d['nonorth']; fl = d['flat_list']; C = d['cost'].astype(int); nf = len(fl)
elems = np.load('eis_elems.npy').astype(np.int64)
classes = pickle.load(open('classes.pkl','rb'))
def cyclic(g):
    H = [np.arange(n)]; x = g.copy()
    while not np.array_equal(x, np.arange(n)):
        H.append(x.copy()); x = g[x]
    return H
def build(H, Qo, Qi):
    o = len(H); pool = IDPool(); cl = []
    kinds = ['orb'] * Qo + ['inv'] * Qi; q = Qo + Qi
    a = [[pool.id(('a', j, t)) for t in range(n)] for j in range(q)]
    b = [[pool.id(('b', j, t)) for t in range(n)] for j in range(q)]
    L = [[pool.id(('L', j, k)) for k in range(1, 5)] for j in range(q)]   # level>=k
    wl = []
    for j in range(q):
        for k in range(3): cl.append([-L[j][k + 1], L[j][k]])
        sF = [pool.id(('F', j, k)) for k in range(nf)]; sG = [pool.id(('G', j, k)) for k in range(nf)]
        cl.append(sF); cl.append(sG)
        for k in range(nf):
            for t in range(n):
                if not (fl[k] >> t) & 1:
                    cl.append([-sF[k], -a[j][t]]); cl.append([-sG[k], -b[j][t]])
        for x, y in np.argwhere(C >= 1):
            cl.append([-sF[int(x)], -sG[int(y)], L[j][int(C[x, y]) - 1]])
        if kinds[j] == 'inv':
            for h in H:
                for t in range(n):
                    if int(h[t]) != t:
                        cl.append([-a[j][t], a[j][int(h[t])]]); cl.append([-b[j][t], b[j][int(h[t])]])
        w = o if kinds[j] == 'orb' else 1
        wl += [lit for lit in L[j] for _ in range(w)]
        # symmetry breaking among orbit reps: levels nonincreasing
    for j in range(Qo - 1):
        for k in range(4): cl.append([-L[j + 1][k], L[j][k]])
    for j in range(Qo, q - 1):
        for k in range(4): cl.append([-L[j + 1][k], L[j][k]])
    Hinv = [np.argsort(h) for h in H]
    andc = {}
    def and_(x, y):
        if (x, y) not in andc:
            z = pool.id(); cl.extend([[-z, x], [-z, y], [z, -x, -y]]); andc[(x, y)] = z
        return andc[(x, y)]
    def xor_eq(lits, val):
        if not lits:
            if val: cl.append([])
            return
        acc = lits[0]
        for x in lits[1:]:
            y = pool.id(); cl.extend([[-y, acc, x], [-y, -acc, -x], [y, -acc, x], [y, acc, -x]]); acc = y
        cl.append([acc] if val else [-acc])
    seen = set()
    cons = [(t, t, 1) for t in range(n)] + [(t, s, 0) for t in range(n) for s in range(n) if (nonorth[t] >> s) & 1]
    for t, s, v in cons:
        if (t, s) in seen: continue
        for h in H: seen.add((int(h[t]), int(h[s])))
        lits = [and_(a[j][int(hi[t])], b[j][int(hi[s])]) for j in range(Qo) for hi in Hinv]
        lits += [and_(a[j][t], b[j][s]) for j in range(Qo, q)]
        xor_eq(lits, v)
    tot = ITotalizer(lits=wl, ubound=len(wl), top_id=pool.top)
    cl.extend(tot.cnf.clauses)
    return cl, a, b, tot, kinds
if __name__ == '__main__':
    ci = int(sys.argv[1]); start = int(sys.argv[2]); tlim = float(sys.argv[3])
    o, size, rep, fixed = classes[ci]; H = cyclic(elems[rep])
    Qo = start // o; Qi = min(start, max(0, int(sys.argv[4]) if len(sys.argv) > 4 else (8 if fixed else 0)))
    cl, a, b, tot, kinds = build(H, Qo, Qi)
    S = Cadical153(bootstrap_with=cl)
    budget = start; t0 = time.time()
    while budget >= 0:
        tm = threading.Timer(tlim, lambda: S.interrupt()); tm.start()
        ok = S.solve_limited(assumptions=[-tot.rhs[budget]], expect_interrupt=True); tm.cancel()
        tag = {True: 'SAT', False: 'UNSAT', None: 'TIMEOUT'}[ok]
        print('class %d order %d fixed %d Qo %d Qi %d budget %d -> %s %.0fs' % (ci, o, fixed, Qo, Qi, budget, tag, time.time() - t0), flush=True)
        if not ok: break
        m = set(x for x in S.get_model() if x > 0)
        R = [[t for t in range(n) if a[j][t] in m] for j in range(len(kinds))]
        A = [[t for t in range(n) if b[j][t] in m] for j in range(len(kinds))]
        from symsat2 import verify
        okv, cost, nu = verify(H, R, A, kinds)
        print('   verify', okv, 'true cost', cost, 'rects', nu, flush=True)
        pickle.dump((ci, [list(map(int, h)) for h in H], R, A, kinds), open('symbud_c%d_%d.pkl' % (ci, cost), 'wb'))
        budget = min(budget, cost) - 1

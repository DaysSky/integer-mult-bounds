"""SAT with a global cost budget: fitting decoder with r rectangles, minimise sum of flat-pair costs."""
import pickle, sys, time
import numpy as np
from pysat.solvers import Cadical153
from pysat.formula import IDPool
from pysat.card import ITotalizer
d = pickle.load(open('eis.pkl','rb'))
n = 40; nonorth = d['nonorth']; fl = d['flat_list']; C = d['cost'].astype(int)
nf = len(fl)

def build(r, maxlev=4):
    pool = IDPool(); cl = []
    a = [[pool.id(('a',t,i)) for i in range(r)] for t in range(n)]
    b = [[pool.id(('b',t,i)) for i in range(r)] for t in range(n)]
    L = [[pool.id(('L',i,k)) for k in range(1, maxlev+1)] for i in range(r)]  # L[i][k-1]: cost_i >= k
    for i in range(r):
        for k in range(maxlev-1):
            cl.append([-L[i][k+1], L[i][k]])
        if i + 1 < r:
            for k in range(maxlev):
                cl.append([-L[i+1][k], L[i][k]])  # levels nonincreasing in i
        sF = [pool.id(('F',i,k)) for k in range(nf)]
        sG = [pool.id(('G',i,k)) for k in range(nf)]
        cl.append(sF); cl.append(sG)
        for k in range(nf):
            for t in range(n):
                if not (fl[k] >> t) & 1:
                    cl.append([-sF[k], -a[t][i]]); cl.append([-sG[k], -b[t][i]])
        for x, y in np.argwhere(C >= 1):
            c = int(C[x, y])
            if c > maxlev:
                cl.append([-sF[x], -sG[y]])
            else:
                cl.append([-sF[x], -sG[y], L[i][c-1]])
    def xor_eq(lits, val):
        acc = lits[0]
        for x in lits[1:]:
            y = pool.id()
            cl.extend([[-y, acc, x], [-y, -acc, -x], [y, -acc, x], [y, acc, -x]])
            acc = y
        cl.append([acc] if val else [-acc])
    def and_(x, y):
        z = pool.id(); cl.extend([[-z, x], [-z, y], [z, -x, -y]]); return z
    pairs = [(t, t, 1) for t in range(n)] + [(t, s, 0) for t in range(n) for s in range(n) if (nonorth[t]>>s)&1]
    for t, s, v in pairs:
        xor_eq([and_(a[t][i], b[s][i]) for i in range(r)], v)
    flatL = [x for row in L for x in row]
    tot = ITotalizer(lits=flatL, ubound=len(flatL), top_id=pool.top)
    cl.extend(tot.cnf.clauses)
    return cl, a, b, L, tot

def extract(S, a, b, r):
    m = set(x for x in S.get_model() if x > 0)
    R = [[t for t in range(n) if a[t][i] in m] for i in range(r)]
    A = [[t for t in range(n) if b[t][i] in m] for i in range(r)]
    B = np.zeros((n, n), dtype=np.uint8)
    for Ri, Ai in zip(R, A):
        for t in Ri:
            for s in Ai: B[t, s] ^= 1
    ok = all(B[t, t] for t in range(n)) and not any(B[t, s] for t in range(n) for s in range(n) if (nonorth[t]>>s)&1)
    table = d['table']
    def clo(Sx):
        f = 0
        for t in Sx: f = table[f][t]
        return f
    costs = [int(C[clo(Ri), clo(Ai)]) for Ri, Ai in zip(R, A)]
    return ok, costs, R, A

if __name__ == '__main__':
    r = int(sys.argv[1]); start = int(sys.argv[2])
    t0 = time.time()
    cl, a, b, L, tot = build(r)
    print('r', r, 'clauses', len(cl), 'build %.1fs' % (time.time()-t0), flush=True)
    S = Cadical153(bootstrap_with=cl)
    budget = start
    while budget >= 0:
        ok = S.solve(assumptions=[-tot.rhs[budget]]) if budget < len(tot.rhs) else S.solve()
        print('budget', budget, 'SAT' if ok else 'UNSAT', '%.1fs' % (time.time()-t0), flush=True)
        if not ok: break
        okv, costs, R, A = extract(S, a, b, r)
        print('  verify', okv, 'costs', costs, 'true total', sum(costs), 'sizes', [(len(x), len(y)) for x, y in zip(R, A)], flush=True)
        pickle.dump((R, A, costs), open('budget_r%d_c%d.pkl' % (r, sum(costs)), 'wb'))
        budget = min(budget, sum(costs)) - 1

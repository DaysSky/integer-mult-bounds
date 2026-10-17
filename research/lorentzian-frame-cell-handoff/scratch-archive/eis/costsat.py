"""SAT: fitting F2 decoder B = sum_i 1_{R_i} 1_{A_i}^T with R_i in F_i, A_i in G_i, cost(F_i,G_i) <= c_i."""
import pickle, sys, time
import numpy as np
from pysat.solvers import Cadical153
from pysat.formula import IDPool
d = pickle.load(open('eis.pkl','rb'))
n = 40; nonorth = d['nonorth']; fl = d['flat_list']; C = d['cost'].astype(int)
nf = len(fl)
nonempty = [k for k in range(nf) if fl[k]]

def build(pattern):
    pool = IDPool(); cl = []
    r = len(pattern)
    a = [[pool.id(('a',t,i)) for i in range(r)] for t in range(n)]
    b = [[pool.id(('b',t,i)) for i in range(r)] for t in range(n)]
    for i, ci in enumerate(pattern):
        sF = {k: pool.id(('F',i,k)) for k in nonempty}
        sG = {k: pool.id(('G',i,k)) for k in nonempty}
        cl.append(list(sF.values())); cl.append(list(sG.values()))
        for k in nonempty:
            for t in range(n):
                if not (fl[k] >> t) & 1:
                    cl.append([-sF[k], -a[t][i]]); cl.append([-sG[k], -b[t][i]])
        bad = np.argwhere(C > ci)
        for x, y in bad:
            if fl[x] and fl[y]:
                cl.append([-sF[int(x)], -sG[int(y)]])
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
    return pool, cl, a, b

def verify(R, A):
    B = np.zeros((n, n), dtype=np.uint8)
    for Ri, Ai in zip(R, A):
        for t in Ri:
            for s in Ai:
                B[t, s] ^= 1
    ok = all(B[t, t] == 1 for t in range(n)) and all(B[t, s] == 0 for t in range(n) for s in range(n) if (nonorth[t]>>s)&1)
    # true cost via closure
    table = d['table']
    def clo(S):
        f = 0
        for t in S: f = table[f][t]
        return f
    cost = sum(int(C[clo(Ri), clo(Ai)]) for Ri, Ai in zip(R, A))
    return ok, cost

if __name__ == '__main__':
    pattern = [int(x) for x in sys.argv[1].split(',')]
    t0 = time.time()
    pool, cl, a, b = build(pattern)
    print('pattern', pattern, 'sum', sum(pattern), 'clauses', len(cl), 'build %.1fs' % (time.time()-t0), flush=True)
    S = Cadical153(bootstrap_with=cl)
    ok = S.solve()
    print('SAT' if ok else 'UNSAT', '%.1fs' % (time.time()-t0), flush=True)
    if ok:
        m = set(x for x in S.get_model() if x > 0)
        R = [[t for t in range(n) if a[t][i] in m] for i in range(len(pattern))]
        A = [[t for t in range(n) if b[t][i] in m] for i in range(len(pattern))]
        okv, cost = verify(R, A)
        print('verify', okv, 'true cost', cost, [(len(x), len(y)) for x, y in zip(R, A)])
        pickle.dump((R, A), open('dec_%s.pkl' % '_'.join(map(str, pattern)), 'wb'))

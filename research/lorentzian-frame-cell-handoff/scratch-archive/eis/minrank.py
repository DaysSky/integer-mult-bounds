import pickle, sys, itertools, time
from pysat.solvers import Cadical153
from pysat.formula import IDPool
d = pickle.load(open('eis.pkl','rb'))
n = 40; nonorth = d['nonorth']
def find_clique7():
    adj = [[(nonorth[t]>>s)&1 for s in range(n)] for t in range(n)]
    def ext(cl, cand):
        if len(cl) == 7: return cl
        for c in cand:
            r = ext(cl+[c], [x for x in cand if x > c and adj[c][x]])
            if r: return r
        return None
    for t in range(n):
        r = ext([t], [x for x in range(n) if x > t and adj[t][x]])
        if r: return r
def solve(r, extra=None, timeout=None):
    pool = IDPool(); cl = []
    a = [[pool.id(('a',t,i)) for i in range(r)] for t in range(n)]
    b = [[pool.id(('b',t,i)) for i in range(r)] for t in range(n)]
    def xor_eq(lits, val):
        # chain encoding
        acc = lits[0]
        for x in lits[1:]:
            y = pool.id(); # y = acc xor x
            cl.extend([[-y, acc, x], [-y, -acc, -x], [y, -acc, x], [y, acc, -x]])
            acc = y
        cl.append([acc] if val else [-acc])
    def and_(x, y):
        z = pool.id(); cl.extend([[-z, x], [-z, y], [z, -x, -y]]); return z
    pairs = [(t, t, 1) for t in range(n)] + [(t, s, 0) for t in range(n) for s in range(n) if (nonorth[t]>>s)&1]
    for t, s, v in pairs:
        xor_eq([and_(a[t][i], b[s][i]) for i in range(r)], v)
    Q = find_clique7()
    for k, t in enumerate(Q):
        for i in range(r):
            cl.append([a[t][i]] if i == k else [-a[t][i]])
    S = Cadical153(bootstrap_with=cl)
    ok = S.solve()
    sol = None
    if ok:
        m = set(x for x in S.get_model() if x > 0)
        sol = ([[int(a[t][i] in m) for i in range(r)] for t in range(n)], [[int(b[t][i] in m) for i in range(r)] for t in range(n)])
    return ok, sol, Q
if __name__ == '__main__':
    for r in map(int, sys.argv[1:]):
        t0 = time.time(); ok, sol, Q = solve(r)
        print('r', r, 'SAT' if ok else 'UNSAT', '%.1fs' % (time.time()-t0), 'clique', Q, flush=True)
        if ok: pickle.dump(sol, open('minrank_sol_%d.pkl' % r, 'wb'))

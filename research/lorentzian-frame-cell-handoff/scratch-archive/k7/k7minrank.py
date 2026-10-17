import pickle, sys, time, threading
import networkx as nx
from pysat.solvers import Cadical153
from pysat.formula import IDPool
d = pickle.load(open('k7.pkl','rb')); orth = d['orth']; n = len(orth)
G = nx.Graph(); G.add_nodes_from(range(n))
for i in range(n):
    for j in range(i + 1, n):
        if not orth[i][j]: G.add_edge(i, j)   # non-orthogonality graph
import random
best = []
adj = {i: set(G[i]) for i in range(n)}
for trial in range(3000):
    rnd = random.Random(trial); order = list(range(n)); rnd.shuffle(order)
    c = []
    for v in order:
        if all(v in adj[u] for u in c): c.append(v)
    if len(c) > len(best): best = c
cl = best
print('max nonorth clique size', len(cl), flush=True)
def solve(r, tmax):
    pool = IDPool(); cls = []
    a = [[pool.id(('a', t, i)) for i in range(r)] for t in range(n)]
    b = [[pool.id(('b', t, i)) for i in range(r)] for t in range(n)]
    def xor_eq(lits, val):
        acc = lits[0]
        for x in lits[1:]:
            y = pool.id(); cls.extend([[-y, acc, x], [-y, -acc, -x], [y, -acc, x], [y, acc, -x]]); acc = y
        cls.append([acc] if val else [-acc])
    def and_(x, y):
        z = pool.id(); cls.extend([[-z, x], [-z, y], [z, -x, -y]]); return z
    for t in range(n):
        for s in range(n):
            if t == s or not orth[t][s]:
                xor_eq([and_(a[t][i], b[s][i]) for i in range(r)], 1 if t == s else 0)
    for k, t in enumerate(cl):
        for i in range(r):
            cls.append([a[t][i]] if i == k else [-a[t][i]])
    S = Cadical153(bootstrap_with=cls)
    tm = threading.Timer(tmax, lambda: S.interrupt()); tm.start()
    ok = S.solve_limited(expect_interrupt=True); tm.cancel()
    sol = None
    if ok:
        m = set(x for x in S.get_model() if x > 0)
        sol = ([[int(a[t][i] in m) for i in range(r)] for t in range(n)], [[int(b[t][i] in m) for i in range(r)] for t in range(n)])
    return ok, sol
for r in range(len(cl), 40):
    t0 = time.time(); ok, sol = solve(r, float(sys.argv[1]) if len(sys.argv) > 1 else 600)
    print('r', r, {True: 'SAT', False: 'UNSAT', None: 'TIMEOUT'}[ok], '%.1fs' % (time.time() - t0), flush=True)
    if ok:
        pickle.dump(sol, open('k7_minrank_%d.pkl' % r, 'wb')); break

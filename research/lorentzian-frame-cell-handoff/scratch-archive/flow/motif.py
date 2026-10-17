"""Paper-style 3-stage bit motif with a general F2 decoder; topology + scalar check + fractional flow LP."""
import itertools, numpy as np
from scipy.optimize import linprog
import os
METHOD = os.environ.get('LPM', 'highs')
from scipy.sparse import coo_matrix

def triple_unit(h):
    ports = list(itertools.combinations(range(h), 3))
    v = len(ports)
    side = {S: [T for T in range(v) if len(set(ports[S]) & set(ports[T])) == 1] for S in range(v)}
    cent = [([T for T in range(v) if i in ports[T]], [S for S in range(v) if i in ports[S]]) for i in range(h)]
    return v, side, cent

class Circ:
    def __init__(self):
        self.wires = []; self.gates = []   # gate: (ports tuple, xors list of (tgt, ctl))
    def wire(self, name):
        self.wires.append(name); return len(self.wires) - 1
    def gate(self, xors, extra=()):
        ports = sorted(set([a for a, b in xors] + [b for a, b in xors]) | set(extra))
        self.gates.append((tuple(ports), list(xors)))

def build(v, side, cent, grouping='paper'):
    c = Circ()
    X = [c.wire(('X', a)) for a in range(v)]
    Y = [c.wire(('Y', a)) for a in range(v)]
    def invocation(src, tgt, st, inverse):
        A = {(S, T): c.wire(('A', st, S, T)) for S in range(v) for T in side[S]}
        C = [c.wire(('C', st, i)) for i in range(len(cent))]
        rows = []
        r_side = [[(tgt[S], A[S, T]) for T in side[S]] for S in range(v)]
        r_scat = [(tgt[S], C[i]) for i, (G, R) in enumerate(cent) for S in R]
        r_copy = [[(A[S, T], src[T]) for S in range(v) if T in side[S]] for T in range(v)]
        r_gath = [(C[i], src[T]) for i, (G, R) in enumerate(cent) for T in G]
        rows = [('pt', r_side), ('one', r_scat), ('pt', r_copy), ('one', r_gath),
                ('one', r_scat), ('pt', r_side), ('one', r_gath), ('pt', r_copy)]
        if inverse:
            rows = rows[::-1]
        for kind, r in rows:
            if grouping == 'paper':
                if kind == 'pt':
                    for g in r:
                        if g: c.gate(g)
                else:
                    c.gate(r)
            else:  # primitive XOR gates
                flat = [x for g in r for x in g] if kind == 'pt' else r
                for x in flat:
                    c.gate([x])
    invocation(X, Y, 0, False)
    invocation(Y, X, 1, True)
    invocation(X, Y, 2, False)
    W = len(c.wires)
    rho = list(range(W))
    for a in range(v):
        rho[X[a]], rho[Y[a]] = Y[a], X[a]
    return c, rho

def scalar_check(c, rho):
    W = len(c.wires)
    M = np.eye(W, dtype=np.uint8)
    for ports, xors in c.gates:
        for t, s in xors:
            M[t] ^= M[s]
    P = np.zeros((W, W), dtype=np.uint8)
    for w in range(W):
        P[rho[w], w] = 1
    return np.array_equal(M, P)

def topology(c):
    """vertices: 0..G-1 gates, then in(w)=G+2w, out(w)=G+2w+1. edges along each wire."""
    G = len(c.gates); W = len(c.wires)
    seq = [[] for _ in range(W)]
    for g, (ports, xors) in enumerate(c.gates):
        for p in ports:
            seq[p].append(g)
    edges = []
    for w in range(W):
        path = [G + 2 * w] + seq[w] + [G + 2 * w + 1]
        for a, b in zip(path, path[1:]):
            edges.append((a, b, w))
    return G + 2 * W, edges

def max_flow(c, rho, directed=False):
    nV, edges = topology(c)
    W = len(c.wires); G = len(c.gates); E = len(edges)
    arcs = [(a, b, e) for e, (a, b, w) in enumerate(edges)]
    if not directed:
        arcs += [(b, a, e) for e, (a, b, w) in enumerate(edges)]
    nA = len(arcs)
    # variables: x[k, arc] for commodity k, plus f[k]
    nvar = W * nA + W
    rows, cols, vals = [], [], []
    beq = []
    r = 0
    for k in range(W):
        s = G + 2 * k; t = G + 2 * rho[k] + 1
        # conservation: for each vertex, out - in = f_k [s] or -f_k [t] or 0
        for j, (a, b, e) in enumerate(arcs):
            rows.append(r + a); cols.append(k * nA + j); vals.append(1.0)
            rows.append(r + b); cols.append(k * nA + j); vals.append(-1.0)
        rows.append(r + s); cols.append(W * nA + k); vals.append(-1.0)
        rows.append(r + t); cols.append(W * nA + k); vals.append(1.0)
        r += nV
    Aeq = coo_matrix((vals, (rows, cols)), shape=(r, nvar)).tocsr()
    beq = np.zeros(r)
    rows, cols, vals = [], [], []
    for k in range(W):
        for j, (a, b, e) in enumerate(arcs):
            rows.append(e); cols.append(k * nA + j); vals.append(1.0)
    Aub = coo_matrix((vals, (rows, cols)), shape=(E, nvar)).tocsr()
    bub = np.ones(E)
    cost = np.zeros(nvar); cost[W * nA:] = -1.0
    bounds = [(0, None)] * (W * nA) + [(0, 1)] * W
    res = linprog(cost, A_ub=Aub, b_ub=bub, A_eq=Aeq, b_eq=beq, bounds=bounds, method=METHOD)
    return -res.fun, res, W, E

if __name__ == '__main__':
    import sys
    h = int(sys.argv[1]); grouping = sys.argv[2] if len(sys.argv) > 2 else 'paper'
    v, side, cent = triple_unit(h)
    c, rho = build(v, side, cent, grouping)
    print('h', h, 'v', v, 'W', len(c.wires), 'gates', len(c.gates), 'scalar ok', scalar_check(c, rho))
    for directed in (True, False):
        F, res, W, E = max_flow(c, rho, directed)
        print('directed' if directed else 'undirected', 'F*', round(F, 6), 'W', W, 'W-F*', round(W - F, 6), 'status', res.status)

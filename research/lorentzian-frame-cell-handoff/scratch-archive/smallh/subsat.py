"""Port-subset minrank SAT: choose a subset of candidate label lines (>= N ports) and an F2 decoder of rank c
fitting their orthogonality (B_TS = 0 for non-orthogonal pairs), optionally with corrector span limited to
planes (a=2): each present target T picks one plane C_T (perp to T, spanned by candidate lines) and B_TS may be
nonzero only for S with label in C_T.  Asymmetric decoders.  Cardinality via pysat CardEnc."""
import sys, itertools, time, threading, numpy as np
from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153
def run(L, F, c, N, a=None, tlimit=300, verbose=True):
    L = [np.array(l) for l in L]; F = np.array(F); v = len(L)
    G = np.array([[int(x @ F @ y) for y in L] for x in L])
    h = np.linalg.matrix_rank(np.array(L, dtype=float))
    pool = IDPool(); cl = []
    P = [pool.id(('p', i)) for i in range(v)]
    U = [[pool.id(('u', i, j)) for j in range(c)] for i in range(v)]
    V = [[pool.id(('v', i, j)) for j in range(c)] for i in range(v)]
    def AND(a_, b_):
        z = pool.id(('and', a_, b_)); cl.extend([[-z, a_], [-z, b_], [z, -a_, -b_]]); return z
    def XOR(a_, b_):
        z = pool.id(('xor', a_, b_)); cl.extend([[-z, a_, b_], [-z, -a_, -b_], [z, -a_, b_], [z, a_, -b_]]); return z
    def dot(i, k):
        lits = [AND(V[i][j], U[k][j]) for j in range(c)]
        acc = lits[0]
        for l in lits[1:]: acc = XOR(acc, l)
        return acc
    for i in range(v):
        for j in range(c):
            cl.append([P[i], -U[i][j]]); cl.append([P[i], -V[i][j]])
        cl.append([-P[i], dot(i, i)])
    # planes
    Y = {}
    if a == 2:
        for T in range(v):
            orth = [S for S in range(v) if S != T and G[T, S] == 0]
            planes = {}
            for S1, S2 in itertools.combinations(orth, 2):
                M = np.array([L[S1], L[S2]], dtype=float)
                if np.linalg.matrix_rank(M) < 2: continue
                mem = tuple(S for S in orth if np.linalg.matrix_rank(np.vstack([M, L[S]])) == 2)
                planes[mem] = 1
            for S in orth:  # single-line 'planes' are subsumed; also allow lines alone
                planes.setdefault((S,), 1)
            Y[T] = [(pool.id(('y', T, k)), mem) for k, mem in enumerate(planes)]
            cl.append([-P[T]] + [y for y, _ in Y[T]])
    for T in range(v):
        for S in range(v):
            if S == T: continue
            d = dot(T, S)
            if G[T, S] != 0:
                cl.append([-d])
            elif a == 2:
                cl.append([-d] + [y for y, mem in Y[T] if S in mem])
    card = CardEnc.atleast(lits=P, bound=N, vpool=pool, encoding=EncType.seqcounter)
    cl.extend(card.clauses)
    s = Cadical153(bootstrap_with=cl)
    tm = threading.Timer(tlimit, lambda: s.interrupt()); tm.start()
    t = time.time(); r = s.solve_limited(expect_interrupt=True); tm.cancel()
    res = {True: 'SAT', False: 'UNSAT', None: 'TIMEOUT'}[r]
    out = dict(v=v, h=int(h), c=c, N=N, a=a, res=res, sec=round(time.time()-t, 1))
    if r:
        m = set(x for x in s.get_model() if x > 0)
        out['ports'] = [i for i in range(v) if P[i] in m]
    if verbose: print({k: out[k] for k in out if k != 'ports'}, flush=True)
    return out
if __name__ == '__main__':
    pass

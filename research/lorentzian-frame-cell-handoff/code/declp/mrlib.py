"""Find small line sets Y of I_{11,1} whose decoder pattern has F2 minrank >= 11 (a rank-10 B = W U^T with unit
diagonal, zero on non-orthogonal pairs of Y, is UNSAT).  Y = 10-clique Q (gauge U_Q = W_Q = I) + extra lines Z;
greedy growth then greedy shrink to an inclusion-minimal Y.  library part of mr11.py (mr_le10, C10)"""
import sys, random, pickle, time
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
sys.path.insert(0, '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/dec')
from lw import g, V
from minrank_sat import CNF
from pysat.solvers import Cadical153
G = g.G
D = '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/declp/'
orb = pickle.load(open(D + 'corbits.pkl', 'rb'))
C10 = [c for k, v in orb.items() if len(v[0]) == 10 for c in v]
def mr_le10(Y, Q):
    c = 10; f = CNF()
    U = {y: [f.new() for _ in range(c)] for y in Y}; W = {y: [f.new() for _ in range(c)] for y in Y}
    def B(t, s): return f.xorlist([f.AND(W[t][j], U[s][j]) for j in range(c)])
    for t in Y: f.cl.append([B(t, t)])
    for t in Y:
        for s in Y:
            if s != t and G[t, s] != 0: f.cl.append([-B(t, s)])
    for i, q in enumerate(Q):
        for j in range(c):
            f.cl.append([U[q][j]] if j == i else [-U[q][j]]); f.cl.append([W[q][j]] if j == i else [-W[q][j]])
    s = Cadical153(bootstrap_with=f.cl); r = s.solve(); s.delete()
    return r

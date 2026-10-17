"""Find small line sets Y of I_{11,1} whose decoder pattern has F2 minrank >= 11 (a rank-10 B = W U^T with unit
diagonal, zero on non-orthogonal pairs of Y, is UNSAT).  Y = 10-clique Q (gauge U_Q = W_Q = I) + extra lines Z;
greedy growth then greedy shrink to an inclusion-minimal Y.  usage: mr11.py NTRIALS SEED"""
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
NT, seed = int(sys.argv[1]), int(sys.argv[2]); rnd = random.Random(seed)
found = []
t0 = time.time()
for trial in range(NT):
    Q = list(rnd.choice(C10)); Z = []
    others = [x for x in range(V) if x not in Q]; rnd.shuffle(others)
    for x in others:
        Z.append(x)
        if not mr_le10(Q + Z, Q): break
    else:
        print('trial', trial, 'never reached minrank 11 (all lines)', flush=True); continue
    # shrink Z
    for x in list(Z):
        Z2 = [z for z in Z if z != x]
        if not mr_le10(Q + Z2, Q): Z = Z2
    Y = tuple(sorted(Q + Z))
    found.append((Y, tuple(sorted(Q))))
    print('trial %d: minimal Y size %d (clique 10 + %d extra) types Q %s Z %s  %.0fs' % (trial, len(Y), len(Z),
          ''.join(sorted(g.kind[q] for q in Q)), ''.join(sorted(g.kind[z] for z in Z)), time.time() - t0), flush=True)
    pickle.dump(found, open(D + 'mr11_%d.pkl' % seed, 'wb'))

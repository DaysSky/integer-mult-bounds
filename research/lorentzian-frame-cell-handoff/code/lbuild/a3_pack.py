"""Constructive A3-parity selection for I_{11,1}: (1) all A3 subsystems (6-line rank-3 flats: 4 A2 triangles, 3
orthogonal opposite pairs); (2) CP-SAT maximum packing of line-disjoint A3 blocks; (3) block lines take their block
triple (two triangles through t + pair {t, opp t}, defect opp t); (4) leftover targets: CP-SAT over their defect<=1
triples (a3_triples.pkl) where planes already used by blocks are free, minimising new planes + new defect lines.
Writes a3_choice_pack.pkl in the a3_choice format.  usage: python3 a3_pack.py [TL]"""
import sys, os, pickle, collections, itertools, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lmid'))
import lw
from lw import V, g, bits, nondegenerate
from fastcl import fclosure
from ortools.sat.python import cp_model
HYP = g.HYP; G = g.G; pc = lambda m: bin(m).count('1')
TL = float(sys.argv[1]) if len(sys.argv) > 1 else 300
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
def pm(m):
    r = (1 << V) - 1
    for s in bits(m): r &= HYP[s]
    return r
# A2 triangles
tri = set()
for a in range(V):
    for b in range(a + 1, V):
        if abs(int(G[a][b])) == 1:
            Q = fclosure((1 << a) | (1 << b))
            if pc(Q) == 3: tri.add(Q)
log('A2 triangles', len(tri))
A3 = set()
for Q in tri:
    for w in range(V):
        if Q >> w & 1: continue
        F = fclosure(Q | (1 << w))
        if pc(F) == 6 and F not in A3:
            L = bits(F)
            orth = [(a, b) for a, b in itertools.combinations(L, 2) if G[a][b] == 0]
            tris = [m for m in (fclosure((1 << a) | (1 << b)) for a, b in itertools.combinations(L, 2) if G[a][b] != 0) if pc(m) == 3]
            if len(orth) == 3 and len(set(tris)) == 4 and nondegenerate(F): A3.add(F)
A3 = sorted(A3)
log('A3 subsystems', len(A3))
M = cp_model.CpModel(); xb = [M.NewBoolVar('') for _ in A3]
for u in range(V): M.Add(sum(xb[i] for i, F in enumerate(A3) if F >> u & 1) <= 1)
M.Maximize(sum(xb))
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = 4
st = sv.Solve(M)
blocks = [A3[i] for i in range(len(A3)) if sv.Value(xb[i])]
log('packing', sv.StatusName(st), '| blocks', len(blocks), '| bound', sv.BestObjectiveBound(), '| lines covered', 6 * len(blocks))
choice = {}
for F in blocks:
    L = bits(F)
    for t in L:
        opp = next(u for u in L if u != t and G[t][u] == 0)
        tq = [m for m in set(fclosure((1 << t) | (1 << u)) for u in L if u != t and G[t][u] != 0) if pc(m) == 3]
        assert len(tq) == 2
        pair = fclosure((1 << t) | (1 << opp))
        tot = pm(tq[0]) ^ pm(tq[1]) ^ pm(pair) ^ (1 << opp)
        assert tot == HYP[t], ('A3 identity fails', t)
        choice[t] = (tq[0], tq[1], pair, opp)
usedQ = {Q for c in choice.values() for Q in c[:3]}; usedD = {c[3] for c in choice.values()}
left = [t for t in range(V) if t not in choice]
log('block targets', len(choice), '| leftover', len(left), 'by kind', dict(collections.Counter(g.kind[t] for t in left)))
TR = pickle.load(open('a3_triples.pkl', 'rb'))
M = cp_model.CpModel(); yv = {}; dvv = {}; X = {}
def yq(Q):
    if Q not in yv: yv[Q] = M.NewBoolVar('')
    return yv[Q]
def dd(d):
    if d not in dvv: dvv[d] = M.NewBoolVar('')
    return dvv[d]
for t in left:
    xs = []
    for k, (a, b, c, d) in enumerate(TR[t]):
        x = M.NewBoolVar(''); X[(t, k)] = x; xs.append(x)
        for Q in (a, b, c):
            if Q not in usedQ: M.AddImplication(x, yq(Q))
        if d >= 0 and d not in usedD: M.AddImplication(x, dd(d))
    M.AddExactlyOne(xs)
M.Minimize(sum(yv.values()) + sum(dvv.values()))
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = 4
st = sv.Solve(M)
for t in left:
    k = next(k for k in range(len(TR[t])) if sv.Value(X[(t, k)]))
    choice[t] = TR[t][k]
used = {Q for c in choice.values() for Q in c[:3]}
users = collections.Counter(Q for c in choice.values() for Q in c[:3])
log('leftover selection', sv.StatusName(st), '| total distinct planes', len(used), '| defects', len({c[3] for c in choice.values() if c[3] >= 0}),
    '| users per section', dict(collections.Counter(users.values())))
pickle.dump(choice, open('a3_choice_pack.pkl', 'wb'))

"""Evaluate an identical-parts design (lr8identical.py output): independent check that for every line t the parts W_F of
its 4 nodes partition R(t); node cost with copies: a node whose shared part W_F needs m_F rank-<=5 pieces costs
m_F - 1 assembly leftovers if it has a delivered user, m_F if all its users read it in-chain (in-chain node chosen by
CP-SAT to minimise the total).  m_F: upper bound kappa5(W_F) (cover by rank-5 closed sets, exact CP-SAT),
lower bound ceil(rank(W_F)/5).  R = 440 + total.  usage: lr8identeval.py sol.json"""
import sys, json, collections
from lgeo import *
from lclosed import closed_sets, kappa
from ortools.sat.python import cp_model
sol = json.load(open(sys.argv[1]))
rot = [img_line(s, [(i + 1) % n for i in range(n)]) for s in range(V)]
rotp = [list(range(V))]
for k in range(1, n): rotp.append([rot[x] for x in rotp[-1]])
def rotm(m, k):
    r = 0
    for s in bits(m): r |= 1 << rotp[k % n][s]
    return r
orb = {}; reps = []
for s in range(V):
    if s in orb: continue
    reps.append(s); x = s
    for k in range(n): orb[x] = (len(reps) - 1, k); x = rot[x]
Wc = {int(k, 16): int(v, 16) for k, v in sol['W'].items()}
def fkey(F):
    best = None
    for k in range(n):
        Fc = rotm(F, -k)
        if best is None or Fc < best[0]: best = (Fc, k)
    return best
def Wof(F):
    Fc, k = fkey(F); return rotm(Wc.get(Fc, 0), k)
nodes_of = {}; users = collections.defaultdict(list)
for t in range(V):
    o, k = orb[t]
    secs = [rotm(int(h, 16), k) for h in sol['covers'][str(reps[o])]]
    tot = 0
    for F in secs:
        w = Wof(F); assert w & ~pm(F) == 0, 'part outside node perp'
        assert tot & w == 0, 'parts overlap'; tot |= w
        users[F].append(t)
    assert tot == HYP[t], 'parts do not partition R(t)'
    nodes_of[t] = secs
print('CHECK OK: every line R(t) = disjoint union of its 4 node parts;', len(users), 'nodes')
hist = collections.Counter(len(u) for u in users.values()); print('users per node', sorted(hist.items()))
mF = {}; mlo = {}; done = {}
for F in users:
    W = Wof(F); key = fkey(F)[0]
    if key not in done:
        r = rank(W)
        if r <= 5: done[key] = (1, 1, r)
        else:
            # greedy partition into rank-<=5 pieces (best of several line orders) as the upper bound
            import random as _r
            best = 99; Wl = bits(W)
            for trial in range(30):
                _r.seed(trial); order = Wl[:]; _r.shuffle(order); rem = list(order); cnt = 0
                while rem:
                    S = 0; nxt = []
                    for u in rem:
                        if rank(S | (1 << u)) <= 5: S |= 1 << u
                        else: nxt.append(u)
                    rem = nxt; cnt += 1
                best = min(best, cnt)
            done[key] = (best, -(-r // 5), r)
    mF[F], mlo[F], _ = done[key]
print('node part rank histogram', sorted(collections.Counter(done[fkey(F)[0]][2] for F in users).items()))
print('m_F (kappa5 upper) histogram', sorted(collections.Counter(mF.values()).items()))
# in-chain choice
M = cp_model.CpModel(); ic = {}
for t in range(V):
    ls = [M.NewBoolVar('') for _ in nodes_of[t]]; M.AddExactlyOne(ls)
    for F, l in zip(nodes_of[t], ls): ic[(t, F)] = l
cost = []
for F, us in users.items():
    alln = M.NewBoolVar('')       # all users in-chain
    M.Add(sum(ic[(t, F)] for t in us) == len(us)).OnlyEnforceIf(alln)
    M.Add(sum(ic[(t, F)] for t in us) <= len(us) - 1).OnlyEnforceIf(alln.Not())
    cost.append((mF[F] - 1) + alln)
M.Minimize(sum(cost)); sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = 60; sv.parameters.num_workers = 4
st = sv.Solve(M)
tot = int(sv.ObjectiveValue()); lo = sum(mlo[F] - 1 for F in users)
print('in-chain choice', sv.StatusName(st), '| leftover registers (upper, kappa5) %d  -> R <= %d ;  lower bound from ranks %d -> R >= %d' % (tot, 440 + tot, lo, 440 + lo))

"""PG(2,3)-based good-frame partition of I_{13,1} and the cell-sharing set-cover relaxation (E8: exactly 3/line).
Blocks: lines L_k = {k,k+1,k+3,k+9} mod 13 of PG(2,3), apex p_k = k + c; block = {P(ij), T(ij p_k)}: 3 PPTT frames
(one per perfect matching of L_k).  Remaining T lines tiled by TTTT (Pasch) good frames (CP-SAT exact cover).
Demands per frame f: Q = lines orthogonal to all of f; 6 E-sets (lines orthogonal to x, y and to neither other member).
Per line u: min #partners v (+ singles) so that every demand containing u contains a chosen partner (CP-SAT)."""
import sys, itertools, pickle, collections, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
from ortools.sat.python import cp_model
g = Geom(13); V = g.V; G = g.G
idx = {(g.kind[i], g.supp[i]): i for i in range(V)}
P = lambda a, b: idx[('P', tuple(sorted((a % 13, b % 13))))]
T = lambda a, b, c: idx[('T', tuple(sorted((a % 13, b % 13, c % 13))))]
D = [0, 1, 3, 9]
best = None
for c in range(13):
    if c in D: continue
    Ts = [T(k + d1, k + d2, k + c) for k in range(13) for d1, d2 in itertools.combinations(D, 2)]
    if len(set(Ts)) == 78: best = c; break
print('apex offset c =', best)
c = best
pptt = []
for k in range(13):
    W = [(k + d) % 13 for d in D]; p = (k + c) % 13
    for (a, b), (cc, d) in [((W[0], W[1]), (W[2], W[3])), ((W[0], W[2]), (W[1], W[3])), ((W[0], W[3]), (W[1], W[2]))]:
        pptt.append((P(a, b), P(cc, d), T(a, b, p), T(cc, d, p)))
used = set(l for f in pptt for l in f)
assert len(used) == 156
orth = (G == 0); np.fill_diagonal(orth, False)
OM = [sum(1 << j for j in range(V) if orth[i, j]) for i in range(V)]
def good(q):
    for t in q:
        es = [e for e in q if e != t]
        R = OM[t] & ~sum(1 << e for e in es); a, b, cc = (OM[e] for e in es)
        if R & ~(a ^ b ^ cc): return False
    return all(orth[x, y] for x, y in itertools.combinations(q, 2))
assert all(good(f) for f in pptt), 'PPTT block frames not good'
rest = [l for l in range(V) if l not in used]
print('PPTT frames', len(pptt), 'remaining T lines', len(rest))
frames, comp_lists, kinds = pickle.load(open('compat13.pkl', 'rb'))
restset = set(rest)
cand = [tuple(q) for q, k in zip(frames, kinds) if k == 'TTTT' and set(q) <= restset]
print('TTTT candidates inside remaining lines', len(cand))
def shiftl(l, k):
    return idx[(g.kind[l], tuple(sorted((p + k) % 13 for p in g.supp[l])))]
candset = {q: i for i, q in enumerate(cand)}
orbit_of = {}
for i, q in enumerate(cand):
    orb = tuple(sorted(candset[tuple(sorted(shiftl(l, k) for l in q))] for k in range(13)))
    orbit_of[i] = orb
orbits = sorted(set(orbit_of.values()))
print('TTTT candidate orbits', len(orbits))
m = cp_model.CpModel(); y = {o: m.NewBoolVar('o%d' % n) for n, o in enumerate(orbits)}
x = [None] * len(cand)
for i in range(len(cand)): x[i] = y[orbit_of[i]]
for l in rest: m.Add(sum(y[o] * sum(1 for i in o if l in cand[i]) for o in orbits if any(l in cand[i] for i in o)) == 1)
s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 600; s.parameters.num_workers = 2
st = s.Solve(m); print('Pasch tiling of remaining T lines:', s.StatusName(st))
if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE): sys.exit()
tttt = sorted(set(cand[i] for o in orbits if s.Value(y[o]) for i in o))
part = pptt + tttt
assert sorted(l for f in part for l in f) == list(range(V))
pickle.dump(part, open('pg23_partition.pkl', 'wb'))
# demands
dem = set()
for f in part:
    U = 0
    for u in f: U |= 1 << u
    Q = OM[f[0]] & OM[f[1]] & OM[f[2]] & OM[f[3]]
    dem.add(Q)
    for a, b in itertools.combinations(range(4), 2):
        o = [z for z in range(4) if z not in (a, b)]
        dem.add(OM[f[a]] & OM[f[b]] & ~OM[f[o[0]]] & ~OM[f[o[1]]])
dem = [d for d in dem if d]
print('demands', len(dem), 'sizes', sorted(collections.Counter(bin(d).count('1') for d in dem).items()))
mem = collections.defaultdict(set)
for i, d in enumerate(dem):
    for u in range(V):
        if d >> u & 1: mem[u].add(i)
def lorbit(u):
    return min(shiftl(u, k) for k in range(13))
reps = sorted(set(lorbit(u) for u in range(V)))
print('line orbits', len(reps))
res = []; resd = {}
for u in reps:
    Du = sorted(mem[u])
    if not Du: res.append(0); continue
    mm = cp_model.CpModel()
    xv = {v: mm.NewBoolVar('v%d' % v) for v in range(V) if v != u and mem[u] & mem[v]}
    sv = {d: mm.NewBoolVar('s%d' % d) for d in Du}
    for d in Du: mm.Add(sum(xv[v] for v in xv if d in mem[v]) + sv[d] >= 1)
    mm.Minimize(sum(xv.values()) + sum(sv.values()))
    ss = cp_model.CpSolver(); ss.parameters.num_workers = 3; ss.parameters.max_time_in_seconds = 300
    st2 = ss.Solve(mm); res.append(int(ss.ObjectiveValue())); resd[u] = (int(ss.ObjectiveValue()), int(ss.BestObjectiveBound()), ss.StatusName(st2))
    print('  orbit rep', g.kind[u], g.supp[u], 'cost', resd[u], flush=True)
w = {u: sum(1 for v in range(V) if lorbit(v) == u) for u in reps}
print('I13 PG(2,3) Z13 partition set-cover parts per line: weighted mean %.2f (lower bounds mean %.2f) min %d max %d' % (sum(resd[u][0]*w[u] for u in reps)/V, sum(resd[u][1]*w[u] for u in reps)/V, min(res), max(res)))

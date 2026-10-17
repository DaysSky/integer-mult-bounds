"""Aligned good-frame partitions of I_{13,1} invariant under Z13 (i -> i+1 mod 13).
Frames: PPTT {P(ab),P(cd),T(abx),T(cdx)} and TTTT Pasch {T(abc),T(ade),T(bdf),T(cef)}.  Compatible(i,j): disjoint and
for every cell (pair of members) of each frame, the other frame meets its E-set evenly; E-set of cell (a,b) of frame
F = lines orthogonal to F_a and F_b and to neither of the other two members.
Search: 7 frame orbits (each covering 4 distinct line orbits) forming an exact cover of the 28 line orbits, pairwise
(and self-) compatible.  CP-SAT."""
import sys, itertools, collections, numpy as np, pickle, time
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
n = 13
g = Geom(n); V = g.V; G = g.G
idx = {(g.kind[i], g.supp[i]): i for i in range(V)}
orth = (G == 0); np.fill_diagonal(orth, False)
OM = [sum(1 << j for j in range(V) if orth[i, j]) for i in range(V)]
def P(a, b): return idx[('P', tuple(sorted((a, b))))]
def T(a, b, c): return idx[('T', tuple(sorted((a, b, c))))]
def shift_line(l, k):
    kind, s = g.kind[l], g.supp[l]
    return idx[(kind, tuple(sorted((p + k) % n for p in s)))]
# enumerate good frames
frames = set()
pts = range(n)
for x in pts:
    others = [p for p in pts if p != x]
    for (a, b), (c, d) in itertools.combinations(itertools.combinations(others, 2), 2):
        if len({a, b, c, d}) < 4: continue
        frames.add(tuple(sorted((P(a, b), P(c, d), T(a, b, x), T(c, d, x)))))
for S6 in itertools.combinations(pts, 6):
    # Pasch configurations on S6: 4 triples pairwise meeting in exactly one point, covering each point twice
    trip = list(itertools.combinations(S6, 3))
    for q in itertools.combinations(trip, 4):
        if all(len(set(u) & set(w)) == 1 for u, w in itertools.combinations(q, 2)):
            frames.add(tuple(sorted(T(*u) for u in q)))
frames = sorted(frames)
print('good frames', len(frames), flush=True)
# verify goodness quickly on a sample
def good_for(t, es):
    R = OM[t] & ~sum(1 << e for e in es)
    a, b, c = (OM[e] for e in es)
    return (R & ~(a ^ b ^ c)) == 0
import random
for q in random.sample(frames, 200):
    assert all(good_for(t, [e for e in q if e != t]) for t in q), q
# E-set signature per frame: list of 6 bitmasks
pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
def esets(q):
    out = []
    for a, b in pairs:
        o = [c for c in range(4) if c not in (a, b)]
        E = OM[q[a]] & OM[q[b]] & ~OM[q[o[0]]] & ~OM[q[o[1]]]
        out.append(E)
    return out
def compat(q1, e1, q2, e2):
    if set(q1) & set(q2): return False
    m2 = sum(1 << x for x in q2); m1 = sum(1 << x for x in q1)
    return all(bin(E & m2).count('1') % 2 == 0 for E in e1) and all(bin(E & m1).count('1') % 2 == 0 for E in e2)
# line orbits
lorb = {}
for l in range(V):
    if l in lorb: continue
    for k in range(n): lorb[shift_line(l, k)] = len(set(lorb.values())) if False else None
lid = {}; cur = 0
for l in range(V):
    if l in lid: continue
    for k in range(n): lid[shift_line(l, k)] = cur
    cur += 1
print('line orbits', cur, flush=True)
# frame orbits
fset = set(frames); forb = []; seen = set()
for q in frames:
    if q in seen: continue
    orbit = [tuple(sorted(shift_line(l, k) for l in q)) for k in range(n)]
    for o in orbit: seen.add(o)
    forb.append(orbit)
print('frame orbits', len(forb), flush=True)
# candidates: 4 distinct line orbits and self-compatible
cand = []
for orbit in forb:
    q = orbit[0]
    if len({lid[l] for l in q}) < 4: continue
    e0 = esets(q)
    if all(compat(q, e0, o, esets(o)) for o in orbit[1:]):
        cand.append(orbit)
print('self-compatible candidate orbits', len(cand), collections.Counter(''.join(sorted(g.kind[l] for l in o[0])) for o in cand), flush=True)
pickle.dump((frames, cand), open('align13_cand.pkl', 'wb'))
# pairwise orbit compatibility
t0 = time.time()
E0 = [esets(o[0]) for o in cand]
Eall = [[esets(q) for q in o] for o in cand]
nc = len(cand)
comp = np.zeros((nc, nc), dtype=bool)
cover = [frozenset(lid[l] for l in o[0]) for o in cand]
for i in range(nc):
    for j in range(i + 1, nc):
        if cover[i] & cover[j]: continue
        q1 = cand[i][0]
        ok = all(compat(q1, E0[i], cand[j][k], Eall[j][k]) for k in range(n))
        comp[i, j] = comp[j, i] = ok
    if i % 200 == 0: print('compat row', i, '%.0fs' % (time.time() - t0), flush=True)
print('compatible orbit pairs', int(comp.sum()) // 2, flush=True)
pickle.dump((cand, comp, cover), open('align13_comp.pkl', 'wb'))
# exact cover search with CP-SAT
from ortools.sat.python import cp_model
m = cp_model.CpModel(); x = [m.NewBoolVar('x%d' % i) for i in range(nc)]
for lo in range(cur):
    m.AddExactlyOne([x[i] for i in range(nc) if lo in cover[i]])
for i in range(nc):
    for j in range(i + 1, nc):
        if not comp[i, j] and not (cover[i] & cover[j]):
            m.AddBoolOr([x[i].Not(), x[j].Not()])
s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 3000; s.parameters.num_workers = 4
st = s.Solve(m)
print('status', s.StatusName(st))
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    sol = [i for i in range(nc) if s.Value(x[i])]
    print('ALIGNED Z13 PARTITION FOUND:', [(''.join(sorted(g.kind[l] for l in cand[i][0])), [g.supp[l] for l in cand[i][0]]) for i in sol])
    pickle.dump([cand[i] for i in sol], open('align13_solution.pkl', 'wb'))

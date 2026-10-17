"""Cyclic apex offsets c (p_k = k + c): 13 complete PPTT blocks on PG(2,3) lines, then tile the remaining T lines
by complete Pasch pairs.  First a Z13-invariant tiling (orbits of pairs), then an unrestricted CP-SAT."""
from part13 import *
import collections, sys
from ortools.sat.python import cp_model
frames, per_frame, cnt = pickle.load(open('halfshare.pkl', 'rb'))
byhalf = collections.defaultdict(list)
for i, hs in enumerate(per_frame):
    for hh in hs: byhalf[hh].append(i)
pairs = set()
for i, f in enumerate(frames):
    if g.kind[f[0]] == 'T' and g.kind[f[1]] == 'T':
        c = collections.Counter(j for hh in per_frame[i] for j in byhalf[hh] if j != i)
        pairs.add(tuple(sorted((i, [j for j, k in c.items() if k == len(per_frame[i])][0]))))
pairs = sorted(pairs); pp = [frozenset(set(frames[i]) | set(frames[j])) for i, j in pairs]
ppidx = {p: k for k, p in enumerate(pp)}
shift = lambda l: g.T(*[(x + 1) % 13 for x in g.supp[l]])
def rot(p): return frozenset(shift(l) for l in p)
Ls = [sorted(((k + d) % 13) for d in (0, 1, 3, 9)) for k in range(13)]
TL = int(sys.argv[1]) if len(sys.argv) > 1 else 300
for c in range(13):
    if c in (0, 1, 3, 9): continue
    blk = set()
    for k in range(13):
        for x, y in itertools.combinations(Ls[k], 2): blk.add(g.T(x, y, (k + c) % 13))
    if len(blk) != 78: print('c', c, 'T collision'); continue
    rest = set(range(78, V)) - blk
    cand = [k for k, p in enumerate(pp) if p <= rest]
    # Z13 orbits of candidate pairs
    orbs = {}; 
    for k in cand:
        o = [pp[k]]
        for _ in range(12): o.append(rot(o[-1]))
        key = min(sorted(map(sorted, o)))
        orbs.setdefault(tuple(key), set(ppidx[q] for q in o))
    ol = list(orbs.values())
    m = cp_model.CpModel(); y = [m.NewBoolVar('o%d' % i) for i in range(len(ol))]
    for l in rest: m.Add(sum(y[i] * sum(1 for q in ol[i] if l in pp[q]) for i in range(len(ol))) == 1)
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 60; s.parameters.num_workers = 4
    st = s.Solve(m); print('c', c, 'cand pairs', len(cand), 'orbits', len(ol), 'Z13-invariant tiling:', s.StatusName(st), flush=True)
    sel = None
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        sel = sorted(q for i in range(len(ol)) if s.Value(y[i]) for q in ol[i])
    else:
        m = cp_model.CpModel(); x = {k: m.NewBoolVar('p%d' % k) for k in cand}
        for l in rest: m.AddExactlyOne([x[k] for k in cand if l in pp[k]])
        s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = TL; s.parameters.num_workers = 4
        st = s.Solve(m); print('c', c, 'unrestricted tiling:', s.StatusName(st), flush=True)
        if st in (cp_model.OPTIMAL, cp_model.FEASIBLE): sel = [k for k in cand if s.Value(x[k])]
    if sel:
        newpart = []
        for k in range(13):
            W = Ls[k]; p = (k + c) % 13
            for (u, w), (yy, z) in [((W[0], W[1]), (W[2], W[3])), ((W[0], W[2]), (W[1], W[3])), ((W[0], W[3]), (W[1], W[2]))]:
                newpart.append((g.P(u, w), g.P(yy, z), g.T(u, w, p), g.T(yy, z, p)))
        for k in sel: newpart += [frames[pairs[k][0]], frames[pairs[k][1]]]
        assert sorted(l for f in newpart for l in f) == list(range(V))
        pickle.dump(newpart, open('pgpasch_c%d.pkl' % c, 'wb')); print('c', c, 'SAVED', len(newpart), 'frames', flush=True)

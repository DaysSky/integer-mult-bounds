"""PG(2,3) good-frame partition of I_{13,1} (39 PPTT block frames + Pasch TTTT tiling), demands (Q, E-sets) with frames."""
import itertools, pickle, collections, os
from geo13 import *
from ortools.sat.python import cp_model
idx = g.idx
P = lambda a, b: idx[('P', tuple(sorted((a % 13, b % 13))))]
T = lambda a, b, c: idx[('T', tuple(sorted((a % 13, b % 13, c % 13))))]
D = [0, 1, 3, 9]
OM = HYP
def good(q):
    for t in q:
        es = [e for e in q if e != t]
        R = OM[t] & ~sum(1 << e for e in es); a, b, cc = (OM[e] for e in es)
        if R & ~(a ^ b ^ cc): return False
    return all(G[x, y] == 0 for x, y in itertools.combinations(q, 2))
def build():
    for c in range(13):
        if c in D: continue
        Ts = [T(k + d1, k + d2, k + c) for k in range(13) for d1, d2 in itertools.combinations(D, 2)]
        if len(set(Ts)) == 78: break
    pptt = []
    for k in range(13):
        W = [(k + d) % 13 for d in D]; p = (k + c) % 13
        for (a, b), (cc, d) in [((W[0], W[1]), (W[2], W[3])), ((W[0], W[2]), (W[1], W[3])), ((W[0], W[3]), (W[1], W[2]))]:
            pptt.append((P(a, b), P(cc, d), T(a, b, p), T(cc, d, p)))
    assert all(good(f) for f in pptt)
    used = set(l for f in pptt for l in f); rest = [l for l in range(V) if l not in used]
    rs = set(rest)
    # Pasch frames among remaining T lines: 4 triples on 6 points, pairwise meeting in exactly one point
    cand = []
    Tl = [l for l in rest]
    sup = {l: set(g.supp[l]) for l in Tl}
    for a, b in itertools.combinations(Tl, 2):
        if len(sup[a] & sup[b]) != 1: continue
    # enumerate via 6-point sets: Pasch = complement structure of K4 on 4 'lines'
    for S6 in itertools.combinations(range(13), 6):
        trs = [l for l in Tl if sup[l] <= set(S6)]
        for q in itertools.combinations(trs, 4):
            if all(len(sup[x] & sup[y]) == 1 for x, y in itertools.combinations(q, 2)) and good(q): cand.append(q)
    cand = sorted(set(tuple(sorted(q)) for q in cand))
    m = cp_model.CpModel(); x = [m.NewBoolVar('x%d' % i) for i in range(len(cand))]
    for l in rest: m.AddExactlyOne([x[i] for i, q in enumerate(cand) if l in q])
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 600; s.parameters.num_workers = 4
    st = s.Solve(m); assert st in (cp_model.OPTIMAL, cp_model.FEASIBLE), s.StatusName(st)
    tttt = [cand[i] for i in range(len(cand)) if s.Value(x[i])]
    part = pptt + tttt
    assert sorted(l for f in part for l in f) == list(range(V))
    return part
F = 'pg23_partition.pkl'
if os.path.exists(F): part = pickle.load(open(F, 'rb'))
else: part = build(); pickle.dump(part, open(F, 'wb'))
# demands: Q (frame pm(Phi)), E_te (frame pm(t,e))
DEM = []   # (kind, frame-mask-of-lines (closed), lines-mask, frame-index, users)
for fi, f in enumerate(part):
    Q = OM[f[0]] & OM[f[1]] & OM[f[2]] & OM[f[3]]
    DEM.append(('Q', Q, Q, fi, f))
    for a, b in itertools.combinations(range(4), 2):
        o = [z for z in range(4) if z not in (a, b)]
        E = OM[f[a]] & OM[f[b]] & ~OM[f[o[0]]] & ~OM[f[o[1]]]
        DEM.append(('E', OM[f[a]] & OM[f[b]], E, fi, (f[a], f[b])))
if __name__ == '__main__':
    print('frames', len(part), collections.Counter(''.join(sorted(g.kind[x] for x in f)) for f in part))
    print('demands', len(DEM), 'distinct contents', len(set(d[2] for d in DEM)))
    print('sizes', sorted(collections.Counter((d[0], pc(d[2]), pc(d[1])) for d in DEM).items()))
    load = collections.Counter()
    for d in set(dd[2] for dd in DEM):
        for u in bits(d): load[u] += 1
    print('load per line mean %.1f' % (sum(load.values()) / V), 'P', sum(load[u] for u in range(78)) / 78, 'T', sum(load[u] for u in range(78, V)) / 286)

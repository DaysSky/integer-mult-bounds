"""Exact: does I_{13,1} have a block-closed good-frame partition (full D4 blocks for PPTT frames, Pasch-pair blocks for
TTTT frames)?  Full PPTT blocks force the 13 lines of PG(2,3) (unique S(2,4,13), WLOG fixed); apexes free (p_L not on
L).  CP-SAT exact cover of all 286 T lines.  Also variant: TTTT frames free (single Pasch frames)."""
import sys, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
from ortools.sat.python import cp_model
g = Geom(13); V = g.V
def T(*a): return g.idx[('T', tuple(sorted(x % 13 for x in a)))]
D = [0, 1, 3, 9]
Ls = [sorted((k + d) % 13 for d in D) for k in range(13)]
assert len({frozenset(itertools.combinations(L, 2)) for L in Ls}) == 13
blocks = []
for li, L in enumerate(Ls):
    for p in range(13):
        if p in L: continue
        blocks.append((li, p, [T(a, b, p) for a, b in itertools.combinations(L, 2)]))
pp = set(); pasch = set()
for S in itertools.combinations(range(13), 6):
    for perm in itertools.permutations(S):
        a, b, c, d, e, f = perm
        if a != S[0]: break
        P1 = frozenset([T(a, b, c), T(a, d, e), T(b, d, f), T(c, e, f)])
        P2 = frozenset(T(*[x for x in S if x not in g.supp[t]]) for t in P1)
        pp.add(frozenset([P1, P2])); pasch.add(P1); pasch.add(P2)
pp = [sorted(set(p[0]) | set(p[1])) for p in map(list, pp)]
pasch = [sorted(q) for q in pasch]
print('PPTT blocks', len(blocks), 'Pasch pairs', len(pp), 'Pasch frames', len(pasch), flush=True)
Tl = [l for l in range(V) if g.kind[l] == 'T']
for name, units in (('Pasch-pair blocks', pp), ('free Pasch frames', pasch)):
    m = cp_model.CpModel()
    xb = [m.NewBoolVar('') for _ in blocks]; xu = [m.NewBoolVar('') for _ in units]
    for li in range(13): m.AddExactlyOne([xb[i] for i, b in enumerate(blocks) if b[0] == li])
    byl = collections.defaultdict(list)
    for i, b in enumerate(blocks):
        for l in b[2]: byl[l].append(xb[i])
    for i, q in enumerate(units):
        for l in q: byl[l].append(xu[i])
    for l in Tl: m.AddExactlyOne(byl[l])
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 1200; s.parameters.num_workers = 2
    st = s.Solve(m)
    print('%s: %s (%.0fs)' % (name, s.StatusName(st), s.WallTime()), flush=True)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print('  apexes', [(blocks[i][0], blocks[i][1]) for i in range(len(blocks)) if s.Value(xb[i])])

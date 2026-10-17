import itertools, numpy as np
from e8geo import e8_roots
from ortools.sat.python import cp_model
L = e8_roots()
# enumerate E8 lattice vectors (doubled coords) with norm <= NMAX (true norm = sum/4)
NMAX = 16
vecs = set()
rng = range(-4, 5)
# integer type: all coords even (doubled), sum of halves even
for c in itertools.product(range(-2, 3), repeat=8):
    if sum(c) % 2 == 0 and sum(x*x for x in c) <= NMAX:
        vecs.add(tuple(2*x for x in c))
for c in itertools.product((-3, -1, 1, 3), repeat=8):
    if sum(x*x for x in c)/4 <= NMAX and (sum(c)//2) % 2 == 0 and sum(c) % 4 == 0:
        vecs.add(tuple(c))
vecs.discard((0,)*8)
sets = {}
for z in vecs:
    s = frozenset(np.nonzero(L @ np.array(z) == 0)[0].tolist())
    if len(s) >= 20: sets[s] = z
# keep maximal
S = sorted(sets, key=len, reverse=True)
maxi = [s for s in S if not any(s < t for t in S if len(t) > len(s))]
from collections import Counter
print('candidate perps', len(sets), 'maximal', len(maxi), Counter(len(s) for s in maxi))
for k in (3, 4, 5):
    m = cp_model.CpModel(); x = [m.NewBoolVar('') for _ in maxi]
    for l in range(120): m.Add(sum(x[i] for i, s in enumerate(maxi) if l in s) >= 1)
    m.Add(sum(x) <= k)
    sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = 120; sv.parameters.num_workers = 4
    r = sv.Solve(m)
    print('cover with', k, ':', sv.StatusName(r))
    if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        ch = [i for i in range(len(maxi)) if sv.Value(x[i])]
        print('  sizes', [len(maxi[i]) for i in ch], 'z', [sets[maxi[i]] for i in ch]); break

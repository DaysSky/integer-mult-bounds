"""THE ROLE-ASSIGNMENT SOLVER (ii19_nat39.py) — the running-sum ladder's full feasibility.

THE ROLES (exclusive per source!!): 1st (the singleton reads: any number, FREE!!) | 2nd (ONE
cell-partner a: all its 2nd-pieces share the pair (a, b)!!) | 3rd (NO cell: its rung F(c) =
span(c + its 3rd-pieces' pairs), ⊆ ∩perp(its readers) AUTOMATICALLY (the ⊥-closure!!)).
PER PIECE {x,y,z}: one 1st (a), one 2nd (b: the cell span{a,b}), one 3rd (c: the gate-3 at
F(c) ⊇ span{a,b} + c); the piece's chain: 0 -> singleton(a) -> cell(a,b) -> F(c) -> the read
groups (dims 5-8!!).
THE CARRIERS: the same ladder pattern over the leftover lines (the carrier's chain: 0 ->
singleton -> cell -> F-rungs -> perp(t)!!) — the 3rd-role sources' F-rungs must be ⊆ perp(t)
for the carriers too (the reader-intersection constraint!!).
OUTPUT: the assignment (or the failures) + the leftovers + the honest R + the feasibility map.
"""
import os, sys, itertools, json
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
sys.argv = ['ii19_nat20.py']
exec(open('ii19_nat20.py').read().split('# (1) chain-shape census')[0])
V, H = V, H
log = lambda *a: print(*a, file=sys.stderr, flush=True)

G4 = [[sum(w['lines'][s][i] * w['form']['num'][i][j] * w['lines'][t][j]
            for i in range(H) for j in range(H) if w['form']['num'][i][j]) for t in range(V)] for s in range(V)]
PERP = [set(s for s in range(V) if s != t and G4[s][t] == 0) for t in range(V)]

def greedy(kmin, umin):
    pair_count = Counter(); pair_users = defaultdict(list)
    for ti, pl in enumerate(PERP):
        for a, b in itertools.combinations(sorted(pl), 2):
            pair_count[(a, b)] += 1; pair_users[(a, b)].append(ti)
    covered = [set() for _ in range(V)]
    pool = []; pool_users = []
    while True:
        cands = []
        for (a, b), c in pair_count.items():
            if c < 2: continue
            users = [ti for ti in pair_users[(a, b)] if a not in covered[ti] and b not in covered[ti]]
            if len(users) < umin: continue
            common = None
            for ti in users:
                unc = PERP[ti] - covered[ti]
                common = unc if common is None else (common & unc)
            if common is None or len(common) < kmin: continue
            piece = frozenset(sorted(common)[:kmin])
            real = [ti for ti in users if piece <= PERP[ti] - covered[ti]]
            if len(real) < umin: continue
            saving = len(piece) * len(real) - (len(piece) + len(real))
            if saving <= 0: continue
            cands.append((saving, piece, real))
        if not cands: break
        cands.sort(key=lambda c: c[0], reverse=True)
        for saving, piece, real in cands[:50]:
            if any(piece <= PERP[ti] - covered[ti] for ti in real):
                pool.append(piece); pool_users.append(real)
                for ti in real: covered[ti] |= set(piece)
                break
        else: break
    return pool, pool_users, [PERP[ti] - covered[ti] for ti in range(V)]

pool, pool_users, leftovers = greedy(3, 4)
log('the (3,4) economy: %d pieces, %d carriers-worth leftovers' % (len(pool), sum(1 for lo in leftovers if lo)))

# ============ THE ROLE SOLVER ============
# per piece: try all 6 role-permutations; the constraints:
#  - the 2nd-source b: ONE partner globally (its cell): all b's 2nd-pieces share (a, b);
#  - the 3rd-source c: NO cell-role anywhere (c never a 2nd!!);
#  - the 1st-source a: no constraint (the singleton reads are free!!).
# greedy: process the pieces sorted by user-count (the most-shared first!!); on conflict: drop
# the piece to the leftover pool (the R-trade measured at the end!!).
role2 = {}             # b -> its partner a
role3 = set()          # the 3rd-role sources
drop = set()
order = sorted(range(len(pool)), key=lambda i: -len(pool_users[i]))
covered2 = [set() for _ in range(V)]
kept = []
for i in order:
    piece = sorted(pool[i])
    ok = False
    perms = list(itertools.permutations(piece))
    # prefer: b with an existing partner; c already a 3rd
    perms.sort(key=lambda p: (p[1] in role2 and role2[p[1]] == p[0], p[2] in role3), reverse=True)
    for a, b, c in perms:
        if b in role2 and role2[b] != a: continue
        if b in role3: continue               # a 3rd can never be a 2nd!!
        if c in role2: continue               # a 2nd can never be a 3rd!!
        role2[b] = a
        role3.add(c)
        kept.append((i, a, b, c))
        ok = True
        break
    if not ok:
        drop.add(i)
for i, a, b, c in kept:
    for ti in pool_users[i]: covered2[ti] |= set(pool[i])
left2 = [PERP[ti] - covered2[ti] for ti in range(V)]
nleft = sum(1 for lo in left2 if lo)
R = len(kept) + nleft + 9
log('THE ROLE ASSIGNMENT: %d/%d pieces kept | dropped %d' % (len(kept), len(pool), len(drop)))
log('  the 2nd-role sources: %d | the 3rd-role: %d | the 1st-only: %d' % (
    len(role2), len(role3), V - len(role2) - len(role3)))
log('  THE POST-SOLVER ECONOMY: %d pieces + %d carriers + 9 gathers = R %d (R/v %.2f)' % (
    len(kept), nleft, R, R / V))
# the c-rung feasibility: F(c) = span(c + its 3rd-pieces' pairs): the dim + the reader-intersection
LIN = np.array([[float(x) for x in l] for l in w['lines']])
thirds = defaultdict(list)
for i, a, b, c in kept:
    thirds[c].append((a, b))
bad_rung = 0
for c, pairs in thirds.items():
    lines = {c}
    for a, b in pairs: lines.add(a); lines.add(b)
    d = int(np.linalg.matrix_rank(LIN[sorted(lines)]))
    # the readers: the users of all c's pieces
    readers = set()
    for i, a2, b2, c2 in kept:
        if c2 == c: readers |= set(pool_users[i])
    inter = int(np.linalg.matrix_rank(LIN[sorted(readers)])) if readers else 0
    # the constraint: F(c) (dim d) C= the perps of all readers: the readers' span rank <= 9 - d
    if inter > H - d: bad_rung += 1
log('THE C-RUNG FEASIBILITY: the 3rd-sources %d | the BAD (the reader-span too big for the rung!!): %d' % (
    len(thirds), bad_rung))
hist = Counter()
for i, a, b, c in kept:
    hist[1] += 1                                  # the piece: 0 -> singleton(a)
    hist[1] += 1                                  # singleton -> cell(a,b)
    d = int(np.linalg.matrix_rank(LIN[sorted({c} | {x for p in thirds[c] for x in p})]))
    hist[max(1, d - 2)] += 1                       # cell -> F(c)
for t in range(V): hist[8] += 1                    # the targets
for lo in left2:
    if lo: hist[6] += 2                           # the carriers: build + read (rank ~6!!)
hist[8] += 8; hist[9] += 1                         # the copy
M = 9 * R + 73 + 1936
mass = sum(r * c2 for r, c2 in hist.items())
diff = M - mass
while diff > 0:
    r = 1 if diff % 2 or diff == 1 else 2
    hist[r] += 1; diff -= r
json.dump({'kept': [(i, a, b, c) for i, a, b, c in kept], 'pool': [sorted(p) for p in pool],
           'users': pool_users, 'left2': [sorted(lo) for lo in left2], 'role2': dict(role2)},
          open('ii19_nat39_assign.json', 'w'))
log('saved ii19_nat39_assign.json | the hist estimate %s (mass %d vs %d)' % (
    dict(sorted(hist.items())), sum(r * c2 for r, c2 in hist.items()), M))

"""THE RELAXED ROLE-SOLVER (ii19_nat43.py) — the dual-roles + the partner ⊥-budgets.

THE RELAXATION vs nat39: a source CAN be both a 2nd (with a cell) and a 3rd (no cell was
the old rule!!) WHEN its cell-partner is C= the perps of ALL the users of ALL its 3rd-pieces
(the partner-line C= the users (the C=perp budget!!)). THE PARTNERS: chosen AFTER the piece
assignment (the budget-aware!!). THE GOAL: keep >= 130/147 pieces -> the leftover loads
<= ~11/line -> the singleton-pieces' ceilings >= dim 2-4 (the machinery fits!!).
"""
import os, sys, itertools, json
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
sys.argv = ['ii19_nat20.py']
exec(open('ii19_nat20.py').read().split('# (1) chain-shape census')[0])
V, H = V, H
log = lambda *a: print(*a, file=sys.stderr, flush=True)
Linn = np.array([[float(x) for x in l] for l in w['lines']])

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

pool, pool_users, _ = greedy(3, 4)
log('the (3,4) economy: %d pieces' % len(pool))

# ============ THE RELAXED SOLVER ============
# per piece {x,y,z}: the roles (a=1st, b=2nd, c=3rd): NO exclusivity between 2nd/3rd!!
# the constraints (checked GLOBALLY at the end + incrementally where cheap!!):
#  - b's partner: ONE a globally (all b's 2nd-pieces share the pair!!)
#  - the partner-line a must be C= the perps of the users of b's 3rd-pieces (the budget!!)
#  - c's reads: at c's positions: c's OWN chain must serve (the partner of c (if c is also a
#    2nd!!) C= the users of c's 3rd-pieces!!!)
# GREEDY: the pieces by the user-count; the roles: prefer consistency; the conflict -> drop.
partner = {}              # b -> a
third_pieces = defaultdict(list)   # c -> [(i, users)]
kept = []
drop = []
order = sorted(range(len(pool)), key=lambda i: -len(pool_users[i]))
for i in order:
    piece = sorted(pool[i])
    ok = False
    for a, b, c in itertools.permutations(piece):
        if b in partner and partner[b] != a: continue
        # the budget: a (the partner-line) C= the perps of b's 3rd-pieces' users!!
        # (the existing 3rd-pieces of b: a C= their users!!)
        if any(a not in PERP[u] for j, us in third_pieces[b] for u in us): continue
        # symmetric: if a or c is a 2nd elsewhere, their partners C= THIS piece's users!!
        if a in partner and any(partner[a] not in PERP[u] for u in pool_users[i]): continue
        if c in partner and any(partner[c] not in PERP[u] for u in pool_users[i]): continue
        # the cell (a, b) on b's chain: also a's chain (a = the 1st here: no constraint!!)
        partner[b] = a
        third_pieces[c].append((i, pool_users[i]))
        kept.append((i, a, b, c))
        ok = True
        break
    if not ok:
        drop.append(i)
log('THE RELAXED SOLVER: kept %d/%d | dropped %d' % (len(kept), len(pool), len(drop)))
log('  the partners assigned: %d | the 3rd-sources: %d' % (len(partner), len(third_pieces)))
# the budget violations (the partner-line C=perp checks!!) — the global verification!!
viol = 0
for c, plist in third_pieces.items():
    if c in partner:
        p = partner[c]
        for j, us in plist:
            if any(p not in PERP[u] for u in us):
                viol += 1
log('  the partner-budget violations (the 3rd-sources with cells!!): %d' % viol)
# the coverage + the singleton-loads
covered2 = [set() for _ in range(V)]
for i, a, b, c in kept:
    for ti in pool_users[i]: covered2[ti] |= set(pool[i])
left2 = [PERP[ti] - covered2[ti] for ti in range(V)]
sing_users = defaultdict(set)
for t in range(V):
    for l in left2[t]: sing_users[l].add(t)
loads = Counter(len(u) for u in sing_users.values())
log('THE SINGLETON-LOADS after the relaxed solve: %s' % dict(sorted(loads.items())))
nleft = sum(1 for lo in left2 if lo)
log('THE ECONOMY: %d pieces + %d carriers + 9 = R %d' % (len(kept), nleft, len(kept) + nleft + 9))
# the singleton-pieces' ceilings: 9 - rank(the users!!)
ceil = Counter()
for l, us in sing_users.items():
    d = 9 - int(np.linalg.matrix_rank(Linn[sorted(us)]))
    ceil[d] += 1
log('THE SINGLETON CEILINGS (9 - rank(users)): %s (the frames at dims <= the ceiling!!)' % dict(sorted(ceil.items())))
json.dump({'kept': [(i, a, b, c) for i, a, b, c in kept], 'pool': [sorted(p) for p in pool],
           'users': pool_users, 'left2': [sorted(lo) for lo in left2], 'partner': partner},
          open('ii19_nat43_assign.json', 'w'))
log('saved ii19_nat43_assign.json')

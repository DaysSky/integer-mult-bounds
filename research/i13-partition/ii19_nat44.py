"""THE CHAIN-AWARE GREEDY (ii19_nat44.py) — the pieces born feasible!!

THE CONSTRAINTS AT BIRTH (all baked in!!):
- the pair (a, b): b = the 2nd (ONE partner globally!!), a = the 1st (free!!);
- the third c: from the common-set, with the budgets: if c is a 2nd elsewhere, its partner
  C= this piece's users; c's F-rung room: 9 - rank(ALL its 3rd-pieces' users) >= span{a,b,c}!!
- the user-cap: <= 21 (the span-3 group ceiling 6+5+4+3+2+1!!);
- the orientation matching: each source as the 2nd in <= 1 pair!!
OUTPUT: the feasible piece pool + the loads + the ceilings + the economy.
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
rank = lambda lines: int(np.linalg.matrix_rank(Linn[sorted(lines)])) if lines else 0

# ============ THE CHAIN-AWARE GREEDY ============
partner = {}                        # the 2nd-source b -> its partner a
third_users = defaultdict(set)      # the 3rd-source c -> ALL its 3rd-pieces' users
pairs_of = defaultdict(list)         # the 3rd-source c -> its pieces' pairs
covered = [set() for _ in range(V)]
pool = []; pool_users = []; pool_roles = []
CAP = 21
itter = 0
while True:
    itter += 1
    best = None
    # the candidates: the pairs (a, b) with b unclaimed OR partner[b] == a!!
    for b in range(V):
        for a in PERP[b]:
            if a >= b: continue                       # the orientation: a < b (the fixed choice!!)
            if b in partner and partner[b] != a: continue
            # the users: the targets with a, b uncovered (a, b C= their perps!!)
            users = [t for t in range(V) if a in PERP[t] and b in PERP[t]
                     and a not in covered[t] and b not in covered[t]]
            if len(users) < 4: continue
            if len(users) > CAP:
                users = sorted(users)[:CAP]           # THE TRIM (serve a subset!!)
            # the third c: from the users' uncovered common!!
            common = None
            for t in users:
                unc = PERP[t] - covered[t]
                common = set(unc) if common is None else (common & unc)
            common -= {a, b}
            for c in sorted(common):
                piece = frozenset({a, b, c})
                # the budgets!!
                if c in partner and any(partner[c] not in PERP[t] for t in users): continue
                nu = third_users[c] | set(users)
                if any(x not in PERP[u] for u in (third_users[c] - set(users)) for x in (a, b)):
                    continue                            # the pair C= c's OTHER users!!
                frung = {a, b, c} | {x for p in pairs_of[c] for x in p}
                if rank(nu) + rank(frung) > 9: continue # the F-rung room!!
                saving = 3 * len(users) - (3 + len(users))
                if saving <= 0: continue
                if best is None or saving > best[0]:
                    best = (saving, a, b, c, users)
    if best is None: break
    saving, a, b, c, users = best
    pool.append(frozenset({a, b, c})); pool_users.append(users); pool_roles.append((a, b, c))
    partner[b] = a
    third_users[c] |= set(users)
    pairs_of[c].append((a, b))
    for t in users: covered[t] |= {a, b, c}
log('THE CHAIN-AWARE GREEDY: %d pieces | the iterations %d' % (len(pool), itter))
log('  the partners (the 2nd-sources): %d | the 3rd-sources: %d' % (len(partner), len(third_users)))
uc = Counter(len(u) for u in pool_users)
log('  the piece user-counts: %s' % dict(sorted(uc.items())))
# the leftovers + the loads
left = [PERP[t] - covered[t] for t in range(V)]
sing_users = defaultdict(set)
for t in range(V):
    for l in left[t]: sing_users[l].add(t)
loads = Counter(len(u) for u in sing_users.values())
log('THE LEFTOVERS: %d lines over %d targets | THE SINGLETON-LOADS: %s' % (
    sum(len(lo) for lo in left), sum(1 for lo in left if lo), dict(sorted(loads.items()))))
ceil = Counter()
for l, us in sing_users.items():
    ceil[9 - rank(us)] += 1
log('THE SINGLETON CEILINGS: %s' % dict(sorted(ceil.items())))
nleft = sum(1 for lo in left if lo)
R = len(pool) + nleft + 9
log('THE ECONOMY: %d pieces + %d carriers + 9 gathers = R %d (R/v %.2f)' % (
    len(pool), nleft, R, R / V))
json.dump({'pool': [sorted(p) for p in pool], 'users': pool_users, 'roles': pool_roles,
           'partner': partner, 'left': [sorted(lo) for lo in left]},
          open('ii19_nat44_assign.json', 'w'))
log('saved ii19_nat44_assign.json')

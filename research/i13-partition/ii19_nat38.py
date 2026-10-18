"""THE BUILD'S ASSIGNMENT CENSUS (ii19_nat38.py) — the running-sum ladder's feasibility on the (3,4) economy.

THE ARCHITECTURE (the word4's own mechanism, resolved!!): each piece (a, b, c) built by 3 gates:
  gate 1 at a's SINGLETON (the piece climbs 0->1; a read free!!),
  gate 2 at the CELL span{a, b} (the piece 1->2, nests (a in the cell!!); b at its cell!!),
  gate 3 at the DIM-4 FRAME F3 (the piece 2->4; c at its dim-4 rung!!) with {a, b, c} all in F3
  (the cell span{a,b} C= F3 automatically (F3 a subspace containing a, b!!!)).
THE SOURCES' FLAG: singleton -> cell -> ITS ONE dim-4 rung -> (B) the perp duties -> FULL.
THE CONSTRAINTS: (i) per piece: a dim-4 frame containing {a, b, c}; (ii) per source: ONE cell
(the pair with its 2nd-source piece's partner); (iii) per source: ONE dim-4 rung containing
ALL its 3rd-source pieces' pairs; (iv) the source's cell C= its dim-4 rung (the nesting!!).
HERE: the greedy matching over the (3,4) pieces -> the feasible fraction + the leftovers.
"""
import os, sys, itertools
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
sys.argv = ['ii19_nat20.py']
exec(open('ii19_nat20.py').read().split('# (1) chain-shape census')[0])
V, H = V, H
log = lambda *a: print(*a, file=sys.stderr, flush=True)

# (1) the 70 dim-4 frames' source-sets
dim4 = {}
for F in range(len(w['frames'])):
    if dims[F] == 4:
        mem = frozenset(s for s in range(V) if cont(F, s))
        if len(mem) >= 3:
            dim4[F] = mem
log('the dim-4 frames: %d | the source-populations: %s' % (
    len(dim4), Counter(len(m) for m in dim4.values())))

# (2) the (3,4) greedy pieces (nat34's perp-direct!!)
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
log('the (3,4) economy: %d pieces' % len(pool))

# (3) the in-frame feasibility: per piece: the dim-4 frames containing its triple
inframe = 0; frame_options = []
for piece in pool:
    opts = [F for F, m in dim4.items() if piece <= m]
    frame_options.append(opts)
    if opts: inframe += 1
log('the pieces with their triple INSIDE a dim-4 frame: %d/%d' % (inframe, len(pool)))
log('the frame-option counts: %s' % dict(sorted(Counter(len(o) for o in frame_options).items())))

# (4) the role/frame assignment (the greedy): per piece: choose (a, b, c) = the roles + F3:
#  - c (the 3rd source): its dim-4 rung F(c) must contain {a, b, c};
#  - b (the 2nd): its cell = span{a, b} C= F(c) (automatic!!) — but b's cell is ONE per source:
#    b's cell-partner FIXED once assigned;
#  - c's dim-4 rung: ONE per source, must contain ALL its 3rd-pieces' pairs.
# GREEDY: process the pieces by their frame-option scarcity; assign c's rung + b's cell.
src_cell = {}          # b -> its cell partner a
src_d4 = {}            # c -> its dim-4 rung frame
assigned = []
pieces = sorted(((len(frame_options[i]), i) for i in range(len(pool))))
bad = []
for _, i in pieces:
    piece = sorted(pool[i])
    done = False
    for F in frame_options[i]:
        mem = dim4[F]
        # try each source as the 3rd (c): c's rung = F (consistent with its other duties!!)
        for c in piece:
            if src_d4.get(c, F) != F: continue
            rest = [x for x in piece if x != c]
            a, b = rest
            # b's cell: the pair (a, b); b's cell-partner must be consistent
            if b in src_cell and src_cell[b] != a: continue
            # the nesting: b's cell C= F: automatic (a, b in mem!!)
            # a: the 1st source (free singleton read!!)
            src_d4[c] = F; src_cell[b] = a
            assigned.append((i, F, a, b, c))
            done = True
            break
        if done: break
    if not done:
        bad.append(i)
log('THE ASSIGNMENT: %d/%d pieces assigned | unassigned %d' % (len(assigned), len(pool), len(bad)))
log('  the sources with a dim-4 rung: %d | with a cell: %d' % (len(src_d4), len(src_cell)))
multi_d4 = Counter(src_d4.values())
log('  the dim-4 rung loads: %s' % dict(sorted(Counter(multi_d4.values()).items())))
# the unassigned pieces' diagnosis
if bad:
    log('  the unassigned pieces (first 10): %s' % [(sorted(pool[i]), len(frame_options[i])) for i in bad[:10]])
# the coverage after dropping the unassigned: the carriers
covered2 = [set() for _ in range(V)]
for i, F, a, b, c in assigned:
    for ti in pool_users[i]: covered2[ti] |= set(pool[i])
left2 = [PERP[ti] - covered2[ti] for ti in range(V)]
nleft = sum(1 for lo in left2 if lo)
R = len(assigned) + nleft + 9
log('THE POST-ASSIGNMENT ECONOMY: %d pieces + %d carriers + 9 = R %d' % (len(assigned), nleft, R))
json_pool = {'assigned': [(i, F, a, b, c) for i, F, a, b, c in assigned],
             'pool': [sorted(p) for p in pool], 'users': pool_users,
             'leftovers': [sorted(lo) for lo in left2]}
import json
json.dump(json_pool, open('ii19_nat38_assign.json', 'w'))
log('saved ii19_nat38_assign.json')

"""THE SHARED-RUNG GROUP-PACKING (ii19_nat40.py) — the emission's last feasibility measurement.

THE STRUCTURE (fully resolved!!): the kept pieces (73, the role-solved 3-gate builds!!) + the
SINGLETON-PIECES (the per-line helpers covering the leftovers: build at the line's own
singleton (rank 1!!), read-groups at the frames C= the uncovered-targets' perps!!).
PER PIECE: the users partitioned into the dim-groups; the group at dim d needs a dim-d frame
C= every member's perp AND C= the piece's value (the lines C= the users' perps by the balance!!)
AND the piece's chain nested (build-frame C= G_low C= G_high...!!).
PER TARGET: the read-frames (its pieces'/singletons' group-frames!!) must form ONE nested
chain (one frame per dim, increasing!!) ending at perp(t).
HERE: the greedy group-packing + the frame construction (the spans of the C=perp lines!!) +
THE PER-TARGET NESTING CHECK -> the feasibility verdict + the honest R + the emission inputs.
"""
import os, sys, itertools, json
from collections import Counter, defaultdict
import numpy as np
from fractions import Fraction
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
sys.argv = ['ii19_nat20.py']
exec(open('ii19_nat20.py').read().split('# (1) chain-shape census')[0])
V, H = V, H
log = lambda *a: print(*a, file=sys.stderr, flush=True)
LINf = [[Fraction(x) for x in l] for l in w['lines']]
Linn = np.array([[float(x) for x in l] for l in w['lines']])

G4 = [[sum(w['lines'][s][i] * w['form']['num'][i][j] * w['lines'][t][j]
            for i in range(H) for j in range(H) if w['form']['num'][i][j]) for t in range(V)] for s in range(V)]
PERP = [set(s for s in range(V) if s != t and G4[s][t] == 0) for t in range(V)]

A39 = json.load(open('ii19_nat39_assign.json'))
kept = [(i, a, b, c) for i, a, b, c in A39['kept']]
pool = [frozenset(p) for p in A39['pool']]
users = [list(u) for u in A39['users']]
left2 = [set(l) for l in A39['left2']]
log('loaded: %d kept pieces | the leftovers: %d targets with leftovers' % (
    len(kept), sum(1 for lo in left2 if lo)))

# the singleton-pieces: per line l: its uncovered targets (the users!!)
sing_users = defaultdict(set)
for t in range(V):
    for l in left2[t]:
        sing_users[l].add(t)
sings = {l: sorted(us) for l, us in sing_users.items() if len(us) >= 1}
log('the singleton-pieces: %d (the users mean %.1f)' % (
    len(sings), sum(len(u) for u in sings.values()) / max(1, len(sings))))

def span_rank(lines):
    if not lines: return 0
    return int(np.linalg.matrix_rank(Linn[sorted(lines)]))

def gramed(lines):
    """the frame (the lines' span) Gram nondegeneracy check (exact!!)."""
    if not lines: return True
    M = [[sum(LINf[a][i] * LINf[a][j] * (w['form']['num'][i][j]) for i in range(H) for j in range(H) if w['form']['num'][i][j]) for b in lines] for a in lines]
    # the exact determinant via Fraction Gaussian elimination
    M2 = [[Fraction(x, w['form']['den']) for x in r] for r in M]
    n = len(M2); det = Fraction(1)
    for c in range(n):
        p = next((i for i in range(c, n) if M2[i][c] != 0), None)
        if p is None: return False
        M2[c], M2[p] = M2[p], M2[c]
        det *= M2[c][c]
        for i in range(c + 1, n):
            f = M2[i][c] / M2[c][c]
            M2[i] = [x - f * y for x, y in zip(M2[i], M2[c])]
    return det != 0

# ============ THE GROUP-PACKING (per piece: the users -> the dim-groups) ============
# the group at dim d: the members' perps' C= room: the members + the piece's lines together
# must span <= 9?? NO: the frame (dim d) C= each member's perp: the frame's LINES (the dim-d
# basis from the C=perp lines!!) — the constraint: d <= dim of the members' perps' intersection.
# the piece's value C= the intersection (the balance!!) -> the frame = the value's span
# EXTENDED by the extra C=perp lines to dim d!!!
def pack_groups(us, piece_lines):
    """the users -> [(dim, [users])] with the frames constructible (the intersection has room!!)."""
    rem = sorted(us); groups = []
    val = set(piece_lines)
    while rem:
        placed = False
        for d in range(8, 2, -1):        # the high dims first (the small groups; more room!!)
            # try to grow a group whose perps' intersection dim >= d
            grp = []
            inter_lines = None
            for u in rem:
                cand = grp + [u]
                # the intersection: the lines C= ALL the members' perps + the piece's value
                il = set(val)
                for uu in cand:
                    il &= PERP[uu]
                if span_rank(il) >= d:
                    grp = cand
            if len(grp) >= 1 and span_rank(set(val) & PERP[grp[0]] if len(grp) == 1 else
                __import__('functools').reduce(lambda A, u: A & PERP[u], grp[1:], PERP[grp[0]] & set(val))) >= d:
                groups.append((d, grp))
                rem = [u for u in rem if u not in grp]
                placed = True
                break
        if not placed:
            return None
    return groups

npieces_ok = 0; the_groups = []
for (i, a, b, c) in kept:
    gl = pool[i]
    g = pack_groups(users[i], gl)
    if g is None:
        the_groups.append(None)
    else:
        npieces_ok += 1
        the_groups.append(g)
nsing_ok = 0; sing_groups = {}
for l, us in sings.items():
    g = pack_groups(us, [l])
    if g is None:
        sing_groups[l] = None
    else:
        nsing_ok += 1
        sing_groups[l] = g
log('THE GROUP-PACKING: the pieces ok %d/%d | the singleton-pieces ok %d/%d' % (
    npieces_ok, len(kept), nsing_ok, len(sings)))
bad = [(i, a, b, c) for (i, a, b, c), g in zip(kept, the_groups) if g is None]
if bad:
    log('  the pieces failing the packing (first 5): %s' % [(sorted(pool[i]), len(users[i])) for i, a, b, c in bad[:5]])
bad_s = [l for l, g in sing_groups.items() if g is None]
if bad_s:
    log('  the singleton-pieces failing (first 5): %s (the users: %s)' % (
        bad_s[:5], [len(sings[l]) for l in bad_s[:5]]))
# the group-dim profiles
dims_hist = Counter()
for g in the_groups:
    if g: dims_hist[tuple(d for d, grp in g)] += 1
log('the piece group-dim profiles (the first 10): %s' % dict(list(sorted(dims_hist.items(), key=lambda kv: -kv[1]))[:10]))
json.dump({'groups': [[(d, grp) for d, grp in g] if g else None for g in the_groups],
           'sing_groups': {str(l): ([(d, grp) for d, grp in g] if g else None) for l, g in sing_groups.items()}},
          open('ii19_nat40_groups.json', 'w'))
log('saved ii19_nat40_groups.json')

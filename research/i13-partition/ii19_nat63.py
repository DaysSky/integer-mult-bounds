"""THE 2-CLASS BUILD STAGE 9 (ii19_nat63.py) — THE Z-GATE CARRIER DESIGN (the word4's own!!).

THE MECHANISM (the word4's proven (§1928: the B-scratch-chains load-bearing!!)): the
per-target carriers inside perp(t)-space: their builds = the running-sums over THE PIECES
(the pieces' values (NOT the raw sources (the nat60 wall dissolves!!))) read at the SHARED
RUNGS (the dim-2 cells (inside ~112 perps!!) + the dim-4 12-frames (~50!!) + the dim-6s!!)
nested along the carrier's ladder: 0 -> the rungs (dim-ascending!!) -> perp(t) (9!!) -> FULL.
HERE: (1) the per-target piece-sets (nat56!!); (2) THE READ-RUNG ASSIGNMENT (the pieces
read at the shared rungs inside perp(t)!!); (3) the carriers' ladders + the z-gates;
(4) THE ARRIVAL LAW (the reads vs 10R!!); (5) THE HIST MODEL + THE PRICE!!
"""
import os, sys, itertools, json
from collections import Counter, defaultdict
import numpy as np
from fractions import Fraction
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
import pricer
log = lambda *a: print(*a, file=sys.stderr, flush=True)
price = lambda hist, v, h, R: pricer.price({int(k): int(val) for k, val in hist.items()}, v, h, R)
FC = Fraction(str('0.001744385950814795279853'))

roots240 = set()
for i, j in itertools.combinations(range(8), 2):
    for si, sj in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
        v = [0] * 8
        v[i] = si; v[j] = sj
        roots240.add(tuple(v))
for s in itertools.product([1, -1], repeat=8):
    if sum(s) % 4 == 0:
        roots240.add(tuple(Fraction(x, 2) for x in s))

def canon(v):
    for x in v:
        if x != 0:
            return tuple(v) if x > 0 else tuple(-y for y in v)
    return tuple(v)

d8 = {canon(r): r for r in roots240}
roots = sorted(d8.values())
V = 240
H = 10
L = []
for c in (0, 1):
    for a in roots:
        L.append([Fraction(x) for x in a] + [Fraction(c), Fraction(0)])
FORM = [[Fraction(0)] * H for _ in range(H)]
for i in range(8): FORM[i][i] = Fraction(1)
FORM[8][9] = FORM[9][8] = Fraction(1)
def ip(x, y):
    return sum(x[i] * y[j] * FORM[i][j] for i in range(H) for j in range(H) if FORM[i][j])
G = [[ip(L[s], L[t]) for t in range(V)] for s in range(V)]
CLS = [s // 120 for s in range(V)]
CPERP = [set(s for s in range(V) if CLS[s] == CLS[t] and s != t and G[s][t] == 0) for t in range(V)]

D56 = json.load(open('ii19_nat56_delivery.json', 'rt'))
pool = [set(p) for p, u in D56['pool']]
users = [list(u) for p, u in D56['pool']]
log('THE PIECES: %d' % len(pool))

# (1) the per-target piece-sets!!
t_pieces = defaultdict(list)
for i, (p, u) in enumerate(D56['pool']):
    for t in u:
        t_pieces[t].append((i, set(p)))
log('(1) THE PER-TARGET PIECES: mean %.1f (the distribution: %s!!)' % (
    sum(len(v) for v in t_pieces.values()) / V,
    dict(sorted(Counter(len(v) for v in t_pieces.values()).items()))))

# (2) THE READ-RUNG ASSIGNMENT: the piece P read by t at a shared rung F:
# the candidate rungs: the piece's OWN span (dim 2-3!! — the piece's lines' plane!!) +
# the extensions (the rungs ⊇ the piece's value + C= perp(t)!!)
# THE SIMPLEST LEGAL READ-FRAME: THE PIECE'S SPAN ITSELF (the piece's value C= its span
# BY CONSTRUCTION (the lines!!)!!) — the target reads the piece AT THE PIECE'S SPAN-FRAME:
# the target's chain must PASS the piece's span (C= perp(t) ✓ (the piece's lines C= perp(t)
# (the balance!!))) — the target's ladder: 0 -> the pieces' spans (NESTED?!) -> perp(t)!!
# THE PER-TARGET NESTING: the spans (dim 2-3, INCOMPARABLE!!) — the one-frame-per-dim law!!
# THE RESOLUTION (the word4's!!): the target reads at MOST ONE piece per dim-level; the
# rest via THE CARRIERS (the z-assembly INSIDE perp(t)!!)
spandim = Counter()
spans = []
for p, u in D56['pool']:
    xs = [L[x][:8] for x in p]
    lv = [L[x][8] for x in p]
    # the span: the x-parts' rank + the level-direction (the a-coordinate!!)
    r = int(np.linalg.matrix_rank(np.array([[float(z) for z in x] for x in xs]))) if xs else 0
    # the level: the a-coords: the class-0: (0): no level; the class-1: (1): +1 dim!!
    r += (1 if any(a != 0 for a in lv) else 0)
    spandim[r] += 1
    spans.append(r)
log('(2) THE PIECE SPAN-DIMS: %s' % dict(sorted(spandim.items())))
# the per-target: the pieces' spans + the one-per-dim capacity!!
over = 0
for t, plist in t_pieces.items():
    dc = Counter(spans[i] for i, p in plist)
    over += sum(c - 1 for d, c in dc.items() if c > 1)
log('    THE PER-TARGET SPAN-COLLISIONS (the same-dim pieces!!): %d (the z-work!!)' % over)

# (3) THE CARRIERS' LADDERS: the per-target carrier: the running-sum over the collision-
# pieces (the same-dim ones!!) at ONE perp(t)-local frame + the singleton-pieces for the
# leftovers (the nat60 design at the PIECE level!!)!!
# THE Z-COUNT: per target: the collisions + the leftover-carriers!!
ncar = 240 + over // 12                      # the base carriers + the z-scratch!!
RET = 18
Rz = len(D56['pool']) + ncar + RET
log('(3) THE Z-CARRIER ECONOMY: %d pieces + %d carriers (the base + the z!!) + %d = R %d' % (
    len(D56['pool']), ncar, RET, Rz))
# (4) THE ARRIVAL: the reads ~ the pieces per target (mean %.1f!!) + the scatter!!
mean_reads = sum(len(v) for v in t_pieces.values()) / V
log('(4) THE ARRIVAL: the mean piece-reads per target %.1f vs the 10R/R = %.1f' % (
    mean_reads, 10))
# (5) THE HIST MODEL + THE PRICE at Rz!!
CST = 162
climb = 10.0 * Rz + 2.0 * V * 9
# the natural hist: the pieces' builds (the 3-gate running-sums: the ranks 1,1,2!!) + the
# read-rungs (the pieces' span-climbs!!) + the carriers (the z-ladders!!) + the targets!!
nat = Counter()
nat[1] += 2 * len(D56['pool'])               # the 1st/2nd gates (the singleton/cell!!)!!
nat[2] += len(D56['pool'])                   # the 3rd gates (the dim-4!!)!!
nat[2] += over                               # the z-scratch (the dim-2-ish!!)!!
nat[9] += 240                                # the targets (0 -> perp (rank 9!!)!!
nat[9] += ncar + len(D56['pool'])            # the helpers' finals (-> FULL: rank 1..9!!
nat[7] += 2 * V                              # the sources (1 -> FULL: ~rank 9?? the A-duties
nat[9] += RET                                # the retained!!
h = dict(nat)
# the mass-exact fill!!
M = int(climb) + CST
cur = sum(r * c for r, c in h.items())
diff = M - cur
log('    the natural hist: %s | the mass %d vs the identity %d (the fill %d!!)' % (
    dict(sorted(h.items())), cur, M, diff))
if diff > 0:
    h[1] = h.get(1, 0) + diff               # the fill at rank 1 (the finest!!!!
c = price(h, V, H, Rz)
if c and c[0] and 1e-4 < float(c[0]) < 1e-2:
    log('(5) THE NATURAL-ECONOMY PRICE at R %d: %+.2f%% vs the frontier' % (
        Rz, 100 * (float(c[0]) / float(FC) - 1)))
    # THE MX at the same R!!
    hmx = {9: int(climb) // 9 + 18 + diff}
    c2 = price(hmx, V, H, Rz)
    if c2 and c2[0]:
        log('    THE MX at R %d: %+.2f%%' % (Rz, 100 * (float(c2[0]) / float(FC) - 1)))
json.dump({'Rz': Rz, 'over': over, 't_pieces': {str(k): [i for i, p in v] for k, v in t_pieces.items()}},
          open('ii19_nat63_zcarriers.json', 'w'))
log('saved ii19_nat63_zcarriers.json')

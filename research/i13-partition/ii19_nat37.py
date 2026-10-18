"""THE WITHIN-12-FRAME PIECE CENSUS (ii19_nat37.py) — the build's economy under the flag constraint.

THE ARCHITECTURE (the chain constraints' resolution!!): the pieces WITHIN the 12-frames (the
word4's own 10 shared dim-4 rungs, 12 sources each — THE SAME 121-LINE SYSTEM, the flag copied
verbatim!!): each source's piece-duties collapse to ITS 12-frame (one climb!!); the pieces'
builds: one gate at the 12-frame (rank-4 climbs!!); the read groups nest at dims 5-8.
HERE: the greedy per 12-frame (the pieces = the subsets shared by >=2 targets within their
compatible 12-frames!!) -> the pool/carriers/R + the per-(target, 12f) leftover structure
(the perp-local assembly's z-work map!!).
"""
import os, sys, itertools
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
from pricer import price
from mpmath import mp

sys.argv = ['ii19_nat20.py']
exec(open('ii19_nat20.py').read().split('# (1) chain-shape census')[0])
V, H, nreg = V, H, nreg
FRONT = mp.mpf('0.001744385950814795279853')
log = lambda *a: print(*a, file=sys.stderr, flush=True)

# the 12-frames from the word4 (the sources' dim-4 rungs: the 10 shared frames!!)
dim4 = {}
for F in range(len(w['frames'])):
    if dims[F] == 4:
        mem = set(s for s in range(V) if cont(F, s))
        if len(mem) >= 2:
            dim4[F] = mem
t12 = sorted(dim4.items(), key=lambda kv: len(kv[1]), reverse=True)
log('the word4 dim-4 frames: %d | the source-populations: %s' % (len(t12), sorted(len(v) for k, v in t12)))

# the perp/12-frame compatibility: perp(t)'s lines per 12-frame
G4 = [[sum(w['lines'][s][i] * w['form']['num'][i][j] * w['lines'][t][j]
            for i in range(H) for j in range(H) if w['form']['num'][i][j]) for t in range(V)] for s in range(V)]
PERP = [set(s for s in range(V) if s != t and G4[s][t] == 0) for t in range(V)]

# THE GREEDY PER 12-FRAME: the pieces = the subsets of the 12-frame's lines shared by >=2
# targets whose perps contain them; cover perp(t) ∩ 12f for the compatible (t, 12f)!!
pool = []; pool_users = []
covered = defaultdict(set)          # (t, fi) -> covered lines
for fi, (F, members) in enumerate(t12):
    mem = sorted(members)
    # the (target, 12f) parts
    parts = {}
    for t in range(V):
        pt = PERP[t] & set(mem)
        if len(pt) >= 3:
            parts[t] = pt
    pair_count = Counter(); pair_users = defaultdict(list)
    for t, pt in parts.items():
        for a, b in itertools.combinations(sorted(pt), 2):
            pair_count[(a, b)] += 1; pair_users[(a, b)].append(t)
    while True:
        cands = []
        for (a, b), c in pair_count.items():
            if c < 2: continue
            users = [t for t in pair_users[(a, b)] if a not in covered[(t, fi)] and b not in covered[(t, fi)]]
            if len(users) < 2: continue
            common = None
            for t in users:
                unc = parts[t] - covered[(t, fi)]
                common = unc if common is None else (common & unc)
            if common is None or len(common) < 2: continue
            piece = frozenset(sorted(common)[:3])
            real = [t for t in users if piece <= parts[t] - covered[(t, fi)]]
            if len(real) < 2: continue
            saving = len(piece) * len(real) - (len(piece) + len(real))
            if saving <= 0: continue
            cands.append((saving, piece, real))
        if not cands: break
        cands.sort(key=lambda c: c[0], reverse=True)
        for saving, piece, real in cands[:50]:
            if any(piece <= parts[t] - covered[(t, fi)] for t in real):
                pool.append((fi, piece)); pool_users.append(real)
                for t in real: covered[(t, fi)] |= set(piece)
                break
        else:
            break
leftovers = {t: set() for t in range(V)}
for (t, fi) in list(covered.keys()) + []:
    pass
for t in range(V):
    for fi, (F, members) in enumerate(t12):
        mem = set(members)
        pt = PERP[t] & mem
        if len(pt) >= 3:
            left = pt - covered[(t, fi)]
            if left: leftovers[t] |= set(left)
nleft = sum(1 for t in range(V) if leftovers[t])
lsize = sum(len(leftovers[t]) for t in range(V))
R = len(pool) + nleft + 9
log('THE WITHIN-12-FRAME ECONOMY: pool %d (mean %.1f lines, mean %.1f users) | target-carriers %d | leftover lines %d | R %d'
    % (len(pool), sum(len(p) for fi, p in pool) / max(1, len(pool)),
       sum(len(us) for us in pool_users) / max(1, len(pool)), nleft, lsize, R))
# the per-(t, 12f) leftover map (the z-work!!)
zl = Counter()
for t in range(V):
    for fi, (F, members) in enumerate(t12):
        pt = PERP[t] & set(members)
        if len(pt) >= 3:
            left = pt - covered[(t, fi)]
            if left: zl[len(left)] += 1
log('the per-(target, 12f) leftover sizes: %s (the z-work map!!)' % dict(sorted(zl.items())))
# the honest hist: the pieces: build (rank 4!!) + the read groups (dims 5-8!!); the carriers: the z-assembled perp-locals!!
M = 9 * R + 73 + 1936
hist = Counter()
hist[4] += len(pool)                                  # the piece builds (rank 4!!)
for fi, p in pool: pass
for us in pool_users: hist[1] += max(1, len(us) // 4)   # the read groups (the cap model ~4 users/group!!)
hist[8] += V                                         # the targets
hist[4] += nleft * 2                                 # the carriers: build + read (rank 4!!)
hist[8] += 8; hist[9] += 1                            # the copy
srcm = 0
srcd = Counter()
for fi, p in pool:
    for s in p: srcd[s] += 1
for s, c in srcd.items(): srcm += 2                   # ~the cell+12f climbs (rank ~2 each!!)
hist[2] += srcm
mass = sum(r * c for r, c in hist.items())
diff = M - mass
while diff > 0:
    r = 1 if diff % 2 or diff == 1 else 2
    hist[r] += 1; diff -= r
assert sum(r * c for r, c in hist.items()) == M
try:
    c = price(dict(hist), V, H, R)[0]
    log('THE WITHIN-12-FRAME HIST (mass-exact %d): %s | c = %s (%+.2f%%!!)' % (
        M, dict(sorted(hist.items())), mp.nstr(c, 22), float((c / FRONT - 1) * 100)))
except AssertionError:
    log('NO-ROOT at the within-12-frame hist (R %d)' % R)

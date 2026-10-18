"""THE GREEDY GRID + THE NATURAL-HIST MODEL (ii19_nat35.py) — THE +20/+30% TARGET SEARCH.

THE MAP (nat33): the OG-shape crosses +19..+30% at R 220-280; the W4-shape at R~240.  THE HONEST
QUESTION: what (R, hist) does the native economy REALIZE?  Here: the greedy variants (the
piece-selection heuristics + thresholds) -> the (pool, carriers, R) grid, and per variant the
NATURAL-HIST MODEL priced at its R:
  - the pieces: 1 build climb (0 -> the span, rank = the span dim (the E8-triple spans ~2-3!!))
    + the read rungs (the users partitioned into the perp-compatibility groups (the slot
    capacity: the group at dim d serves the users whose lines span <= 9-d)); the rung count
    g_i, each rank ~1-2.
  - the sources: the flag chains (1 -> the span-clusters -> 9): ~3-5 climbs of rank 1-3.
  - the carriers: 2 climbs (the build (rank ~4) + the read (rank ~4)).
  - the targets: 1 climb (rank 8) | the gathers: ~4 climbs each | the copy {8: 8, 9: 1}.
MASS-EXACT (the identity 9R + 73 + 1936) with the largest-remainder; priced at (121, 9, R).
The model is honest +-10 points (the actual hist emerges from the Stage-B build!!).
"""
import os, sys, itertools, json
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
from pricer import price
from mpmath import mp

sys.argv = ['ii19_nat20.py']
exec(open('ii19_nat20.py').read().split('# (1) chain-shape census')[0])
V, H = V, H
LM = (1 << V) - 1
FRONT = mp.mpf('0.001744385950814795279853')
log = lambda *a: print(*a, file=sys.stderr, flush=True)

G4 = [[sum(w['lines'][s][i] * w['form']['num'][i][j] * w['lines'][t][j]
            for i in range(H) for j in range(H) if w['form']['num'][i][j]) for t in range(V)] for s in range(V)]
PERP = [sum(1 << s for s in range(V) if s != t and G4[s][t] == 0) for t in range(V)]
perps = [[s for s in range(V) if (PERP[t] >> s) & 1] for t in range(V)]

# the span dim of a line-set (the rank of the lines in the 9-dim line space)
LIN = w['lines']
def span_dim(lines):
    M = np.array([[float(x) for x in LIN[s]] for s in lines] or [[0.0] * H])
    return int(np.linalg.matrix_rank(M))

def greedy(kmin, umin, order):
    pair_count = Counter(); pair_users = defaultdict(list)
    for ti, pl in enumerate(perps):
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
                unc = set(perps[ti]) - covered[ti]
                common = unc if common is None else (common & unc)
            if common is None or len(common) < kmin: continue
            # the piece candidates: the kmin.. subsets of common shared by the most users
            for piece in (frozenset(x) for x in [sorted(common)[:kmin]] if len(x) >= kmin):
                real = [ti for ti in users if piece <= set(perps[ti]) - covered[ti]]
                if len(real) < umin: continue
                saving = len(piece) * len(real) - (len(piece) + len(real))
                if saving <= 0: continue
                cands.append((saving, len(piece), len(real), piece, real))
        if not cands: break
        cands.sort(key=order, reverse=True)
        progressed = False
        for saving, k, u, piece, real in cands[:50]:
            if any(piece <= set(perps[ti]) - covered[ti] for ti in real):
                pool.append(piece); pool_users.append(real)
                for ti in real:
                    covered[ti] |= set(piece)
                progressed = True
            if progressed: break
        if not progressed: break
    leftovers = [set(perps[ti]) - covered[ti] for ti in range(V)]
    return pool, pool_users, leftovers

def group_count(users):
    """the slot model: greedily pack the users into groups; a group at dim d (d = 4..8) serves
    users whose lines span <= 9-d (a common dim-d frame inside all their perps!!)."""
    rem = list(users); g = 0
    while rem:
        for d in range(8, 3, -1):
            cap = H - d
            grp = []
            for u in rem:
                if len(grp) < cap or span_dim_lines(grp + [u]) <= cap:
                    if span_dim_lines(grp + [u]) <= cap:
                        grp.append(u)
            if grp:
                g += 1
                rem = [u for u in rem if u not in grp]
                break
        else:
            g += 1; rem = rem[1:]
    return g

_span_cache = {}
def span_dim_lines(us):
    key = tuple(sorted(us))
    if key not in _span_cache:
        _span_cache[key] = np.linalg.matrix_rank(np.array([[float(x) for x in LIN[u]] for u in us] or [[0.0] * H]))
    return _span_cache[key]

def mass_exact(fracs, M):
    h = Counter(); tot = sum(fracs.values())
    for r, f in fracs.items():
        h[r] = int(f * M / (tot * r))
    rem = M - sum(r * c for r, c in h.items())
    while rem > 0:
        for r in sorted(fracs, key=lambda r: -fracs[r]):
            if r <= rem:
                h[r] += 1; rem -= r; break
        else:
            h[rem] += 1; rem = 0
    return h

def pc(hist, R):
    try:
        return price(dict(hist), V, H, R)[0]
    except AssertionError:
        return None

VARIANTS = [
    ('(2,2) saving-first', 2, 2, lambda c: (c[0],)),
    ('(2,2) users-first', 2, 2, lambda c: (c[2], c[0])),
    ('(3,2) saving-first', 3, 2, lambda c: (c[0],)),
    ('(3,3) saving-first', 3, 3, lambda c: (c[0],)),
    ('(2,3) saving-first', 2, 3, lambda c: (c[0],)),
    ('(4,2) saving-first', 4, 2, lambda c: (c[0],)),
    ('(3,4) saving-first', 3, 4, lambda c: (c[0],)),
]
for name, kmin, umin, order in VARIANTS:
    pool, pool_users, leftovers = greedy(kmin, umin, order)
    carriers = sum(1 for lo in leftovers if lo)
    R = len(pool) + carriers + 9
    # the natural-hist model
    build_mass = sum(span_dim(list(p)) * 1 for p in pool)            # the piece builds (rank = span dim)
    grun = [group_count(us) for us in pool_users]
    read_mass = sum(max(1, g) * 1 for g in grun)                        # the read rungs (rank ~1 each)
    carr_mass = 8 * carriers                                           # the carriers: build(~4) + read(~4)
    tgt_mass = 8 * V                                                   # the targets
    src_mass = 2 * V * 2                                               # the sources: ~2 climbs of rank ~2 (the flag model)
    gath_mass = 8 * 9                                                  # the gathers' ladders
    M = 9 * R + 73 + 1936 - 73                                         # the climb mass (the copy separate!!)
    fracs = {1: build_mass + read_mass + src_mass, 4: carr_mass * 0.5, 8: tgt_mass + carr_mass * 0.5 + gath_mass}
    hist = mass_exact(fracs, M)
    hist[8] += 8; hist[9] += 1
    c = pc(hist, R)
    log('%-22s: pool %3d (users mean %.1f) carriers %3d -> R %3d | the model hist %s | %s' % (
        name, len(pool), sum(len(us) for us in pool_users) / max(1, len(pool)), carriers, R,
        dict(sorted(hist.items())),
        'NO-ROOT' if c is None else 'c %s (%+.2f%%)' % (mp.nstr(c, 12), float((c / FRONT - 1) * 100))))

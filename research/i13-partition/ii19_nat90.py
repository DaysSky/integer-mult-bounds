"""THE FOREST CENSUS (ii19_nat90.py) — the shared-rung feasibility measurement!!

THE nat88/89's settled dial: cst = 72 (the 9 gathers at FULL!!) — the R-map: +42.2% at
R=174 .. +16.9% at R=274. THE EMISSION'S CORE (the two-sided nesting law (the gcheck
climb rule!!)): the piece-side is FREE (span(a,b,c) ⊆ perp(t) ∀ users (the 13.5!!) —
ALL READ AT THE PIECE'S OWN PF (zero climbs!!)); THE TARGET-SIDE IS THE WALL (its ~16
reads' frames must form ONE NESTED CHAIN ⊆ perp(t)!!). THE JOINT LAW: a piece read
above its PF has nested read-frames ⇒ its per-level users MUST SHARE ONE FRAME; the
off-chain users cost DUP-COPIES (the R-budget!!!). THE CENSUS (the feasibility!!):
(1) THE PIECES' USER-STRUCTURE: per piece: the users' lines ⊆ the piece's 5-dim perp —
    the SUFFIX-COMMON-PERP dims (the cluster-capacity curve!!);
(2) THE SHARED-RUNG POOL: per piece: the dim-4..6 candidate frames G ⊇ span(w) with the
    large T(G) = {t : G ⊆ perp(t)} — the co-read groups (the split-counts!!);
(3) THE R-ESTIMATE: pieces + dups (the splits) + gathers + the leftover-carriers —
    the honest R and the price it lands at.
"""
import os, sys, json, itertools
from collections import Counter, defaultdict
from fractions import Fraction
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
log = lambda *a: print(*a, file=sys.stderr, flush=True)

def rref(rows, n):
    m = [[Fraction(x) for x in r] for r in rows]; r = 0
    for c in range(n):
        p = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if p is None: continue
        m[r], m[p] = m[p], m[r]; iv = 1 / m[r][c]; m[r] = [x * iv for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]; m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
    return m[:r]
def rank_of(vecs, n=8):
    return len(rref([list(v) for v in vecs], n))

SPEC = json.load(open('ii19_nat69_spec.json', 'rt'))
lines = [tuple(int(x) for x in l) for l in SPEC['lines']]
V = len(lines)
PERP = [set(p) for p in SPEC['PERP']]
P70 = json.load(open('ii19_nat70_pool.json', 'rt'))
pool = [(sorted(p), sorted(u)) for p, u in P70['pool']]

# (1) THE PIECES' USER-STRUCTURE (the suffix-common-perp capacity)
log('(1) THE PIECES USER-STRUCTURE (the users live in the piece\'s 5-dim perp!!):')
cap_c = Counter()
for k, (ps, users) in enumerate(pool):
    r = rank_of([lines[u] for u in users])
    cap_c[(len(ps), r)] += 1
log('    (piece-size, user-rank) census: %s' % dict(sorted(cap_c.items())))
ur = Counter()
for ps, users in pool:
    ur[rank_of([lines[u] for u in users])] += 1
log('    the users\' rank census: %s' % dict(sorted(ur.items())))

# (2) THE SHARED-RUNG CANDIDATES: per piece: G = span(piece + extra lines) ⊆ users' perps
# the greedy cluster: the piece's users ordered by the SUFFIX-greedy (max suffix-common dim);
# the cluster-frames: dim 3 (PF) -> 4 -> 5 -> 6 (the ⊥-extensions INSIDE the suffix-perps!!)
log('\n(2) THE PER-PIECE CLUSTER-CAPACITY (the suffix-greedy chains!!):')
def cluster_piece(ps, users):
    """greedy: repeatedly peel the user whose removal... build the chain BACK-TO-FRONT:
    the LAST user's perp = the chain's end; prepend users while a frame ⊇ span(ps) fits
    inside the group's common perp; when full, close the cluster and continue."""
    span_r = rref([list(lines[s]) for s in ps], 8)
    d0 = len(span_r)
    clusters = []
    rem = list(users)
    while rem:
        # the end-user: pick the one whose perp gives room; then grow the cluster greedily
        # cluster := a maximal subset with common-perp dim >= d0 (always true: all ⊥ ps!)
        # we want BIG clusters at LOW frames: the whole user-set shares PF (dim d0)!!
        # the next level: a subset with common perp dim >= d0+1 (room for a bigger frame)
        cl = []
        # greedy growth: order by current common-perp dim (the dim only drops as we add)
        best = sorted(rem, key=lambda t: -rank_of([lines[x] for x in cl + [t]]))
        for t in best:
            r_new = rank_of([lines[x] for x in cl + [t]])
            if r_new <= 8 - (d0 + 1):
                cl.append(t)
        clusters.append(cl)
        rem = [t for t in rem if t not in cl]
    return clusters
split_hist = Counter()
tot_clusters = 0
examples = []
for k, (ps, users) in enumerate(pool):
    cl = cluster_piece(ps, users)
    tot_clusters += len(cl)
    split_hist[len(cl)] += 1
    if k < 8: examples.append((len(users), [len(c) for c in cl]))
log('    the cluster-count per piece: %s (the DUP-estimate!!!)' % dict(sorted(split_hist.items())))
log('    the total clusters (= the read-frames needed): %d | examples (users, clusters): %s'
    % (tot_clusters, examples[:6]))

# (3) THE TARGET-SIDE LOAD: per target: its pieces (with the cluster-frames they put it in)
log('\n(3) THE TARGET-SIDE LOAD (the per-target read-counts (the ladder depth!!)):')
tload = Counter()
for k, (ps, users) in enumerate(pool):
    for t in users: tload[t] += 1
log('    the per-target piece-loads: %s' % dict(sorted(Counter(tload.values()).items())))
# the leftover lines (the carriers!!)
cov = defaultdict(set)
for k, (ps, users) in enumerate(pool):
    for t in users: cov[t] |= set(ps)
leftover = {t: PERP[t] - cov[t] for t in range(V)}
log('    the per-target leftovers: %s' % dict(sorted(Counter(len(l) for l in leftover.values()).items())))

# (4) THE R-ESTIMATE + THE PRICE
log('\n(4) THE R-ESTIMATE: pieces 147 + the cluster-splits + gathers 9 + the carriers...')
R_est = len(pool) + tot_clusters + 9
log('    the naive R-estimate: 147 (pieces) + %d (the pieces\' cluster-rungs share...) + 9' % tot_clusters)
log('    NOTE: the clusters are the READ-FRAMES (not registers!!) — the registers: the pieces')
log('    + the DUP-COPIES for the OFF-CHAIN clusters only!!')
# THE DUP-ESTIMATE: per piece: its clusters BEYOND THE FIRST ride the SAME register (the
# chain!!) — the piece's register count = 1 (the chain serves all its clusters!!!)
# => the honest register count: 147 pieces + 9 gathers + the leftover-carriers + the D-phase!!
dup_est = 0
log('    THE HONEST REGISTER COUNT: 147 + 9 + the carriers (the leftovers %d line-deliveries!!)'
    % sum(len(l) for l in leftover.values()))
from pricer import price
from mpmath import mp
TARGET = {1: 1010, 2: 1038, 3: 53, 4: 34, 5: 79, 6: 9, 7: 15}
def synth(R, cst):
    mass = 8 * R + cst + 2 * V * 7
    d = Counter(TARGET); d[1] += mass - sum(r * z for r, z in d.items())
    return dict(d)
for R in (160, 174, 190, 210, 230, 250):
    c, prof, dd = price(synth(R, 72), V, 8, R)
    log('  R=%3d (cst=72): %s' % (R, mp.nstr(c, 9) if c is not None else 'NO-ROOT'))
print(json.dumps({'cluster_hist': dict(split_hist), 'total_clusters': tot_clusters,
                  'leftover_total': sum(len(l) for l in leftover.values())}, indent=1))

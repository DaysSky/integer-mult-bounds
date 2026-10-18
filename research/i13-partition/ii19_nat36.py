"""THE STAGE-B DE-RISK CENSUS (ii19_nat36.py) — the (3,4) economy's HONEST CHAIN STRUCTURE.

Per piece: the users packed into groups (a group at frame-dim d needs the users' perps'
intersection to have dim >= d AND contain the piece's span (automatic: the piece's lines are in
every user's perp!!)); the piece's chain = build-frame (dim = its span, inside the LOWEST
group's frame!!) -> the group frames nested (G_low C= G_high, both containing the span!!).
OUTPUT: the honest per-piece chain structure (the rung counts + the rank profile), the
sources' duty-frame census, the honest hist estimate (mass-exact), priced at R=277.
"""
import os, sys, itertools
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
from pricer import price
from mpmath import mp

sys.argv = ['ii19_nat20.py']
exec(open('ii19_nat20.py').read().split('# (1) chain-shape census')[0])
V, H = V, H
FRONT = mp.mpf('0.001744385950814795279853')
log = lambda *a: print(*a, file=sys.stderr, flush=True)

G4 = [[sum(w['lines'][s][i] * w['form']['num'][i][j] * w['lines'][t][j]
            for i in range(H) for j in range(H) if w['form']['num'][i][j]) for t in range(V)] for s in range(V)]
PERP = [sum(1 << s for s in range(V) if s != t and G4[s][t] == 0) for t in range(V)]
perps = [set(s for s in range(V) if (PERP[t] >> s) & 1) for t in range(V)]
LIN = np.array([[float(x) for x in l] for l in w['lines']])

def srank(us):
    if not us: return 0
    return int(np.linalg.matrix_rank(LIN[sorted(us)]))

def greedy(kmin, umin):
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
                unc = perps[ti] - covered[ti]
                common = unc if common is None else (common & unc)
            if common is None or len(common) < kmin: continue
            piece = frozenset(sorted(common)[:kmin])
            real = [ti for ti in users if piece <= perps[ti] - covered[ti]]
            if len(real) < umin: continue
            saving = len(piece) * len(real) - (len(piece) + len(real))
            if saving <= 0: continue
            cands.append((saving, piece, real))
        if not cands: break
        cands.sort(key=lambda c: c[0], reverse=True)
        for saving, piece, real in cands[:50]:
            if any(piece <= perps[ti] - covered[ti] for ti in real):
                pool.append(piece); pool_users.append(real)
                for ti in real: covered[ti] |= set(piece)
                break
        else:
            break
    leftovers = [perps[ti] - covered[ti] for ti in range(V)]
    return pool, pool_users, leftovers

pool, pool_users, leftovers = greedy(3, 4)
carriers = sum(1 for lo in leftovers if lo)
R = len(pool) + carriers + 9
log('THE (3,4) ECONOMY: %d pieces + %d carriers + 9 gathers = R %d' % (len(pool), carriers, R))

# the group partition per piece: greedy packing by the perp-intersection capacity
def groups_of(users, piece):
    rem = sorted(users); groups = []
    while rem:
        # pack the biggest group possible: low dim d first (cap = 9-d users), then climb
        packed = None
        for d in range(3, 9):
            cap = H - d          # the users' lines may span <= 9-d
            grp = []
            for u in rem:
                if len(grp) < cap and srank(grp + [u]) <= cap:
                    grp.append(u)
            if grp:
                packed = (d, grp)
                break
        if packed is None:
            groups.append((2, rem[:1])); rem = rem[1:]; continue
        d, grp = packed
        groups.append((d, grp))
        rem = [u for u in rem if u not in grp]
    return groups

rungs = Counter(); ranks = Counter()
srcduties = Counter()
for pi, (piece, users) in enumerate(zip(pool, pool_users)):
    gs = groups_of(users, piece)
    span = srank(list(piece))
    rungs[len(gs)] += 1
    ranks[span] += 1                       # the build climb (rank = the span dim)
    prev = span
    for d, grp in gs:
        ranks[max(1, d - prev)] += 1        # the group climb (rank = the dim gap!!)
        prev = d
    for s in piece:
        srcduties[s] += 1
log('the pieces: the span-rank profile %s | the rung-count profile %s' % (dict(sorted(ranks.items())), dict(sorted(rungs.items()))))
log('the sources: the piece-duty counts %s (mean %.1f)' % (
    dict(sorted(Counter(srcduties.values()).items())), sum(srcduties.values()) / V))

# the honest hist: the measured piece ladders + the flag-model sources/carriers/gathers,
# then the remainder (the flag chains' extra low-rank mass!!) filled at rank 1-2 to mass-exact.
hist = Counter(ranks)                                   # the pieces: builds + rung gaps (measured!!)
for t in range(V): hist[8] += 1                          # the targets
for s, c in srcduties.items():
    hist[max(2, min(8, c // 2))] += 1                   # the sources: ~1 flag climb of rank ~c/2 each
for lo in leftovers:
    if lo:
        hist[4] += 2                                     # the carriers: build + read
hist[6] += 9 * 2                                         # the gathers: ~2 climbs each (rank ~6)
hist[8] += 8; hist[9] += 1                               # the copy
mass = sum(r * c for r, c in hist.items())
M = 9 * R + 73 + 1936
log('the honest hist (pre-fill) %s | mass %d vs the identity %d (the remainder %d -> the flag chains!!)' % (
    dict(sorted(hist.items())), mass, M, M - mass))
diff = M - mass
while diff > 0:                                          # the flag-chain remainder: rank 1-2 climbs
    r = 1 if diff % 2 or diff == 1 else 2
    take = min(diff, r)
    hist[r] += 1
    diff -= take
assert sum(r * c for r, c in hist.items()) == M
try:
    c = price(dict(hist), V, H, R)[0]
    log('THE HONEST-(3,4) PRICE (mass-exact!!): c = %s (%+.2f%% vs the frontier!!)' % (mp.nstr(c, 22), float((c / FRONT - 1) * 100)))
except AssertionError:
    log('NO-ROOT at the honest hist')
# THE ROBUSTNESS BAND: the fill's shape (the flag chains) is a model choice — the scenarios
# fill the REMAINDER (1347, the pre-fill shortfall) only, on top of the MEASURED pre-fill hist!!
prefill = Counter({1: 399, 2: 167, 3: 100, 4: 242, 5: 1, 6: 18, 8: 129, 9: 1})
assert sum(r * c for r, c in prefill.items()) == 3155
REM = M - 3155
for tag, ones in (('all-rank-1 fill (the WORST!!)', REM), ('the 50/50 fill (the honest!!)', (REM // 2) * 1 + (REM % 2))):
    h2 = Counter(prefill)
    h2[1] += ones
    rest = REM - ones
    h2[2] += rest // 2
    h2[1] += rest % 2
    assert sum(r * c for r, c in h2.items()) == M
    try:
        cc = price(dict(h2), V, H, R)[0]
        if cc is None or not (mp.mpf('0.0001') < cc < mp.mpf('0.01')):
            log('  the %s: %s (the spurious/out-of-range root rejected!!)' % (tag, cc))
        else:
            log('  the %s: c = %s (%+.2f%%)' % (tag, mp.nstr(cc, 12), float((cc / FRONT - 1) * 100)))
    except AssertionError:
        log('  the %s: NO-ROOT' % tag)

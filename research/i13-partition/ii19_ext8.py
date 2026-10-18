"""THE COVERING's LOWER BOUND + THE PRICE GRID — THE ARCHITECTURE's FLOOR AND REACHABILITY
(ii19_ext8.py).

THE HANDOFF §5.2: the m = 42 is the GREEDY's; the LP/combinatorial lower bound over the
D4-frames' served sets decides the architecture's floor: R_min = 421 + m_lb!!
THE HANDOFF §5.3: the pricer at the R grid with the ext7's hist shape -> the c(R) curve ->
THE HONEST FRONTIER-REACHABILITY VERDICT for this architecture!!

THE BOUNDS:
(1) THE COUNTING BOUND: 120 / max|served(X)|!!
(2) THE PACKING BOUND (the integral dual!!): the max set of targets pairwise-not-co-served
    (no candidate serves two of them!!) -> each needs its OWN carrier: m >= |T|!!
(3) THE LP BOUND (the fractional dual!!): max sum(y_t) s.t. for each candidate X:
    sum_{t in served(X)} y_t <= 1; y >= 0 — the LP <= any integral cover!!
THE CANDIDATE POOL: the dim-4/6 frames (the D4s/D6s!!) + the per-target cells (the fallback
singletons!!) — THE ARCHITECTURE's LEGAL CARRIERS (the perp-based F_j = the FULL: the
targets' chains dim-8-finals: ILLEGAL!! the cells: the singleton-served only (the ext5's
cell-level sharing ZERO!!))!!

THE HIST MODEL (the honest decomposition!!): the ext7's measured hist
{1: 1091, 2: 1710, 3: 331, 4: 144, 6: 1, 8: 8, 9: 4} = THE CORE
{1: 1049, 2: 1710, 3: 331, 4: 60, 6: 1, 8: 8, 9: 4} + THE m CARRIERS {1: m, 4: 2m}
(the A-build +1, the first-read +4, the final +4!!) — THE MASS: 5808 + 9m =
9(421 + m) + 83 + 1936 EXACTLY THE IDENTITY!!! (the model verified at m = 42!!)
"""
import gzip, json, random, sys, time
from collections import Counter, defaultdict
import numpy as np
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

# ============ (0) THE CENSUS CORE (the ext5/ext6 verbatim!) ============
W = json.load(gzip.open('research/e8-bit-r420/data/bitE8mut-r420.json.gz', 'rt'))
v0, h0, R0 = W['v'], W['h'], W['R']
frames0, lines0 = W['frames'], W['lines']

def dot(a, b): return sum(x * y for x, y in zip(a, b))
G0 = [[dot(lines0[i], lines0[j]) for j in range(v0)] for i in range(v0)]
PU = [sum(1 << j for j in range(v0) if G0[j][t] == 0) for t in range(v0)]
CNT2DIM0 = {0: 0, 1: 1, 2: 2, 12: 4, 30: 6, 63: 7, 120: 8}
dims0 = [CNT2DIM0[len(fr)] for fr in frames0]

chains = defaultdict(list)
for F, d, srcs in W['B']:
    if v0 <= d < 2 * v0:
        chains[d - v0].append((F, list(srcs)))
prior_span = {}
for t, gl in chains.items():
    last = None
    for (F, srcs) in gl:
        if F == W['final'][v0 + t]:
            break
        last = F
    prior_span[t] = frozenset(frames0[last]) if last is not None else frozenset()

def served(X):
    if not X:
        return set()
    xm = 0
    for r in X:
        xm |= 1 << r
    out = []
    for u in prior_span:
        if not (set(prior_span[u]) <= X):
            continue
        if xm & ~PU[u]:
            continue
        out.append(u)
    return set(out)

big = []
for fi in range(len(frames0)):
    if dims0[fi] not in (4, 6):
        continue
    X = set(frames0[fi])
    S = served(X)
    if S:
        big.append((frozenset(X), S))
big.sort(key=lambda z: -len(z[1]))
covered = set()
greedy_groups = []
for (X, S) in big:
    if S - covered:
        greedy_groups.append((X, sorted(S - covered)))
        covered |= S
for t in prior_span:
    if t not in covered:
        greedy_groups.append((prior_span[t], [t]))
m_greedy = len(greedy_groups)
log('(0) THE CENSUS: the greedy m = %d (the groups %s) | the candidates: %d big + %d cells' % (
    m_greedy, dict(sorted(Counter(len(S) for (X, S) in greedy_groups).items())),
    len(big), len(prior_span)))

# ============ (1) THE COUNTING BOUND ============
mx = max(len(S) for (X, S) in big)
counting = -(-v0 // mx)
log('(1) THE COUNTING BOUND: 120 / max|served| = 120 / %d = %d' % (mx, counting))

# ============ (2) THE PACKING BOUND (the integral dual!!) ============
cands = big + [(prior_span[t], {t}) for t in prior_span]    # THE FULL LEGAL POOL!!
adj = [set() for _ in range(v0)]
for (X, S) in cands:
    Ss = sorted(S)
    for i in range(len(Ss)):
        for j in range(i + 1, len(Ss)):
            adj[Ss[i]].add(Ss[j])
            adj[Ss[j]].add(Ss[i])
random.seed(12345)
best_pack = 0
best_set = None
for trial in range(4000):
    order = list(range(v0))
    random.shuffle(order)
    chosen = set()
    for u in order:
        if not (adj[u] & chosen):
            chosen.add(u)
    if len(chosen) > best_pack:
        best_pack = len(chosen)
        best_set = sorted(chosen)
log('(2) THE PACKING BOUND: the max pairwise-not-co-served set (4000 greedy trials): %d' % best_pack)

# ============ (3) THE LP BOUND (the fractional dual: the simplex!!) ============
def lp_cover_bound(sets, nT):
    """max sum(y_t) s.t. for each S: sum_{t in S} y_t <= 1; y >= 0 (the cover's LP dual!!)"""
    nC = len(sets)
    nV = nT + nC
    A = np.zeros((nC, nV))
    for i, S in enumerate(sets):
        for t in S:
            A[i, t] = 1.0
        A[i, nT + i] = 1.0
    b = np.ones(nC)
    c = np.zeros(nV)
    c[:nT] = -1.0                        # min -sum(y)!!
    basis = list(range(nT, nV))           # the slacks (feasible start!)
    for it in range(3000):
        Binv = np.linalg.inv(A[:, basis])
        xB = Binv @ b
        rc = c - c[basis] @ (Binv @ A)
        j = int(np.argmin(rc))
        if rc[j] > -1e-10:
            obj = float(c[basis] @ xB)      # the min-objective (negative!!)
            return -obj, it                  # the LP bound = sum(y) = -obj!!
        dcol = Binv @ A[:, j]
        pos = dcol > 1e-12
        if not pos.any():
            return None, it
        ratios = np.full(nC, np.inf)
        ratios[pos] = xB[pos] / dcol[pos]
        i = int(np.argmin(ratios))
        basis[i] = j
    return None, 3000

sets = [sorted(S) for (X, S) in cands]
lp_val, lp_it = lp_cover_bound(sets, v0)
log('(3) THE LP BOUND: %s (the simplex iters %d)' % (
    ('%.6f' % lp_val) if lp_val is not None else 'UNBOUNDED/FAILED', lp_it))

m_lb = max(counting, best_pack, int(np.ceil(lp_val)) if lp_val else 0)
log('    THE FLOOR: m_lb = max(%d, %d, %d) = %d -> R_min = 421 + %d = %d' % (
    counting, best_pack, int(np.ceil(lp_val)) if lp_val else 0, m_lb, m_lb, 421 + m_lb))

# ============ (4) THE PRICE GRID (the handoff §5.3!!) ============
sys.path.insert(0, 'research/lorentzian-frame-cell-handoff/code/price')
from pricer import price
from mpmath import mp, mpf
mp.dps = 40
P111 = mp.mpf('0.001733052823330162099157')
FRONTIER = mp.mpf('0.001733427')          # the P111-tuned reference (the handoff §1!!)

# THE HIST MODEL: the core + the carriers (VERIFIED at m = 42!!)
CORE = {1: 1049, 2: 1710, 3: 331, 4: 60, 6: 1, 8: 8, 9: 4}
def hist_model(m):
    h = dict(CORE)
    h[1] = CORE[1] + m
    h[4] = CORE[4] + 2 * m
    return h
# THE SELF-CHECK at m = 42 (the ext7's measured!!)
chk = hist_model(42)
MEASURED = {1: 1091, 2: 1710, 3: 331, 4: 144, 6: 1, 8: 8, 9: 4}
log('(4) THE HIST MODEL SELF-CHECK at m=42: %s -> %s' % (
    chk, 'MATCH!!' if chk == MEASURED else 'MISMATCH!!'))
assert chk == MEASURED, 'THE HIST MODEL IS WRONG!!'
# THE MASS CHECK: 5808 + 9m = 9(421+m) + 83 + 1936!!
for m in [m_lb, 42, 63]:
    mass = sum(k * n for k, n in hist_model(m).items())
    ident = 9 * (421 + m) + 83 + 2 * 121 * 8
    assert mass == ident, 'THE MASS MODEL BROKEN at m=%d!!' % m
log('    the mass model: 5808 + 9m = the identity ✓ (checked at m_lb, 42, 63!!)')

log('    m    R     c                    vs_P111        the verdict')
best = (None, -1)
for m in range(m_lb, 64):
    hist = hist_model(m)
    R = 421 + m
    c, prof, d = price(hist, 121, 9, R)
    if c is None:
        log('    %d  %d   %s (%s)' % (m, R, 'NO PRICE', d.get('error')))
        continue
    pct = float((c / P111 - 1) * 100)
    if best[0] is None or c > best[0]:
        best = (c, m)
    tag = 'BEST!!' if m == m_lb else ''
    log('    %d  %d   %s   %+0.4f%%   %s' % (m, R, mp.nstr(c, 14), pct, tag))
log('    THE BEST: c = %s at m = %d (R = %d) | vs the frontier 0.001733427: %s' % (
    mp.nstr(best[0], 14) if best[0] is not None else 'NONE', best[1], 421 + best[1],
    'REACHED!!' if best[0] is not None and best[0] >= FRONTIER else
    'NOT REACHED (the gap %.2fx!!)' % (float(FRONTIER / best[0]) if best[0] is not None else 0)))
log('DONE — THE FLOOR + THE GRID')

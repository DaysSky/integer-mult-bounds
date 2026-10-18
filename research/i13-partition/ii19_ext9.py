"""THE II19 MAX-PUSH — STEP 1: THE PRICE ATTRIBUTION + THE FRAME-MIX DESIGN SPACE
(ii19_ext9.py).

THE USER'S DIRECTIVE (§2046!!): 'work on II19 push it to the max' — THE §1349: 'dont try
to disprove II19, try to PUSH it'!!

THE QUESTIONS:
(1) THE ATTRIBUTION (decisive!!): the word3's c = 0.000956 vs the R420's 0.001654 (the −42%!!):
    WHAT COSTS IT — THE HIST's SHAPE or THE (v, h, R) PARAMS?! THE EXPERIMENT: the R420's
    hist priced AT the word3's params (121, 9, 463) — if ~0.00096: the params dominate
    (the hist-work bounded!!); if ~0.0016: THE HIST IS THE 1.7x LEVER (the shape-hunt!!).
(2) THE CARRIER-FRAME MIX (the unexplored!!): the D4-carriers (F_j dim 5: the targets'
    detours +2+3+3 = the {2: 120, 3: 240}!!) vs THE D6-CARRIERS (F_j dim 7: the detours
    +2+5+1 = the {2: 120, 5: 120, 1: 120}!!) — the same legality, THE DIFFERENT SHAPES —
    THE PRICER DECIDES!!
(3) THE (m, mix)-GRID: THE JOINT MAX (the honest model: the word3's verified core + the
    design's contributions; the mass identity exact at every point!!).
"""
import gzip, json, sys, time
from collections import Counter, defaultdict
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

sys.path.insert(0, 'research/lorentzian-frame-cell-handoff/code/price')
from pricer import price
from mpmath import mp, mpf
mp.dps = 40
P111 = mp.mpf('0.001733052823330162099157')

def try_price(hist, v, h, R, tag):
    c, prof, d = price(dict(hist), v, h, R)
    if c is None:
        log('    %-44s v=%d h=%d R=%d: %s (%s)' % (tag, v, h, R, 'NO PRICE', d.get('error')))
        return None
    log('    %-44s v=%d h=%d R=%d: c = %s  (%+0.4f%% vs P111)' % (
        tag, v, h, R, mp.nstr(c, 14), float((c / P111 - 1) * 100)))
    return c

# ============ (1) THE ATTRIBUTION (the decisive first!!) ============
log('(1) THE ATTRIBUTION: the hist vs the params!!')
R420H = {1: 1320, 2: 1440, 4: 60, 5: 120, 8: 9}              # the R420's true hist!!
W3H = {1: 1091, 2: 1710, 3: 331, 4: 144, 6: 1, 8: 8, 9: 4}   # the word3's true hist!!
try_price(W3H, 121, 9, 463, 'A: the word3 hist @ word3 params (control)')
try_price(R420H, 121, 9, 463, 'B: the R420 hist @ word3 params!!')
try_price(W3H, 120, 8, 420, 'C: the word3 hist @ R420 params!!')
try_price(R420H, 120, 8, 420, 'D: the R420 (control)')

# ============ (2) THE CENSUS (the D4 + the D6 candidates!!) ============
log('(2) THE CENSUS: the D4/D6 candidates + the coverings!!')
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

cand = {4: [], 6: []}
for fi in range(len(frames0)):
    if dims0[fi] not in (4, 6):
        continue
    X = frozenset(frames0[fi])
    S = served(set(X))
    if S:
        cand[dims0[fi]].append((X, S))
log('    the candidates: the D4 %d | the D6 %d' % (len(cand[4]), len(cand[6])))
s4 = Counter(len(S) for (X, S) in cand[4])
s6 = Counter(len(S) for (X, S) in cand[6])
log('    the served-size hists: the D4 %s | the D6 %s' % (
    dict(sorted(s4.items())), dict(sorted(s6.items()))))

def greedy_cover(clist):
    cl = sorted(clist, key=lambda z: -len(z[1]))
    covered = set()
    groups = []
    for (X, S) in cl:
        if S - covered:
            groups.append((X, sorted(S - covered)))
            covered |= S
    return groups, covered

g4, c4 = greedy_cover(cand[4])
g6, c6 = greedy_cover(cand[6])
gm, cm = greedy_cover(cand[4] + cand[6])
log('    the greedy coverings: the D4-only m=%d (covered %d/120) | the D6-only m=%d (covered %d/120) | the MIXED m=%d (covered %d/120)' % (
    len(g4), len(c4), len(g6), len(c6), len(gm), len(cm)))
if len(c6) < v0:
    miss6 = sorted(set(prior_span) - c6)
    log('    the D6-only misses %d targets (the D4-fallback needed!!): %s...' % (
        len(miss6), miss6[:8]))
# THE MIXED's composition (the dim by the frame's line-count: 12 = the D4, 30 = the D6!!)
byd = Counter(4 if len(X) == 12 else 6 for (X, S) in gm)
a4mix = sum(len(S) for (X, S) in gm if len(X) == 12)
log('    the MIXED greedy: the D4-groups %d + the D6-groups %d | the targets on the D4s %d' % (
    byd[4], byd[6], a4mix))

# ============ (3) THE (m, mix)-GRID (the honest hist models!!) ============
log('(3) THE (m, mix)-GRID: the core + the design contributions (the mass identity exact!!)')
# THE CORE (the word3's minus the D4-design's contributions: verified at m=42!!):
#   the word3 {1: 1091, 2: 1710, 3: 331, 4: 144, 6: 1, 8: 8, 9: 4}
#   - the D4-targets {2: 120, 3: 240} - the D4-carriers {1: 42, 4: 84}
#   = the core {1: 1049, 2: 1590, 3: 91, 4: 60, 6: 1, 8: 8, 9: 4}
CORE = {1: 1049, 2: 1590, 3: 91, 4: 60, 6: 1, 8: 8, 9: 4}

def hist_model(m4, m6, a4):
    """m4 + m6 = m carriers; a4 of the 120 targets on the D4-carriers (the rest on the D6)."""
    a6 = v0 - a4
    h = dict(CORE)
    h[1] = CORE[1] + m4 + m6 + a6          # the carriers' A-builds + the D6-targets' +1s!!
    h[2] = CORE[2] + v0 + m6               # the targets' 0->cell + the D6-carriers' finals!!
    h[3] = CORE[3] + 2 * a4                # the D4-targets' detours!!
    h[4] = CORE[4] + 2 * m4                # the D4-carriers' climbs!!
    h[5] = CORE.get(5, 0) + a6             # the D6-targets' cell->F_j!!
    h[6] = CORE[6] + m6                    # the D6-carriers' {120}->F_j!!
    h = {k: z for k, z in h.items() if z}
    # THE MASS IDENTITY CHECK!!
    mass = sum(k * z for k, z in h.items())
    ident = 9 * (421 + m4 + m6) + 83 + 2 * 121 * 8
    assert mass == ident, 'THE MASS MODEL BROKEN: %d != %d!!' % (mass, ident)
    return h

log('    the self-check at (m4=42, m6=0, a4=120): %s' % (
    'MATCH!!' if hist_model(42, 0, 120) == W3H else 'MISMATCH: %s' % hist_model(42, 0, 120)))
log('    m4   m6   a4    R     c                    vs_P111')
best = (None, None, None)
grid = []
for (m4, m6, a4) in [
    (42, 0, 120),                          # the current (the control!!)
    (0, len(g6) + (v0 - len(c6)), 0) if len(c6) < v0 else (0, len(g6), 0),   # the D6-max!!
    (byd[4], byd[6], a4mix),                # the mixed greedy!!
    (30, 0, 120),                          # the LP-floor pure-D4!!
]:
    m = m4 + m6
    R = 421 + m
    h = hist_model(m4, m6, a4)
    c = try_price(h, 121, 9, R, 'm4=%d m6=%d a4=%d' % (m4, m6, a4))
    grid.append((m4, m6, a4, c))
    if c is not None and (best[0] is None or c > best[0]):
        best = (c, (m4, m6, a4), R)
log('    THE BEST: %s at m4=%s m6=%s a4=%s (R=%s)' % (
    mp.nstr(best[0], 14) if best[0] is not None else 'NONE', best[1][0], best[1][1], best[1][2], best[2]))
log('DONE — STEP 1 (the attribution + the mix!!)')

"""THE FRESH-SYSTEMS' CENSUS-BY-THE-MASTER-LAW (ii19_fresh1.py) — the §38's STEP 2!!

THE USER'S DIRECTIVE: 'keep pushing for frontier' — the #75/#1349 (PUSH!!).

THE SESSION'S PRIOR FINDING (the §151-audit of the 2-class, delivered this session!!):
the 2-class's perps were CLASS-RESTRICTED (CLS[s]==CLS[t]: the 63-line same-class demands;
the rank-18 class-blocked decoder) — NOT the true E8(+)U-multiplication (the 63 CROSS-CLASS
⊥-pairs per target missing: the word2-incompleteness class!!).  THE TRUE 2-CLASS: the kernel
analysis (lambda = P.lambda over GF(2)): the cross-class coupling forces lambda_A =
lambda_B = mu with mu = P8(2.mu) = 0 -> the kernel 0 -> the B0-rank 240 (FULL!!) -> the
deficit NEGATIVE -> DEAD.  THE 2-CLASS: CLOSED (the deeper reason!!).  VERIFIED HERE (the
control!!).

THE MASTER-LAW SCREEN (the own1's c = (256v - 288*CST)/ln-mass!!): the CST ~ rho*(h-1..h),
rho = the GF(2)-rank of B0 = I+P_S (the {t} u perp(t) rows — the DECODER'S TRUE SPAN!!).
THE FRONTIER-CLASS CONDITION: rho/v <= ~0.065-0.075 (the kernel-density >= 0.93!!):
the E8 (111/120 = 0.925: the R434-frontier's own class!), the P111 (-0.65%!!), the 121
(0.917: the -44%: the h=9's mass penalty!).  THE h-PENALTY: -288*rho per h-step: the h=8
the sweet-spot; the h >= 9 needs the rho/v <= 0.065 AND the honest-R ~ 1.0-1.3v.

THE CENSUS (the §38's candidate pool!!):
  (1) THE CONTROLS (the known rho's verified by MY OWN machinery!!): the E8 (9), the 121
      (10), the 2-class-TRUE (240?!), the 361 (241), the level-2 (531), the B1-only (9?!),
      the II_{1,17}-root+C (the E8(+)E8(+)U's analog: ~19-20?! the h=17's deficit?!).
  (2) THE T-MIXTURES (THE UNMEASURED!!): the A+C+T (T subset of the B1-class: the
      D4-aligned (the 12-root C(8,4)-sets!), the D6-aligned (the 30-root C(8,6)-sets!), the
      random-k) -> THE rho(k)-CURVES!!  + the A+T' (T' subset of the L2-class (lm,1,-1): the
      h=9 (the (0,1,-1)-direction's NONDEGENERATE span!!)) -> THE QUESTION: does ANY subset
      beat the kernel-density-0.93 barrier?!
  (3) THE SURVIVORS' PRICE (the price() grids: the shapes x the R-band!!) -> THE SHORTLIST
      (the c >= the frontier!!).
"""
import itertools, random, sys, time
from collections import Counter
from fractions import Fraction
import numpy as np

sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import price, idle_slots, host_greedy, root
from mpmath import mp, mpf
mp.dps = 40
P111 = mpf('0.001733052823330162099157')
FRONTIER = mpf('0.001744386')              # the R434 (the frontier!!)

t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

# ============ (0) THE MACHINERY ============
# THE E8 ROOT LINES (the unit convention: norm 2; the same ⊥-structure as the R420's halved!!)
E8 = []
for i in range(8):
    for j in range(i + 1, 8):
        for si in (1, -1):
            for sj in (1, -1):
                v = np.zeros(8); v[i] = si; v[j] = sj
                E8.append(v)
for s in itertools.product([1, -1], repeat=8):
    if s.count(-1) % 2 == 0:
        E8.append(np.array(s) / 2)
def canon(v):
    for x in v:
        if x != 0:
            return tuple(v) if x > 0 else tuple(-v)
    return tuple(v)
r8 = {}
for v in E8: r8[canon(v)] = np.array(v)
AL = list(r8.values())                    # the 120 E8 root lines
# the integral norm-4 vectors (the level-2 class's lm's!!)
n4 = {}
norm4 = []
for i in range(8):
    for s in (2, -2):
        v = np.zeros(8); v[i] = s
        norm4.append(v)
for combo in itertools.combinations(range(8), 4):
    for signs in itertools.product([1, -1], repeat=4):
        v = np.zeros(8)
        for k, idx in enumerate(combo): v[idx] = signs[k]
        norm4.append(v)
for v in norm4: n4[canon(v)] = np.array(v)
N4 = list(n4.values())
log('(0) the E8 lines %d | the norm-4 classes %d' % (len(AL), len(N4)))

# THE FORM on the 10-dim (alpha, a, b): x.x' + a.d + b.c  (the E8(+)U embedding!!)
FORM10 = np.zeros((10, 10)); FORM10[:8, :8] = np.eye(8); FORM10[8, 9] = FORM10[9, 8] = 1.0
FORM18 = np.zeros((18, 18)); FORM18[:16, :16] = np.eye(16); FORM18[16, 17] = FORM18[17, 16] = 1.0

def sys_ii19(kind):
    """the line-tuples (alpha, a, b) by class: 'A', 'A+C', 'A+B1', 'A+B1+B2+C', 'L2', 'B1',
    'A+T' handled separately (the mixture builder below)."""
    L = []
    if kind in ('A', 'A+C', 'A+B1', 'A+B1+B2+C'):
        for al in AL: L.append((al, 0, 0))
    if kind in ('A+B1', 'A+B1+B2+C'):
        for al in AL: L.append((al, 1, 0))
    if kind == 'A+B1+B2+C':
        for al in AL: L.append((al, 0, 1))
        L.append((np.zeros(8), 1, 1))
    if kind == 'A+C':
        L.append((np.zeros(8), 1, 1))
    if kind == 'B1':
        for al in AL: L.append((al, 1, 0))
    if kind == 'L2':                      # the SS1810: the 360 + the norm-4-(lm,1,-1) + the C!!
        for al in AL:
            L.append((al, 0, 0)); L.append((al, 1, 0)); L.append((al, 0, 1))
        for lm in N4: L.append((lm, 1, -1))
        L.append((np.zeros(8), 1, 1))
    return L

def mixture(base, T):
    """base: the list of tuples; T: the extra tuples (the B1/L2 subsets!!)."""
    return base + list(T)

def gram(lines, form):
    co = np.array([list(al) + [a, b] for al, a, b in lines])
    Gm = co @ form[:co.shape[1], :co.shape[1]] @ co.T
    return co, Gm

def perps_and_rho(co, Gm):
    """the perp masks (exactly-0 test on the float Gram), the B0 = {t} u perp(t), the GF(2) rank."""
    n = len(co)
    Z = np.abs(Gm) < 1e-9
    B0 = []
    for t in range(n):
        m = 1 << t
        row = Z[t]
        for j in range(n):
            if j != t and row[j]:
                m |= 1 << j
        B0.append(m)
    basis = {}
    rank = 0
    for r in B0:
        while r:
            p = (r & -r).bit_length() - 1
            if p in basis:
                r ^= basis[p]
            else:
                basis[p] = r
                rank += 1
                break
    perp_sizes = [bin(m).count('1') - 1 for m in B0]
    return B0, rank, perp_sizes

def span_and_h(co, form):
    """the EXACT rref (Fractions!!) -> the span dim; the span-Gram determinant -> the h
    (the +1 if the span's form DEGENERATE (the radical killed by the +1 U-direction!!))."""
    d = co.shape[1]
    rows = [[Fraction(x) for x in co[i]] for i in range(co.shape[0])]
    # the rref (the exact!!)
    piv = []
    r0 = 0
    for c in range(d):
        p = None
        for i in range(r0, len(rows)):
            if rows[i][c] != 0:
                p = i; break
        if p is None: continue
        rows[r0], rows[p] = rows[p], rows[r0]
        pv = rows[r0][c]
        rows[r0] = [x / pv for x in rows[r0]]
        for i in range(len(rows)):
            if i != r0 and rows[i][c] != 0:
                f = rows[i][c]
                rows[i] = [x - f * y for x, y in zip(rows[i], rows[r0])]
        piv.append(c); r0 += 1
        if r0 == len(rows): break
    s = r0
    bas = [[Fraction(0)] * d for _ in range(s)]
    for i, c in enumerate(piv): bas[i] = rows[i]
    # the span-Gram (the Fractions!!): G_ij = bas_i . form . bas_j
    FG = [[Fraction(x) for x in form[r]] for r in range(d)]
    def ipf(u, v):
        return sum(Fraction(u[k]) * FG[k][j] * Fraction(v[j]) for k in range(d) for j in range(d))
    GM = [[ipf(bas[i], bas[j]) for j in range(s)] for i in range(s)]
    deg = False
    if s:
        # the exact determinant test (the Gaussian elimination over the Fractions!!)
        A = [row[:] for row in GM]
        rankG = 0
        for c in range(s):
            p = None
            for i in range(rankG, s):
                if A[i][c] != 0:
                    p = i; break
            if p is None: continue
            A[rankG], A[p] = A[p], A[rankG]
            pv = A[rankG][c]
            A[rankG] = [x / pv for x in A[rankG]]
            for i in range(s):
                if i != rankG and A[i][c] != 0:
                    f = A[i][c]
                    A[i] = [x - f * y for x, y in zip(A[i], A[rankG])]
            rankG += 1
        deg = (rankG < s)
    h = s + (1 if deg else 0)
    return s, deg, h

def screen(lines, tag, form=FORM10, price_it=True, extra_note=''):
    """THE FULL PIPELINE: the system -> the Gram -> the rho -> the h -> the deficit-band ->
    (the survivors: the price grids!!) -> the verdict line."""
    co, Gm = gram(lines, form)
    n = len(lines)
    B0, rho, psz = perps_and_rho(co, Gm)
    s, deg, h = span_and_h(co, form)
    kd = (n - rho) / n if n else 0.0
    d_lo = 256 * n - 288 * rho * h
    d_hi = 256 * n - 288 * rho * max(1, h - 1)
    log('    %-26s v=%-4d span=%-2d h=%-2d rho=%-4d (kern %d/%d=%.3f)  deficit[%d..%d]  %s'
        % (tag, n, s, h, rho, n - rho, n, kd, d_lo, d_hi, extra_note))
    res = dict(tag=tag, v=n, h=h, rho=rho, span=s, kd=kd, d_lo=d_lo, d_hi=d_hi,
               perp=Counter(psz))
    if price_it and d_hi > 0 and h <= 12:      # the h <= 12: the viable window class!!
        res['price'] = price_grids(n, h, rho)
    else:
        res['price'] = None
    return res

# ============ THE PRICE STAGE (the DAMPED fixed-point + the validation battery!!) ============
def price_damped(local, v, h, R, K=4, T=32):
    """THE PRICE()'s UNDAMPED FIXED-POINT OSCILLATES (the host_greedy's order is q-dependent:
    the map q->q2 has period-2 cycles and the 30-iteration loop returns the LAST iterate =
    GARBAGE at some (hist, R)!!  THIS: the damped q <- (q+q2)/2 loop + the convergence flag
    (the true fixed-point q* = F(q*) is UNCHANGED by the damping!!)."""
    L = 2 * K + 1; a = h - 1; m = 1 + L * a; w = h
    slots = {}
    for c in idle_slots(K, a):
        slots[c] = slots.get(c, 0) + 2 * v
    nres = R * L
    W = 2 * K * v * T
    cap = sum(n * (c // w) for c, n in slots.items())
    if nres > cap:
        return None, None, 'hosting wall'
    q = mpf('0.0017')
    q2 = None
    for it in range(200):
        rem = host_greedy(slots, nres, w, q, m)
        prof = {}
        for r, z in local.items(): prof[r] = prof.get(r, 0) + z * T * L
        for r, z in rem.items(): prof[r] = prof.get(r, 0) + z * T
        q2 = root(prof, m, W)
        if q2 is None:
            return None, prof, 'no root'
        if abs(q2 - q) < mpf(10) ** -25:
            return q2, prof, 'converged'
        q = (q + q2) / 2
    return q2, prof, 'DAMPED-200 (the oscillation damped!!)'

def hist_D(v, h, R, CST, rho):
    """the R420's own climb fractions (the calibrated family!!) on the climb mass + the
    retained's copy children {h-1: rho} (the 121's own {8: 9}-structure!!) — the INT-EXACT!!"""
    climb = h * R + 2 * v * (h - 1)
    hist = {1: int(round(0.262 * climb)), 2: int(round(0.571 * climb / 2.0)),
            4: int(round(0.048 * climb / 4.0)), 5: int(round(0.119 * climb / 5.0)),
            max(1, h - 1): rho}
    mass = sum(k * z for k, z in hist.items())
    dd = (h * R + CST + 2 * v * (h - 1)) - mass
    guard = 0
    while dd != 0 and guard < 100000:
        guard += 1
        if dd > 0:
            hist[1] = hist.get(1, 0) + 1; dd -= 1
        else:
            k = max(z for z in hist if hist[z] > 0)
            hist[k] -= 1; dd += k
            if hist[k] == 0: del hist[k]
    return {k: int(z) for k, z in hist.items() if z}

def price_grids(v, h, rho):
    """the c-band at the R-grid x the CST-band [rho(h-1) .. rho.h] (the frames' honest
    bracket!!) -> the best c (vs the frontier!!)."""
    CSTs = sorted(set([rho * max(1, h - 1), rho * h]))
    out = {}
    best = None
    for CST in CSTs:
        for R in sorted(set(int(x) for x in [1.1 * v, 1.3 * v, 1.6 * v, 2.0 * v, 2.5 * v,
                                             3.0 * v, 3.5 * v])):
            hist = hist_D(v, h, R, CST, rho)
            c, prof, stat = price_damped(hist, v, h, R)
            if c is None:
                out[(CST, R)] = None
                continue
            out[(CST, R)] = c
            if best is None or c > best[0]:
                best = (c, R, CST, stat)
    return dict(CSTs=CSTs, grid=out, best=best)

# THE VALIDATION BATTERY (the oscillation-fix's proof!!)!!
log('THE VALIDATION BATTERY (the damped price vs the published!!)!!')
R420H = {1: 1320, 2: 1440, 4: 60, 5: 120, 8: 9}
P111H = {1: 1321, 2: 1342, 3: 80, 4: 47, 5: 102, 6: 10, 7: 18}
W3H = {1: 1091, 2: 1710, 3: 331, 4: 144, 6: 1, 8: 8, 9: 4}
for (hst, vv, hh, RR, pub, nm) in [
        (R420H, 120, 8, 420, '0.001653826988146798944268', 'the R420 true hist'),
        (P111H, 111, 8, 439, '0.001733052823330162099157', 'the P111 hist'),
        (W3H, 121, 9, 463, '0.0009558217144810735671339', 'the word3 true hist')]:
    c1, p1, s1 = price_damped(hst, vv, hh, RR)
    c2, p2, d2 = price(dict(hst), vv, hh, RR)
    log('    %-24s damped: %s (%s) | the undamped: %s | the published: %s' % (
        nm, mp.nstr(c1, 12) if c1 is not None else 'NONE', s1,
        mp.nstr(c2, 12) if c2 is not None else 'NONE', pub))

# ============ (1) THE CONTROLS (the known rho's verified!!) ============
log('(1) THE CONTROLS — the known decoder-ranks verified by the census machinery!!')
controls = []
controls.append(screen(sys_ii19('A'), 'E8 (A-only)', FORM10,
                        extra_note='(the h=8; the rho=9; the R434-class!)'))
controls.append(screen(sys_ii19('A+C'), '121 (A+C)'))
controls.append(screen(sys_ii19('A+B1'), '2-class TRUE (A+B1)'))
controls.append(screen(sys_ii19('A+B1+B2+C'), '361 (A+B1+B2+C)'))
controls.append(screen(sys_ii19('L2'), 'level-2 (the SS1810!)'))
controls.append(screen(sys_ii19('B1'), 'B1-only'))
log('    the II_{1,17} analog (the E8(+)E8(+)U): the root-class + the special!!')
L17 = []
for al in AL: L17.append((np.concatenate([al, np.zeros(8)]), 0, 0))
for al in AL: L17.append((np.concatenate([np.zeros(8), al]), 0, 0))
L17.append((np.zeros(16), 1, 1))
def gram17(lines):
    co = np.array([[*(list(x)), a, b] for x, a, b in lines])
    return co, co @ FORM18 @ co.T
co17, Gm17 = gram17(L17)
B017, rho17, psz17 = perps_and_rho(co17, Gm17)
s17, deg17, h17 = span_and_h(co17, FORM18)
log('    %-26s v=%-4d span=%-2d h=%-2d rho=%-4d (kern %d/%d=%.3f)  deficit[%d..%d]'
    % ('II17-root+C', len(L17), s17, h17, rho17, len(L17) - rho17, len(L17),
       (len(L17) - rho17) / len(L17),
       256 * len(L17) - 288 * rho17 * h17, 256 * len(L17) - 288 * rho17 * max(1, h17 - 1)))

# ============ (2) THE T-MIXTURES (the unmeasured rho(k)-curves!!) ============
log('(2) THE T-MIXTURES — the rho(k)-curves (the decisive unmeasured!!)')
random.seed(12345)
BASE_AC = sys_ii19('A+C')
BASE_A = sys_ii19('A')
def B1_T(idx): return [(AL[i], 1, 0) for i in idx]
def L2_T(idx): return [(N4[i], 1, -1) for i in idx]

# the structured T's: the D4-aligned (the C(8,4) 12-root sets!!), the D6-aligned (the 30!!)
def d4_roots(combo):
    keys = []
    for (i, j) in itertools.combinations(combo, 2):
        for v in (np.eye(8)[i] + np.eye(8)[j], np.eye(8)[i] - np.eye(8)[j]):
            c = canon(v)
            if c in r8 and c not in keys:
                keys.append(c)
    return [r8[c] for c in keys]

log('    the D4-subsystem check: the 12-root sets (the C(8,4) coordinate 4-sets!!)')
mix_results = []
for (combo, nm) in [((0, 1, 2, 3), 'D4[0-3]'), ((0, 1, 4, 5), 'D4[0,1,4,5]')]:
    roots = d4_roots(combo)
    log('      %s: %d root lines (expect 12!!)' % (nm, len(roots)))
    if len(roots) >= 2:
        idxB1 = [i for i, al in enumerate(AL) if any(np.allclose(al, r) for r in roots)]
        mix_results.append(screen(mixture(BASE_AC, B1_T(idxB1)), 'A+C+B1(D4 %s)' % nm))
        mix_results.append(screen(mixture(BASE_A, B1_T(idxB1)), 'A+B1(D4 %s)' % nm))

for k in (1, 2, 4, 8, 12, 24, 60, 120):
    idx = random.sample(range(120), k)
    mix_results.append(screen(mixture(BASE_AC, B1_T(idx)), 'A+C+B1(rand k=%d)' % k,
                            price_it=(k <= 24)))
for k in (1, 2, 4, 8, 12, 24, 60, 120, 240, 480):
    idx = random.sample(range(len(N4)), min(k, len(N4)))
    mix_results.append(screen(mixture(BASE_A, L2_T(idx)), 'A+L2(rand k=%d)' % k,
                              price_it=(k <= 24)))
# the L2-structured: the 2e_i-class (the 4!) + the (1111)-class!!
idx2e = [i for i, v in enumerate(N4) if len(np.nonzero(v)[0]) == 1]
idx41 = [i for i, v in enumerate(N4) if len(np.nonzero(v)[0]) == 4]
log('    the L2 structured: the 2e_i-class %d | the (1111)-class %d' % (len(idx2e), len(idx41)))
mix_results.append(screen(mixture(BASE_A, L2_T(idx2e)), 'A+L2(2e_i k=%d)' % len(idx2e)))
mix_results.append(screen(mixture(BASE_A, L2_T(idx41[:24])), 'A+L2((1111) k=24)'))
mix_results.append(screen(mixture(BASE_AC, L2_T(idx2e)), 'A+C+L2(2e_i k=%d)' % len(idx2e)))

# ============ (3) THE SHORTLIST (the deficit-positive + the price verdicts!!) ============
log('(3) THE SHORTLIST — the survivors (the deficit-positive) x the price grids!!')
allres = controls + mix_results
alive = [r for r in allres if r['d_hi'] > 0]
log('    the deficit-positive: %d of %d' % (len(alive), len(allres)))
for r in alive:
    pr = r.get('price')
    if pr and pr.get('best'):
        c, R, CST, stat = pr['best']
        log('    %-26s v=%-4d h=%-2d rho=%-3d CST-band%s: the best c=%.9f at R=%d (CST=%d)  (%+0.2f%% vs frontier)  [%s]'
            % (r['tag'], r['v'], r['h'], r['rho'], pr['CSTs'], float(c), R, CST,
               float((c / FRONTIER - 1) * 100), stat))
        log('        the full c(R) grid: %s' % (
            ' | '.join('C%d/R%d: %s' % (C0, R0, ('%.6f' % float(cc)) if cc is not None else 'X')
                       for (C0, R0), cc in sorted(pr['grid'].items()))))
    elif pr is not None:
        log('    %-26s v=%-4d h=%-2d rho=%-3d: NO ROOTS at the R-grid (the regime too light!!)'
            % (r['tag'], r['v'], r['h'], r['rho']))
log('    (the rest: the deficit NEGATIVE (the rho*(h-1) >= 256v/288!!) — the DEAD class!!)')
log('DONE — THE FRESH-SYSTEMS CENSUS!!')

"""THE I_{1,9}-ODD CLASSES CENSUS (ii19_i19odd.py) — the record's remaining-item (d)!!

THE SYSTEM: the odd-unimodular Lorentzian I_{1,9} = Z^10 with the form n(x) = x0^2 - sum_{i>=1} xi^2.
THE RECORD's finding: the lowest class ((2,1,1): 144 lines, norm +2) is PERP-FREE (the identity-class:
rho = v: DEAD!!) — the HIGHER CLASSES: UNMEASURED (the SS1571's item (d)!!).

THE STRUCTURAL INSIGHT (the fresh!!): the (0,·)-classes (the ZERO in the positive slot) live
ENTIRELY in the 9-dim NEGATIVE-DEFINITE subspace -> THE SPAN h = 9 (NO h=10 PENALTY!!):
    C011  = (0,1,1):    norm -2, v = 72    (THE D9 ROOT SYSTEM!!)
    C01111= (0,1,1,1,1):norm -4, v = 1008  (the D9's second shell!)
    C0211 = (0,2,1,1):  norm -6, v = 1008
    C022  = (0,2,2):    norm -8, v = 36
THE h=10 CLASSES (the positive slot used):
    C211  = (2,1,1):    norm +2, v = 144   (the record's PERP-FREE control!!)
    C2211 = (2,2,1,1):  norm -2, v = 2016
THE QUESTIONS: (1) the rho of the D9-root class (the E8-analog at h=9?!); (2) the rho(k)-law
for the shells (the +2/line or the STRUCTURED COLLAPSE?!); (3) ANY union with rho/v <= 0.075
+ a positive deficit = THE FRONTIER-CLASS CANDIDATE (the breakthrough!!).
"""
import itertools, sys, time
from collections import Counter
from fractions import Fraction
import numpy as np

sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import idle_slots, host_greedy, root
from mpmath import mp, mpf
mp.dps = 40
FRONTIER = mpf('0.001744386')

t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

# ============ (0) THE CLASS ENUMERATION (the I_{1,9} = diag(1, -1^9)!!) ============
def canon(v):
    for x in v:
        if x != 0:
            return tuple(v) if x > 0 else tuple(-x for x in v)
    return tuple(v)

def enum_class(pattern, pos2):
    """pattern: the tuple of |coords| in the NEGATIVE slots; pos2: True -> a +-2 in the
    POSITIVE slot (x0 = +-2).  Yields the up-to-sign lines."""
    seen = {}
    k = len(pattern)
    for sl in itertools.permutations(range(1, 10), k):
        for signs in itertools.product([1, -1], repeat=k):
            if pos2:
                for s0 in (1, -1):
                    v = [2 * s0] + [0] * 9
                    for idx, (pc, sg) in enumerate(zip(pattern, signs)):
                        v[sl[idx]] = pc * sg
                    seen[canon(v)] = True
            else:
                v = [0] + [0] * 9
                for idx, (pc, sg) in enumerate(zip(pattern, signs)):
                    v[sl[idx]] = pc * sg
                seen[canon(v)] = True
    return [list(k_) for k_ in seen]

CLASSES = {
    'C011':   (enum_class((1, 1), False), -2, 9),
    'C01111': (enum_class((1, 1, 1, 1), False), -4, 9),
    'C0211':  (enum_class((2, 1, 1), False), -6, 9),
    'C022':   (enum_class((2, 2), False), -8, 9),
    'C211':   (enum_class((1, 1), True), +2, 10),
    'C2211':  (enum_class((2, 1, 1), True), -2, 10),
}
FORM = np.diag([1.0] + [-1.0] * 9)
for nm, (L, nrm, hh) in CLASSES.items():
    norms = [v[0] ** 2 - sum(x * x for x in v[1:]) for v in L]
    assert all(n == nrm for n in norms), '%s: the norm mismatch!!' % nm
    log('(0) %-8s: %5d lines (the norm %+d, the expected h=%d) [check %d]' % (
        nm, len(L), nrm, hh, norms[0]))

# ============ (1) THE MACHINERY (the census port!!) ============
def gram(lines):
    co = np.array(lines, dtype=float)
    return co, co @ FORM @ co.T

def perps_and_rho(co, Gm):
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

def span_and_h(co):
    d = co.shape[1]
    rows = [[Fraction(x) for x in co[i]] for i in range(co.shape[0])]
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
    bas = [rows[i] for i in range(s)]
    FG = [[Fraction(x) for x in FORM[r]] for r in range(d)]
    def ipf(u, v):
        return sum(Fraction(u[k]) * FG[k][j] * Fraction(v[j])
                   for k in range(d) for j in range(d))
    GM = [[ipf(bas[i], bas[j]) for j in range(s)] for i in range(s)]
    deg = False
    if s:
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
    return s, deg, s + (1 if deg else 0)

def price_damped(local, v, h, R, K=4, T=32):
    L = 2 * K + 1; a = h - 1; m = 1 + L * a; w = h
    slots = {}
    for c in idle_slots(K, a):
        slots[c] = slots.get(c, 0) + 2 * v
    nres = R * L
    W = 2 * K * v * T
    cap = sum(n * (c // w) for c, n in slots.items())
    if nres > cap:
        return None, None, 'hosting wall'
    q = mpf('0.0017'); q2 = None
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
    return q2, prof, 'DAMPED-200'

def hist_D(v, h, R, CST, rho):
    climb = h * R + 2 * v * (h - 1)
    hist = {1: int(round(0.262 * climb)), 2: int(round(0.571 * climb / 2.0)),
            4: int(round(0.048 * climb / 4.0)), 5: int(round(0.119 * climb / 5.0)),
            max(1, h - 1): rho}
    mass = sum(k * z for k, z in hist.items())
    dd = (h * R + CST + 2 * v * (h - 1)) - mass
    guard = 0
    while dd != 0 and guard < 200000:
        guard += 1
        if dd > 0:
            hist[1] = hist.get(1, 0) + 1; dd -= 1
        else:
            k = max(z for z in hist if hist[z] > 0)
            hist[k] -= 1; dd += k
            if hist[k] == 0: del hist[k]
    return {k: int(z) for k, z in hist.items() if z}

def screen(lines, tag, price_it=True):
    co, Gm = gram(lines)
    n = len(lines)
    B0, rho, psz = perps_and_rho(co, Gm)
    s, deg, h = span_and_h(co)
    kd = (n - rho) / n if n else 0.0
    d_lo = 256 * n - 288 * rho * h
    d_hi = 256 * n - 288 * rho * max(1, h - 1)
    log('    %-30s v=%-5d span=%-2d h=%-2d rho=%-5d (kern %d/%d=%.3f)  deficit[%d..%d]  perps %s'
        % (tag, n, s, h, rho, n - rho, n, kd, d_lo, d_hi,
           dict(sorted(Counter(psz).items())) if len(set(psz)) < 8 else
           ('min %d / max %d' % (min(psz), max(psz)))))
    res = dict(tag=tag, v=n, h=h, rho=rho, kd=kd, d_lo=d_lo, d_hi=d_hi)
    if price_it and d_hi > 0 and h <= 10:
        CSTs = sorted(set([rho * max(1, h - 1), rho * h]))
        best = None
        grid = {}
        for CST in CSTs:
            for R in sorted(set(int(x) for x in [1.1 * n, 1.3 * n, 1.6 * n, 2.0 * n,
                                                2.5 * n, 3.0 * n, 3.5 * n])):
                hist = hist_D(n, h, R, CST, rho)
                c, prof, stat = price_damped(hist, n, h, R)
                grid[(CST, R)] = c
                if c is not None and (best is None or c > best[0]):
                    best = (c, R, CST, stat)
        res['grid'] = grid
        res['best'] = best
        if best:
            log('        THE BEST: c=%.9f at R=%d (CST=%d) = %+.2f%% vs frontier [%s] | the grid %s'
                % (float(best[0]), best[1], best[2], float((best[0] / FRONTIER - 1) * 100),
                   best[3], ' | '.join('C%d/R%d:%s' % (C0, R0, ('%.6f' % float(cc)) if cc is not None else 'X')
                                       for (C0, R0), cc in sorted(grid.items()))))
    return res

# ============ (2) THE SCREENS ============
log('(2) THE SINGLE CLASSES (the rho-question!!)')
sing = {}
for nm in ('C011', 'C022', 'C01111', 'C0211', 'C211', 'C2211'):
    sing[nm] = screen(CLASSES[nm][0], nm, price_it=(nm in ('C011', 'C022')))

log('(3) THE h=9 UNIONS (the NO-PENALTY family!!)')
def U(*nms):
    L = []
    for nm in nms:
        L.extend([list(v) for v in CLASSES[nm][0]])
    return L
u9 = {}
u9['D9+C022'] = screen(U('C011', 'C022'), 'C011 U C022 (108)')
u9['D9+2nd-shell'] = screen(U('C011', 'C01111'), 'C011 U C01111 (1080)')
u9['D9+C0211'] = screen(U('C011', 'C0211'), 'C011 U C0211 (1080)')
u9['THE FULL h=9'] = screen(U('C011', 'C022', 'C01111', 'C0211'), 'ALL the (0,.)-family (2124)')

log('(4) THE h=10 UNIONS (the penalty class)')
u10 = {}
u10['C211+D9'] = screen(U('C211', 'C011'), 'C211 U C011 (216)')
u10['C2211+D9'] = screen(U('C2211', 'C011'), 'C2211 U C011 (2088)')
u10['THE FULL'] = screen(U('C211', 'C2211', 'C011', 'C022', 'C01111', 'C0211'),
                         'ALL classes (4260)')

log('(5) THE VERDICT — the frontier-class condition rho/v <= 0.075 + deficit > 0!!')
allr = dict(sing, **u9, **u10)
cands = [(nm, r) for nm, r in allr.items() if r['kd'] >= 0.93 and r['d_hi'] > 0]
for nm, r in cands:
    log('    THE CANDIDATE: %s v=%d h=%d rho=%d kd=%.3f deficit[%d..%d]' % (
        nm, r['v'], r['h'], r['rho'], r['kd'], r['d_lo'], r['d_hi']))
if not cands:
    log('    NO frontier-class candidate — the I_{1,9}-odd family: CLOSED (the §151 done!!)')
log('DONE — THE I_{1,9}-ODD CENSUS!!')

"""Schedule levers for the B_K bit template (exact; 8-bank scalar model of research/e8-early-reset-kernel/bit_global.py).

1. The shipped recipe composes to the identity (control).
2. Unsplit idle stretches would reprice P111-tuned at +6.13% (same local profile, idle slots without the bridge split).
3. Split-free schedules are impossible with unit-shear locals unless every pair does 3 locals:
   (a) bridges only at block junctions (plus start/end): the last pair is touched only by the last junction and its
       own block, so that junction is +-identity and the block a signed swap; induction inward (checked by search on
       the two 4-pair patterns (3,1,2,3), (3,2,1,3) with junction words up to length 2, coefficients in {-2..2});
   (b) two pairs active in the same stages with 2 locals each: L2 J L1 is never anti-diagonal (algebra in the README
       notes; checked by search with bridge words up to length 2).
4. Independent 3-local triples price far below P111-tuned (or hit the hosting wall).
usage: python3 schedule_checks.py"""
import itertools, sys, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'price'))
import pricer as P
import mpmath as mp
def I(n): return np.eye(n, dtype=np.int64)
def loc(n, p, rev):
    M = I(n)
    if rev: M[2 * p, 2 * p + 1] = -1
    else: M[2 * p + 1, 2 * p] = 1
    return M
def br(n, d, s, c):
    M = I(n); M[2 * d, 2 * s] += c; M[2 * s + 1, 2 * d + 1] -= c; return M
def ex(n):
    M = np.zeros((n, n), dtype=np.int64)
    for j in range(n // 2): M[2 * j, 2 * j + 1] = 1; M[2 * j + 1, 2 * j] = -1
    return M
def comp(ops, n):
    T = I(n)
    for M in ops: T = M @ T
    return T
def anti(W):
    X = list(range(0, len(W), 2)); Y = list(range(1, len(W), 2))
    return not W[np.ix_(X, X)].any() and not W[np.ix_(Y, Y)].any()
K = 4; n = 8
ops = [loc(n, 0, False)]
for j in range(K):
    ops.append(loc(n, j, True))
    if j < K - 1: ops.append(br(n, j, j + 1, 1))
    ops.append(loc(n, j, False))
    if j < K - 1: ops.append(br(n, j, j + 1, -1))
for j in reversed(range(K - 1)): ops.append(br(n, j + 1, j, 1))
ops.append(ex(n))
print('1. shipped recipe composes to identity:', (comp(ops, n) == I(n)).all())
ref = mp.mpf('0.001733427039589844')
tuned = {1: 1323, 2: 1342, 3: 79, 4: 44, 5: 102, 6: 11, 7: 19}
c0 = P.price(tuned, 111, 8, 439)[0]
orig = P.idle_slots
P.idle_slots = lambda K_, a, split=True: orig(K_, a, False)
c1 = P.price(tuned, 111, 8, 439)[0]; P.idle_slots = orig
print('2. P111-tuned with unsplit idle stretches: %s (%+.2f%%)' % (mp.nstr(c1, 10), float((c1 / c0 - 1) * 100)))
C = [c for c in range(-2, 3) if c]
def jw(j, maxj=2):
    seen = {}
    for L in range(maxj + 1):
        for w in itertools.product([(j, j + 1, c) for c in C] + [(j + 1, j, c) for c in C], repeat=L):
            M = comp([br(n, *b) for b in w], n); seen.setdefault(M.tobytes(), M)
    return list(seen.values())
JW = [jw(j) for j in range(K - 1)]; sols = 0
for lens in ((3, 1, 2, 3), (3, 2, 1, 3)):
    for orient in itertools.product(*[list(itertools.product((False, True), repeat=l)) for l in lens]):
        S = [comp([loc(n, p, r) for r in o], n) for p, o in enumerate(orient)]
        for J0 in JW[0]:
            A1 = S[1] @ J0 @ S[0]
            for J1 in JW[1]:
                A2 = S[2] @ J1 @ A1
                sols += sum(anti(S[3] @ J2 @ A2) for J2 in JW[2])
print('3a. junction-only bridge schedules for (3,1,2,3)/(3,2,1,3), words <= 2: solutions', sols)
n2 = 4; sols2 = 0
JW2 = {}
for L in range(3):
    for w in itertools.product([(0, 1, c) for c in C] + [(1, 0, c) for c in C], repeat=L):
        M = comp([br(n2, *b) for b in w], n2); JW2.setdefault(M.tobytes(), M)
JW2 = list(JW2.values())
for oA in itertools.product((False, True), repeat=2):
    for oB in itertools.product((False, True), repeat=2):
        L1 = loc(n2, 0, oA[0]) @ loc(n2, 1, oB[0]); L2 = loc(n2, 0, oA[1]) @ loc(n2, 1, oB[1])
        sols2 += sum(anti(L2 @ J @ L1) for J in JW2)
print('3b. two simultaneous pairs with 2 locals each, middle bridge words <= 2: solutions', sols2)
sys.path.insert(0, HERE)
from genprice import price as gprice, triples_idle
for pairs in (3, 4):
    L, idle = triples_idle(pairs, 7)
    c, d = gprice(tuned, 111, 8, 439, L, pairs, idle)
    print('4. independent triples, %d pairs, %d stages:' % (pairs, L), ('%+.2f%%' % float((c / ref - 1) * 100)) if c else d)

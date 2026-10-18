"""THE nat115: THE DEEP-PUNCTURE SCAN (j=13..60!!) — the large breakthrough's floor-hunt!!
THE LAWS (the nat114!!): the rank 9 (the j-independence!!) | the {7: j} (the dim-7-gather-per-removed!!) |
  the cst = 72 - j | the measured sensitivities: +1.89%/line, -3.12%/cst -> the +1.23%/depth-line!!
THE QUESTIONS: (1) how deep do the laws hold?! (2) the perp-structures' viability (the B0-patterns (the targets!!))!
  (3) the removal-set's legality (the Gram (the form (the live-system!!!))); (4) THE HONEST PRICE at each depth
  (the pricer at (v, 8, R~3.5v, cst=72-j) + the nat109-style shape (the r434-mirror's own!!))!!
"""
import json
from collections import Counter
from fractions import Fraction
import os, sys
import mpmath as mp
mp.mp.dps = 50
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
from pricer import price

log = print
SPEC = json.load(open('ii19_nat69_spec.json', 'rt'))
L120 = [tuple(int(c) for c in l) for l in SPEC['lines']]
def dot(a, b): return sum(x * y for x, y in zip(a, b))
RM9 = [6, 58, 81, 88, 97, 109, 112, 115, 116]

def rref_gf2(rows, n):
    m = [list(r) for r in rows]; r = 0
    for c in range(n):
        p = next((i for i in range(r, len(m)) if m[i][c]), None)
        if p is None: continue
        m[r], m[p] = m[p], m[r]
        for i in range(len(m)):
            if i != r and m[i][c]:
                m[i] = [(a ^ b) for a, b in zip(m[i], m[r])]
        r += 1
    return m[:r]

def rref_rat(rows, n):
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

# THE REMOVAL-SET: the r434-9 + the greedy ⊥-clustering extensions!!
ext = []
cur = set(RM9)
while len(cur) < 60:
    best, bs = None, -1
    for i in range(120):
        if i in cur: continue
        P = [s for s in range(120) if s != i and dot(L120[i], L120[s]) == 0]
        sc = len([s for s in P if s in cur])
        if sc > bs: bs, best = sc, i
    cur.add(best); ext.append(best)

def deep_census(j, cap=1023):
    rm = set(RM9 + ext[:max(0, j - 9)]) if j > 9 else set(RM9[:j])
    L = [l for i, l in enumerate(L120) if i not in rm]
    Vn = len(L)
    B0 = []
    perp_sz = Counter()
    for t in range(Vn):
        P = [s for s in range(Vn) if s != t and dot(L[t], L[s]) == 0]
        perp_sz[len(P)] += 1
        row = [0] * Vn; row[t] = 1
        for s in P: row[s] = 1
        B0.append(row)
    M = rref_gf2(B0, Vn)
    rank = len(M)
    d7 = 0; d1 = 0
    for mask in range(1, min(1 << rank, cap) + 1):
        v = [0] * Vn
        for i in range(rank):
            if (mask >> i) & 1:
                v = [(a ^ b) for a, b in zip(v, M[i])]
        sup = [i for i in range(Vn) if v[i]]
        if not sup: continue
        d = len(rref_rat([list(L[i]) for i in sup], 8))
        if d == 7: d7 += 1
        if d <= 1: d1 += 1
    return Vn, rank, d7, d1, dict(sorted(perp_sz.items()))

log('THE nat115: THE DEEP-SCAN (the j=9..60!!): the rank | the {7: j}?! | the perps | THE PRICE!!')
P111 = mp.mpf('0.001733052823330162099157')
def price_at(v, cst, R):
    # the nat109-style: the r434-mirror's shape scaled: the rank-1/2-heavy favorable!!
    mass = 8 * R + cst + 2 * v * 7
    h1 = int(mass * 0.44); h2 = int((mass - h1) * 0.82 / 2)
    rest_m = mass - h1 - 2 * h2
    h5 = rest_m // 2; h3 = rest_m - h5
    hist = {1: h1, 2: h2, 3: h3, 5: h5}
    m2 = sum(r * c for r, c in hist.items())
    hist[1] += mass - m2
    c, prof, d = price(hist, v, 8, R)
    return c

log('  j |  v | rank | d7 | d1 | the perps        | cst | R~3.5v | c (favorable-shape!!)')
for j in (9, 12, 15, 18, 21, 24, 27, 30, 36, 42, 48, 54, 60):
    Vn, rank, d7, d1, ps = deep_census(j)
    cst = 7 * j + 8 * max(0, rank - j) if j <= rank else 7 * rank
    R = int(3.5 * Vn)
    c = price_at(Vn, cst, R)
    pv = ('%+.2f%%' % (float((c - P111) / P111) * 100)) if c else 'NO-ROOT'
    log('  %2d | %3d | %4d | %3d | %2d | %s | %3d | %4d | %s %s' % (j, Vn, rank, d7, d1, str(ps)[:40], cst, R, ('%.6f' % float(c)) if c else '-', pv))

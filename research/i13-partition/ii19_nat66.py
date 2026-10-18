"""THE P111 STRUCTURE CENSUS (ii19_nat66.py) — the system's true identity!!

THE nat64/nat65 DISCOVERY: the P111's lines are NOT the E8-roots (the e_8-type lines!!):
all raw-norm-4, the form I/2 (the true norm 2!!), the ip-structure {0, +-2raw}!!
HERE: (1) the support-sizes (the nonzero counts!!) + the sign-patterns; (2) THE CLASS
IDENTITY (the 4-nonzero-pattern system?! the codeword class?!); (3) THE POOL: the full
line-pool of the class (the extension candidates (the 120/125/130-line SUPERSETS (the
family-legal!!! the +13/+19.6/+25.6% targets!!!))); (4) THE DECODER-RANK GATES!!!
"""
import os, sys, itertools, json
from collections import Counter
from fractions import Fraction
import numpy as np
log = lambda *a: print(*a, file=sys.stderr, flush=True)

w = json.load(open('ii19_pub2_p111-r434.json', 'rt'))
V, H = w['v'], w['h']
L = [[Fraction(x) for x in l] for l in w['lines']]
# (1) the supports!!
supp = Counter()
for l in L:
    supp[(sum(1 for x in l if x != 0), tuple(sorted(set(str(x) for x in l if x != 0))))] += 1
log('(1) THE P111 LINES (the support-size, the value-set): %s' % {
    (k[0], k[1]): v for k, v in sorted(supp.items())})
# the value-patterns!!
vals = Counter(tuple(sorted((str(x) for x in l))) for l in L)
log('    the distinct value-multisets: %s' % {k: v for k, v in sorted(vals.items())[:12]})
# the honest per-line dump (the first 12!!)
log('    the first 12 lines: %s' % [[str(x) for x in l] for l in L[:12]])
# (2) the class: the raw-norm-4 8-dim lines!!
log('(2) THE CLASS: all raw-norm-4: %s' % all(sum(x * x for x in l) == 4 for l in L))
# the candidate pool: the raw-norm-4 vectors with the E8-ish integrality: the ±2e_i (16!!)
# + the ±1^4-patterns (C(8,4)*2^4/2?! — the canonical!!) + the (±2, ±1, ±1)-type (raw 6?! no!!)
pool = []
for i in range(8):
    for s in (1, -1):
        v = [0] * 8
        v[i] = 2 * s
        pool.append(tuple(v))
for comb in itertools.combinations(range(8), 4):
    for signs in itertools.product([1, -1], repeat=4):
        v = [0] * 8
        for k, idx in enumerate(comb):
            v[idx] = signs[k]
        pool.append(tuple(v))
poolcanon = {}
for v in pool:
    for x in v:
        if x != 0:
            key = tuple(v) if x > 0 else tuple(-y for y in v)
            break
    poolcanon.setdefault(key, v)
log('    THE RAW-NORM-4 POOL: %d canonical candidates (16 + %d)' % (
    len(poolcanon), len(poolcanon) - 16))
P111 = set()
for l in L:
    for x in l:
        if x != 0:
            key = tuple(int(x) for x in l) if x > 0 else tuple(-int(y) for y in l)
            break
    P111.add(key)
log('    THE P111 IN THE POOL: %d/%d' % (len(P111 & set(poolcanon)), V))
log('    THE POOL SURPLUS (the extension candidates!!): %d' % (len(poolcanon) - len(P111)))
# (3) the ip-checks (the pool's ip-structure: the P111-compat!!)
# (4) THE DECODER GATES (the rank at the 111 (the control!!) + the extension previews!!)
def gf2_rank(M):
    M = M.copy(); rr = 0; rows, cols = M.shape
    for c in range(cols):
        p = next((i for i in range(rr, rows) if M[i][c]), None)
        if p is None: continue
        M[[rr, p]] = M[[p, rr]]
        for i in range(rows):
            if i != rr and M[i][c]:
                M[i] ^= M[rr]
        rr += 1
    return rr
lines111 = [poolcanon[k] for k in sorted(P111 & set(poolcanon))]
G = [[sum(a[i] * b[i] for i in range(8)) for b in lines111] for a in lines111]
PERP = [set(s for s in range(len(lines111)) if s != t and G[s][t] == 0) for t in range(len(lines111))]
B0 = np.array([[1 if (s == t or s in PERP[t]) else 0 for s in range(len(lines111))]
                for t in range(len(lines111))], dtype=np.uint8)
log('(4) THE P111 DECODER RANK (the control!!): %d' % gf2_rank(B0))
json.dump({'pool': {str(k): v for k, v in poolcanon.items()}, 'P111': [list(k) for k in sorted(P111)]},
          open('ii19_nat66_pool.json', 'w'))
log('saved ii19_nat66_pool.json')

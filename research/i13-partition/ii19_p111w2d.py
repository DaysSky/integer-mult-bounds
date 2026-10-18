"""THE STAR-SOLVE ORDERINGS (ii19_p111w2d.py) — THE MOST-CONSTRAINED-FIRST!!
The v3: 3/9 solved (the stars 0,1,6!!) with the residues 3-41 -> THE REORDERING HEURISTICS:
the most-constrained-first (the ascending pools / the descending residues!!) + the rotations
+ the exact small-search!!  THE TARGET: ALL 9 SOLVED (the one-use!!)
"""
import gzip, json, itertools, time
from collections import Counter, defaultdict
from fractions import Fraction
W = json.load(gzip.open('/Users/dayssky/integer-mult-bounds/research/e8-bit-r420/data/bitE8mut-r420.json.gz', 'rt'))
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

RM = [21, 23, 24, 29, 53, 71, 80, 89, 103]
kept = [i for i in range(120) if i not in RM]
old2new = {o: n for n, o in enumerate(kept)}
lines = W['lines']
v0 = W['v']
frames0 = W['frames']

def iph(a, b): return sum(x * y for x, y in zip(a, b)) / 2

def basis_of(idx_list):
    rr = [[Fraction(z) for z in lines[i]] for i in idx_list]
    bas = []
    for row in rr:
        y = row
        for b in bas:
            p = next((c for c in range(8) if b[c] != 0), None)
            if p is not None and y[p] != 0:
                f = y[p] / b[p]
                y = [a2 - f * c for a2, c in zip(y, b)]
        p = next((c for c in range(8) if y[c] != 0), None)
        if p is not None: bas.append(y)
    return bas
FBAS = [basis_of(f) if f else [] for f in frames0]
FDIM = [len(b) for b in FBAS]
WiBAS = []
STARS_NEW = []
for L in RM:
    s_new = 0
    for u in kept:
        if iph(lines[L], lines[u]) == 0:
            s_new |= 1 << old2new[u]
    STARS_NEW.append(s_new)
    WiBAS.append(basis_of([u for u in range(120) if u != L and iph(lines[L], lines[u]) == 0]))

def in_W(fbas, wbas):
    for y in fbas:
        z = list(y)
        for b in wbas:
            p = next((c for c in range(8) if b[c] != 0), None)
            if p is not None and z[p] != 0:
                f = z[p] / b[p]
                z = [a2 - f * c for a2, c in zip(z, b)]
        if any(z[c] != 0 for c in range(8)):
            return False
    return True

nreg0 = len(W['start'])
val = [1 << r for r in range(nreg0)]
cur = list(W['start'])
for F, d, srcs in W['D']:
    for s in srcs: val[d] ^= val[s]
for gi, (F, d, srcs) in enumerate(W['A']):
    x = 0
    for s in srcs: x ^= val[s]
    val[d] ^= x
    for s in srcs:
        if FDIM[cur[s]] < FDIM[F] or not in_W(FBAS[cur[s]], FBAS[F]):
            cur[s] = F
    cur[d] = F
CONT = {}
for r in range(nreg0):
    proj = 0
    for b in range(v0):
        if (val[r] >> b) & 1 and b in old2new:
            proj |= 1 << old2new[b]
    CONT[r] = proj
pools = []
for si in range(9):
    pools.append([r for r in range(nreg0) if cur[r] and FDIM[cur[r]] <= 7
                  and in_W(FBAS[cur[r]], WiBAS[si])])
log('(0) the pools: %s' % [len(p) for p in pools])

def try_order(order):
    used = set()
    sols = {}
    for si in order:
        s = STARS_NEW[si]
        pool = [r for r in pools[si] if r not in used and CONT[r]]
        piv = {}
        for r in pool:
            x = CONT[r]
            chain = 1 << r
            while x:
                p = (x & -x).bit_length() - 1
                if p in piv:
                    x2, m2 = piv[p]
                    x ^= x2
                    chain |= m2
                else:
                    piv[p] = (x, chain)
                    break
        x = s
        chain = 0
        while x:
            p = (x & -x).bit_length() - 1
            if p in piv:
                x2, m2 = piv[p]
                x ^= x2
                chain |= m2
            else:
                break
        if x: return None, si, bin(x).count('1')
        sol = [r for r in pool if (chain >> r) & 1]
        used.update(sol)
        sols[si] = sol
    return sols, None, 0

# (1) THE HEURISTIC ORDERINGS!!
orders = {
    'identity': list(range(9)),
    'pool-asc': sorted(range(9), key=lambda si: len(pools[si])),
    'pool-desc': sorted(range(9), key=lambda si: -len(pools[si])),
    'residue-desc': [8, 3, 4, 5, 7, 2, 0, 1, 6],
}
for nm, o in orders.items():
    sols, fail_si, res = try_order(o)
    log('(1) %s: %s' % (nm, 'ALL SOLVED!!!' if sols else 'FAIL at %d (the residue %d!!)' % (fail_si, res)))

# (2) THE RANDOM PERMUTATION SEARCH!!
import random
random.seed(111)
best = (99, None)
for trial in range(3000):
    o = list(range(9))
    random.shuffle(o)
    sols, fail_si, res = try_order(o)
    nfail = 0 if sols else 1
    if sols:
        log('(2) THE TRIAL %d: THE ORDER %s -> ALL 9 SOLVED!!!' % (trial, o))
        best = (0, o)
        break
    if res < best[0]:
        best = (res, o)
        log('    the trial %d: the fail-residue %d (the order %s!!)' % (trial, res, o))
log('(2) THE BEST: %s' % ('SOLVED: %s' % best[1] if best[0] == 0 else 'the residue %d (the order %s!!)' % best))
log('DONE — THE ORDERINGS!!')

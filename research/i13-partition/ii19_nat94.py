"""THE SPAN TEST + THE RICH-POOL CACHE (ii19_nat94.py) — the B-wire family's verdict!!

THE nat93's CRITICAL NEGATIVE: the XOR-greedy stuck at 17 wires (7,416/8,000 residual);
the span-finish failed for ALL 129 demands. THE FUNDAMENTAL QUESTION (this script!!):
IS perp(t) IN THE GF(2)-SPAN OF THE PERP-RICH-FRAME PATTERNS?! (and the 9 patterns over
the full pool!!) — THE VERDICT DECIDES THE WIRE FAMILY (the aggregate-route (R ~100-200
(the price +30-47%!!)) vs the piece+carrier-route (the nat67 economy (R ~276-350 (the
price +15-22%!!)))). THE CACHE: the rich pool saved once (ii19_nat94_richpool.npz!!).
"""
import os, sys, json
import numpy as np
from collections import Counter
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

SPEC = json.load(open('ii19_nat69_spec.json', 'rt'))
lines = [tuple(int(x) for x in l) for l in SPEC['lines']]
V = len(lines)
PERP = [set(p) for p in SPEC['PERP']]
B0 = [sum(1 << s for s in ({t} | PERP[t])) for t in range(V)]
G8 = [[sum(a[i] * b[i] for i in range(8)) for b in lines] for a in lines]
P70 = json.load(open('ii19_nat70_pool.json', 'rt'))
pool3 = [(sorted(p), sorted(u)) for p, u in P70['pool']]

def rspan(vecs): return len(rref([list(v) for v in vecs], 8))
rich = {}
seen = set()
for ps, users in pool3:
    for s4 in range(V):
        if s4 in ps: continue
        key = tuple(sorted(ps + [s4]))
        if key in seen: continue
        seen.add(key)
        if rspan([lines[x] for x in key]) != 4: continue
        basis = rref([list(lines[x]) for x in key], 8)
        inF = [x for x in range(V) if len(rref(list(basis) + [list(lines[x])], 8)) == 4]
        if len(inF) >= 5:
            rich[key] = (sorted(inF), sorted(t for t in range(V) if all(G8[k][t] == 0 for k in key)))
log('the rich-4 pool: %d' % len(rich))
keys = sorted(rich.keys())
masks = np.array([[1 if s in rich[k][0] else 0 for s in range(V)] for k in keys], dtype=np.uint8)
Tmat = np.array([[1 if t in rich[k][1] else 0 for t in range(V)] for k in keys], dtype=np.uint8)  # (pool, V)
np.savez_compressed('ii19_nat94_richpool.npz', masks=masks, Tmat=Tmat,
                    keys=np.array([list(k) for k in keys]))
log('CACHED ii19_nat94_richpool.npz (%d x %d masks + the T-matrix!!)' % masks.shape)

def gf2_solve(A, b):
    """solve A x = b over GF(2) (A: m x n); return a solution x or None."""
    A = A.copy() % 2; b = b.copy() % 2
    m, n = A.shape
    r = 0
    piv = []
    for c in range(n):
        p = None
        for i in range(r, m):
            if A[i, c]: p = i; break
        if p is None: continue
        A[[r, p]] = A[[p, r]]; b[[r, p]] = b[[p, r]]
        for i in range(m):
            if i != r and A[i, c]:
                A[i] ^= A[r]; b[i] ^= b[r]
        piv.append(c); r += 1
        if r == m: break
    for i in range(r, m):
        if b[i]: return None
    x = np.zeros(n, dtype=np.uint8)
    for i, c in enumerate(piv):
        x[c] = b[i]
    return x

# THE SPAN TEST: perp(t) in span{the perp-rich-frame patterns}?!
log('\nTHE SPAN TEST (perp(t) via the perp-rich-frames!!):')
ok = 0; sizes = Counter(); ncand = Counter()
for t in range(V):
    sel = Tmat[:, t].astype(bool)
    cand = masks[sel]
    ncand[int(sel.sum())] += 1
    b = np.array([1 if s in PERP[t] else 0 for s in range(V)], dtype=np.uint8)
    x = gf2_solve(cand.T, b)
    if x is None:
        sizes['NO'] += 1
    else:
        ok += 1; sizes[int(x.sum())] += 1
log('  the candidate counts per target: %s' % dict(sorted(ncand.items())))
log('  perp(t) IN SPAN: %d/120 | the solution-sizes: %s' % (ok, dict(sorted(sizes.items(), key=str))))

# THE 9 PATTERNS over the FULL pool (the gathers' side!!)
log('\nTHE GATHER-SIDE SPAN TEST (the 9 patterns over the full pool!!):')
BASIS_IDX = SPEC['BASIS_IDX']
pats = []
for c, o in BASIS_IDX:
    v = 0
    for tt in o: v ^= B0[tt]
    pats.append(v)
gsz = Counter()
for g, pat in enumerate(pats):
    b = np.array([(pat >> s) & 1 for s in range(V)], dtype=np.uint8)
    x = gf2_solve(masks.T, b)
    gsz[int(x.sum()) if x is not None else 'NO'] += 1
    log('  pattern %d (%d lines): %s' % (g, bin(pat).count('1'),
        ('combo-size %d' % int(x.sum())) if x is not None else 'NOT IN SPAN'))
log('  the pattern combo-sizes: %s' % dict(sorted(gsz.items(), key=str)))

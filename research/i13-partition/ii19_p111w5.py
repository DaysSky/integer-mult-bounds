"""THE LOW-PART INDEPENDENCE (ii19_p111w5.py) — THE PURE-CLIMB DESIGN!!
THE DISCOVERY (the gcheck's code!!): THE PURE-CLIMB GATES [F, d, []] ARE LEGAL!!! -> THE
RETS' BUILDS AT THE LOWS (the conflict-free zone!!!) + THE PURE-CLIMBS TO THE W_i (the
CST 63!!!) — THE RETS' X-PARTS = ANY 9 INDEPENDENT VECTORS (the W-solve over any basis!!)
— THE SIMPLEST: THE SINGLE-READ BUILDS (one sub-cell each!!!).
THE QUESTIONS: (1) the sub-cells (the R420's cells ⊆ the F_lows (the W_i-internal!!)):
the per-star choices; (2) THE 9 INDEPENDENT single-cell contents (one per star!!)!
"""
import gzip, json, time
from collections import Counter
from fractions import Fraction
W = json.load(gzip.open('/Users/dayssky/integer-mult-bounds/research/e8-bit-r420/data/bitE8mut-r420.json.gz', 'rt'))
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

RM = [1, 8, 20, 24, 45, 63, 82, 89, 102]      # THE MINIS-17 PUNCTURE (the current best!!)
kept = [i for i in range(120) if i not in RM]
old2new = {o: n for n, o in enumerate(kept)}
V = 111
lines = W['lines']
v0 = W['v']
frames0 = W['frames']
nreg0 = len(W['start'])

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

val = [1 << r for r in range(nreg0)]
cur = list(W['start'])
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
log('(0) the base-replay done!!')

# (1) THE W_i + THE W_i-INTERNAL FRAMES (the cells!!)!
WiB = []
for L in RM:
    WiB.append(basis_of([u for u in range(120) if u != L and iph(lines[L], lines[u]) == 0]))
log('(1) the W_i: %s' % [len(b) for b in WiB])
# the W_i-internal frames: the R420's frames (dims 1..6!!) with the span ⊆ W_i!!
WIF = []
for si in range(9):
    cand = [(fi, FDIM[fi]) for fi in range(len(frames0))
            if 1 <= FDIM[fi] <= 6 and in_W(FBAS[fi], WiB[si])]
    WIF.append(cand)
    log('    the W_%d-internal frames: %d (the dims %s!!)' % (
        si, len(cand), dict(sorted(Counter(d for _, d in cand).items()))))

# (2) THE SUB-CELL CANDIDATES: the helpers whose cur-frame ⊆ W_i (the dim <= 6!!) —
#     the SAME-AS-POOLS but now for the SINGLE-READ low-builds!!
CONT = {}
for r in range(nreg0):
    c = 0
    for b in range(v0):
        if (val[r] >> b) & 1:
            c |= 1 << b
    CONT[r] = c
log('(2) the helper-contents (the OLD indexing!!):')
# the per-star candidate sets: the helpers h with cur(h) ⊆ W_i (the single-cell low-parts!!)
CAND = []
for si in range(9):
    cs = [h for h in range(2 * v0, nreg0)
          if cur[h] and FDIM[cur[h]] <= 6 and in_W(FBAS[cur[h]], WiB[si])
          and bin(CONT[h]).count('1') >= 1]
    CAND.append(cs)
    log('    the W_%d: the single-cell candidates %d (the content-weights %s!!)' % (
        si, len(cs), dict(sorted(Counter(bin(CONT[h]).count('1') for h in cs).items()))))

# (3) THE 9 INDEPENDENT SINGLE-CELL CONTENTS (one per star!!)!
#     the greedy: the star-order [the fewest-candidates-first!!] + the rank-check!!
#     NOTE: the contents in the OLD-indexed bits: the independence over GF(2)!!
bx = {}
picks = []
order = sorted(range(9), key=lambda si: len(CAND[si]))
ok = True
for si in order:
    found = None
    # the most-independent-first: the heaviest contents (the richest!!)!
    for h in sorted(CAND[si], key=lambda h: -bin(CONT[h]).count('1')):
        x = CONT[h]
        y = x
        pb = {}
        # reduce h's content over the current basis!!
        red = x
        # the manual elimination against bx!!
        z = x
        while z:
            p = (z & -z).bit_length() - 1
            if p in bx:
                z ^= bx[p]
            else:
                break
        if z:
            found = h
            # the insert!!
            zz = z
            p = (zz & -zz).bit_length() - 1
            bx[p] = z
            break
    if found is None:
        ok = False
        log('(3) the star %d: NO independent candidate (the rank so far %d!!)' % (si, len(bx)))
    else:
        picks.append((si, found, bin(CONT[found]).count('1')))
        log('    the star %d: THE PICK h=%d (the content-weight %d!!)' % (
            si, found, bin(CONT[found]).count('1')))
log('(3) THE INDEPENDENCE: %s (the rank %d/9!!)' % (ok, len(bx)))
if ok:
    log('    THE PICKS: %s' % picks)
    # (4) THE PROJECTION-CHECK: the picks' contents PROJECTED (the 111!!): still independent?!
    bxp = {}
    for si, h, wt in picks:
        proj = 0
        for b in range(v0):
            if (CONT[h] >> b) & 1 and b in old2new:
                proj |= 1 << old2new[b]
        z = proj
        while z:
            p = (z & -z).bit_length() - 1
            if p in bxp: z ^= bxp[p]
            else: bxp[p] = z; break
    log('(4) THE PROJECTED INDEPENDENCE: %d/9!!' % len(bxp))
    # (5) THE W-SOLVE-CHECK: the Brows ∈ the projected-span?!
    BROWS = []
    for t in kept:
        m = 1 << old2new[t]
        for u in kept:
            if u != t and iph(lines[t], lines[u]) == 0:
                m |= 1 << old2new[u]
        BROWS.append(m)
    # the full projected-basis span!!
    SPAN = {}
    bxs = {}
    for si, h, wt in picks:
        proj = 0
        for b in range(v0):
            if (CONT[h] >> b) & 1 and b in old2new:
                proj |= 1 << old2new[b]
        x = proj
        while x:
            p = (x & -x).bit_length() - 1
            if p in bxs: x ^= bxs[p]
            else: bxs[p] = x; break
    n_ok = 0
    for t in range(V):
        z = BROWS[t]
        while z:
            p = (z & -z).bit_length() - 1
            if p in bxs: z ^= bxs[p]
            else: break
        if z == 0: n_ok += 1
    log('(5) THE W-SOLVE: the Brows in the span: %d/%d!!' % (n_ok, V))
log('DONE — THE LOW-PART INDEPENDENCE!!')

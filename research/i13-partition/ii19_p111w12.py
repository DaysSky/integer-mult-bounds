"""THE P111-WORD v12 (ii19_p111w12.py) — THE MIXED-DELIVERY's HONEST-MINIMUM (THE R-VERDICT!!!)

THE MEASURED-LANDSCAPE (the v10-v11!!!): the pools-sparse (the star-D6-helpers: 4-7-per-star
(the span-FALSE-x9!!)) | the sources-ALL-pinned (the B's-cell-reads (the 111/111!!)) | THE
FREE-SAME-FRAME-READS (the §1750!!!): the sources-readable-AT-THEIR-OWN-CELLS (NO-CLIMBS!!!).

THE MIXED-DELIVERY (the per-star-star-pattern (58-60-bits!!)):
  (a) THE POOL-HELPERS (the star-D6-at-frame (the FREE!!)): the ~30-bit-parts (the 4-7!!)
  (b) THE LUCKY-CELL-PIECES: the cells {u, w} ⊆ W_si (the ~13-16-per-star!!): 2-bits-per-piece
      (the sources-read-FREE-at-their-own-cells!!!)
  (c) THE SINGLETON-PIECES: the unlucky-sources: the piece-at-the-singleton (1-bit!! (the
      source-read-FREE-at-the-START (the pre-A-order (the build-BEFORE-the-cell-climbs!!))!!)
      -> the climb: the singleton (1!!) -> W_si (7!!) ✓✓)

THE SOLVE (the GF(2)-over-the-mixed-pools (the pool-helpers (the 30-parts!!) FIRST (the
R-efficiency!!!) + the lucky-cells (the 2-bits!!) + the singletons (the 1-bit-residue!!!)):
THE OUTPUT: the pieces'-count (the R-VERDICT: the crossing (<= 428!!) vs the honest-class!!!)
"""
import gzip, json, random, time
from collections import Counter
from fractions import Fraction

W = json.load(gzip.open('/Users/dayssky/integer-mult-bounds/research/e8-bit-r420/data/bitE8mut-r420.json.gz', 'rt'))
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

RM = [1, 8, 20, 24, 45, 63, 82, 89, 102]
kept = [i for i in range(120) if i not in RM]
old2new = {o: n for n, o in enumerate(kept)}
V, H = 111, 8
lines = W['lines']
v0 = W['v']
frames0 = W['frames']
nreg0 = len(W['start'])
R0 = W['R']

def iph(a, b): return sum(x * y for x, y in zip(a, b)) / 2
def basis_of(idx_list):
    rr = [[Fraction(z) for z in lines[i]] for i in idx_list]
    bas = []
    for row in rr:
        y = list(row)
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
STARS, WiB = [], []
for L in RM:
    s_new = 0
    for u in kept:
        if iph(lines[L], lines[u]) == 0:
            s_new |= 1 << old2new[u]
    STARS.append(s_new)
    WiB.append(basis_of([u for u in range(120) if u != L and iph(lines[L], lines[u]) == 0]))

# ============ (1) THE MIXED-POOLS (the items: (the kind, the id, the bits, the cost)!!) ============
# (a) the pool-helpers (the star-D6-at-frame!!): cost-1 (the piece-per-D6!!!!) per ~30-bits?!
#     hmm — WAIT: the piece-per-FRAME (the at-frame-helpers-read-by-ONE-piece-at-the-D6!!)
#     -> the items: the HELPER-reads (the piece-count = the DISTINCT-D6s!!)
# (b) the lucky-cells: the piece-per-cell (the 2-bits!!)
# (c) the singletons: the piece-per-bit!!
ITEMS = []          # (si, kind, key, bits)
for si in range(9):
    # (a) the star-D6-helpers (the FREE-at-frame!!)
    for h in range(2 * v0, nreg0):
        if CONT[h] and FDIM[cur[h]] == 6 and in_W(FBAS[cur[h]], WiB[si]):
            ITEMS.append((si, 'h', h, CONT[h]))
    # (b) the lucky-cells: the cell-SPAN ⊆ W_si (the sources-at-the-cell!!)
    cell_seen = {}
    for u_old in kept:
        c = cur[u_old]
        if FDIM[c] == 2 and in_W(FBAS[c], WiB[si]):
            cell_seen.setdefault(c, []).append(u_old)
    for c, us in cell_seen.items():
        bits = 0
        for u_old in us:
            bits |= 1 << old2new[u_old]
        ITEMS.append((si, 'c', c, bits))
    # (c) the singletons (ALL the star-bits'-sources (the 1-bit-each!!))
    for i in range(V):
        if (STARS[si] >> i) & 1:
            u_old = kept[i]
            ITEMS.append((si, 's', u_old, 1 << i))
log('(1) the mixed-items: %d (the helpers %d | the cells %d | the singletons %d!!)' % (
    len(ITEMS), sum(1 for x in ITEMS if x[1] == 'h'),
    sum(1 for x in ITEMS if x[1] == 'c'), sum(1 for x in ITEMS if x[1] == 's')))

# ============ (2) THE GREEDY-WEIGHTED-SOLVE (the R-efficiency: the helpers-first!!!) ============
# the per-star: the span-solve (the max-helpers (the big-parts!!) -> the max-cells (the
# 2-bits!!) -> the singleton-residues (the 1-bits!!!)) — the CONFLICT-FREE (the exclusive!!)
def star_solve(si, exclude):
    best = {'h': [], 'c': [], 's': []}
    rem = STARS[si]
    # (a) the helpers-first (the rank-greedy (the max-coverage!!))
    hs = [x for x in ITEMS if x[0] == si and x[1] == 'h' and x[2] not in exclude]
    rng.shuffle(hs)
    piv = {}
    chosen_h = []
    for si2, kind, key, bits in hs:
        x = bits; chain = 1 << key
        while x:
            p = (x & -x).bit_length() - 1
            if p in piv:
                x2, m2 = piv[p]; x ^= x2; chain ^= m2
            else:
                piv[p] = (x, chain); break
    z = rem; chain = 0
    while z:
        p = (z & -z).bit_length() - 1
        if p in piv:
            x2, m2 = piv[p]; z ^= x2; chain ^= m2
        else:
            break
    if z == 0:
        chosen_h = [key for (si2, kind, key, bits) in hs if (chain >> key) & 1]
        return {'h': chosen_h, 'c': [], 's': []}, 0
    # the partial: the helpers'-contribution
    used_bits = rem ^ z
    best['h'] = []
    # (b) the cells (the 2-bit-pieces!!)
    cs = [x for x in ITEMS if x[0] == si and x[1] == 'c']
    cell_pick = []
    z2 = z
    for si2, kind, key, bits in sorted(cs, key=lambda x: -bin(x[3] & z2).count('1')):
        g = bin(bits & z2).count('1')
        if g >= 1:                        # the helpful-cell (the >=1-new-bit!!)
            cell_pick.append(key)
            z2 &= ~bits
    best['c'] = cell_pick
    # (c) the singletons (the residue!!)
    best['s'] = [i for i in range(V) if (z2 >> i) & 1]
    return best, z2

rng = random.Random(11111)
results = star_solve(0, set())
best_tot = None
for trial in range(500):
    used_h = set()
    tot = {'h': [], 'c': [], 's': []}
    order = list(range(9)); rng.shuffle(order)
    for si in order:
        r, z2 = star_solve(si, used_h)
        used_h.update(r['h'])
        tot['h'] += [(si, k) for k in r['h']]
        tot['c'] += [(si, k) for k in r['c']]
        tot['s'] += [(si, k) for k in r['s']]
    n_h = len(set(tot['h'])); n_c = len(tot['c']); n_s = len(tot['s'])
    score = n_h + n_c + n_s
    if best_tot is None or score < best_tot[0]:
        best_tot = (score, n_h, n_c, n_s)
        log('    the trial %d: the pieces %d (the D6-pieces %d | the cell-pieces %d | the '
            'singleton-pieces %d!!)' % (trial, score, n_h, n_c, n_s))
score, n_h, n_c, n_s = best_tot
R_new = R0 + score + 9 + 9
log('(2) THE MIXED-MINIMUM: the pieces %d (the D6 %d | the cells %d | the singletons %d!!)' % (
    score, n_h, n_c, n_s))
log('    THE R-VERDICT: %d (the base %d + the pieces %d + the rets 9 + the mimics 9!!)' % (
    R_new, R0, score))
log('    the crossing at 428: %s | the §1928\'s-estimate: 510-535' % (
    'REACHABLE!!!' if R_new <= 428 else 'UNREACHABLE (the honest-class!!)'))
log('DONE — THE v12-MIXED-MINIMUM!!')

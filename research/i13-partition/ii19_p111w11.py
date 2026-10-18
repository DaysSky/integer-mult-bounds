"""THE P111-WORD v11 (ii19_p111w11.py) — THE STAR-D6-PIECES (THE FREE-SAME-FRAME-READS!!!)

THE v10-VERDICT (the measured!!!): the crude-B-pin-filter kills the pools (the ranks 1-4 (the
star-in-span: FALSE-x9!!) -> 469-minis (R=907: DEAD!!)).  THE CORRECT-MECHANISM (the §1750!!!
the gcheck's-line-77: `if cur[r] == F: return`!!!): THE FREE-SAME-FRAME-READS — the sources
ALL-at-the-dim-2-cells (the {2: 120}!!) | the 331-helpers-at-the-dim-6-D6s!!

THE PIECE-DESIGN (the zero-pin-violation!!!):
  - the PIECE P (a fresh register!!) at a STAR-INTERNAL frame F ⊆ W_si (the star-D6 (dim-6!!)
    / the lucky-cell (dim-2!!)): reads the helpers/SOURCES ALREADY-AT-F (THE FREE-reads (the
    cur == F -> NO-CLIMB -> NO-PIN-VIOLATION!!!)) — one-piece-per-F (the F's must chain!!):
    the pieces' chains: F -> W_si (7!!) -> FULL ✓✓✓
  - the star-RET at W_si: [W_si, RET, [the pieces!!]] — the pieces' cur == W_si (FREE!!!)
  - the residues (the star-bits outside the D6-span!!): the lucky-cell-pieces (the sources at
    their own-cells (FREE!!) + the lucky-cell ⊆ W_si (the partner ⊥ L_si!!)!!)
  - THE REGISTER-BITS: the pieces'/the helpers'/the sources'-self-bits -> the computed-D-cancel
    (the nat19's-D-extension-law (the §1862!!!) (the w8's-(5)-machinery ✓!!))

THIS-SCRIPT: (1) the star-D6-pools (the D6s ⊆ W_si + the at-frame-helpers!!);
(2) the span-sufficiency + the cross-star-conflicts; (3) THE EXCLUSIVE-SOLVE (the pieces!!)
+ the residues (the lucky-cells!!); (4) the piece-count (the R-estimate!!) + THE SAVE.
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

# (0) the base-replay + the contents!!
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
log('(0) the base-replay done!!')
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
log('    the stars: %s' % [bin(s).count('1') for s in STARS])

# ============ (1) THE STAR-D6-POOLS ============
D6S = [fi for fi in range(len(frames0)) if FDIM[fi] == 6]
log('(1) the R420-D6s: %d' % len(D6S))
STAR_D6 = []
for si in range(9):
    cand = [fi for fi in D6S if in_W(FBAS[fi], WiB[si])]
    STAR_D6.append(cand)
    # the helpers at those frames!!
    at = {}
    for h in range(2 * v0, nreg0):
        if cur[h] in cand and CONT[h]:
            at.setdefault(cur[h], []).append(h)
    n_at = sum(len(v2) for v2 in at.values())
    log('    the star %d: the D6s %d | the at-frame-helpers %d (the frames-with-helpers %d)!!' % (
        si, len(cand), n_at, len(at)))

# ============ (2) THE SPAN-SUFFICIENCY + THE CONFLICTS ============
POOLS = []
for si in range(9):
    cand = STAR_D6[si]
    pool = [h for h in range(2 * v0, nreg0) if cur[h] in cand and CONT[h]]
    POOLS.append(pool)
    piv = {}
    for r in pool:
        x = CONT[r]
        while x:
            p = (x & -x).bit_length() - 1
            if p in piv: x ^= piv[p]
            else: piv[p] = x; break
    z = STARS[si]
    while z:
        p = (z & -z).bit_length() - 1
        if p in piv: z ^= piv[p]
        else: break
    log('(2) the star %d: the pool %d | the rank %d | THE STAR-IN-THE-SPAN: %s' % (
        si, len(pool), len(piv), z == 0))
# the cross-star conflicts (the helpers in multiple pools!!)
mem = {}
for si in range(9):
    for h in POOLS[si]:
        mem.setdefault(h, []).append(si)
conf = Counter(len(v) for v in mem.values())
log('    the pool-memberships: %s (the conflict-helpers: %d!!)' % (
    dict(sorted(conf.items())), sum(1 for v in mem.values() if len(v) > 1)))

# ============ (3) THE EXCLUSIVE-SOLVE + THE RESIDUES (the lucky-cells!!) ============
# the lucky-cells (the sources'-cells ⊆ W_si!!) — the residual-delivery!!!
LUCKY = {}
for si in range(9):
    lk = []
    for u_old in kept:
        c = cur[u_old]
        if FDIM[c] <= 6 and in_W(FBAS[c], WiB[si]):
            lk.append(u_old)
    LUCKY[si] = set(lk)
log('(3) the lucky-sources per star: %s' % [len(LUCKY[si]) for si in range(9)])

def solve_one(si, exclude):
    pool = [r for r in POOLS[si] if r not in exclude and CONT[r]]
    piv = {}
    for r in pool:
        x = CONT[r]; chain = 1 << r
        while x:
            p = (x & -x).bit_length() - 1
            if p in piv:
                x2, m2 = piv[p]; x ^= x2; chain ^= m2
            else:
                piv[p] = (x, chain); break
    x = STARS[si]; chain = 0
    while x:
        p = (x & -x).bit_length() - 1
        if p in piv:
            x2, m2 = piv[p]; x ^= x2; chain ^= m2
        else:
            break
    return [r for r in pool if (chain >> r) & 1], x

rng = random.Random(11111)
best = None
for trial in range(2000):
    order = list(range(9)); rng.shuffle(order)
    used = set()
    sols_t = {}; resid_bits = {}
    for si in order:
        sol, res = solve_one(si, used)
        if sol is not None and res == 0:
            sols_t[si] = sol; used.update(sol); resid_bits[si] = 0
            continue
        # the partial (the residues!!)
        pool = [r for r in POOLS[si] if r not in used and CONT[r]]
        piv = {}
        for r in pool:
            x = CONT[r]; chain = 1 << r
            while x:
                p = (x & -x).bit_length() - 1
                if p in piv:
                    x2, m2 = piv[p]; x ^= x2; chain ^= m2
                else:
                    piv[p] = (x, chain); break
        x = STARS[si]; chain = 0
        while x:
            p = (x & -x).bit_length() - 1
            if p in piv:
                x2, m2 = piv[p]; x ^= x2; chain ^= m2
            else:
                break
        sols_t[si] = [r for r in pool if (chain >> r) & 1]
        used.update(sols_t[si])
        resid_bits[si] = x
    # the resid-luck (the residual-bits'-sources-lucky?!)
    dead = 0
    for si in range(9):
        rb = resid_bits[si]
        for i in range(V):
            if (rb >> i) & 1 and kept[i] not in LUCKY[si]:
                dead += 1
    score = (dead, sum(bin(resid_bits[si]).count('1') for si in range(9)))
    if best is None or score < best[0]:
        best = (score, sols_t, resid_bits, order)
        log('    the trial %d: the dead %d | the resid-bits %d (the order %s!!)' % (
            trial, dead, score[1], order[:3]))
        if dead == 0 and score[1] == 0:
            break
score, final_sols, resid_bits, best_order = best
log('(3b) THE BEST: the dead %d | the resid-bits %d' % score)
# the piece-count (the distinct-D6s + the lucky-cells!!)
pieces = 0
for si in range(9):
    frames_used = set(cur[r] for r in final_sols[si])
    pieces += len(frames_used)
    rb = resid_bits[si]
    cells_used = set()
    for i in range(V):
        if (rb >> i) & 1:
            cells_used.add(cur[kept[i]])
    pieces += len(cells_used)
log('    THE PIECES: %d (the D6-pieces + the lucky-cell-pieces!!)' % pieces)
log('    THE R-ESTIMATE: %d (the base %d + the pieces %d + the rets 9 + the mimics 9!!)' % (
    R0 + pieces + 9 + 9, R0, pieces))

# ============ (4) THE SAVE ============
json.dump(dict(rm=RM, sols={si: final_sols[si] for si in range(9)},
               resid_bits={si: resid_bits[si] for si in range(9)}),
          open('ii19_p111_sol3.json', 'wt'))
log('(4) THE SAVE: ii19_p111_sol3.json')
log('DONE — THE v11-STAR-D6-SOLVE!!')

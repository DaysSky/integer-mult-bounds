"""THE P111-WORD v13 (ii19_p111w13.py) — THE PUNCTURE-LUCK SCAN (THE DECISIVE-R!!!)

THE v12's-verdict: the mixed-minimum 197-pieces (R=635!!) — TWO-R-shave-levers-unmeasured:
(A) THE D6-PARTIAL-PIECES (the v12's-all-or-nothing-bug!!): the per-D6-frame-pieces (the
    chosen-at-frame-helpers (the FREE-reads!!!) — the ~30-bit-parts!!)
(B) THE PUNCTURE-SET's-LUCK: the unlucky-singletons (73!!) are RM-DEPENDENT (the phunt4's
    40-candidates (the committed-json!!!))!

THIS-SCAN: the per-candidate: the stars + the mixed-solve (the D6-pieces (the per-frame
best-subset (the max-new-bits!!)) + the lucky-cells (2-bits!!) + the singleton-residues!!)
-> THE PIECES'-COUNT + THE R-VERDICT (the best-set (the crossing?!))!!
"""
import gzip, json, time
from collections import Counter
from fractions import Fraction

W = json.load(gzip.open('/Users/dayssky/integer-mult-bounds/research/e8-bit-r420/data/bitE8mut-r420.json.gz', 'rt'))
CANDS = json.load(open('ii19_phunt4_cands.json'))
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

lines = W['lines']
v0 = W['v']
frames0 = W['frames']
nreg0 = len(W['start'])
R0 = W['R']
V, H = 111, 8

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

# (0) the base-replay (ONCE (the R420's-own!!) — the set-independent!!)
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
        if (val[r] >> b) & 1 and b in old2new if False else (val[r] >> b) & 1 and b < v0:
            proj |= 1 << b
CONT = {}
# the per-set projection: recompute per set (the kept-map!!)
log('(0) the base-replay done!!')
# the precomputable: the helpers-at-the-D6-frames (the contents (the OLD-bits!!)!!)
HELPS_AT_D6 = {}
for h in range(2 * v0, nreg0):
    if FDIM[cur[h]] == 6 and val[h] >> v0:
        HELPS_AT_D6.setdefault(cur[h], []).append(h)
log('    the D6-frames-with-helpers: %d (the helpers %d!!)' % (
    len(HELPS_AT_D6), sum(len(v) for v in HELPS_AT_D6.values())))
SRC_CELL = {}
for u_old in range(v0):
    if FDIM[cur[u_old]] == 2:
        SRC_CELL.setdefault(cur[u_old], []).append(u_old)
CELL_OF = {u_old: cur[u_old] for u_old in range(v0) if FDIM[cur[u_old]] == 2}
log('    the source-cells: %d frames (the %d sources!!)' % (
    len(SRC_CELL), sum(len(v) for v in SRC_CELL.values())))

def scan_set(RM):
    kept = [i for i in range(120) if i not in RM]
    old2new = {o: n for n, o in enumerate(kept)}
    # the contents (the projected!!)
    def CONTp(r):
        c = 0
        for b in range(v0):
            if (val[r] >> b) & 1 and b in old2new:
                c |= 1 << old2new[b]
        return c
    stars = []
    WiB = []
    for L in RM:
        s_new = 0
        for u in kept:
            if iph(lines[L], lines[u]) == 0:
                s_new |= 1 << old2new[u]
        stars.append(s_new)
        WiB.append(basis_of([u for u in range(120) if u != L and iph(lines[L], lines[u]) == 0]))
    pieces = 0
    resid_total = 0
    for si in range(9):
        rem = stars[si]
        # (a) the D6-pieces: the frames ⊆ W_si with helpers!!
        d6fr = [fi for fi in HELPS_AT_D6 if in_W(FBAS[fi], WiB[si])]
        used_fr = set()
        while rem:
            best = None
            for fi in d6fr:
                if fi in used_fr: continue
                hs = HELPS_AT_D6[fi]
                # the best-subset (the <=2^k-options (k <= ~3!!)): the max-new-bits!!
                for m in range(1, 1 << len(hs)):
                    bits = 0
                    for j in range(len(hs)):
                        if (m >> j) & 1:
                            bits ^= CONTp(hs[j])
                    g = bin(bits & rem).count('1')
                    if g > 0 and (best is None or g > best[0]):
                        best = (g, fi, bits)
            # (b) the lucky-cells (the 2-bit!!)
            for c, us in SRC_CELL.items():
                if c in used_fr: continue
                if not in_W(FBAS[c], WiB[si]): continue
                bits = 0
                for u_old in us:
                    if u_old in old2new and (stars[si] >> old2new[u_old]) & 1:
                        bits |= 1 << old2new[u_old]
                g = bin(bits & rem).count('1')
                if g > 0 and (best is None or g > best[0]):
                    best = (g, c, bits)
            if best is None:
                break
            g, fi, bits = best
            used_fr.add(fi)
            pieces += 1
            rem &= ~bits
        # (c) the singleton-residues (1-bit-each!!)
        pieces += bin(rem).count('1')
        resid_total += bin(rem).count('1')
    return pieces, resid_total

SETS = [[s, rm] for s, rm in CANDS] + [[0, [1, 8, 20, 24, 45, 63, 82, 89, 102]]]
log('(1) THE SCAN (%d sets!!)' % len(SETS))
best = None
for sc, rm in SETS:
    pieces, resid = scan_set(rm)
    R = R0 + pieces + 9 + 9
    tag = 'THE CURRENT' if sc == 0 else 'cand-%d' % sc
    log('    %s (rm %s): the pieces %d (the singletons %d!!) -> R = %d' % (
        tag, rm, pieces, resid, R))
    if best is None or pieces < best[0]:
        best = (pieces, rm, R)
log('(2) THE BEST: rm %s: the pieces %d -> R = %d (the crossing at 428: %s!!)' % (
    best[1], best[0], best[2], 'REACHABLE!!!' if best[2] <= 428 else 'UNREACHABLE'))
log('DONE — THE v13-LUCK-SCAN!!')

"""THE 121-LINE WORD BUILD v2 — THE R420-STYLE (the SS1708 directive: 'fully build and verify it').

THE COMPLETE RECIPE (the R420 measured: SS1736/SS1742/SS1752!!):
- THE FLAG: the singletons (1!) -> the cells (2!) -> the 12-frames (4!) -> the dim-6 unions
  (6!) -> the perps (8!) -> FULL (9!)
- THE CARRIERS: the sources read FREE at their singletons (the [1, 1, 2]-style!!)
- THE ROOMS: the 12-frame D4 rooms (the census: ii19_121d4.py!!) + the room-sums R_f
- THE PER-TARGET SUMS: the S_t chains (the incremental accumulations at the rooms!!)
- THE TARGETS: the few-frame reads (the R420's [2, 7]-analog!!)
- THE GATHERS: the 9 decoder rows (the W!)
- THE TRANSITIVE D-DIRT: the val-simulation's parity sets (the SS1742's R420 confirmation!!!)

THE CENSUS-INDEPENDENT MACHINERY (this file, the parts DONE!!):
(1) THE SYSTEM + THE DECODER (the proven SS1716 parts!!)
(2) THE FRAMES' MACHINERY (the singletons, FULL, the t-perps)
(3) THE VAL-SIMULATION (the SS1745-validated replay!!) + THE D-DIRT'S AUTO-DERIVATION
    (the per-target helper-indicator parity sets!!!)
(4) THE WORD-DICT + THE GCHECK INTERFACE

THE CENSUS-DEPENDENT PARTS (the STUBS — the census's notification pending!!):
- THE ROOMS (the 12-frames!!), THE ROOM-SUMS R_f, THE S_t CHAINS, THE TARGETS' READS
"""
import sys, json, itertools, time
from collections import Counter, defaultdict
import numpy as np

sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/tword')

t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

# ============ (1) THE SYSTEM ============
roots = []
for i in range(8):
    for j in range(i + 1, 8):
        for si in (1, -1):
            for sj in (1, -1):
                v8 = np.zeros(8); v8[i] = si; v8[j] = sj
                roots.append(v8)
half = [np.array(s, dtype=float) / 2 for s in itertools.product([1, -1], repeat=8) if s.count(-1) % 2 == 0]
def canon(vv):
    for x in vv:
        if x != 0:
            return tuple(vv) if x > 0 else tuple(-vv)
    return tuple(vv)
d8 = {}
for r in list(roots) + half: d8[canon(r)] = np.array(r)
AL = list(d8.values())
L = np.array([list(al) + [0.0] for al in AL] + [[0.0] * 8 + [1.0]])
V = len(L)
H = 9
FORM = np.diag([1.0] * 8 + [2.0])
G = L @ FORM @ L.T
assert V == 121 and all(abs(G[i][i] - 2.0) < 1e-9 for i in range(V)), 'the norms!!'
PERP = []
for t in range(V):
    m = 0
    for s in range(V):
        if s != t and abs(G[s][t]) < 1e-9:
            m |= (1 << s)
    PERP.append(m)
jlines = [[s for s in range(V) if (PERP[t] >> s) & 1] for t in range(V)]
log('(1) the system: %d lines; h=%d; the norms 2 OK' % (V, H))

# ============ (2) THE DECODER (the perp-pattern B0: rank 9!!) ============
B0 = [(1 << t) | PERP[t] for t in range(V)]
dec_basis = []          # the (row-mask, pivot) pairs — the decoder's basis!!
dec_rows = []
for t in range(V):
    r = B0[t]
    for pr, pi in [(b[0], b[1]) for b in dec_basis]:
        if (r >> pi) & 1:
            r ^= pr
    if r == 0:
        continue
    pi = (r & -r).bit_length() - 1
    dec_basis.append((r, pi))
    dec_rows.append(t)
assert len(dec_basis) == 9, 'the decoder rank!! (%d)' % len(dec_basis)
W = [[0] * 9 for _ in range(V)]
for t in range(V):
    r = B0[t]
    for k, (br, pi) in enumerate(dec_basis):
        if (r >> pi) & 1:
            W[t][k] = 1
            r ^= br
    assert r == 0, 'the W solve!!'
log('(2) the decoder: rank %d; the basis rows %s' % (len(dec_basis), dec_rows))

# ============ (3) THE FRAMES' MACHINERY ============
frames = [[]]
fidx = {}
def add_frame(basis_vecs, key):
    frames.append([[float(x) for x in bv] for bv in basis_vecs])
    fidx[key] = len(frames) - 1
    return fidx[key]
for s in range(V):
    add_frame([L[s]], ('sing', s))
full_basis = []
for s in range(V):
    vec = L[s]
    if any(abs(float(np.array(b) @ (FORM @ vec))) > 1e-9 for b in full_basis):
        continue
    full_basis.append(vec)
    if len(full_basis) == H:
        break
assert len(full_basis) == H
fidx_full = add_frame(full_basis, ('full',))
for t in range(V):
    perp = jlines[t]
    pb = []
    for s in perp:
        vec = L[s]
        if any(abs(float(np.array(b) @ (FORM @ vec))) > 1e-9 for b in pb):
            continue
        pb.append(vec)
        if len(pb) == H - 1:
            break
    assert len(pb) == H - 1, (t, len(pb))
    add_frame(pb, ('tperp', t))
log('(3) the frames: %d (the census-dependent rooms to be added!!)' % len(frames))

# ============ (4) THE CENSUS-DEPENDENT STUBS ============
# TODO (the census's notification!!): the rooms (the 12-frames!!), the room-sums R_f,
# the S_t chains, the targets' reads — the design per the census's covers!!
# THE EXPECTED (the SS1758's design!!): the ~70 12-frames; the perp(t) = the ~5-6 rooms +
# the remainder (the ~2-4 direct lines!!); the S_t chains: 0 -> the 12-frames (the FREE
# re-reads at the SAME frames!!!) -> the dim-6 unions -> the t-perp (8!!)
rooms = []              # TODO: the census's rooms (the (frozenset-lines, dim, mask)!!)!!
A = []                  # TODO: the builds (the carriers + the room-sums + the S_t chains!!)
B = []                  # TODO: the targets' reads!!
ret = []                # TODO: the 9 gathers!!
ret_frames = []
scatter = [[k for k in range(9) if W[t][k]] for t in range(V)]
R = 0                   # TODO: the honest R (the carriers + the room-sums + the S_t + the gathers!!)
log('(4) the census-dependent stubs in place (the design pending the census!!)')

# ============ (5) THE VAL-SIMULATION + THE D-DIRT'S AUTO-DERIVATION ============
# THE VALIDATED MACHINERY (the SS1745's control: the ratio 1.0!!!):
# (a) simulate the A-phase -> the full vals (the bitmask XORs!!)
# (b) the per-target: the scatter-vals ^ the B-vals (the read-XOR!!)
# (c) THE S_D(t): the helper-indicator parity sets (the bits >= 2V with the odd parity!!)
# (d) emit the D-gates (the dirt-doubling: the indicators cancel by the D + the reads!!)
def derive_dirt(A, B, ret, scatter, nreg, start):
    """the full val-simulation -> the per-target S_D sets (the transitive parity!!!)"""
    val = [1 << i for i in range(nreg)]
    for F, d, srcs in A:
        for s in srcs:
            val[d] ^= val[s]
    dirt = []
    for t in range(V):
        x = 0
        for k in scatter[t]:
            x ^= val[ret[k]]
        for F, d, srcs in B:
            if d == V + t:
                for s in srcs:
                    x ^= val[s]
        sd = []
        for q in range(2 * V, nreg):
            if (x >> q) & 1:
                sd.append(q)
        dirt.append(sd)
    return dirt

# ============ (6) THE WORD-DICT + THE GCHECK INTERFACE ============
# TODO (the census!!): the full assembly (the D-gates via the derive_dirt!!) + the gcheck run!!!
log('the scaffolding complete — awaiting the census (the background run!!)')

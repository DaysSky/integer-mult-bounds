"""THE 121-LINE WORD BUILD (the user's SS1708: 'ok can you actually fully build and verify it').

THE COMPLETE WORD (per the SS1713/SS1714 template + checker reads!!):
- v = 121 (the 120 E8 roots + the special (0,1,1)); h = 9 (the PD span: E8 + hyperbolic!!)
- THE FORM: the 10x10: the E8's 8x8 identity + the hyperbolic 2x2 (rows 8-9!!) — the lines:
  the roots (alpha, 0, 0); the special (0, 1, 1) — all norm 2 (the E8: alpha.alpha = 2; the
  special: 2*1*1 = 2!!!) ✓✓
- THE REGISTERS: 121 sources + 121 targets + THE HELPERS: THE PIECES (210!!) + THE TAILS
  (120!!) + THE GATHERS (9!!) = R = 339 ✓✓ (the SS1685 economy!!!)
- THE FRAMES: 0 (empty), the 121 singletons, FULL (dim 9), the 121 t-perps (dim 8), the
  pieces' spans (the ~2-4), the read-rooms (the per-piece: the users' common perp ⊇ the
  content ✓✓), the tails' joint-frames, THE FULL (the gathers: the cst = 9 x 9 = 81!!!)
- THE PHASES:
  D: [0, V+t, [the W[t]-gathers]] — the dirt pre-reads (the indicators' doubling!!!)
  A: the builds: the pieces at THEIR SPANS (the sources: {s} -> the pair-span -> the
     quad-span ✓ nested!!!); the tails at the joint-frames; the gathers at FULL
  scatter: the target t XORs its W[t]-weighted gathers — the payload: {t} ∪ junk(t)!!!
  B: [F_room, V+t, [the pieces + the tail]] — the junk cancellation (the XOR == junk(t)!!)
  C: the literal reverse of the A+B z-gates ✓
- THE gcheck RUN: the verdict; the true histogram; THE TRUE PRICE!!!

THE HONEST CAVEATS (the build's acceptance = the gcheck!!!): the piece-level rooms (the
ONE per piece ✓ by construction!!!) but the TARGETS' chains (the ~21 rooms at the dims
2-4: the one-per-dim!!!) may collide — THE GCHECK PINS THEM (the iterative fix!!!).
"""
import sys, json, itertools, time
from collections import Counter
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
log('(1) the system: %d lines; h=%d; the norms 2 ✓' % (V, H))

# ============ (2) THE DECODER (the perp-pattern B0: rank 9!!) ============
# the B0 rows: {t} ∪ perp(t) (the SS1149-1150 analysis!!!); the basis: the 9 rows; the W:
# junk(t) ∪ {t} = Σ_k W[t][k] * gather_k  (over GF(2)!!)
B0 = []
for t in range(V):
    row = [(1 << t) | PERP[t]]
    B0.append(row[0])
# the GF(2) basis of the row space (the pivot elimination!!)
basis = []          # the list of the (row-mask, the pivot-line)
basis_rows = []     # the original-row indices
piv2row = {}
for t in range(V):
    r = B0[t]
    for pr, pi in [(b[0], b[1]) for b in basis]:
        if (r >> pi) & 1:
            r ^= pr
    if r == 0:
        continue
    pi = (r & -r).bit_length() - 1
    basis.append((r, pi))
    basis_rows.append(t)
    piv2row[pi] = t
assert len(basis) == 9, 'the decoder rank!! (%d)' % len(basis)
# THE W: for each target t: the combination of the basis rows = the B0[t]!!
W = [[0] * 9 for _ in range(V)]
for t in range(V):
    r = B0[t]
    comb = []
    # the elimination: the recorded combination!!
    work = []
    for k, (br, pi) in enumerate(basis):
        if (r >> pi) & 1:
            comb.append(k)
            r ^= br
    assert r == 0, 'the W solve!!'
    for k in comb:
        W[t][k] = 1
log('(2) the decoder: rank %d; the basis rows %s' % (len(basis), basis_rows))

# ============ (3) THE PIECES' ECONOMY [the SS1685!!] ============
# the partition: the 30 disjoint 4-frames!!
avail = set(range(120))
pframes = []
while avail:
    a = min(avail)
    fr = [a]
    for b in sorted(avail):
        if len(fr) >= 4:
            break
        if all(abs(G[b][x]) < 1e-9 for x in fr):
            fr.append(b)
    for x in fr:
        avail.discard(x)
    pframes.append(sorted(fr))
piece_users = {}
for f in pframes:
    for r in (2, 3, 4):
        for sub in itertools.combinations(f, r):
            mask = PERP[sub[0]]
            for x in sub[1:]:
                mask &= PERP[x]
            users = [t for t in range(V) if t not in sub and (mask >> t) & 1]
            if len(users) >= 2:
                piece_users[sub] = users
covered = [set() for _ in range(V)]
pool = []
assigned = [[] for _ in range(V)]
while True:
    best = None
    for sub, users in piece_users.items():
        real = [t for t in users if all(s not in covered[t] for s in sub)]
        if len(real) < 2:
            continue
        k = len(sub); u = len(real)
        saving = k * u - (k + u)
        if saving < 4:
            continue
        if best is None or saving > best[0]:
            best = (saving, sub, real)
    if best is None:
        break
    _, sub, real = best
    pool.append((sub, real))
    for t in real:
        covered[t] |= set(sub)
        assigned[t].append(len(pool) - 1)
leftovers = [sorted(set(jlines[t]) - covered[t]) for t in range(V)]
n_pieces = len(pool)
n_tails = sum(1 for x in leftovers if x)
log('(3) the economy: %d pieces + %d tails + 9 gathers' % (n_pieces, n_tails))
N_pieces = n_pieces
N_tails = n_tails
N_gathers = 9
R = N_pieces + N_tails + N_gathers
log('    R = %d' % R)

# ============ (4) THE FRAMES ============
frames = [[]]                      # 0: the empty
fidx = {}
def add_frame(basis_vecs, key):
    frames.append([[float(x) for x in bv] for bv in basis_vecs])
    fidx[key] = len(frames) - 1
    return fidx[key]
for s in range(V):
    add_frame([L[s]], ('sing', s))
FULLB = [np.eye(10)[i][:9] for i in range(9)]      # hmm: the 9x10?! — the form is 10x10; the vectors are 10-dim!!!
# THE FIX: the ambient is 10-dim (the form!!); the lines are 10-dim; FULL = the span of the lines (dim 9!!)
# the FULL basis: the rref of the lines' span: the 9 independent lines!!!
full_basis = []
for s in range(V):
    vec = L[s]
    if any(abs(float(np.array(b) @ (FORM @ vec))) > 1e-9 for b in full_basis):
        continue
    full_basis.append(vec)
    if len(full_basis) == 9:
        break
assert len(full_basis) == 9
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
# the pieces' spans (the build-frames!!)
for qi, (sub, users) in enumerate(pool):
    add_frame([L[s] for s in sub], ('piece', qi))
# the tails' joint-frames (the span of the leftovers' 4-frames?!) — the SIMPLEST: the span of the leftover lines!!!
for t in range(V):
    if leftovers[t]:
        add_frame([L[s] for s in leftovers[t]], ('tail', t))
# the read-rooms: THE PER-PIECE: the piece's users' common perp ⊇ the piece ✓✓ — the frame: the
# piece's own span + the fillers INSIDE the common perp (the nondegenerate Gram!!!)
def fill_nondeg(vecs, cperp_lines):
    """extend the basis with the cperp lines until the Gram is nondegenerate; the dim minimal!!"""
    basis = [np.array(v, dtype=float) for v in vecs]
    changed = True
    while changed:
        changed = False
        M = np.array([[float(np.array(a) @ (FORM @ np.array(b))) for b in basis] for a in basis])
        if abs(np.linalg.det(M)) > 1e-12:
            break
        for s in cperp_lines:
            vec = L[s]
            if any(abs(float(np.array(b) @ (FORM @ vec))) > 1e-9 for b in basis):
                continue
            # the candidate: does it fix the degeneracy?!
            basis.append(vec)
            M2 = np.array([[float(np.array(a) @ (FORM @ np.array(b))) for b in basis] for a in basis])
            if abs(np.linalg.det(M2)) > 1e-12:
                changed = True
                break
            basis.pop()
        if not changed:
            raise RuntimeError('cannot fill the room!!')
    return basis
room_idx = {}
for qi, (sub, users) in enumerate(pool):
    cperp = PERP[users[0]]
    for t in users[1:]:
        cperp &= PERP[t]
    cperp_lines = [s for s in range(V) if (cperp >> s) & 1]
    room_idx[qi] = add_frame(fill_nondeg([L[s] for s in sub], cperp_lines), ('room', qi))
log('(4) the frames: %d' % len(frames))

# ============ (5) THE REGISTERS ============
nreg = 2 * V + R
# the helpers: the pieces (2V .. 2V+N_pieces-1!!), the tails, the gathers
piece_reg = lambda qi: 2 * V + qi
tail_reg = lambda t: 2 * V + N_pieces + t        # hmm: the tails: the per-target (the ones with leftovers!!)
tail_targets = [t for t in range(V) if leftovers[t]]
tail_reg_of = {t: 2 * V + N_pieces + i for i, t in enumerate(tail_targets)}
gather_reg = lambda k: 2 * V + N_pieces + N_tails + k
start = [0] * nreg
final = [0] * nreg
for s in range(V):
    start[s] = fidx[('sing', s)]
    final[s] = fidx_full
for t in range(V):
    start[V + t] = 0
    final[V + t] = fidx[('tperp', t)]
for q in range(2 * V, nreg):
    start[q] = 0
    final[q] = fidx_full

# ============ (6) THE GATES ============
# D: [0, V+t, [the W[t]-gathers]] — the dirt pre-reads (the indicators' doubling!!!)
D = []
for t in range(V):
    # THE DIRT-DOUBLING: pre-read EVERY register whose val the target XORs later (the scatter's
    # gathers + the B's pieces + the tail!!) — the indicators cancel by the doubling!!!
    dirt = [gather_reg(k) for k in range(9) if W[t][k]]
    dirt += [piece_reg(qi) for qi in assigned[t]]
    if t in tail_reg_of:
        dirt.append(tail_reg_of[t])
    D.append([0, V + t, dirt])
# A: the builds!!
A = []
# the pieces: at their spans (the sources: {s} -> the piece's span (the s ∈ the span!!!)!!)
for qi, (sub, users) in enumerate(pool):
    A.append([fidx[('piece', qi)], piece_reg(qi), list(sub)])
# the tails: at the leftovers' spans (the sources: {s} -> the span (the s ∈ it!!)!!)
for t in tail_targets:
    A.append([fidx[('tail', t)], tail_reg_of[t], list(leftovers[t])])
# the gathers: at FULL (the sources: the 4-frames -> FULL?? — hmm: THE SOURCES' CHAINS!!!
# the source s: the piece-spans (the ~2-3-dim!!!) -> the FULL: the climb 3->9?!!
# the NESTING: the piece-span ⊆ FULL ✓✓ (the lines ⊆ the FULL!!!) ✓ LEGAL!!
# BUT: the source's chain: the {s} -> the piece-spans (the ~2-3!!!): the MULTIPLE piece-spans!!!
# the one-frame-per-dim: the s's pieces: the ~2-7: the spans at the SAME dim (the 2-3!!!):
# THE COLLISIONS — THE GCHECK PINS THEM (the honest first cut!!!)!!
for k, (brow, pi) in enumerate(basis):
    srcs = [s for s in range(V) if (brow >> s) & 1]
    A.append([fidx_full, gather_reg(k), srcs])
# the scatter: the retained = the 9 gathers; the W-weighted!!
ret = [gather_reg(k) for k in range(9)]
ret_frames = [fidx_full] * 9
scatter = [[k for k in range(9) if W[t][k]] for t in range(V)]
# B: the junk cancellation: the target reads its pieces (at the piece-rooms!!) + its tail!!
B = []
for t in range(V):
    for qi in assigned[t]:
        B.append([room_idx[qi], V + t, [piece_reg(qi)]])
    if t in tail_reg_of:
        # the tail's room: the tail's span ⊆ the t-perp ✓; the target's chain: the tail-span!!
        B.append([fidx[('tail', t)], V + t, [tail_reg_of[t]]])
# C: the literal reverse of the A+B z-gates!!
zg = [[F, d, s] for F, d, s in A + B if not (V <= d < 2 * V)]
C = [[fidx_full, d, s] for (_, d, s) in reversed(zg)]

w = dict(
    h=H, v=V, R=R,
    form=dict(num=[[int(x) for x in row] for row in FORM], den=1),
    lines=[[float(x) for x in L[s]] for s in range(V)],
    frames=frames, start=start, final=final,
    D=D, A=A, B=B, C=C,
    ret=ret, ret_frames=ret_frames, scatter=scatter,
)
path = '/private/var/folders/cg/9jd0z3791rv0t784bs323m7m0000gn/T/opencode/ii19_121_word.json'
import os
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, 'wt') as f:
    json.dump(w, f)
log('the word written: %s (R = %d)' % (path, R))
log('the gates: D %d | A %d | B %d | C %d' % (len(D), len(A), len(B), len(C)))

from gcheck import main
try:
    out = main(path, do_price=True)
    log('GCHECK VERDICT:')
    print(json.dumps(out, indent=1, default=str))
except Exception as e:
    log('REJECT: %s' % e)
    sys.exit(1)

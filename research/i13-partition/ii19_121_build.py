"""THE 121-LINE WORD — THE BUILD STAGE 2a: THE DECODER FACTORIZATION + THE READ CLUSTERING.

THE STAGE-1 GATES (ii19_121slots.py, SS1419): ALL PASS (the dims!!, the packings!!, the
frames-per-piece budget!!, the honest R = 299!!).

THE STAGE 2a (this script):
1. THE DECODER FACTORIZATION: the perp-pattern B (the GF(2) rank 9!!) = U·W^T:
   the 9 basis rows u_k (THE GATHERS: the retained's content!!) + the W-coordinates
   (THE SCATTER: the target t XORs the gathers {k : W[t,k] = 1}!!): B[t] = Σ W[t,k]·u_k.
2. THE READ CLUSTERING: at each dim d, the reads (piece, target) form the CONNECTED
   COMPONENTS (the transitive: the piece's dim-d frame == the target's dim-d slot!!):
   each component shares ONE frame: span(∪ the pieces) + the fillers ⊆ ∩(the targets'
   perps), at the dim d.  THE CHECKS: (a) span(∪P) ⊆ ∩perps; (b) rank(∪P) <= d;
   (c) d <= 9 - rank(the component's targets!!).
3. THE NESTING: the pieces'/targets' chains: the frames at the ascending dims: the
   incremental fillers (F_d2 ⊇ F_d1 + the new content!!).
4. THE VERDICT + the stage-2b pickle (the clusters + the frames for the word!!).
"""
import sys, time, resource, itertools, pickle
from collections import Counter
import numpy as np
t0 = time.time()
def log(*a): print('[%5.0fs rss=%dMB]' % (time.time() - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // (1024 * 1024)), *a, flush=True)

# the system: the 120 E8 roots + the special (0,1,1)  [the SS1419 code]
roots = []
for i in range(8):
    for j in range(i + 1, 8):
        for si in (1, -1):
            for sj in (1, -1):
                v = np.zeros(8); v[i] = si; v[j] = sj
                roots.append(v)
half = [np.array(s, dtype=float) / 2 for s in itertools.product([1, -1], repeat=8) if s.count(-1) % 2 == 0]
def canon(v):
    for x in v:
        if x != 0:
            return tuple(v) if x > 0 else tuple(-v)
    return tuple(v)
d8 = {}
for r in list(roots) + half: d8[canon(r)] = np.array(r)
AL = list(d8.values())
L = [list(al) + [0, 0] for al in AL]
L.append([0.0] * 8 + [1.0, 1.0])
L = np.array(L, dtype=float)
V = len(L)
FORM = np.zeros((10, 10)); FORM[:8, :8] = np.eye(8); FORM[8, 9] = FORM[9, 8] = 1.0
G = L @ FORM @ L.T
PERP = []
for t in range(V):
    m = 0
    for s in range(V):
        if s != t and abs(G[s][t]) < 1e-9:
            m |= (1 << s)
    PERP.append(m)
log('the 121-line system: %d lines' % V)

# the stage-1 design data
D = pickle.load(open('/Users/dayssky/integer-mult-bounds/research/i13-partition/ii19_121_design.pkl', 'rb'))
pool = [list(p) for p in D['pool']]
pool_users = D['pool_users']
pranks = D['pranks']
leftovers = D['leftovers']
tgt_slot = D['tgt_slot']       # (target, piece_id or -1) -> the slot dim
src_assign = D['src_assign']    # (source, piece_id) -> the dim
rank_B = D['rank_B']
carriers = sum(1 for lo in leftovers if lo)
log('the design data: %d pieces, %d carriers, rank %d, R_honest %d' % (len(pool), carriers, rank_B, D['R_honest']))

# ============ (1) THE DECODER FACTORIZATION ============
Brows = [PERP[t] | (1 << t) for t in range(V)]
# the reduction: the pivot (col, row) pairs
rows = list(Brows)
basis = []   # the (pivot_col, the reduced row) — ascending pivots!!
r = 0
for col in range(V):
    piv = next((i for i in range(r, len(rows)) if (rows[i] >> col) & 1), None)
    if piv is None:
        continue
    rows[r], rows[piv] = rows[piv], rows[r]
    for i in range(len(rows)):
        if i != r and (rows[i] >> col) & 1:
            rows[i] ^= rows[r]
    basis.append((col, rows[r]))
    r += 1
log('(1) the factorization: the GF(2) rank %d (the pivots: %s)' % (len(basis), [c for c, _ in basis]))
assert len(basis) == rank_B == 9

def gf2_solve(target_row):
    """the coordinates of the target row in the reduced basis (the residual must be 0!!)"""
    coords = [0] * len(basis)
    rrow = target_row
    for k, (col, row) in enumerate(basis):
        if (rrow >> col) & 1:
            coords[k] = 1
            rrow ^= row
    assert rrow == 0, 'the residual nonzero!!'
    return coords

W = [gf2_solve(Brows[t]) for t in range(V)]
gathers = [row for _, row in basis]   # the 9 basis rows: the retained's content (the bitmasks!!)
gsets = [[s for s in range(V) if (g >> s) & 1] for g in gathers]
log('    the gathers (the U-columns): the sizes %s (mean %.1f)' % (sorted(len(gs) for gs in gsets), sum(len(gs) for gs in gsets) / 9))
wloads = Counter(sum(w) for w in W)
log('    the W-rows (the scatter): the weights %s (mean %.1f)' % (dict(sorted(wloads.items())), sum(sum(w) for w in W) / V))
# the verification: B[t] == Σ W[t,k]·u_k
for t in range(V):
    acc = 0
    for k in range(9):
        if W[t][k]:
            acc ^= gathers[k]
    assert acc == Brows[t], ('the factorization mismatch at %d' % t)
log('    the factorization VERIFIED: B[t] = Σ W[t,k]·u_k for all %d targets' % V)

# ============ (2) THE READ CLUSTERING (the components at each dim) ============
# the reads: the (piece_id or -1, target) with the §1419 slot dims
reads = []
for (ti, pid), d in tgt_slot.items():
    reads.append((pid, ti, d))
log('(2) the reads: %d (the pieces) + the tails' % len(reads))

# the union-find over the reads at each dim: the pieces + the targets: the components
def uf_find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x
def uf_union(parent, a, b):
    ra, rb = uf_find(parent, a), uf_find(parent, b)
    if ra != rb:
        parent[ra] = rb
        return True
    return False

# the node ids: the pieces: 0..155; the targets: 1000+ti
NODE_T = 1000
# the components per dim: the union-find + the members
dim_components = {}
fail_span, fail_dim, ok_comps = 0, 0, 0
comp_pieces = {}
comp_targets = {}
for d in range(2, 9):
    dreads = [(p, u) for (p, u, dd) in reads if dd == d]
    if not dreads:
        continue
    parent = {}
    def node(x):
        if x not in parent:
            parent[x] = x
        return x
    for p, u in dreads:
        node(p); node(NODE_T + u)
        uf_union(parent, p, NODE_T + u)
    # the members
    comps = {}
    for x in list(parent.keys()):
        root = uf_find(parent, x)
        comps.setdefault(root, {'pieces': [], 'targets': []})
        if x < NODE_T:
            comps[root]['pieces'].append(x)
        else:
            comps[root]['targets'].append(x - NODE_T)
    # THE CHECKS: span(∪P) ⊆ ∩(U's perps) + rank(∪P) <= d + d <= 9 - rank(U's targets)
    n_ok = 0
    for root, mem in comps.items():
        plines = sorted(set(itertools.chain.from_iterable(pool[p] for p in mem['pieces'])))
        span_r = int(np.linalg.matrix_rank(np.array([L[i] for i in plines]))) if plines else 0
        trank = int(np.linalg.matrix_rank(np.array([L[i] for i in mem['targets']]))) if mem['targets'] else 0
        # the ∩perps: the vectors ⊥ all the targets: rank-based: dim = 9 - trank
        ipdim = 9 - trank
        # the span ⊆ the ∩perps: every piece line ⊥ every target!!
        ok_orth = all(abs(G[p][u]) < 1e-9 for p in plines for u in mem['targets'])
        if ok_orth and span_r <= d <= ipdim:
            n_ok += 1
            ok_comps += 1
            comp_pieces[(d, root)] = plines
            comp_targets[(d, root)] = mem['targets']
        else:
            fail_span += (span_r > d)
            fail_dim += (d > ipdim)
    dim_components[d] = len(comps)
    log('    dim %d: %d components (%d ok, %d pieces, %d targets); the failures so far: span %d, dim %d'
        % (d, len(comps), n_ok, sum(len(c['pieces']) for c in comps.values()),
           sum(len(c['targets']) for c in comps.values()), fail_span, fail_dim))

log('(2) THE CLUSTERING: %d components ok, %d span-failures, %d dim-failures'
    % (ok_comps, fail_span, fail_dim))
tot = sum(len(v) for v in dim_components.values())
log('    the components per dim: %s (total %d)' % (dict(sorted(dim_components.items())), tot))

# ============ (3) THE NESTING (the chains' frames) ============
# the pieces' chains: the build-frame (the span!!) + the read-frames (the ascending dims!!)
# the targets' chains: the read-frames (the ascending dims!!) + the t-perp
piece_read_dims = {p: sorted(set(d for (pp, u, d) in reads if pp == p)) for p in range(len(pool))}
nest_viol = 0
for p, dims in piece_read_dims.items():
    if any(dims[i] == dims[i + 1] for i in range(len(dims) - 1)):
        nest_viol += 1
log('(3) the nesting: the pieces\' read-dims distinct: %d violations' % nest_viol)
tgt_read_dims = {t: sorted(set(d for (p, u, d) in reads if u == t)) for t in range(V)}
tv = sum(1 for t, dims in tgt_read_dims.items() if any(dims[i] == dims[i+1] for i in range(len(dims)-1)))
log('    the targets\' read-dims distinct: %d violations' % tv)

# ============ (4) THE VERDICT + THE STAGE-2b PICKLE ============
ok = (fail_span == 0) and (fail_dim == 0) and (nest_viol == 0) and (tv == 0)
log('(4) THE STAGE-2a VERDICT: %s' % ('FEASIBLE — the clusters + the factorization saved; the stage 2b (the word!!) proceeds!!' if ok
    else 'TIGHT: the repairs needed (the re-dimming of the failing reads!!)'))
out = dict(gathers=gsets, W=W, comp_pieces={str(k): v for k, v in comp_pieces.items()},
           comp_targets={str(k): v for k, v in comp_targets.items()},
           piece_read_dims={str(k): v for k, v in piece_read_dims.items()},
           tgt_read_dims={str(k): v for k, v in tgt_read_dims.items()},
           reads=reads, rank_B=rank_B)
with open('/Users/dayssky/integer-mult-bounds/research/i13-partition/ii19_121_stage2a.pkl', 'wb') as f:
    pickle.dump(out, f)
log('the stage-2a data pickled: ii19_121_stage2a.pkl')
log('DONE')

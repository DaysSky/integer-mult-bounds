"""Dead-minimizer for the PG(2,3) frame-top instance of I_{13,1} (the register identity R + v = sum c_t + dead
with c_t = 2 proven, so R = 364 + dead; frontier allowance dead <= ~1,020-1,310).

Model (exact at the pool-accounting level, mirroring 7c's flat-sum middle):
- Pieces: closed nondegenerate flats F (rank <= 10) with content c(F) = any vector of L(F); one register per
  distinct piece (F, subset-reduced by XOR identity is handled at the demand side).
- Each demand E (lines, at frame S) must be the XOR of pieces whose flats lie in S and whose union covers E
  is NOT required (overlap lines cancel) — only the exact GF(2) sum matters.  To keep the model finite we use
  the 7c flat-sum semantics: a demand is served by pieces e_1..e_k (disjoint, union = E) OR by an XOR-combination
  of >= 2 pieces whose symmetric difference is E.  XOR-combinations multiply pools, so v1 uses disjoint covers
  (each demand partitioned into pieces), the 7c accounting; XOR variants are a v2 refinement.
- Cost: dead = sum over pieces of (uses_in_pools(arrivals) - 1) when a piece feeds >= 2 pools...  Precisely the
  7c rule: a pool (formed flat) with k input registers and m outputs (m = #demands it serves distinctly) costs
  max(0, m - k) extra registers; each piece register itself costs 1 (carried from the bottom).
  Total registers = (#pieces) + sum_pools max(0, m_p - k_p) + v, and dead = R (non-target registers) minus the
  branch floor 2v: R = 2v + dead is the 7c frame-0 budget; we minimise R = sum(1 for pieces) + sum(max(0, m-k)).

v1 scope: pieces = flats of the demand frames and their pairwise intersections (hubs1 vocabulary), plus
demand-sized sums; disjoint piece covers of demands; pools = the distinct flats used >= 2 times.
This is a linear program: minimise sum_p x_p (piece registers) + sum_p max(0, uses_p - 1) where uses_p counts
demands served with p as a *formed* intermediate.  Simplification faithful to 7c: dead = sum_p (c_p - 1) over
formed flats c_p (each formed flat with c inputs loses c-1 registers), and leaf pieces (line sums at rank 1/2)
are free inputs.  So: minimise total cost = sum over non-leaf pieces (inputs - 1), where a demand served by a
single leaf piece costs only the piece chain below it.
"""
import os, pickle, collections, itertools, sys, time
import numpy as np
from ortools.sat.python import cp_model

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g13 = Geom(13); V = g13.V; HYP = g13.HYP; G = g13.G
bits = g13.bits
pc = lambda m: bin(m).count('1')
def pm(m):
    r = (1 << V) - 1
    for s in bits(m): r &= HYP[s]
    return r
def cl(m): return g13.closure(m)[0] if m else 0
def rk(m): return g13.closure(m)[1] if m else 0

# rebuild the PG(2,3) instance exactly as i13n/part13.py (self-contained: no /home/user paths)
idx = g13.idx
P = lambda a, b: idx[('P', tuple(sorted((a % 13, b % 13))))]
T = lambda a, b, c: idx[('T', tuple(sorted((a % 13, b % 13, c % 13))))]
D = [0, 1, 3, 9]
def good(q):
    for t in q:
        es = [e for e in q if e != t]
        R = HYP[t] & ~sum(1 << e for e in es); a, b, cc = (HYP[e] for e in es)
        if R & ~(a ^ b ^ cc): return False
    return all(G[x, y] == 0 for x, y in itertools.combinations(q, 2))
def build_partition():
    for c in range(13):
        if c in D: continue
        Ts = [T(k + d1, k + d2, k + c) for k in range(13) for d1, d2 in itertools.combinations(D, 2)]
        if len(set(Ts)) == 78: break
    pptt = []
    for k in range(13):
        W = [(k + d) % 13 for d in D]; p = (k + c) % 13
        for (a, b), (cc, d) in [((W[0], W[1]), (W[2], W[3])), ((W[0], W[2]), (W[1], W[3])), ((W[0], W[3]), (W[1], W[2]))]:
            pptt.append((P(a, b), P(cc, d), T(a, b, p), T(cc, d, p)))
    assert all(good(f) for f in pptt)
    used = set(l for f in pptt for l in f); rest = [l for l in range(V) if l not in used]
    Tl = list(rest); sup = {l: set(g13.supp[l]) for l in Tl}
    cand = []
    for S6 in itertools.combinations(range(13), 6):
        trs = [l for l in Tl if sup[l] <= set(S6)]
        for q in itertools.combinations(trs, 4):
            if all(len(sup[x] & sup[y]) == 1 for x, y in itertools.combinations(q, 2)) and good(q): cand.append(q)
    cand = sorted(set(tuple(sorted(q)) for q in cand))
    m = cp_model.CpModel(); x = [m.NewBoolVar('x%d' % i) for i in range(len(cand))]
    for l in rest: m.AddExactlyOne([x[i] for i, q in enumerate(cand) if l in q])
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 600; s.parameters.num_workers = 8
    st = s.Solve(m); assert st in (cp_model.OPTIMAL, cp_model.FEASIBLE), s.StatusName(st)
    tttt = [cand[i] for i in range(len(cand)) if s.Value(x[i])]
    return pptt + tttt
PF = os.path.join(HERE, 'pg23_partition.pkl')
if os.path.exists(PF): part = pickle.load(open(PF, 'rb'))
else: part = build_partition(); pickle.dump(part, open(PF, 'wb'))
assert sorted(l for f in part for l in f) == list(range(V))

# demands (7c convention)
DEM = []
for fi, f in enumerate(part):
    Q = HYP[f[0]] & HYP[f[1]] & HYP[f[2]] & HYP[f[3]]
    DEM.append(('Q', Q, Q, fi, f))
    for a, b in itertools.combinations(range(4), 2):
        o = [z for z in range(4) if z not in (a, b)]
        E = HYP[f[a]] & HYP[f[b]] & ~HYP[f[o[0]]] & ~HYP[f[o[1]]]
        DEM.append(('E', HYP[f[a]] & HYP[f[b]], E, fi, (f[a], f[b])))
ddem = list(set(d[2] for d in DEM))
print('frames', len(part), 'demands', len(DEM), 'distinct', len(ddem), flush=True)

# piece candidates: closed flats S with 1 <= rank <= 10 that are subsets of some demand frame, union-closed closure
# of the demand-frame intersection lattice (hubs1 vocabulary) PLUS per-demand sub-flats from ecover hyperplanes.
t0 = time.time()
def log(*a, **kw): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
frames = sorted(set(d[1] for d in DEM))
log('distinct demand frames', len(frames))
cand = set()
for S in frames:
    cand.add(S)
    Sl = bits(S)
    # line-normal hyperplanes (the ecover vocabulary) and their closures
    for u in Sl:
        A = cl(S & HYP[u])
        if A != S: cand.add(A)
# pairwise intersections (hubs1); triples are left to column generation (the ILP master requests them)
for i in range(len(frames)):
    for j in range(i + 1, len(frames)):
        x = frames[i] & frames[j]
        if pc(x) >= 4: cand.add(x)
cand = {A for A in cand if A and rk(A) <= 10 and A != (1 << V) - 1}
log('candidate flats', len(cand), '%.0fs' % (time.time() - t0))
# nondegeneracy + reachability: only flats of rank <= 10 that can be built from below (any flat can: build
# greedily line by line inside itself).  Nondegenerate check:
ND = {}
def nondeg(A):
    if A not in ND:
        b = []
        for i in bits(A):
            if np.linalg.matrix_rank(g13.LA[b + [i]]) > len(b): b.append(i)
        Gm = np.array([[G[a, bb] for bb in b] for a in b], dtype=float)
        ND[A] = abs(round(np.linalg.det(Gm))) > 0
    return ND[A]
cand = {A for A in cand if nondeg(A)}
log('nondegenerate candidates', len(cand))

# demands: for each distinct content E with frame S, the candidate pieces are candidate flats A with
# cl(A) <= S... no: piece frame must lie INSIDE the demand frame S (content-in-frame), and piece content
# is a set of lines (we use flat line sets; sums of flats as sets = symmetric difference at the vector level,
# but 7c flat-sum semantics = set union for disjoint pieces).  v1: disjoint set covers of E by candidate
# flats inside S.
dem_cand = {}
for E in ddem:
    S = cl(E)
    dem_cand[E] = sorted(A for A in cand if A & ~S == 0 and A != S)
log('piece options per demand: min %d max %d mean %.0f' % (
    min(len(v) for v in dem_cand.values()), max(len(v) for v in dem_cand.values()),
    sum(len(v) for v in dem_cand.values()) / len(dem_cand)), flush=True)
pickle.dump({'part': part, 'DEM_kind': [(d[0], d[1], d[2]) for d in DEM], 'cand': sorted(cand),
             'dem_cand': dem_cand}, open(os.path.join(HERE, 'deadmin_instance.pkl'), 'wb'))
log('instance saved')

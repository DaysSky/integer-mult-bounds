"""THE CLASS-PARTITION CENSUS (ii19_nat108.py) — the E8-block analog on the ext120, confirmed or killed.

The §744 step (1).  The ext120 system (ii19_nat69_spec.json) partitioned into disjoint line families; for each
family: the class span-dims, the ⊥-target sets (the targets t with span(class) ⊆ t-perp), and whether the B-reads
of the nat107 read design (the 54 matched pieces + the source-fills) can be taken at ONE shared class-frame per
target gate (the r434's dying-wire block nodes: all of a node's readers at one frame, zero climbs).

Families (each found as an exact cover by MILP over its candidate sets):
  axis15   8 classes of 15 lines, one coordinate axis each, at the minimum common span-dim (the §744 classes)
  D4pairs  10 D4 blocks (12 lines, span 4) in 5 complementary pairs
  frame4   30 orthogonal D4-type 4-frames (4 lines, span 4)
  frame8   15 orthogonal 8-frames (8 lines, span 8)
  A3       20 disjoint A3 sub-systems (6 lines, span 3)
  A2       40 disjoint A2 triples (3 lines, span 2)
The shared-frame test per (target t, wire w) read: some class K with home(w) ⊆ span(K) ⊆ t-perp.  Per target the
class frames it can use form a chain (one frame per dim, nested); same-family classes are pairwise incomparable,
so a target uses at most one class frame per family-dim.  The census reports, per family, the reads servable at
a class frame, the per-target best single-frame coverage of its reads, and the dup-fills the rest would need
under the nat107 accounting (one dup per extra frame of a wire), against the dup budget 47.
"""
import os, sys, json, itertools
from collections import Counter, defaultdict
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
log = lambda *a: print(*a, file=sys.stderr, flush=True)

SPEC = json.load(open('ii19_nat69_spec.json', 'rt'))
L = np.array(SPEC['lines'], dtype=float)
V = len(L)
G = L @ L.T
PERP = [set(p) for p in SPEC['PERP']]
PM = [sum(1 << s for s in PERP[t]) for t in range(V)]
AXES = [i for i in range(V) if np.count_nonzero(L[i]) == 1]
assert len(AXES) == 8

_span = {}
def span_mask(idx):
    """the lines inside span(L[idx]) as a bitmask, and the span dim"""
    key = tuple(sorted(idx))
    if key in _span: return _span[key]
    A = L[list(key)]
    u, s, vt = np.linalg.svd(A)
    r = int((s > 1e-9).sum())
    Q = vt[:r]
    res = L - (L @ Q.T) @ Q
    m = 0
    for i in np.nonzero(np.abs(res).max(axis=1) < 1e-9)[0]: m |= 1 << int(i)
    _span[key] = (m, r)
    return m, r
bits = lambda m: [i for i in range(V) if (m >> i) & 1]
pc = lambda m: m.bit_count()

def exact_cover(cands, name, extra=None):
    """choose disjoint candidate sets covering all 120 lines (MILP feasibility)"""
    n = len(cands)
    A = np.zeros((V, n))
    for j, c in enumerate(cands):
        for i in c: A[i, j] = 1
    cons = [LinearConstraint(A, 1, 1)]
    if extra is not None: cons += extra(cands)
    res = milp(c=np.zeros(n), constraints=cons, integrality=np.ones(n), bounds=Bounds(0, 1),
               options=dict(time_limit=600))
    if res.x is None:
        log('  %s: NO exact cover (%s)' % (name, res.message)); return None
    sel = [cands[j] for j in range(n) if res.x[j] > 0.5]
    log('  %s: exact cover with %d classes' % (name, len(sel)))
    return sel

# ---------------- the candidate families ----------------
ORTH = [[j for j in range(V) if j != i and G[i, j] == 0] for i in range(V)]
def cliques(k):
    out = []
    def rec(cl, cand):
        if len(cl) == k: out.append(tuple(cl)); return
        for j in cand:
            if j > cl[-1]: rec(cl + [j], [x for x in cand if x > j and G[j, x] == 0])
    for i in range(V): rec([i], [x for x in ORTH[i] if x > i])
    return out
log('(0) the candidates')
fr4 = [q for q in cliques(4) if pc(span_mask(q)[0]) == 12]
log('  D4-type orthogonal 4-frames: %d' % len(fr4))
fr8 = cliques(8)
log('  orthogonal 8-frames: %d' % len(fr8))
d4 = sorted(set(span_mask(q)[0] for q in fr4))
log('  D4 sub-systems (4-dim, 12 lines): %d' % len(d4))
a2 = sorted(set(span_mask((i, j))[0] for i in range(V) for j in range(i + 1, V) if abs(G[i, j]) == 2))
a2 = [m for m in a2 if pc(m) == 3]
log('  A2 triples: %d' % len(a2))
a3 = set()
for m in a2:
    i, j, k = bits(m)
    for x in range(V):
        if (m >> x) & 1: continue
        mm, r = span_mask((i, j, x))
        if r == 3 and pc(mm) == 6: a3.add(mm)
a3 = sorted(a3)
log('  A3 sub-systems (3-dim, 6 lines): %d' % len(a3))

# ---------------- the exact covers ----------------
log('(1) the exact covers')
FAM = {}
comp = {m: span_mask(bits(sum(1 << x for x in range(V) if all(G[x, y] == 0 for y in bits(m)))))[0] for m in d4}
pairs = [(m, comp[m]) for m in d4 if pc(comp[m]) == 12 and m < comp[m]]
log('  complementary D4 pairs: %d' % len(pairs))
sel = exact_cover([bits(a | b) for a, b in pairs], 'D4pairs')
if sel:
    FAM['D4pairs'] = []
    for s in sel:
        a, b = next((a, b) for a, b in pairs if (a | b) == sum(1 << x for x in s))
        FAM['D4pairs'] += [bits(a), bits(b)]
for name, cands in (('frame4', [list(q) for q in fr4]), ('frame8', [list(q) for q in fr8]),
                    ('A3', [bits(m) for m in a3]), ('A2', [bits(m) for m in a2])):
    sel = exact_cover(cands, name)
    if sel: FAM[name] = sel

# the axis-anchored 15-line classes: 8 classes, one axis each, every class inside a d-dim subspace
def axis_classes(d):
    """candidate d-dim subspaces (spanned by lines) holding >= 15 lines and exactly one axis"""
    subs = set()
    base = {3: a3, 4: d4}.get(d)
    if d == 5:
        # every 5-dim subspace with >= 15 lines contains a D4: enumerate the spans of a D4 4-frame + one line
        frame_of = {}
        for q in fr4: frame_of.setdefault(span_mask(q)[0], list(q))
        for m, q in frame_of.items():
            for x in range(V):
                if (m >> x) & 1: continue
                mm, r = span_mask(q + [x])
                if r == 5 and pc(mm) >= 15: subs.add(mm)
    return [m for m in subs if sum(1 for a in AXES if (m >> a) & 1) >= 1]
log('(2) the axis-anchored 15-line classes')
AX = None
for d in (5,):
    subs = axis_classes(d)
    log('  dim %d: %d candidate subspaces with >= 15 lines' % (d, len(subs)))
    # MILP: z[l,i] line l in class i; u[S,i] class i uses subspace S (S must hold axis i)
    S_of = {i: [m for m in subs if (m >> AXES[i]) & 1] for i in range(8)}
    nz = V * 8; idxu = {}
    for i in range(8):
        for m in S_of[i]: idxu[(m, i)] = nz + len(idxu)
    n = nz + len(idxu)
    rows, lo, hi = [], [], []
    def row(coef, a, b):
        r = np.zeros(n)
        for k, v in coef: r[k] = v
        rows.append(r); lo.append(a); hi.append(b)
    for l in range(V): row([(l * 8 + i, 1) for i in range(8)], 1, 1)
    for i in range(8):
        row([(l * 8 + i, 1) for l in range(V)], 15, 15)
        row([(AXES[i] * 8 + i, 1)], 1, 1)
        row([(idxu[(m, i)], 1) for m in S_of[i]], 1, 1)
        for l in range(V):
            row([(l * 8 + i, 1)] + [(idxu[(m, i)], -1) for m in S_of[i] if (m >> l) & 1], -np.inf, 0)
    res = milp(c=np.zeros(n), constraints=[LinearConstraint(np.array(rows), lo, hi)],
               integrality=np.ones(n), bounds=Bounds(0, 1), options=dict(time_limit=900))
    if res.x is not None:
        AX = [[l for l in range(V) if res.x[l * 8 + i] > 0.5] for i in range(8)]
        log('  dim %d: FEASIBLE — 8 classes of 15, each inside a %d-dim subspace' % (d, d))
        break
    log('  dim %d: infeasible (%s)' % (d, res.message))
if AX is None:
    # the fallback: a balanced 15-line assignment (no span constraint) — the classes then span what they span
    log('  the fallback: the axis-anchored greedy by inner product (the classes span freely)')
    AX = [[a] for a in AXES]
    rest = [l for l in range(V) if l not in AXES]
    for l in rest:
        best = min((i for i in range(8) if len(AX[i]) < 15),
                   key=lambda i: (span_mask(AX[i] + [l])[1], -abs(G[l, AXES[i]])))
        AX[best].append(l)
FAM['axis15'] = AX

# ---------------- (3) the census per family ----------------
log('(3) the census: span-dims, the ⊥-target sets, the per-target coverage')
summary = {}
for name, classes in FAM.items():
    cm = [sum(1 << x for x in c) for c in classes]
    sp = [span_mask(c) for c in classes]
    dims = Counter(r for _, r in sp)
    perpT = [[t for t in range(V) if (sp[k][0] & ~PM[t]) == 0] for k in range(len(classes))]
    nperp = Counter(len(p) for p in perpT)
    tcov = []
    for t in range(V):
        ks = [k for k in range(len(classes)) if t in perpT[k]]
        tcov.append((len(ks), max((pc(sp[k][0] & PM[t]) for k in ks), default=0)))
    summary[name] = dict(classes=len(classes), sizes=dict(Counter(len(c) for c in classes)),
                         span_dims=dict(dims), perp_targets=dict(sorted(nperp.items())),
                         per_target_classes=dict(sorted(Counter(a for a, _ in tcov).items())),
                         per_target_best_frame_lines=dict(sorted(Counter(b for _, b in tcov).items())))
    log('  %-8s %3d classes sizes %s | span-dims %s | ⊥-targets/class %s | classes ⊥ t %s | best frame covers %s of the 63'
        % (name, len(classes), dict(Counter(len(c) for c in classes)), dict(dims), dict(sorted(nperp.items())),
           summary[name]['per_target_classes'], summary[name]['per_target_best_frame_lines']))

# ---------------- (4) the shared class-frame read test on the nat107 read design ----------------
log('(4) the nat107 read design at the class frames')
P70 = json.load(open('ii19_nat70_pool.json', 'rt'))
pool3 = [(sorted(p), sorted(u)) for p, u in P70['pool']]
pool3.sort(key=lambda pu: -len(pu[1]))
bc_used = set(); kept = []
for ps, users in pool3:
    if any(x in bc_used for x in ps): continue
    kept.append(tuple(ps)); bc_used.update(ps)
    if len(kept) >= 54: break
PMASK = {p: sum(1 << s for s in p) for p in kept}
def solve_pieces(t):
    res = set(PERP[t]); base = []
    while True:
        resm = sum(1 << s for s in res)
        best_p, best_red = None, 0
        for p in kept:
            if PMASK[p] & ~PM[t]: continue
            m = pc(PMASK[p] & resm); red = m - (3 - m)
            if red > best_red: best_red = red; best_p = p
        if best_p is None or best_red <= 0: break
        base.append(best_p); res ^= set(best_p)
    return base, res
readers = defaultdict(list)
for t in range(V):
    b, f = solve_pieces(t)
    for p in b: readers[('P', p)].append(t)
    for s in f: readers[('S', s)].append(t)
home = {w: (span_mask(list(w[1]))[0] if w[0] == 'P' else 1 << w[1]) for w in readers}
nreads = sum(len(r) for r in readers.values())
log('  the design: %d wires (%d pieces + %d source-fills), %d (target, wire) reads'
    % (len(readers), sum(1 for w in readers if w[0] == 'P'), sum(1 for w in readers if w[0] == 'S'), nreads))
for name, classes in FAM.items():
    sp = [span_mask(c)[0] for c in classes]
    # per (t, w): the classes K with home(w) ⊆ span(K) ⊆ t-perp
    ok = 0; per_t = defaultdict(lambda: defaultdict(list))
    for w, rs in readers.items():
        for t in rs:
            ks = [k for k in range(len(sp)) if (home[w] & ~sp[k]) == 0 and (sp[k] & ~PM[t]) == 0]
            if ks:
                ok += 1
                for k in ks: per_t[t][k].append(w)
    # one shared class-frame per target gate: the target's best single class frame (one per family-dim)
    best_one = sum(max((len(v) for v in per_t[t].values()), default=0) for t in range(V))
    # the wire side: a wire read at a class frame by all of its readers (zero climbs, the r434 node)
    whole = sum(1 for w, rs in readers.items()
                if any(all((home[w] & ~sk) == 0 and (sk & ~PM[t]) == 0 for t in rs) for sk in sp))
    left = nreads - best_one
    summary[name].update(reads_servable=ok, reads_at_one_frame_per_target=best_one, wires_whole=whole,
                         reads_left=left)
    log('  %-8s reads servable at some class frame %5d/%d | at ONE class frame per target %5d | wires with all '
        'readers at one class frame %d/%d | reads left for the forest %d (the dup budget 47)'
        % (name, ok, nreads, best_one, whole, len(readers), left))
json.dump(dict(families={k: v for k, v in FAM.items()}, summary=summary, reads=nreads, wires=len(readers)),
          open('ii19_nat108_census.json', 'wt'))
log('SAVED ii19_nat108_census.json')

"""THE SHARED-CARRIER CENSUS (the SS1993 directive: 'keep pushing II19'!!).

THE SS1985 WORD: the 121-line, the gcheck-PASSING (the R 541!) — closed at the hosting wall
(the cap 4,356 vs the nres 4,869: the over by the 57!!). THE MECHANISM: the R = the 420 core
+ the 121 completeness channel (the odd + the 120 PER-TARGET carriers!).

THE BREAKTHROUGH IDEA: THE TARGETS' CLIMB-MASS IS FRAME-INDEPENDENT (the sum of the deltas
= the final dim!!) — THE INTERMEDIATE VISITS ARE MASS-FREE!!! THE SHARED CARRIERS: the
carrier climbs ONCE to a shared frame F (the {120}-containing!), then ALL its target-reads
at F are FREE (the cur == F!!!). THE COST: the ~m carriers vs the 120 (the per-target!):
THE R = the 420 + 1 + m <= the 484 (the wall!) iff m <= 63!!

THE LEGALITY (the carrier at the shared frame F = {120} U X serves the target u iff):
  (a) span(P_u) IS-CONTAINED-IN span(F) — the u's PRIOR chain-span inside F (the nesting!)
  (b) span(F) IS-CONTAINED-IN perp_u — the F's lines orthogonal to u (the F in u's perp!)
  (c) F CONTAINS the special — the carrier's content ({120}) inside F!
THE SHARED GROUP S(X) = {u : P_u inside X AND X inside perp(u)} — the conservative proxy:
  the line-SET inclusion P_u as a set inside X, and every line of X orthogonal to u!

THE CENSUS:
(1) the R420's per-target B-chains: the prior frames' line-sets (the P_t!) + the dims!
(2) the natural X-candidates: the P_t's themselves!
(3) the greedy covering: the largest-|S(X)| first -> the m + the uncovered!
(4) THE R RECOUNT: the 420 + 1 + m: THE WALL-CHECK (the 484!!)
(5) THE SPECIAL's COMPLETENESS FLAG (the SS1998 discovery!!): the special's junk = {120}
    only — the 120 (root, special) pairs MISSING: the honest correction owed!!
"""
import json, gzip, time
from collections import Counter, defaultdict

t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

# ============ (0) THE SYSTEM (the R420's lines + the form!) ============
SRC = 'research/e8-bit-r420/data/bitE8mut-r420.json.gz'
with gzip.open(SRC, 'rt') as f:
    W = json.load(f)
v0 = W['v']; h0 = W['h']; R0 = W['R']
LINES = W['lines']
n0 = len(LINES[0])
V0 = len(LINES)

def ip(a, b):                                 # the SS2002 fix: the 'form' key is a STRING tag,
    return sum(x * y for x, y in zip(a, b))   # not a matrix — the R420's lines are integer
                                               # vectors under the plain dot product!

G = [[ip(LINES[i], LINES[j]) for j in range(V0)] for i in range(V0)]
# PU[t]: the mask of the lines orthogonal to t (the perp, self EXCLUDED: G[t][t] != 0!)
PU = [sum(1 << j for j in range(V0) if G[j][t] == 0) for t in range(V0)]
perp_sizes = Counter(bin(m).count('1') for m in PU)
log('(0) the R420: v=%d h=%d R=%d | the lines %d | the perp sizes %s' % (
    v0, h0, R0, V0, dict(sorted(perp_sizes.items()))))

# ============ (1) THE PER-TARGET B-CHAINS (the prior spans!) ============
frames = W['frames']
final = W['final']
B = W['B']
CNT2DIM = {0: 0, 1: 1, 2: 2, 12: 4, 30: 6, 63: 7, 120: 8}
dims = [CNT2DIM[len(fr)] for fr in frames]

chains = defaultdict(list)
for F, d, srcs in B:
    if v0 <= d < 2 * v0:
        chains[d - v0].append((F, list(srcs)))
log('(1) the B-gates: %d | the targets with B-gates: %d' % (len(B), len(chains)))

prior_span = {}          # the t -> (the prior line-set, its dim)!
n_gates = Counter()
for t, gl in chains.items():
    n_gates[len(gl)] += 1
    last = None
    hit_perp = False
    for (F, srcs) in gl:
        if F == final[v0 + t]:
            hit_perp = True
            break
        last = F
    if last is None:
        prior_span[t] = (frozenset(), 0)
    else:
        prior_span[t] = (frozenset(frames[last]), dims[last])
log('    the gates-per-target histogram: %s' % dict(sorted(n_gates.items())))
pd = Counter(d for (_, d) in prior_span.values())
log('    the prior-span dims: %s' % dict(sorted(pd.items())))
ps = Counter(len(s) for (s, _) in prior_span.values())
log('    the prior-span line-counts: %s' % dict(sorted(ps.items())))

# ============ (2) THE X-CANDIDATES (the P_t's!) + THE SERVED SETS ============
# S(X) = {u : P_u as a SET inside X AND every line of X orthogonal to u}
def served(X):
    if not X:
        return set()
    xm = 0
    for r in X:
        xm |= 1 << r
    out = []
    for u in prior_span:
        P_u, _ = prior_span[u]
        if not (set(P_u) <= X):
            continue
        if xm & ~PU[u]:
            continue
        out.append(u)
    return set(out)

cands = {}
for t, (X, d) in prior_span.items():
    if X:
        key = (X, d)
        cands.setdefault(key, set()).add(t)
log('(2) the distinct prior-spans (the X-candidates): %d' % len(cands))
cand_list = []
for (X, d), ts in cands.items():
    S = served(set(X))
    cand_list.append((X, d, S))
cand_list.sort(key=lambda z: -len(z[2]))
log('    the top candidates (the X-dim, |X|, the |S|): %s' % [
    (d, len(X), len(S)) for (X, d, S) in cand_list[:14]])

# ============ (3) THE GREEDY COVERING ============
covered = set()
chosen = []
for (X, d, S) in cand_list:
    if covered >= set(prior_span.keys()):
        break
    if S - covered:
        chosen.append((X, d, S - covered))
        covered |= S
uncovered = set(prior_span.keys()) - covered
log('(3) THE GREEDY: %d shared carriers cover %d/%d targets | the uncovered %d' % (
    len(chosen), len(covered), len(prior_span), len(uncovered)))
for (X, d, S) in chosen[:20]:
    log('    the carrier X(dim %d, %d lines) serves %d: %s' % (d, len(X), len(S), sorted(S)[:14]))
if uncovered:
    log('    THE UNCOVERED: %s' % sorted(uncovered)[:20])
    # the fallback: the per-target carriers for the uncovered!
    m = len(chosen) + len(uncovered)
else:
    m = len(chosen)
log('    THE m (the shared + the private fallback!): %d' % m)

# ============ (2') THE BIGGER X-CANDIDATES (the R420's OWN frames!!) ============
# THE SS2008 FINDING: the cell-candidates (the P_t's) serve EXACTLY 1 each (all the cells
# DISTINCT!) -> the m = 120 (NO SHARING at the cell level!). THE V2: the bigger X's — the
# R420's dim-4 (the 12-line D4-subsystems!) and dim-6 (the 30-line D6-subsystems!) frames!
# (the set-inclusion proxy is EXACT for the closed subsystems: the span = the line-set!)
big_cands = []
for fi in range(len(frames)):
    if dims[fi] not in (4, 6):
        continue
    X = set(frames[fi])
    S = served(X)
    if S:
        big_cands.append((frozenset(X), dims[fi], S))
big_cands.sort(key=lambda z: -len(z[2]))
log("(2') THE BIGGER X-CANDIDATES (the dim-4/6 frames!): %d with nonempty S" % len(big_cands))
log('    the top (the dim, |S|): %s' % [(d, len(S)) for (X, d, S) in big_cands[:14]])

# ============ (3') THE V2 GREEDY (the big candidates FIRST, the cells as the fallback!) ============
covered2 = set()
chosen2 = []
for (X, d, S) in big_cands:
    if S - covered2:
        chosen2.append((X, d, S - covered2, 'big'))
        covered2 |= S
for (X, d, S) in cand_list:
    if S - covered2:
        chosen2.append((X, d, S - covered2, 'cell'))
        covered2 |= S
uncovered2 = set(prior_span.keys()) - covered2
m = len(chosen2) + len(uncovered2)
log("(3') THE V2 GREEDY: %d big + %d cell carriers cover %d/%d | the uncovered %d -> THE m = %d" % (
    sum(1 for c in chosen2 if c[3] == 'big'), sum(1 for c in chosen2 if c[3] == 'cell'),
    len(covered2), len(prior_span), len(uncovered2), m))
for (X, d, S, kind) in chosen2[:20]:
    log('    the %s carrier X(dim %d, %d lines) serves %d: %s' % (
        kind, d, len(X), len(S), sorted(S)[:12]))
if uncovered2:
    log('    THE UNCOVERED: %s' % sorted(uncovered2)[:20])

# ============ (4) THE R RECOUNT + THE WALL-CHECK ============
R_new = 420 + 1 + m
WALL = 484
log('(4) THE R RECOUNT: 420 (the core) + 1 (the odd) + %d (the carriers) = %d' % (m, R_new))
log('    THE WALL-CHECK: R %d vs the wall %d: %s' % (
    R_new, WALL, 'FITS!!!' if R_new <= WALL else 'OVER by %d' % (R_new - WALL)))
nres = 9 * R_new
cap = 36 * 121
log('    the nres %d vs the cap %d (%.1f%%)' % (nres, cap, 100.0 * nres / cap))

# ============ (5) THE SPECIAL's COMPLETENESS FLAG (the honest!!) ============
log('(5) THE SPECIAL COMPLETENESS FLAG (the SS1998 discovery!!):')
log('    the special junk = {120} only; perp(special) = the 120 roots')
log('    -> THE 120 (root, special) PAIRS ARE MISSING (the special column = a copy!)')
log('    the fix-path: the bigger scatter-row (the odd ^ the rets-combo = the all-roots')
log('    pattern!) + the special reads (the E8-internal registers canceling the roots-part)')
log('    -> the census NEXT: the all-roots-pattern in the rets-span? the reads-search?')
log('DONE')

"""THE EMITTER STAGE 1 (ii19_nat42.py) — the value-DAG + the chain-frame assignment + the balance.

THE FINAL DESIGN (the full word4-frame reuse!!):
- the targets: THE WORD4's target-chains VERBATIM (the same perps!!) + the word4's scatter
  template (the W from the nat30 basis!!) + the D-doubling;
- the pieces (73) + the singleton-pieces (121): the builds (the running-sums at the sources'
  rungs!!) + the reads AT THE WORD4's TARGET-CHAIN FRAMES (the group = the users whose chains
  contain the frame!!!);
- the balance: per target: ⊕(the reads) ⊕ scatter = e_t (the nat34 algebra!!).
HERE: the assignment (the pieces' reads at the chain-frames!!) + the BALANCE VERIFIED +
the read-frame maps -> ii19_nat42_dag.json (the emitter's input!!).
"""
import os, sys, itertools, json
from collections import Counter, defaultdict
import numpy as np
from fractions import Fraction
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
sys.argv = ['ii19_nat20.py']
exec(open('ii19_nat20.py').read().split('# (1) chain-shape census')[0])
V, H = V, H
log = lambda *a: print(*a, file=sys.stderr, flush=True)

# the word4's target-chains (the frames the targets visit, dim-ascending!!)
# (the replay's chainF machinery: the frames per register per phase!!)
def target_chain(t):
    """the word4's target t's read-frames (dim-ascending, ⊆ perp(t)!!)."""
    ch = []
    F = 1
    while F < len(w['frames']):
        pass
    return ch
# (the word4's targets: their B-phase read-frames: extract from the B gates!!)
b_frames = defaultdict(list)   # t -> the B-gate frames reading into it
for F, d, srcs in w['B']:
    if V <= d < 2 * V:
        b_frames[d - V].append(F)
tf = {}
for t in range(V):
    fs = sorted(set(b_frames[t]), key=lambda F: dims[F])
    tf[t] = fs
prof = Counter(tuple(dims[F] for F in tf[t]) for t in range(V))
log('the word4 target-chains (the B read-frame dims): %s' % dict(list(sorted(prof.items(), key=lambda kv: -kv[1]))[:12]))

A39 = json.load(open('ii19_nat39_assign.json'))
kept = [(i, a, b, c) for i, a, b, c in A39['kept']]
pool = [set(p) for p in A39['pool']]
users = [list(u) for u in A39['users']]
left2 = [set(l) for l in A39['left2']]

# THE READ ASSIGNMENT: per piece: its users -> the reads at the users' chain-frames.
# the piece's user u read at ONE of u's chain-frames F (dim >= the build's top!!) with the
# piece's value C= F (the balance guarantees the lines C= perp(u); F C= perp(u) ✓!!) —
# the piece's chain: build-rungs -> the read-frames (dim-ascending, one per dim!!!).
# the constraint: per piece: the read-frames distinct-dim (its chain: one frame per dim!!).
def assign_reads(val_lines, us, top_dim):
    """the greedy: each user -> one of its chain-frames (dim > top_dim), the piece's
    read-frames one-per-dim, the value C= the frame (checked!!!)."""
    rmap = {}
    used_dims = set()
    us_sorted = sorted(us, key=lambda u: len(tf[u]))     # the constrained users first!!
    for u in us_sorted:
        cands = [F for F in tf[u] if dims[F] > top_dim and dims[F] not in used_dims]
        cands = [F for F in cands if val_in_frame(val_lines, F)]
        if not cands:
            return None, u
        F = min(cands, key=lambda F: dims[F])
        rmap[u] = F
        used_dims.add(dims[F])
    return rmap, None

# hmm — the value-in-frame check: the frame ⊇ the value means the frame's SPAN contains the
# lines (⊥ to the frame vectors!!): value-lines ⊥ every frame-vector <=> the lines IN the span?!
# NO!! ⊥ to the frame vectors means the lines ⊥ the frame — NOT in it!!! THE CONTENT RULE:
# val C= F (the span!!): the lines are IN the frame's span: they are ⊥ to the frame's PERP —
# NOT checkable via ⊥ to the frame vectors!!! THE HONEST CHECK: the rref (the span!!).
def val_in_frame(val_lines, F):
    M = [list(v) for v in w['frames'][F]]
    for l in sorted(val_lines):
        M.append([Fraction(x) for x in w['lines'][l]])
    return matrix_rank(M) <= dims[F]

def matrix_rank(M):
    M2 = [[Fraction(x) for x in r] for r in M]
    M2 = [[x / w['form']['den'] for x in r] for r in M2]
    rr = 0; ncols = len(M2[0])
    for c in range(ncols):
        p = next((i for i in range(rr, len(M2)) if M2[i][c] != 0), None)
        if p is None: continue
        M2[rr], M2[p] = M2[p], M2[rr]
        for i in range(rr + 1, len(M2)):
            if M2[i][c] != 0:
                f = M2[i][c] / M2[rr][c]
                M2[i] = [x - f * y for x, y in zip(M2[i], M2[rr])]
        rr += 1
    return rr

# the pieces: the build tops (the 3rd-gate rung dims: the F(c) spans!!)
tops = {}
for (i, a, b, c) in kept:
    lines = pool[i]
    tops[i] = max(2, int(np.linalg.matrix_rank(
        np.array([[float(x) for x in w['lines'][l]] for l in sorted(lines)]))))
piece_reads = {}
fail = []
for (i, a, b, c) in kept:
    rmap, u = assign_reads(pool[i], users[i], tops[i])
    if rmap is None:
        fail.append((i, u))
    else:
        piece_reads[i] = rmap
log('THE PIECE READS: assigned %d/%d | failed %d' % (len(piece_reads), len(kept), len(fail)))
if fail:
    log('  the failures (the piece, the stuck user, its chain-dims): %s' % [
        (sorted(pool[i]), u, [dims[F] for F in tf[u]]) for i, u in fail[:6]])

# the singleton-pieces: the builds at the singletons (top dim 1!!)
sing_reads = {}
sfail = []
sing_users = defaultdict(set)
for t in range(V):
    for l in left2[t]: sing_users[l].add(t)
for l, us in sing_users.items():
    rmap, u = assign_reads({l}, sorted(us), 1)
    if rmap is None: sfail.append((l, u))
    else: sing_reads[l] = rmap
log('THE SINGLETON READS: assigned %d/%d | failed %d' % (len(sing_reads), len(sing_users), len(sfail)))
if sfail:
    log('  the failures (the line, the stuck user, its chain-dims): %s' % [
        (l, u, [dims[F] for F in tf[u]]) for l, u in sfail[:6]])

# THE BALANCE: per target: ⊕(its reads' values) ⊕ perp-pattern = e_t + the scatter-side!!
G4 = [[sum(w['lines'][s][i] * w['form']['num'][i][j] * w['lines'][t][j]
            for i in range(H) for j in range(H) if w['form']['num'][i][j]) for t in range(V)] for s in range(V)]
PERPSET = [set(s for s in range(V) if s != t and G4[s][t] == 0) for t in range(V)]
ok = 0; bad_t = []
for t in range(V):
    got = set()
    for (i, a, b, c) in kept:
        if i in piece_reads and t in piece_reads[i]: got ^= pool[i]
    for l, rmap in sing_reads.items():
        if t in rmap: got ^= {l}
    if got == PERPSET[t]: ok += 1
    else: bad_t.append((t, len(got), len(PERPSET[t])))
log('THE BALANCE (the reads XOR == perp(t)): %d/%d | the bad: %s' % (ok, V, bad_t[:5]))
json.dump({'piece_reads': {str(i): {str(u): F for u, F in r.items()} for i, r in piece_reads.items()},
           'sing_reads': {str(l): {str(u): F for u, F in r.items()} for l, r in sing_reads.items()},
           'tf': {str(t): tf[t] for t in range(V)}},
          open('ii19_nat42_dag.json', 'w'))
log('saved ii19_nat42_dag.json')

"""nat123: THE MERGE-REACH CENSUS (the corrected shape-surgery direction: the mass UP the ranks!!).

For every gate (D/A/B): the participants' climbs could JUMP to the highest legal frame
(the merge): bounded by (i) the src-content containment (the frame >= the content's span,
automatic for bigger frames), (ii) the participants' LATER gates' frames (the chain
dominance: every later gate of p must have frame \u2287 the merged cur - so the merge
ceiling for the gate is the intersection of the later-chains' minima).
The reachable hist (mass-true) + the price.
"""
import json, gzip, os, sys
import numpy as np
import mpmath as mp
from collections import Counter

mp.mp.dps = 50
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
from pricer import price

W = json.load(gzip.open('/tmp/r434-censusplan-tuned.json.gz', 'rt'))
lines = W['lines']
v = W['v']; R = W['R']; nreg = 2 * v + R
start = W['start']; final = W['final']


def rref(rows):
    m = [list(map(mp.mpf, r)) for r in rows]
    ncols = len(m[0]) if m else 0
    r = 0
    for c in range(ncols):
        p = None
        for i in range(r, len(m)):
            if m[i][c]:
                p = i; break
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        for i in range(len(m)):
            if i != r and m[i][c]:
                f = m[i][c] / m[r][c]
                m[i] = [(a - f * b) for a, b in zip(m[i], m[r])]
        r += 1
    return m[:r]


fr_cache = {}


def fdim(F):
    if F not in fr_cache:
        fr_cache[F] = len(rref([lines[i] for i in W['frames'][F]]))
    return fr_cache[F]


dims = [fdim(F) for F in range(len(W['frames']))]
NF = len(W['frames'])

# the frames' subspace containment: sub[a][b] = True iff frames[b] \u2287 frames[a]
# (needed for the chain-dominance: the merged cur must be \u2286 every later gate's frame)
sub = [[False] * NF for _ in range(NF)]
for a in range(NF):
    if not W['frames'][a]:
        for b in range(NF):
            sub[a][b] = True
        continue
    for b in range(NF):
        if a == b or not W['frames'][b]:
            sub[a][b] = (a == b)
            continue
        # rref of a's lines must sit inside b's span: rank(a-rows + b-rows) == rank(b-rows)
        if (dims[a], dims[b]) in fr_cache:
            pass
        A = [lines[i] for i in W['frames'][a]] + [lines[i] for i in W['frames'][b]]
        if len(rref(A)) == dims[b]:
            sub[a][b] = True
print('the containment matrix computed (%d frames)' % NF, flush=True)

# the gates in order + the participants' later-gate frames
seq = [('D', g) for g in W['D']] + [('A', g) for g in W['A']] + [('B', g) for g in W['B']] + \
      [('C', g) for g in W['C']]
# for each register: the ordered list of its gates' frames
reg_gates = [[] for _ in range(nreg)]
for i, (ph, (F, d, ss)) in enumerate(seq):
    for p in [d] + list(ss):
        reg_gates[p].append((i, F))
print('the gate-touch census: mean %.1f' % (sum(len(g) for g in reg_gates) / nreg))

# the merge-reach: process each register's gates BACKWARD: the ceiling for gate i
# = the min-dim frame that dominates all its later gates' frames (via the sub-matrix):
# ceiling[i] = the later-chain's first frame F' with sub-chain... simplest: the merge target
# for the gate at F_i is the LATER chain's minimum: we compute per gate the best frame G:
#   G \u2287 F_i (the gate's own frame \u2287: the delivery still legal),
#   G \u2287 cur before (start or the earlier merged),  and G \u2286 every later frame (dominance)
# => G must be a subframe of ALL later frames: the later chain must be \u2287 G... i.e. G \u2286 F_{i+1}, ...
# So the merge ceiling = the first later frame (the chain runs increasing) - the merge of
# gate i and the later gates' frames: since later frames are \u2287 cur, merging to any
# G with dims[cur] < dims[G] \u2264 dims[the next gate's frame] is legal.
# THE SIMPLE REACH: each register's climb sequence can be re-distributed to the LATER
# frames: i.e., the register can SKIP its early frames and make ONE BIG JUMP at its LATER
# gates: the reachable = the jumps deferred to the highest possible positions.
# Concretely: hist-merge = for each register: the climbs deferred: the register's chain
# 0 -> F1 -> F2 -> ... -> FK (its gates' frames in order, the distinct ones): the merge
# can collapse the chain to ANY coarser increasing subsequence!! The maximum merge:
# the LONGEST steps: keep only the LAST gate's frame (the highest): but the gate
# semantics: the register must BE at the gate's frame AT that gate (the src-content
# check + the val-replay unchanged!)... the gates' frames are where the CONTENT
# arrives: a src read at F must have content \u2286 F: the src's content is ITS OWN
# delivered lines: if we defer the src's climbs, its content at the earlier gates is
# SMALLER (less delivered) -> the content check STILL PASSES (the content \u2286 frame)...
# BUT the DEST's val needs the src's full content: the XOR delivers val[s] (whatever
# it is at that time!!). So deferring changes the DELIVERED CONTENT -> the balance
# breaks!! The merge can only defer the CLIMB, not the delivery: every gate still
# delivers its val at its own frame. The climb-splitting/merging is NOT free: the
# cur-frame at each gate is the gate's own frame!! (gcheck: climb(d, F); climb(s, F))
# SO: the gates' frames are FIXED (the delivery points). The only freedom: the
# FRAMES THEMSELVES (the word's frame list is free!!) - the RE-FRAMING: the gates'
# frames can be REASSIGNED to bigger subspaces (the tuner's 'frame-only' move!!)
# The reach: each gate's frame can grow up to min(later-chain dominance, the content law).
# THE CENSUS: per gate: the ceiling = the min over its participants' later gates'
# frames that must dominate... each participant p: the gate's frame F: p's later gates
# at F' \u2287 F: growing F to G requires G \u2286 F' for the NEXT gate of p (the chain!).
# ceiling(G) = the biggest G with G \u2286 next-frame(p) for all p... = the next gates'
# frames' common subspace!! -> typically the next frame itself.
# => the re-framing reach: gate i's frame can grow to the NEXT gate's frame of ANY
# participant (the min), i.e. the merge = merge gate i INTO the later gates' frames.
# The maximal merge per register: its whole chain collapses onto its LAST gates!!
# (the earliest gates' deliveries re-framed to the latest frames!!)
print('NOTE: the re-framing reach = the gates re-aimed at the participants\' next-gate frames')
print('The census: per gate, the merge ceiling = the min-dim of the participants\' next-gate frames')

# per gate index: the participants' next-gate frames
def next_frames(i, parts):
    nf = []
    for p in parts:
        later = [F for (j, F) in reg_gates[p] if j > i]
        if not later:
            nf.append(dims[final[p]] if p >= 0 else 8)
        else:
            nf.append(dims[later[0]])
    return min(nf)


hist_paid = Counter()
hist_merge = Counter()
for i, (ph, (F, d, ss)) in enumerate(seq):
    if ph == 'C':
        continue  # the C-phase: fixed at dim-8
    parts = [d] + list(ss)
    ceil_dim = next_frames(i, parts)
    for p in parts:
        # p's current dim (approx: the gate's own frame - the paid rank)
        # the paid: climb from the previous frame to F
        prev = [f for (j, f) in reg_gates[p] if j < i]
        d0 = dims[prev[-1]] if prev else (dims[start[p]] if p < len(start) else 0)
        r_paid = dims[F] - d0
        if r_paid <= 0:
            continue
        hist_paid[r_paid] += 1
        # the merge: the gate re-aimed at the ceiling (the biggest legal frame)
        r_merge = ceil_dim - d0
        if r_merge > 0:
            hist_merge[r_merge] += 1
        else:
            hist_merge[r_paid] += 1
# the C + the finals + the copy_ranks: unchanged (the C at dim-8, the finals no-ops, cst=63)
hist_c = Counter()
cur = list(start)
for ph, (F, d, ss) in seq:
    if ph == 'C':
        for p in [d] + list(ss):
            r0 = dims[F] - dims[cur[p]]
            if r0 > 0:
                hist_c[r0] += 1
            cur[p] = F
    else:
        for p in [d] + list(ss):
            cur[p] = F
hist_f = Counter()
for r in range(nreg):
    pass  # the finals: all no-ops (measured)
paid_total = Counter({k: c for k, c in hist_paid.items()}) + Counter({1: 361, 2: 180, 4: 4})
paid_total[7] += 9
merge_total = Counter({k: c for k, c in hist_merge.items()}) + Counter({1: 361, 2: 180, 4: 4})
merge_total[7] += 9
massp = sum(k * c for k, c in paid_total.items())
massm = sum(k * c for k, c in merge_total.items())
print('the paid hist:', dict(sorted(paid_total.items())), 'mass', massp)
print('the merge-reach hist:', dict(sorted(merge_total.items())), 'mass', massm)
P111 = mp.mpf('0.001733052823330162099157')
cp, _, _ = price(dict(paid_total), v, 8, R)
cm, _, _ = price(dict(merge_total), v, 8, R)
print('the paid price: %s (%+.4f%%)' % (mp.nstr(cp, 20), float((cp - P111) / P111) * 100))
print('THE MERGE-REACH PRICE: %s (%+.4f%%)' % (mp.nstr(cm, 20), float((cm - P111) / P111) * 100))

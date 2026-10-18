"""THE NATIVE-121 CENSUS v2 (ii19_nat2.py) — THE NAT1-LITE!!
THE WORD4's OWN LINES (the committed source of truth (the norm-4 system!!!))!!
THE DESIGN (the block-20's rooms + the block-29's FREE-RE-READS + the dim-diversity!!!):
1. the perps (the ip_half=0!!)
2. the pair-common-perps + the greedy co-read groups (the TH_ROOM=12 (the block-20!!))
3. THE ROOMS: the groups' common-perps: the spans + THE CONTENTS (the +-lines: the roots
   + THE SPECIAL-INCLUSION (the special's bit delivered by the rooms?!?!))
4. THE COVERAGE: per target: the rooms' contents' union vs perp(t): the tails + THE
   SPECIAL's coverage in the ROOT-targets' junks!!!
5. THE DIM-DIVERSITY: per target: its rooms' dims (the one-frame-per-dim chain!!!)
6. THE R + the demand (the arrival law!!) + THE PRICE (the coarse + the fine + the
   shape-sensitivity (the block-57's lever!!!))
"""
import sys, json, time
from collections import Counter
import numpy as np
from mpmath import mp
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import price as pprice
mp.dps = 40

FRONTIER = 0.001744386
W4 = json.load(open('ii19_own_word4.json'))
L = [np.array(l, dtype=float) for l in W4['lines']]
V, H = 121, 9
n = 9
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

# the form: the plain dot (the word4's convention: the diag(1^8, 2)?? -> CHECK!!
# the word4's ip-convention: the ip_half (the /2!!) — the perps = the ip_half == 0!!
def ip(a, b): return float(np.dot(a, b))
def iph(a, b): return ip(a, b) / 2

log('(0) the lines: %d | the norms (the plain!!): %s' % (
    len(L), sorted(set(int(ip(l, l)) for l in L))))
# the perps (the ip_half == 0!!)
perp = []
for t in range(V):
    p = [u for u in range(V) if u != t and iph(L[t], L[u]) == 0]
    perp.append(p)
log('(1) the perps: %s (the special (120): %d!!)' % (
    dict(sorted(Counter(len(p) for p in perp).items())), len(perp[120])))
assert len(perp[120]) == 120, 'the special perp!!'

# the pair-common-perps!!
TH_ROOM = 12
common = {}
for i in range(V):
    for j in range(i + 1, V):
        cs = [u for u in range(V) if u != i and u != j and iph(L[i], L[u]) == 0 and iph(L[j], L[u]) == 0]
        common[(i, j)] = cs
sizes = Counter(len(c) for c in common.values())
log('(2) the pair-common-perps: %s' % dict(sorted(sizes.items())))

# the greedy co-read groups (the OVERLAPPING (the per-target cap 8 (the block-20's design!!!)))
groups = []
for seed in range(V):
    grp = [seed]
    cs = set(perp[seed])
    while len(grp) < 8:
        best = None
        for u in range(V):
            if u in grp:
                continue
            cs2 = [x for x in cs if u != x]
            cs2 = [x for x in cs2 if iph(L[u], L[x]) == 0]
            if len(cs2) >= TH_ROOM:
                best = (u, set(cs2))
                break
        if best is None:
            break
        grp.append(best[0])
        cs = best[1]
    groups.append((grp, cs))
# dedup (the same group from different seeds!!)
uniq = []
for g, c in groups:
    if not any(set(g) == set(g2) for g2, _ in uniq):
        uniq.append((g, c))
groups = uniq
log('(3) the greedy groups: %d | the sizes %s' % (
    len(groups), dict(sorted(Counter(len(g) for g, _ in groups).items()))))

# the rooms: the spans (the RREF-dims!!) + the contents (the room's own lines = the common-perp's
# lines ⊥ the group?! — the block-20: the room = the group's common-perp's SPAN (the lines ⊥ the group!!)
# THE CONTENTS: the room-content = the LINES (of the 121!!) inside the room-span AND ⊥ the group!!
def rref_dim(vectors):
    if not vectors:
        return 0
    M = np.array(vectors, dtype=float)
    r = 0
    for c in range(n):
        p = None
        for i in range(r, len(M)):
            if abs(M[i, c]) > 1e-9:
                p = i
                break
        if p is None:
            continue
        M[[r, p]] = M[[p, r]]
        M[r] = M[r] / M[r, c]
        for i in range(len(M)):
            if i != r and abs(M[i, c]) > 1e-9:
                M[i] = M[i] - M[i, c] * M[r]
        r += 1
        if r == len(M):
            break
    return r

rooms = []
for gi, (grp, cs) in enumerate(groups):
    # the room-span: the group's own lines?! — NO!! the room = the common-perp's span!!
    # the common-perp's lines (the cs!!): the span-basis: the cs's first lines (the dim!!)
    # THE CONTENT (the register's val's line-part!!): the 121-lines INSIDE the span AND ⊥ the group!!
    span_vecs = [L[x] for x in cs]
    dim = rref_dim(span_vecs)
    # the content: all the 121-lines in the span (the cs already = the ⊥-lines: the full set!!)
    content = sorted(cs)
    # THE SPECIAL-INCLUSION!!
    rooms.append(dict(gi=gi, grp=grp, dim=dim, content=content,
                      special=(120 in cs)))
log('(4) the rooms: %d | the dims %s | THE SPECIAL-INCLUSION: %d/%d!!!' % (
    len(rooms), dict(sorted(Counter(r['dim'] for r in rooms).items())),
    sum(1 for r in rooms if r['special']), len(rooms)))

# THE COVERAGE: per target: the union of its rooms' contents vs perp(t)!!
tails = []
for t in range(V):
    cov = set()
    for r in rooms:
        if t in r['grp']:
            cov.update(r['content'])
    tail = [u for u in perp[t] if u not in cov]
    tails.append(tail)
log('(5) the coverage: the tails %s | the mean %.1f' % (
    dict(sorted(Counter(len(x) for x in tails).items())), np.mean([len(x) for x in tails])))
spcov = 0
for t in range(120):
    cov = set()
    for r in rooms:
        if t in r['grp']:
            cov.update(r['content'])
    if 120 in cov:
        spcov += 1
log('    the special-target (120): the tail %d | the root-targets: the special-covered %d/120!!!' % (
    len(tails[120]), spcov))

# THE DIM-DIVERSITY: per target: its rooms' dims (the one-frame-per-dim chain!!!)
dimdiv = Counter()
for t in range(V):
    dims = [r['dim'] for r in rooms if t in r['grp']]
    c = Counter(dims)
    if max(c.values()) > 1:
        dimdiv[max(c.values())] += 1
log('(6) the dim-diversity: the targets with the dim-collisions: %d/121 (the max-collision-hist %s!!)' % (
    sum(dimdiv.values()), dict(sorted(dimdiv.items()))))

# THE R + THE DEMAND + THE PRICE!!
R_est = len(rooms) + sum(1 for x in tails if x) + 9
demand = sum(len(r['grp']) for r in rooms)  # the room-reads (the co-read groups' F's!!)
log('(7) THE R-EST: %d (the rooms %d + the tails %d + the gathers 9!!) | the demand %d vs 9R %d (%.0f%%!!)' % (
    R_est, len(rooms), sum(1 for x in tails if x), demand, 9 * R_est, 100 * demand / (9 * R_est)))

# THE PRICE (the coarse (the ALL-big-climbs (the {8, 9}-loads!!!)) + the model-band!!)
log('(8) THE PRICE (the coarse-hist models (the block-57 shape-lever grid!!)):')
# the hist-models: the sources' {8: 121} + the rooms' {the dims' climbs + the finals!!} + ...
# THE SIMPLE-COARSE: the room-registers: the [0 -> the room-dim -> 9]: the deltas {dim, 9-dim}!!
for name, tail_R_add in (('the base', 0), ('the +special-carriers', 42)):
    R = R_est + tail_R_add
    hist = Counter()
    # the sources: the [1 (free!), the FULL-climb (the +8!!)]: {8: 121}
    hist[8] += 121
    # the rooms: the [0 -> the room (dim!!) -> the FULL (9!!)]: the deltas {dim, 9-dim}
    for r in rooms:
        hist[r['dim']] += 1
        hist[9 - r['dim']] += 1
    # the tails: the same (the [0 -> the perp (8!!) -> 9]): {8, 1}
    for x in tails:
        if x:
            hist[8] += 1
            hist[1] += 1
    # the gathers: the [0 -> 9]: {9: 9}
    hist[9] += 9
    # the targets: the [0 -> the F (the rooms' dims (the mixed!!)) -> the perp (8!!)]: the coarse {8: 121}
    hist[8] += 121
    hist[9] += 0
    hist[1] += 121  # the perp -> the final?! — hmm: the targets' final = the perp (dim 8!!): the mass 8!!
    # THE MASS-CHECK: the mass must = 9R + 73 + 2*121*8!!!
    mass = sum(k * v for k, v in hist.items())
    ident = 9 * R + 73 + 2 * V * 8
    c = pprice(dict(hist), v=V, h=H, R=R)
    log('    %s: R=%d | the hist %s | the mass %d vs %d (%s!!) | c = %s' % (
        name, R, dict(sorted(hist.items())), mass, ident,
        'MATCH' if mass == ident else 'MISMATCH', mp.nstr(c, 12)))
    log('      THE VS-FRONTIER: %+.2f%%' % (float((c / FRONTIER - 1) * 100)))
log('DONE — THE NAT2 CENSUS!!')

"""nat131: THE TRIM-EMITTER PREP (the cell-mapping of the r434's registers).

Given the v=111 cell-census (nat120: the cells, their line-sets, their exclusive targets),
map the r434's own wires onto the cells (each wire's delivered content covers which
cells' side-needs), census the per-cell register-counts, and find the >3-cells (the
excess = the trim candidates). The re-routing surgery (the shared-side delivery) then
targets the excess.
"""
import json, gzip, os, sys
from collections import Counter
from fractions import Fraction

W = json.load(gzip.open('/tmp/r434-censusplan-tuned.json.gz', 'rt'))
v = W['v']; R = W['R']; nreg = 2 * v + R
lines = W['lines']; start = W['start']; final = W['final']
A = W['A']; B = W['B']; D = W['D']; C = W['C']


def rref_int(rows):
    m = [list(map(Fraction, r)) for r in rows]
    r = 0
    for c in range(len(m[0]) if m else 0):
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


# (1) the wire-contents: the replay (D then A then B) tracking each register's delivered lines
val = [0] * nreg
for s in range(v):
    val[s] = 1 << s
for F, d, ss in D:
    for s in ss:
        val[d] ^= val[s]
    for p in [d] + list(ss):
        pass  # D at frame 0: no climbs
for ph, gates in (('A', A), ('B', B)):
    for F, d, ss in gates:
        for s in ss:
            val[d] ^= val[s]

# (2) the B-wires' contents (the delivered line-sets)
wires = {}
for F, d, ss in B:
    for s in ss:
        if s >= 2 * v:
            mask = val[s] & ((1 << v) - 1)
            ls = tuple(sorted(i for i in range(v) if (mask >> i) & 1))
            wires.setdefault(s, set()).update(ls)
print('the B-wires: %d | the content-sizes: %s' % (len(wires), dict(sorted(Counter(len(x) for x in wires.values()).items()))))

# (3) the per-target demands: the target t's B0 = {t} ∪ perp(t): which lines each target still needs
# from the wires (the sources deliver their own lines; the wires cover the rest)
tgt_need = {}
for F, d, ss in B:
    if v <= d < 2 * v:
        got = set()
        for s in ss:
            mask = val[s] & ((1 << v) - 1)
            got.update(i for i in range(v) if (mask >> i) & 1)
        tgt_need.setdefault(d, set()).update(got)
sizes = Counter(len(x) for x in tgt_need.values())
print('the targets\' wire-delivered content-sizes:', dict(sorted(sizes.items())))

# (4) the wire->targets bipartite structure (the sharing)
w2t = Counter()
for F, d, ss in B:
    for s in ss:
        if s >= 2 * v:
            w2t[s] += 1
print('the wires\' target-reader counts:', dict(sorted(Counter(w2t.values()).items())))

# (5) the coverage census: for each target, the minimal wire-subsets covering its need
# (the set-cover per target: the greedy) - the sharing-capacity (which wires are redundant)
cover_counts = Counter()
redundant = 0
for t, need in tgt_need.items():
    # greedy cover
    cover = set()
    chosen = []
    rem = set(need)
    cand = [(s, len(wires[s] & rem)) for s in wires if wires[s] & rem]
    while rem and cand:
        cand.sort(key=lambda x: -x[1])
        s, _ = cand[0]
        if s in chosen:
            cand = cand[1:]
            continue
        chosen.append(s)
        rem -= wires[s]
        cand = [(s2, len(wires[s2] & rem)) for s2 in wires if wires[s2] & rem]
    if rem:
        print('  target %d: UNCOVERED %d lines' % (t - v, len(rem)))
    cover_counts[len(chosen)] += 1
print('the per-target greedy cover sizes:', dict(sorted(cover_counts.items())))
print('SAVED the structure to ii19_nat131_wires.json')
json.dump({str(k): sorted(map(int, x)) for k, x in wires.items()},
          open('ii19_nat131_wires.json', 'wt'))

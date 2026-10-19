"""nat134: THE RETIREMENT-EMITTER (the A-DAG flattening + the re-framing -> the R~243 word).

(1) Flatten: every intermediate's consumers re-src to its transitive sources (the
    A-gates rewritten; the intermediates' build-gates dropped).
(2) Re-frame: the nat125 backward-merge over the flattened word (the sources' chains
    must absorb the new reads legally: the frames raised to the chain-compatible ones).
(3) The hist + the D-recompute (the y-cascades vanish: the pre-cancels = the wires'
    self-bits only) + the adapter + gcheck + the price.
"""
import json, gzip, os, sys
import mpmath as mp
from collections import Counter
from fractions import Fraction

mp.mp.dps = 40
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'tword'))
from pricer import price

W = json.load(gzip.open('/tmp/r434-censusplan-tuned.json.gz', 'rt'))
v = W['v']; R = W['R']; nreg = 2 * v + R; NF = len(W['frames'])
lines = W['lines']; start = W['start']; final = W['final']
RET = set(W['ret'])


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


bases = [rref_int([lines[i] for i in W['frames'][F]]) for F in range(NF)]
dims = [len(b) for b in bases]


def contains(b, row):
    row = list(row)
    for br in b:
        c = next((i for i, x in enumerate(row) if x), None)
        if c is None:
            break
        bc = next((i for i, x in enumerate(br) if x), None)
        if bc == c:
            f = row[c] / br[c]
            row = [(a - f * bb) for a, bb in zip(row, br)]
    return all(x == 0 for x in row)


sub = [[False] * NF for _ in range(NF)]
for a in range(NF):
    sub[a][a] = True
    if not bases[a]:
        for b in range(NF):
            sub[a][b] = True
        continue
    for b in range(NF):
        if b == a or dims[b] < dims[a] or dims[b] == 0:
            continue
        sub[a][b] = all(contains(bases[b], row) for row in bases[a])
print('the containment matrix done', flush=True)

D = [list(g) for g in W['D']]; A = [list(g) for g in W['A']]; B = [list(g) for g in W['B']]
C = [list(g) for g in W['C']]

# ---------- (1) THE FLATTENING ----------
# classify: the B-read wires + the totals stay; the intermediates flatten
b_read = set()
for F, d, ss in B:
    for s in ss:
        if s >= 2 * v:
            b_read.add(s)
INTER = set(q for q in range(2 * v, nreg) if q not in b_read and q not in RET)
print('the intermediates to retire: %d' % len(INTER), flush=True)

# per intermediate: its transitive srcs (the flattening closure)
srcs_of = {}
for F, d, ss in A:
    srcs_of.setdefault(d, set()).update(ss)


def flatten_srcs(q):
    """the transitive source-closure of q (the sources + the kept wires only)"""
    out = set()
    stack = [q]
    seen = {q}
    while stack:
        x = stack.pop()
        for s in srcs_of.get(x, ()):
            if s in INTER and s not in seen:
                seen.add(s)
                stack.append(s)
            elif s not in INTER:
                out.add(s)
    return out


flat = {q: flatten_srcs(q) for q in INTER}
# the new A: the kept-dest gates with the flattened srcs
A2 = []
for F, d, ss in A:
    if d in INTER:
        continue
    ns = set()
    for s in ss:
        if s in INTER:
            ns.update(flat[s])
        else:
            ns.add(s)
    A2.append([F, d, sorted(ns)])
print('the flattened A: %d gates (was %d) | the src-counts: %s' % (
    len(A2), len(A), dict(sorted(Counter(len(g[2]) for g in A2).items())[:8])), flush=True)

# ---------- (2) THE RE-FRAMING (the backward merge over the flattened word) ----------
seq = ([('A', i, g) for i, g in enumerate(A2)] + [('B', i, g) for i, g in enumerate(B)])
NG = len(seq)
reg_seq = [[] for _ in range(nreg)]
for k, (ph, gi, (F, d, ss)) in enumerate(seq):
    for p in [d] + list(ss):
        reg_seq[p].append(k)
for ci, (F, d, ss) in enumerate(C):
    for p in [d] + list(ss):
        reg_seq[p].append(NG + ci)

bound = list(final)
raised = 0
for k in range(NG - 1, -1, -1):
    ph, gi, (F, d, ss) = seq[k]
    parts = [d] + list(ss)
    if any(p in RET for p in parts):
        for p in parts:
            bound[p] = F
        continue
    cands = [G for G in range(NF)
             if dims[G] > dims[F] and sub[F][G] and all(sub[G][bound[p]] for p in parts)]
    if cands:
        best = max(cands, key=lambda G: dims[G])
        seq[k] = (ph, gi, [best, d, ss])
        F = best
        raised += 1
    for p in parts:
        bound[p] = F
print('the re-framing: %d gates raised' % raised, flush=True)
for ph, gi, (F, d, ss) in seq:
    if ph == 'A': A2[gi] = [F, d, ss]
    else: B[gi] = [F, d, ss]

# ---------- (3) THE HIST + THE PRICE ----------
cur = list(start); hist = Counter()
for gates in (D, A2, B):
    for F, d, ss in gates:
        for p in [d] + list(ss):
            r0 = dims[F] - dims[cur[p]]
            assert r0 > 0 or cur[p] == F, ('down-climb', p, cur[p], F)
            if r0 > 0:
                hist[r0] += 1
            cur[p] = F
rf = [cur[q] for q in W['ret']]
cst = sum(dims[f] for f in rf)
for f in rf:
    hist[dims[f]] += 1
for F, d, ss in C:
    for p in [d] + list(ss):
        r0 = dims[F] - dims[cur[p]]
        if r0 > 0:
            hist[r0] += 1
        cur[p] = F
# the survivors: the kept registers (the wires + the totals); the retired: their finals drop
kept = [r for r in range(nreg) if not (2 * v <= r < nreg and r in INTER)]
for r in kept:
    r0 = dims[final[r]] - dims[cur[r]]
    if r0 > 0:
        hist[r0] += 1
R2 = R - len(INTER)
mass = sum(k * c for k, c in hist.items())
ident = 8 * R2 + cst + 2 * v * 7
print('R2 = %d | the hist: %s | mass %d vs identity %d' % (
    R2, dict(sorted(hist.items())), mass, ident), flush=True)
P111 = mp.mpf('0.001733052823330162099157')
c, prof, dd = price(dict(hist), v, 8, R2) if mass == ident else (None, None, None)
print('THE RETIRED PRICE: %s (%+.4f%%)' % (mp.nstr(c, 20) if c else 'MASS-MISMATCH/NO-ROOT',
      float((c - P111) / P111) * 100 if c else 0))
json.dump({'hist': dict(hist), 'R2': R2, 'cst': cst, 'c': str(c) if c else None},
          open('ii19_nat134_state.json', 'wt'), indent=1)

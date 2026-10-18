"""nat124: THE MERGE-EMITTER (the shape-surgery: the mass UP the ranks).

Per round: replay the current plan (the cur[] at every gate), then per gate compute the
legal merge target G: an EXISTING frame with dims[G] > dims[F], cur[p] \u2286 G for ALL
participants, and G \u2286 every participant's every later gate's frame (the full chain
dominance), and (the scatter protection) the gate's register-content/scatter invariants.
The vals are untouched (the frames don't affect the XORs). Iterate to the fixed point.
Then: the adapter -> gcheck (the judge) -> the price.
"""
import json, gzip, os, sys
import mpmath as mp
from collections import Counter

mp.mp.dps = 50
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'tword'))
from pricer import price

W = json.load(gzip.open('/tmp/r434-censusplan-tuned.json.gz', 'rt'))
v = W['v']; R = W['R']; nreg = 2 * v + R; NF = len(W['frames'])
lines = W['lines']; start = W['start']; final = W['final']


from fractions import Fraction


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
print('the frame dims:', dict(sorted(Counter(dims).items())), flush=True)

# the containment sub[a][b] = frames[a] \u2286 frames[b] (only where dims[a] \u2264 dims[b])
sub = [[False] * NF for _ in range(NF)]


def contains(b, row):
    """reduce row against basis b; True iff it reduces to zero"""
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
RET = set(W['ret'])
seq = ([('A', i, g) for i, g in enumerate(A)] + [('B', i, g) for i, g in enumerate(B)])
NG = len(seq)


def parts_of(k):
    F, d, ss = seq[k][2]
    return [d] + list(ss)


# per register: its gate-indices in order
reg_seq = [[] for _ in range(nreg)]
for k, (ph, gi, g) in enumerate(seq):
    for p in parts_of(k):
        reg_seq[p].append(k)
for ci, (F, d, ss) in enumerate(C):
    for p in [d] + list(ss):
        reg_seq[p].append(NG + ci)


def merge_round():
    """one pass: the live curs; per gate: the candidates = any existing frame G with
    dims[G] > dims[F], G \u2287 cur[p] \u2200p, G \u2286 p's FIRST later frame (the chain dominance)
    and G \u2286 final[p] \u2200p (the end bound). Apply the best; update the curs incrementally.
    The totals (ret registers) are frozen (the scatter invariant)."""
    cur = list(start)
    curs = [None] * NG
    for k in range(NG):
        curs[k] = list(cur)
        F, d, ss = seq[k][2]
        for p in parts_of(k):
            cur[p] = F
    applied = 0
    for k in range(NG):
        F, d, ss = seq[k][2]
        parts = parts_of(k)
        if any(p in RET for p in parts):
            continue
        if dims[F] >= 8:
            continue
        # the constraints: each part's FIRST later frame (the smallest in its chain) + the final
        dom = []
        bad = False
        for p in parts:
            ls = reg_seq[p]
            idx = ls.index(k)
            lts = ls[idx + 1:]
            if lts:
                j0 = lts[0]
                f0 = seq[j0][2][0] if j0 < NG else C[j0 - NG][0]
                if dims[f0] > dims[F]:
                    dom.append(f0)
                else:
                    bad = True; break
            if dims[final[p]] > dims[F]:
                dom.append(final[p])
        if bad or not dom:
            continue
        cands = [G for G in range(NF)
                 if dims[G] > dims[F]
                 and all(sub[curs[k][p]][G] for p in parts)
                 and all(sub[G][c] for c in dom)]
        if not cands:
            continue
        best = max(cands, key=lambda G: dims[G])
        seq[k] = (seq[k][0], seq[k][1], [best, d, ss])
        applied += 1
        # the live curs update: the parts sit at `best` until their first later gate
        for p in parts:
            ls = reg_seq[p]
            idx = ls.index(k)
            for j in ls[idx + 1:]:
                if j < NG:
                    curs[j][p] = best
                if j < NG and seq[j][2][0] != best:
                    break
    return applied


for rnd in range(12):
    ap = merge_round()
    print('round %d: %d merges applied' % (rnd, ap), flush=True)
    if ap == 0:
        break

for ph, gi, (F, d, ss) in seq:
    if ph == 'A': A[gi] = [F, d, ss]
    else: B[gi] = [F, d, ss]

# the hist + the price
cur = list(start); hist = Counter()
for gates in (D, A, B):
    for F, d, ss in gates:
        for p in [d] + list(ss):
            r0 = dims[F] - dims[cur[p]]
            if r0 > 0:
                hist[r0] += 1
            cur[p] = F
rf = [cur[q] for q in W['ret']]
for f in rf:
    hist[dims[f]] += 1
for F, d, ss in C:
    for p in [d] + list(ss):
        r0 = dims[F] - dims[cur[p]]
        if r0 > 0:
            hist[r0] += 1
        cur[p] = F
for r in range(nreg):
    r0 = dims[final[r]] - dims[cur[r]]
    if r0 > 0:
        hist[r0] += 1
mass = sum(k * c for k, c in hist.items())
print('the merged hist:', dict(sorted(hist.items())), 'mass', mass, '(the identity %d)' % (8 * R + 63 + 2 * v * 7))
P111 = mp.mpf('0.001733052823330162099157')
c, prof, d = price(dict(hist), v, 8, R)
print('THE MERGED PRICE: %s (%+.4f%%)' % (mp.nstr(c, 20) if c else 'NO-ROOT', float((c - P111) / P111) * 100 if c else 0))

# the word + the adapter + gcheck
W2 = dict(W)
W2['D'] = D; W2['A'] = A; W2['B'] = B
W2['form'] = {'num': [[1 if i == j else 0 for j in range(8)] for i in range(8)], 'den': 2}
cur = list(start)
for F, d, ss in W2['D'] + W2['A']:
    cur[d] = F
    for s in ss:
        cur[s] = F
W2['ret_frames'] = [cur[q] for q in W2['ret']]
W2['frames'] = [[list(W2['lines'][i]) for i in F] for F in W2['frames']]
json.dump(W2, open('/tmp/r434-merged.json', 'wt'))
import gcheck
out = gcheck.main('/tmp/r434-merged.json', do_price=True)
for k in ('status', 'R', 'cst', 'local_histogram', 'bit_c_nine_stage', 'vs_P111_percent'):
    print('gcheck %s: %s' % (k, out.get(k)))

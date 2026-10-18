"""nat125: THE BACKWARD MERGE-EMITTER (single exact pass, correct by construction).

Backward over the A+B gates. bound[p] starts at final[p]. At each gate: the parts'
bounds; the frame rises to the best existing G with F \u2286 G \u2286 bound[p] \u2200p (dims grow).
Then bound[p] := G for the parts. The totals (ret) are frozen. The D (frame 0) and the
C (dim-8, the only dim-8 frame) are untouched. The src-content checks stay satisfied
(bigger frames). The zg pairs are untouched (the C-web unchanged). One pass - no
convergence needed. Then the adapter -> gcheck -> the price (the frontier margin!).
"""
import json, gzip, os, sys
import mpmath as mp
from collections import Counter
from fractions import Fraction

mp.mp.dps = 50
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
print('the frame dims:', dict(sorted(Counter(dims).items())), flush=True)


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
seq = ([('A', i, g) for i, g in enumerate(A)] + [('B', i, g) for i, g in enumerate(B)])
NG = len(seq)

# the backward merge
bound = list(final)
merged = 0
for k in range(NG - 1, -1, -1):
    ph, gi, (F, d, ss) = seq[k]
    parts = [d] + list(ss)
    if any(p in RET for p in parts):
        for p in parts:
            bound[p] = F
        continue
    # the candidates: G with sub[F][G], sub[G][bound[p]] \u2200p, dims[G] > dims[F]
    cands = [G for G in range(NF)
             if dims[G] > dims[F] and sub[F][G] and all(sub[G][bound[p]] for p in parts)]
    if cands:
        best = max(cands, key=lambda G: dims[G])
        seq[k] = (ph, gi, [best, d, ss])
        F = best
        merged += 1
    for p in parts:
        bound[p] = F
print('the backward merge: %d gates raised (of %d)' % (merged, NG), flush=True)

for ph, gi, (F, d, ss) in seq:
    if ph == 'A': A[gi] = [F, d, ss]
    else: B[gi] = [F, d, ss]

# the hist + the price (the replay over D+A+B, the scatter, the C, the finals)
cur = list(start); hist = Counter()
for gates in (D, A, B):
    for F, d, ss in gates:
        for p in [d] + list(ss):
            r0 = dims[F] - dims[cur[p]]
            assert r0 > 0 or cur[p] == F, ('the down-climb!', p, cur[p], F)
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
for r in range(nreg):
    r0 = dims[final[r]] - dims[cur[r]]
    if r0 > 0:
        hist[r0] += 1
mass = sum(k * c for k, c in hist.items())
ident = 8 * R + cst + 2 * v * 7
print('the merged hist:', dict(sorted(hist.items())), 'mass', mass, 'the identity', ident)
assert mass == ident, 'THE MASS BROKE!!'
P111 = mp.mpf('0.001733052823330162099157')
c, prof, d = price(dict(hist), v, 8, R)
print('THE MERGED PRICE: %s (%+.4f%%)' % (mp.nstr(c, 20) if c else 'NO-ROOT', float((c - P111) / P111) * 100 if c else 0))

# the word + the adapter + gcheck
W2 = dict(W)
W2['D'] = D; W2['A'] = A; W2['B'] = B
W2['form'] = {'num': [[1 if i == j else 0 for j in range(8)] for i in range(8)], 'den': 2}
cur2 = list(start)
for F, d, ss in W2['D'] + W2['A']:
    cur2[d] = F
    for s in ss:
        cur2[s] = F
W2['ret_frames'] = [cur2[q] for q in W2['ret']]
W2['frames'] = [[list(W2['lines'][i]) for i in F] for F in W2['frames']]
json.dump(W2, open('/tmp/r434-merged2.json', 'wt'))
print('the word written; running gcheck...', flush=True)
import gcheck
out = gcheck.main('/tmp/r434-merged2.json', do_price=True)
for k in ('status', 'R', 'cst', 'local_histogram', 'bit_c_nine_stage', 'vs_P111_percent'):
    print('gcheck %s: %s' % (k, out.get(k)))

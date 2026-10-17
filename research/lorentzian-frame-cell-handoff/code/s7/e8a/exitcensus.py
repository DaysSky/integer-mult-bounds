"""Exit-rank census on an E8 bitE8/1+mut word (E1 / P111-tuned / R420).
For each helper h: z-readers, target-readers, number of writes; inverse row of h in the raw word W0 = (A, scatter, B)
over the z registers (sources + helpers); end-of-B frames of the inverse-row registers; minimal exit frame
U = span(end-of-B frames of h and its inverse row) and its rank."""
import gzip, json, sys, numpy as np
from collections import Counter, defaultdict
path = sys.argv[1]
w = json.load(gzip.open(path, 'rt'))
v, R = w['v'], w['R']; n = 2 * v + R
L = np.array(w['lines'], dtype=float)
fr = w['frames']
fdim = [int(np.linalg.matrix_rank(L[f])) if f else 0 for f in fr]
def is_t(r): return v <= r < 2 * v
zregs = [r for r in range(n) if not is_t(r)]
zidx = {r: i for i, r in enumerate(zregs)}; nz = len(zregs)
# U as rows: track each z register's value as bitmask over initial z registers (python ints)
val = {r: 1 << zidx[r] for r in zregs}
cur = list(w['start'])
zread = defaultdict(list); tread = defaultdict(list); writes = defaultdict(list)
def run(name):
    for k, (f, d, srcs) in enumerate(w[name]):
        for r in [d] + srcs: cur[r] = f if fdim[f] >= fdim[cur[r]] else cur[r]
        for s in srcs:
            if s >= 2 * v:
                (tread if is_t(d) else zread)[s].append((name, k, d))
        if not is_t(d):
            writes[d].append((name, k))
            acc = 0
            for s in srcs: acc ^= val[s]
            val[d] ^= acc
run('A'); run('B')
endB = list(cur)
# inverse: solve for row h of U^{-1}: find coefficients c over z regs with sum_j c_j val[j] == e_h (initial)
# Gaussian elimination over F2 on the matrix whose rows are val[j]; we need, for each h, combination giving unit e_h.
rows = [val[r] for r in zregs]
# build inverse via elimination with tracking
piv = {}   # pivot bit -> (vector, combo)
for i, vec in enumerate(rows):
    combo = 1 << i
    while vec:
        b = vec.bit_length() - 1
        if b in piv: pv, pc = piv[b]; vec ^= pv; combo ^= pc
        else: piv[b] = (vec, combo); break
assert len(piv) == nz, 'U not invertible?'
# reduce to get combos for unit vectors
order = sorted(piv)            # ascending bits
red = {}
for b in order:
    vec, combo = piv[b]
    x = vec ^ (1 << b)
    while x:
        bb = x.bit_length() - 1
        rv, rc = red[bb]
        vec ^= rv; combo ^= rc; x = vec ^ (1 << b)
    red[b] = (vec, combo)
def inv_row(r):
    combo = red[zidx[r]][1]; out = []
    while combo:
        b = combo & -combo; out.append(zregs[b.bit_length() - 1]); combo ^= b
    return out
def span_rank(fids):
    idx = sorted(set(i for f in fids for i in fr[f]))
    return int(np.linalg.matrix_rank(L[idx])) if idx else 0
stats = Counter(); cand = []
for h in range(2 * v, n):
    zr = zread[h]; tr = tread[h]
    # dirt column of h: registers whose final raw value involves initial s_h
    col = [r for r in zregs if val[r] >> zidx[h] & 1]
    clean = (col == [h])
    ir = inv_row(h)
    rk = span_rank([endB[r] for r in ir])
    key = ('zread' if zr else 'noZread', 'clean' if clean else 'dirty', 'U%d' % rk)
    stats[key] += 1
    if not zr and rk <= 7: cand.append((h, len(ir), rk, len(writes[h]), len(tr)))
for k, c in sorted(stats.items()): print(k, c)
print('exit candidates (no z-reader, inverse-row end-of-B span rank <= 7):', len(cand))
for c in cand[:40]: print('  helper', c[0], 'inv-row size', c[1], 'span rank', c[2], 'writes', c[3], 'target reads', c[4])
irs = Counter(len(inv_row(h)) for h in range(2*v, n) if not zread[h])
print('inverse-row sizes of helpers with no z-reader:', sorted(irs.items())[:20])
# ---- the retained totals: inverse rows at end of A (after scatter) and at end of B
print('--- retained totals ---')
w2 = w
valA = {r: 1 << zidx[r] for r in zregs}; curA = list(w['start'])
for f, d, srcs in w['A']:
    for r in [d] + srcs: curA[r] = f if fdim[f] >= fdim[curA[r]] else curA[r]
    if not is_t(d):
        acc = 0
        for s in srcs: acc ^= valA[s]
        valA[d] ^= acc
def inverse_rows(vals):
    rows = [vals[r] for r in zregs]; piv = {}
    for i, vec in enumerate(rows):
        combo = 1 << i
        while vec:
            b = vec.bit_length() - 1
            if b in piv: pv, pc = piv[b]; vec ^= pv; combo ^= pc
            else: piv[b] = (vec, combo); break
    red = {}
    for b in sorted(piv):
        vec, combo = piv[b]; x = vec ^ (1 << b)
        while x:
            bb = x.bit_length() - 1; rv, rc = red[bb]; vec ^= rv; combo ^= rc; x = vec ^ (1 << b)
        red[b] = (vec, combo)
    def row(r):
        combo = red[zidx[r]][1]; out = []
        while combo:
            b = combo & -combo; out.append(zregs[b.bit_length() - 1]); combo ^= b
        return out
    return row
rowA = inverse_rows(valA)
for q in w['ret']:
    irA = rowA(q); irB = inv_row(q)
    print('total helper', q, 'z-readers', len(zread[q]), 'writes', len(writes[q]), '| frame at scatter rank', fdim[curA[q]],
          '| inv row @A size', len(irA), 'span', span_rank([curA[r] for r in irA]),
          '| inv row @B size', len(irB), 'span', span_rank([endB[r] for r in irB]))

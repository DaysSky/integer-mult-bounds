"""nat134b: THE RETIREMENT-EMITTER v2 (the forward greedy re-framing).

The flattening (nat134) + THE FORWARD RE-FRAMING: process the gates in the topological
order; each gate's frame = the existing frame G with sub[cur[p]][G] for ALL participants,
the content-lines inside G, dims[G] > dims[cur[p]] strictly; choose minimal-dim first
(the chain-preserving mode) or maximal (the shape mode) - both censused. The sources'
chains then absorb the new reads legally.
"""
import json, gzip, os, sys
import mpmath as mp
from collections import Counter
from fractions import Fraction

mp.mp.dps = 40
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
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


line_in = [[False] * NF for _ in range(v)]
for i in range(v):
    for G in range(NF):
        line_in[i][G] = contains(bases[G], lines[i]) if bases[G] else False
print('the frames + the line-membership done', flush=True)

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

# (1) the flattening (as nat134)
b_read = set()
for F, d, ss in B:
    for s in ss:
        if s >= 2 * v:
            b_read.add(s)
INTER = set(q for q in range(2 * v, nreg) if q not in b_read and q not in RET)
srcs_of = {}
for F, d, ss in A:
    srcs_of.setdefault(d, set()).update(ss)


def flatten_srcs(q):
    out = set()
    stack = [q]
    seen = {q}
    while stack:
        x = stack.pop()
        for s in srcs_of.get(x, ()):
            if s in INTER and s not in seen:
                seen.add(s); stack.append(s)
            elif s not in INTER:
                out.add(s)
    return out


flat = {q: flatten_srcs(q) for q in INTER}
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
print('the flattened A: %d gates' % len(A2), flush=True)


# (2) THE FORWARD GREEDY RE-FRAMING
import copy


def reframe(mode):
    A2m = copy.deepcopy(A2)
    Bm = copy.deepcopy(B)
    # (a) THE BACKWARD BOUND PRE-PASS: bound[p] at each gate (the ret-gates' frozen
    # frames bound their participants' pre-positions!)
    seqg = [(g, A2m) for g in range(len(A2m))] + [(g, Bm) for g in range(len(Bm))]
    # the per-register gate order
    reg_gates = [[] for _ in range(nreg)]
    for k, (gi, lst) in enumerate(seqg):
        F, d, ss = lst[gi]
        for p in [d] + list(ss):
            reg_gates[p].append(k)
    NGS = len(seqg)
    # the C-phase as the terminal gates
    for ci, (F, d, ss) in enumerate(C):
        for p in [d] + list(ss):
            reg_gates[p].append(NGS + ci)
    bounds = [list() for _ in range(NGS)]   # per gate: {p: the max allowed frame}
    cur_b = list(final)
    for k in range(NGS - 1, -1, -1):
        gi, lst = seqg[k]
        F, d, ss = lst[gi]
        parts = [d] + list(ss)
        bounds[k] = {p: cur_b[p] for p in parts}
        for p in parts:
            cur_b[p] = F
    # (b) THE FORWARD GREEDY with the bounds
    cur = list(start)
    hist = Counter()
    vv = [0] * nreg
    for s in range(v):
        vv[s] = 1 << s
    for F, d, ss in D:
        for s in ss:
            vv[d] ^= vv[s]
    for lst, bound_lst in ((A2m, bounds[:len(A2m)]), (Bm, bounds[len(A2m):])):
        for gi, (F, d, ss) in enumerate(lst):
            parts = [d] + list(ss)
            if any(p in RET for p in parts):
                for p in parts:
                    r0 = dims[F] - dims[cur[p]]
                    if r0 > 0:
                        hist[r0] += 1
                    elif cur[p] != F:
                        return None, None, None, ('ret-freeze down-climb', p)
                    cur[p] = F
                continue

            def lines_of(p):
                m = vv[p] & ((1 << v) - 1)
                return [i for i in range(v) if (m >> i) & 1]

            def legal(G):
                if not all(sub[cur[p]][G] and dims[G] > dims[cur[p]] for p in parts):
                    return False
                bd = bound_lst[gi]
                for p in parts:
                    if not sub[G][bd[p]]:
                        return False
                for p in parts:
                    for i in lines_of(p):
                        if not line_in[i][G]:
                            return False
                return True

            cand = [G for G in range(NF) if legal(G)]
            if not cand:
                return None, None, None, ('no frame', gi, parts, [cur[p] for p in parts])
            if mode == 'min':
                G = min(cand, key=lambda x: dims[x])
            else:
                G = max(cand, key=lambda x: dims[x])
            lst[gi] = [G, d, ss]
            for s in ss:
                vv[d] ^= vv[s]
            for p in parts:
                r0 = dims[G] - dims[cur[p]]
                if r0 > 0:
                    hist[r0] += 1
                cur[p] = G
    return hist, cur, (A2m, Bm), None


for mode in ('min', 'max'):
    h, cur, _, err = reframe(mode)
    if err:
        print('mode %s: FAIL %s' % (mode, str(err)[:120]))
        continue
    hist = Counter(h)
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
    kept = [r for r in range(nreg) if not (2 * v <= r < nreg and r in INTER)]
    for r in kept:
        r0 = dims[final[r]] - dims[cur[r]]
        if r0 > 0:
            hist[r0] += 1
    R2 = R - len(INTER)
    mass = sum(k * c for k, c in hist.items())
    ident = 8 * R2 + cst + 2 * v * 7
    P111 = mp.mpf('0.001733052823330162099157')
    ok = (mass == ident)
    c = None
    if ok:
        c, _, _ = price(dict(hist), v, 8, R2)
    print('mode %s: R2=%d mass %s (identity %d) hist %s' % (mode, R2, mass, ident, dict(sorted(hist.items()))))
    print('   price: %s (%+.4f%%)' % (mp.nstr(c, 20) if c else ('OK' if ok else 'MASS-MISMATCH/NO-ROOT'),
          float((c - P111) / P111) * 100 if c else 0))
    json.dump({'mode': mode, 'hist': dict(hist), 'R2': R2, 'c': str(c) if c else None, 'mass': mass},
              open('ii19_nat134b_%s.json' % mode, 'wt'), indent=1)

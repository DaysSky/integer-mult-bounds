"""Independent exact checker for bitGen/1+mut words (general nondegenerate frames).  Shares no code with the builder.
Checks: labels and form; every listed frame is a nondegenerate subspace (exact Gram determinant); start/final frames;
replay of D, A, scatter, B, C with every operand climbing to the gate frame (nested, dimension nondecreasing); the
content-frame invariant (every line in a register's content lies in its frame); exact F2 semantics on all columns
(x, y, helper dirt); hypotheses H1-H5 of the interleaved scalar-interface lemma; local paid histogram
(each climb = one child of its rank, each retained total = one COPY child of its frame rank); rank-mass identity.
usage: gcheck.py WORD.json[.gz] [--price]

EXTENDED COPY (gcheck_hpe.py, II19 audit 2026-10-19).  Identical to gcheck.py except for an optional word key
'hyperplane_end' = U (a frame of dim h-1): every helper (z register >= 2v) ends at U instead of the full frame,
every C gate runs at U, the rank-mass identity becomes (h-1)R + cst + 2v(h-1), and the price hosts helper
residuals of width h-1.  This models hyperplane-ended cleanup (cf. research/hyperplane-end-lean, proved there
for single-gate complex-side helpers); its bit-side validity for whole cleanups is an open proof obligation."""
import gzip, json, sys
from fractions import Fraction as Fr
from collections import Counter

class Reject(Exception): pass
def need(c, m):
    if not c: raise Reject(m)

def rref(rows, n):
    m = [[Fr(x) for x in r] for r in rows]; r = 0; piv = []
    for c in range(n):
        p = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if p is None: continue
        m[r], m[p] = m[p], m[r]; iv = 1 / m[r][c]; m[r] = [x * iv for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]; m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        piv.append(c); r += 1
    return [tuple(x) for x in m[:r]]

def det(M):
    M = [row[:] for row in M]; k = len(M); d = Fr(1)
    for c in range(k):
        p = next((i for i in range(c, k) if M[i][c] != 0), None)
        if p is None: return Fr(0)
        if p != c: M[c], M[p] = M[p], M[c]; d = -d
        d *= M[c][c]
        for i in range(c + 1, k):
            if M[i][c] != 0:
                f = M[i][c] / M[c][c]; M[i] = [a - f * b for a, b in zip(M[i], M[c])]
    return d

def main(path, do_price=False):
    op = gzip.open if path.endswith('.gz') else open
    w = json.load(op(path, 'rt'))
    h, v, R = w['h'], w['v'], w['R']
    HPE = w.get('hyperplane_end')
    B = [[Fr(x, w['form']['den']) for x in row] for row in w['form']['num']]
    ip = lambda x, y: sum(x[i] * B[i][j] * y[j] for i in range(h) for j in range(h) if B[i][j])
    L = [[Fr(x) for x in l] for l in w['lines']]
    need(len(L) == v, 'line count')
    G = [[ip(L[i], L[j]) for j in range(v)] for i in range(v)]
    need(all(G[i][i] != 0 for i in range(v)), 'zero-norm line')
    # frames
    fr = [rref(F, h) for F in w['frames']]
    dims = [len(F) for F in fr]
    for k, F in enumerate(fr):
        if F: need(det([[ip(a, b) for b in F] for a in F]) != 0, 'degenerate frame %d' % k)
    def subset(a, b): return len(rref(list(fr[a]) + list(fr[b]), h)) == dims[b]
    _sub = {}
    def sub(a, b):
        k = (a, b)
        if k not in _sub: _sub[k] = subset(a, b)
        return _sub[k]
    def contains(F, x): return len(rref(list(fr[F]) + [x], h)) == dims[F]
    _cont = {}
    def cont(F, s):
        k = (F, s)
        if k not in _cont: _cont[k] = contains(F, L[s])
        return _cont[k]
    nreg = 2 * v + R
    start, final = w['start'], w['final']
    for s in range(v): need(dims[start[s]] == 1 and cont(start[s], s), 'source start frame')
    for r in range(v, nreg): need(dims[start[r]] == 0, 'start frame of y/helper')
    if HPE is not None: need(dims[HPE] == h - 1, 'hyperplane_end frame dimension')
    for r in range(v): need(dims[final[r]] == h, 'final full frame')
    for r in range(2 * v, nreg):
        if HPE is None: need(dims[final[r]] == h, 'final full frame')
        else: need(final[r] == HPE, 'helper final at the hyperplane_end frame')
    for t in range(v):
        F = final[v + t]
        need(dims[F] == h - 1 and all(ip(L[t], b) == 0 for b in fr[F]), 'target final frame t-perp')
    cur = list(start); val = [1 << i for i in range(nreg)]; hist = Counter(); moves = 0
    def climb(r, F):
        nonlocal moves
        if cur[r] == F: return
        need(sub(cur[r], F) and dims[F] > dims[cur[r]], 'climb not nested (reg %d)' % r)
        hist[dims[F] - dims[cur[r]]] += 1; moves += 1; cur[r] = F
    def content_ok(r):
        x = val[r] & ((1 << v) - 1); F = cur[r]
        while x:
            b = x & -x; s = b.bit_length() - 1; x ^= b
            if not cont(F, s): return False
        return True
    def run(gates, phase):
        for F, d, srcs in gates:
            need(d not in srcs and len(set(srcs)) == len(srcs), 'gate operands')
            for r in [d] + srcs: climb(r, F)
            if v <= d < 2 * v:
                # a target may hold scattered (dropped) totals; every register it reads must lie inside its frame
                for s in srcs: need(content_ok(s), 'read content outside frame (%s, reg %d)' % (phase, s))
            for s in srcs: val[d] ^= val[s]
            if not (v <= d < 2 * v):
                need(content_ok(d), 'content outside frame (%s, reg %d)' % (phase, d))
    # D: frame 0, writes targets, reads helpers
    for F, d, srcs in w['D']:
        need(dims[F] == 0 and v <= d < 2 * v and all(s >= 2 * v for s in srcs), 'H2 (D)')
    run(w['D'], 'D')
    for F, d, srcs in w['A']: need(not (v <= d < 2 * v) and all(not (v <= s < 2 * v) for s in srcs), 'H3 (A)')
    run(w['A'], 'A')
    # scatter: retained registers at their frames, targets at frame 0
    ret, rf = w['ret'], w['ret_frames']
    copy_ranks = []
    for k, q in enumerate(ret):
        need(cur[q] == rf[k] and q >= 2 * v or q < v, 'retained register frame')
        need(q < v or q >= 2 * v, 'retained register is a z register')
        need(cur[q] == rf[k], 'retained register not at its frame')
        copy_ranks.append(dims[rf[k]])
    for t in range(v):
        need(dims[cur[v + t]] == 0, 'target not at frame 0 at the scatter')
        for k in w['scatter'][t]: val[v + t] ^= val[ret[k]]
    for c in copy_ranks: hist[c] += 1
    for F, d, srcs in w['B']:
        if v <= d < 2 * v: pass
        else: need(all(not (v <= s < 2 * v) for s in srcs), 'H1/H3 (B z-gate reads a target)')
    run(w['B'], 'B')
    for F, d, srcs in w['C']:
        need((dims[F] == h if HPE is None else F == HPE) and not (v <= d < 2 * v), 'H4 (C)')
    # H4: C is the literal reverse of the z-destination gates of A and B
    zg = [[F, d, s] for F, d, s in w['A'] + w['B'] if not (v <= d < 2 * v)]
    need([[d, s] for F, d, s in w['C']] == [[d, s] for F, d, s in reversed(zg)], 'H4 literal reverse')
    run(w['C'], 'C')
    for r in range(nreg): climb(r, final[r])
    # semantics
    for r in range(nreg):
        want = (1 << r) ^ ((1 << (r - v)) if v <= r < 2 * v else 0)
        need(val[r] == want, 'final value of register %d' % r)
    mass = sum(k * n for k, n in hist.items())
    cst = sum(copy_ranks)
    need(mass == (h if HPE is None else h - 1) * R + cst + 2 * v * (h - 1), 'rank mass identity')
    out = dict(status='PASS', hyperplane_end=HPE, h=h, v=v, R=R, rho=R / v, totals=len(ret), cst=cst, x=cst / v, frames=len(fr),
               moves=moves, local_histogram=dict(sorted(hist.items())), rank_mass=mass,
               gates={k: len(w[k]) for k in ('D', 'A', 'B', 'C')})
    if do_price:
        sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', '..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
        from pricer import price
        from mpmath import mp
        c, prof, d = price(dict(hist), v, h, R, w=(h if HPE is None else h - 1))
        P111 = mp.mpf('0.001733052823330162099157')
        out['bit_c_nine_stage'] = mp.nstr(c, 22) if c is not None else str(d)
        if c is not None: out['vs_P111_percent'] = float((c / P111 - 1) * 100)
    return out

if __name__ == '__main__':
    try:
        print(json.dumps(main(sys.argv[1], '--price' in sys.argv), indent=1))
    except Reject as e:
        print('REJECT:', e); sys.exit(1)

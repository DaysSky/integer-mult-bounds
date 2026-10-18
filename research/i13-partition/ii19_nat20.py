"""THE WORD4 ORACLE + ANATOMY (ii19_nat20.py) — the Lorentzian push (the user's directive:
"must be a lorentzian"): this session's r434 machinery (replay oracle -> ladder census) applied
to OUR OWN committed Lorentzian record word ii19_own_word4.json (v=121, h=9, R=472, CST=73,
c = 0.001335891046497132929087 = -23.42% vs the frontier).

The r434 arc's lesson: every route died on the UNSHARED geometry (single-source cells, private
rungs, single-source dim-6 homes).  The word4 was built on the R420 template WITH shared
12-frames (10 frames x 12 sources).  This census measures the word4's own sharing anatomy:
  (0) the replay oracle (w21's, verbatim) + the baseline PASS + the exact-price control;
  (1) the climb-chain shape census (every register's chain dims over D+A, and full);
  (2) the sharing anatomy: own-cell groups (sources per cell), rung sharing (helpers per frame),
      home sharing (sources per dim-4/dim-8 frame) — the r434-census analog.
"""
import json, os, sys, time
from collections import Counter, defaultdict
from fractions import Fraction
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
from pricer import price
from mpmath import mp

SRC = sys.argv[1] if len(sys.argv) > 1 else 'ii19_own_word4.json'
w = json.load(open(SRC, 'rt'))
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

V, H = w['v'], w['h']
nreg = len(w['start'])

def rref(rows, n):
    m = [[Fraction(x) for x in r] for r in rows]; r = 0
    for c in range(n):
        p = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if p is None: continue
        m[r], m[p] = m[p], m[r]; iv = 1 / m[r][c]; m[r] = [x * iv for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]; m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
    return m[:r]
fr = [rref(F, H) for F in w['frames']]
dims = [len(F) for F in fr]
L = [[Fraction(x) for x in l] for l in w['lines']]
_sub, _cont = {}, {}
def sub(a, b):
    if (a, b) not in _sub:
        _sub[(a, b)] = len(rref(list(fr[a]) + list(fr[b]), H)) == dims[b]
    return _sub[(a, b)]
def cont(F, s):
    if (F, s) not in _cont:
        _cont[(F, s)] = len(rref(list(fr[F]) + [L[s]], H)) == dims[F]
    return _cont[(F, s)]

def replay(A):
    """gcheck-exact replay (w21's, verbatim); returns (first-failure or None, hist, C)."""
    cur = list(w['start']); val = [1 << r for r in range(nreg)]; hist = Counter()
    def climb(r, F, where):
        if cur[r] == F: return None
        if not (sub(cur[r], F) and dims[F] > dims[cur[r]]):
            return ('climb', where, r, cur[r], F)
        hist[dims[F] - dims[cur[r]]] += 1; cur[r] = F
    def content_ok(r):
        x = val[r] & ((1 << V) - 1); F = cur[r]
        while x:
            b = x & -x; s = b.bit_length() - 1; x ^= b
            if not cont(F, s): return False
        return True
    def run(gates, phase):
        for gi, (F, d, srcs) in enumerate(gates):
            for r in [d] + srcs:
                e = climb(r, F, (phase, gi))
                if e: return e
            if V <= d < 2 * V:
                for s in srcs:
                    if not content_ok(s): return ('read-content', (phase, gi), s)
            for s in srcs: val[d] ^= val[s]
            if not (V <= d < 2 * V) and not content_ok(d): return ('content', (phase, gi), d)
    zg = [[F, d, s] for F, d, s in A + w['B'] if not (V <= d < 2 * V)]
    C = [[1, d, list(s)] for F, d, s in reversed(zg)]
    e = run(w['D'], 'D') or run(A, 'A')
    if e: return e, hist, C
    for k, q in enumerate(w['ret']):
        if cur[q] != w['ret_frames'][k]: return ('ret-frame', k, q), hist, C
    for t in range(V):
        if dims[cur[V + t]] != 0: return ('scatter-frame', t), hist, C
        for k in w['scatter'][t]: val[V + t] ^= val[w['ret'][k]]
    for f in w['ret_frames']: hist[dims[f]] += 1
    e = run(w['B'], 'B') or run(C, 'C')
    if e: return e, hist, C
    for r in range(nreg):
        e = climb(r, w['final'][r], ('FINAL', r))
        if e: return e, hist, C
    for r in range(nreg):
        if val[r] != ((1 << r) ^ (1 << (r - V)) if V <= r < 2 * V else 1 << r):
            return ('value', r), hist, C
    return None, hist, C

e, hist0, _ = replay(w['A'])
log('(0) baseline replay: %s | hist %s' % (e or 'PASS', dict(sorted(hist0.items()))))
assert e is None
c0 = price(dict(hist0), V, H, w['R'])[0]
FRONT = mp.mpf('0.001744385950814795279853')
log('    price control: %s (%+.4f%% vs the frontier)' % (mp.nstr(c0, 22), float((c0 / FRONT - 1) * 100)))
assert mp.nstr(c0, 20) == mp.nstr(mp.mpf('0.001335891046497132929087'), 20), 'PRICE CONTROL FAILED'

# (1) chain-shape census
PH = ('D', 'A', 'B')
chainDA = defaultdict(list)
cur = list(w['start'])
for F, d, srcs in w['D'] + w['A']:
    for r in [d] + srcs:
        if cur[r] != F and dims[F] >= dims[cur[r]]:
            cur[r] = F; chainDA[r].append(F)
shape = Counter(tuple(dims[f] for f in chainDA[r]) for r in range(2 * V, nreg))
log('(1) helper chain-shape hist (D+A): %s' % dict(sorted(shape.items(), key=lambda x: -x[1])[:12]))
srcshape = Counter(tuple(dims[f] for f in chainDA[s]) for s in range(V))
log('    source chain-shape hist (D+A): %s' % dict(sorted(srcshape.items(), key=lambda x: -x[1])[:12]))

# (2) the sharing anatomy (full chains)
chainF = defaultdict(list)
cur = list(w['start'])
for ph in PH + ('C',):
    for F, d, srcs in w[ph]:
        for r in [d] + srcs:
            if cur[r] != F and dims[F] >= dims[cur[r]]:
                cur[r] = F; chainF[r].append(F)
for r in range(nreg):
    if cur[r] != w['final'][r] and dims[w['final'][r]] >= dims[cur[r]]:
        chainF[r].append(w['final'][r])
for d, label in ((2, 'cells'), (4, 'dim-4 frames'), (8, 'dim-8 frames')):
    home = {}
    for r in range(nreg):
        fs = sorted(set(f for f in chainF[r] if dims[f] == d))
        home[r] = fs[0] if len(fs) == 1 else None
    srchome = Counter(home[s] for s in range(V) if home[s] is not None)
    helperhome = Counter(home[h] for h in range(2 * V, nreg) if home[h] is not None)
    log('(2) %s: sources homed %d at %d distinct (%s) | helpers homed %d at %d distinct (max %d/frame)' % (
        label, sum(srchome.values()), len(srchome), dict(sorted(Counter(srchome.values()).items())),
        sum(helperhome.values()), len(helperhome), max(helperhome.values()) if helperhome else 0))

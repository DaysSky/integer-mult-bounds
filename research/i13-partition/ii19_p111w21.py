"""THE V2-WORD (ii19_p111w21.py) — the r434 hist-reshape, variant v2 (the position-keyed rewrite of w20).

The move: each T155 helper h (chain (0,1,2,4,6)) is built at a singleton [S, h, [s1]] and then
2nd-gated at a dim-2 cell [F2, h, [s2]].  Move the build to just before its 2nd gate and reframe it
to F2: h then climbs 0 -> 2 once (per-h hist {1: -2, 2: +1}, mass preserved).

w20's bugs fixed: builds and 2nd gates are identified by ORIGINAL A-position (not by `d in mobile`);
no cell-gate reordering (the 2nd gates stay put).  Each move is admitted greedily against a
gcheck-exact replay (climbs nested + strictly rising, content-in-frame, final values, H4 C-reverse);
a move that breaks anything is left unmoved.  C is regenerated as the literal reverse of zg at frame 1.
"""
import json, sys, time
from collections import Counter, defaultdict
from fractions import Fraction

SRC = sys.argv[1] if len(sys.argv) > 1 else 'ii19_pub2_p111-r434.json'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'ii19_r434_v2.json'
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
    """gcheck-exact replay; returns (first-failure or None, hist)."""
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

# (1) the T155 helpers and their build / 2nd-gate positions (ORIGINAL A-indices)
cur = list(w['start']); chain = defaultdict(list)
for F, d, srcs in w['D'] + w['A']:
    for r in [d] + srcs:
        if cur[r] != F and dims[F] >= dims[cur[r]]:
            cur[r] = F; chain[r].append(F)
T155 = sorted(h for h in range(2 * V, nreg) if tuple(dims[f] for f in chain[h]) == (1, 2, 4, 6))
touch = defaultdict(list)
for gi, (F, d, srcs) in enumerate(w['A']):
    for r in [d] + srcs: touch[r].append(gi)
cands = []
for h in T155:
    b, s = touch[h][0], touch[h][1]
    Fb, db, sb = w['A'][b]; Fs, ds, ss = w['A'][s]
    if not (db == h and dims[Fb] == 1 and len(sb) == 1 and sb[0] < V and ds == h and dims[Fs] == 2):
        continue
    if not cont(Fs, sb[0]): continue
    cands.append((h, b, s, Fs, sb[0]))
log('(1) T155 %d | well-formed build->2nd pairs %d' % (len(T155), len(cands)))

def build_A(moves):
    """moves: {build-pos: (2nd-pos, F2)} -> reordered + reframed A."""
    key = []
    for gi in range(len(w['A'])):
        key.append(2 * moves[gi][0] - 1 if gi in moves else 2 * gi)
    order = sorted(range(len(w['A'])), key=lambda i: key[i])
    A = []
    for i in order:
        F, d, srcs = w['A'][i]
        A.append([moves[i][1] if i in moves else F, d, list(srcs)])
    return A

# (2) greedy admission, one move at a time against the full replay
moves, rejected = {}, Counter()
for n, (h, b, s, F2, s1) in enumerate(cands):
    trial = dict(moves); trial[b] = (s, F2)
    e, hist, _ = replay(build_A(trial))
    if e is None:
        moves = trial
    else:
        rejected[e[0]] += 1
    if n % 25 == 0:
        log('    %d/%d: admitted %d | rejected %s' % (n + 1, len(cands), len(moves), dict(rejected)))
A2 = build_A(moves)
e, hist, C2 = replay(A2)
log('(2) admitted %d/%d | rejected %s' % (len(moves), len(cands), dict(rejected)))
log('    final replay: %s | hist %s (mass %d, base %d)' % (e or 'PASS', dict(sorted(hist.items())),
    sum(k * c for k, c in hist.items()), sum(k * c for k, c in hist0.items())))
log('    hist delta: %s' % {k: hist[k] - hist0[k] for k in sorted(set(hist) | set(hist0)) if hist[k] != hist0[k]})
assert e is None

word = dict(w)
word['A'] = A2
word['C'] = C2
word['stats'] = dict(w.get('stats', {}), v2_moved_builds=len(moves))
json.dump(word, open(OUT, 'w'))
log('(3) emitted %s' % OUT)

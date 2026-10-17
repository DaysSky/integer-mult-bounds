"""Which helpers can be made dirt-free (K column zero) by inserted pure-dirt reads g += h, legally?
For helper h: E = frame of h's first touch (entrance); h holds pure dirt d until its first write tw.
An inserted gate g += h at time p (before raw gate p, p <= tw) at a listed frame F adds alpha_g(p) to k_h, where
alpha_g(p) is the target-influence of g's content at time p in the raw word W0 = (A, scatter, B).
Legal iff F contains the current frames of g and h and is contained in the next-touch frames of g and h.
k_h = alpha_h(0).  h convertible iff k_h in span of the legal alpha vectors.
usage: span.py WORD.json.gz"""
import gzip, json, sys
from collections import defaultdict
import numpy as np

w = json.load(gzip.open(sys.argv[1], 'rt'))
v, R = w['v'], w['R']; n = 2 * v + R
FR = [frozenset(f) for f in w['frames']]
Lm = np.array(w['lines'], dtype=float)
fd = [int(np.linalg.matrix_rank(Lm[sorted(f)])) if f else 0 for f in FR]
FULL = fd.index(8)
frame_id = {f: k for k, f in enumerate(FR)}
sub = lambda a, b: FR[a] <= FR[b]
G = [tuple(g) for g in w['A']]; NA = len(G)
GB = [tuple(g) for g in w['B']]
# raw sequence: A gates 0..NA-1, scatter at NA (event 'S'), B gates NA+1..
seq = G + [None] + GB
T = len(seq)
is_y = lambda r: v <= r < 2 * v
# touches per register: list of (time, frame); scatter touches targets and ret (copy) -- frames: ret at its frame (no climb)
touch = defaultdict(list)
for t, g in enumerate(seq):
    if g is None: continue
    f, d, srcs = g
    for r in [d] + list(srcs): touch[r].append((t, f))
first_write = {}
for t, g in enumerate(seq):
    if g is None: continue
    first_write.setdefault(g[1], t)
# backward alpha
alpha = [0] * n
for t in range(v): alpha[v + t] = 1 << t
snap = {}   # (r, t) -> alpha_r just before seq[t] for touches (we store at each touch time and at 0)
alpha_before = [None] * (T + 1)
hist = defaultdict(list)   # r -> list of (t, alpha_r(t)) recorded at times t where alpha_r changes going backwards
for r in range(n): hist[r].append((T, alpha[r]))
for t in range(T - 1, -1, -1):
    g = seq[t]
    if g is None:
        acc = defaultdict(int)
        for tt, row in enumerate(w['scatter']):
            for k in row: acc[w['ret'][k]] ^= alpha[v + tt]
        for r, a in acc.items():
            alpha[r] ^= a; hist[r].append((t, alpha[r]))
        continue
    f, d, srcs = g
    for s in srcs:
        alpha[s] ^= alpha[d]; hist[s].append((t, alpha[s]))
def alpha_at(r, p):
    """alpha_r just before seq[p] (value after processing backwards all gates >= p)"""
    # hist[r] has decreasing times; find last entry with time >= p
    best = None
    for tt, a in hist[r]:
        if tt >= p: best = a
        else: break
    return best
# forward check of k_h = alpha_h(0)
val = [1 << r for r in range(n)]
for t, g in enumerate(seq):
    if g is None:
        cop = [val[q] for q in w['ret']]
        for tt, row in enumerate(w['scatter']):
            for k in row: val[v + tt] ^= cop[k]
        continue
    f, d, srcs = g
    acc = 0
    for s in srcs: acc ^= val[s]
    val[d] ^= acc
kcol = {h: sum(1 << t for t in range(v) if val[v + t] >> h & 1) for h in range(2 * v, n)}
for h in range(2 * v, n): assert kcol[h] == alpha[h], h
print('alpha(0) == K columns for all helpers: True')
Dset = set(s for g in w['D'] for s in g[2])
def frame_at(r, p):
    """frame of r just before seq[p], and its next-touch frame (or FULL)"""
    cur = w['start'][r]; nxt = FULL
    for t, f in touch[r]:
        if t < p: cur = f
        else: nxt = f; break
    return cur, nxt
def legal_F(hc, hn, gc, gn):
    for F in (hn, gn, hc, gc):
        if sub(hc, F) and sub(gc, F) and sub(F, hn) and sub(F, gn): return F
    return None
def span_solve(target, vecs):
    """F2: is target in span(vecs)?  returns list of indices or None"""
    basis = {}   # pivot bit -> (vec, combo set)
    for i, x in enumerate(vecs):
        combo = {i}
        while x:
            p = x.bit_length() - 1
            if p in basis:
                bv, bc = basis[p]; x ^= bv; combo ^= bc
            else:
                basis[p] = (x, combo); break
    x = target; combo = set()
    while x:
        p = x.bit_length() - 1
        if p not in basis: return None
        bv, bc = basis[p]; x ^= bv; combo ^= bc
    return sorted(combo)
res = {}
summary = defaultdict(int)
for h in range(2 * v, n):
    if not touch[h]: continue
    t1, F1 = touch[h][0]
    E = F1
    if fd[E] == 0: summary['first touch at frame 0'] += 1; continue
    if kcol[h] == 0:
        res[h] = dict(E=E, dimE=fd[E], ins=[]); summary['already dirt-free'] += 1; continue
    tw = first_write.get(h, T)
    if tw >= NA: pass
    # candidate insertion times: p in [0, tw]; for g, alpha piecewise constant between reads, frames piecewise between touches.
    cands = []
    # breakpoints: touches of h and g
    htimes = [t for t, _ in touch[h] if t <= tw]
    for g in range(n):
        if g == h or is_y(g): continue
        bps = sorted(set([0] + [t for t, _ in touch[g] if t <= tw] + [t + 1 for t, _ in touch[g] if t + 1 <= tw] + htimes + [t + 1 for t in htimes if t + 1 <= tw] + [tw]))
        seen = set()
        for p in bps:
            if p > tw: continue
            hc, hn = frame_at(h, p) if p > 0 else (E, F1)
            if p == 0: hc = E
            gc, gn = frame_at(g, p)
            F = legal_F(hc, hn, gc, gn)
            if F is None: continue
            a = alpha_at(g, p)
            if a == 0 or (a, F) in seen: continue
            seen.add((a, F))
            cands.append((a, g, p, F, gc, gn, hc, hn))
    sol = span_solve(kcol[h], [c[0] for c in cands])
    if sol is None:
        summary['not in span'] += 1; continue
    res[h] = dict(E=E, dimE=fd[E], ins=[cands[i][1:] for i in sol])
    summary['convertible'] += 1
print(dict(summary))
print('convertible helpers:', len(res), 'by entrance dim', dict(sorted(defaultdict(int, {}).items())))
from collections import Counter
print(Counter(r['dimE'] for r in res.values()), 'insertions per helper', Counter(len(r['ins']) for r in res.values()))
json.dump({str(h): r for h, r in res.items()}, open(sys.argv[2] if len(sys.argv) > 2 else 'span.json', 'w'))

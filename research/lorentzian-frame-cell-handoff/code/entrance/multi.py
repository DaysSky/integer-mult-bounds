"""Sequential multi-helper entrance conversion (double-read dirt cancellation, generalised by F2 span).
For each helper h (in order), on the CURRENT word (previous conversions applied):
  F1 = frame of h's first touch; E = F1 if F1 has a live-root orthogonal 8-frame isometry (rank 1, or rank 2 spanned by
  two orthogonal live roots), else a listed rank-1 frame inside F1 with such an isometry (else skip).
  h holds pure dirt d until its first write tw; inserted gate g += h at time p <= tw at frame F adds alpha_g(p) to k_h.
  Candidates: no split for h and g (F in {cur, next} for both, nested); g a z register (source or helper), g != h.
  Solve k_h = sum alpha over F2 (Gaussian elimination, fewest pivots greedy); apply: insert gates, start[h] = E.
At the end D is recomputed from the raw word and C rebuilt as the literal reverse.
usage: multi.py IN.json.gz OUT.json.gz [--max N] [--split] [--no-sources]"""
import gzip, json, sys, copy, hashlib
from collections import defaultdict
import numpy as np

args = sys.argv[1:]
inp, out = args[0], args[1]
MAXN = int(args[args.index('--max') + 1]) if '--max' in args else 10 ** 9
SPLIT = '--split' in args; NOSRC = '--no-sources' in args
w = json.load(gzip.open(inp, 'rt'))
v, R = w['v'], w['R']; n = 2 * v + R
FR = [frozenset(f) for f in w['frames']]
L = w['lines']
Lm = np.array(L, dtype=float)
fd = [int(np.linalg.matrix_rank(Lm[sorted(f)])) if f else 0 for f in FR]
FULL = fd.index(8); ZERO = fd.index(0)
sub = lambda a, b: FR[a] <= FR[b]
dot = lambda a, b: sum(x * y for x, y in zip(a, b))
is_y = lambda r: v <= r < 2 * v
line_frame = {}
for k, f in enumerate(FR):
    if fd[k] == 1: line_frame[next(iter(f))] = k


def ortho_frame(base):
    def rec(cur, cands):
        if len(cur) == 8: return cur
        for k, c in enumerate(cands):
            r = rec(cur + [c], [d for d in cands[k + 1:] if dot(L[c], L[d]) == 0])
            if r: return r
        return None
    if any(dot(L[a], L[b]) for a in base for b in base if a != b): return None
    return rec(list(base), [i for i in range(len(L)) if i not in base and all(dot(L[i], L[b]) == 0 for b in base)])


iso_ok = {}
def has_iso(F):
    if F not in iso_ok:
        lines = sorted(FR[F])
        ok = False
        if fd[F] == 1: ok = ortho_frame(lines) is not None
        elif fd[F] == 2:
            for a in lines:
                for b in lines:
                    if a < b and dot(L[a], L[b]) == 0 and ortho_frame([a, b]):
                        ok = True; break
                if ok: break
        iso_ok[F] = ok
    return iso_ok[F]


def analyse(w):
    """seq, touches, first writes, alpha history"""
    seq = [tuple((g[0], g[1], tuple(g[2]))) for g in w['A']] + [None] + [tuple((g[0], g[1], tuple(g[2]))) for g in w['B']]
    T = len(seq)
    touch = defaultdict(list); fw = {}
    for t, g in enumerate(seq):
        if g is None: continue
        f, d, srcs = g
        for r in (d,) + srcs: touch[r].append((t, f))
        fw.setdefault(d, t)
    alpha = [0] * n
    for t in range(v): alpha[v + t] = 1 << t
    hist = defaultdict(list)
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
    return seq, touch, fw, hist, alpha


def alpha_at(hist, r, p):
    best = None
    for tt, a in hist[r]:
        if tt >= p: best = a
        else: break
    return best


def frame_at(w, touch, r, p):
    cur = w['start'][r]; nxt = FULL
    for t, f in touch[r]:
        if t < p: cur = f
        else: nxt = f; break
    return cur, nxt


def solve(target, vecs):
    basis = {}
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


done = []; skipped = defaultdict(list)
Dset0 = set(s for g in w['D'] for s in g[2])
order = [h for h in range(2 * v, n) if w['start'][h] == ZERO]
for h in order:
    if len(done) >= MAXN: break
    seq, touch, fw, hist, alpha = analyse(w)
    if not touch[h]: skipped['untouched'].append(h); continue
    t1, F1 = touch[h][0]
    if fd[F1] == 0: skipped['first touch at frame 0'].append(h); continue
    if has_iso(F1): E = F1
    else:
        subs = [line_frame[q] for q in sorted(FR[F1]) if q in line_frame and has_iso(line_frame[q])]
        if not subs: skipped['no isometry frame'].append(h); continue
        E = subs[0]
    k = alpha[h]
    tw = fw.get(h, len(seq))
    ins = []
    if k:
        cands = []
        # h's frames: before t1 it is at E (after the change), next F1; afterwards (t1 < p <= tw) as in the word
        htimes = [t for t, _ in touch[h] if t <= tw]
        for g in range(n):
            if g == h or is_y(g) or (NOSRC and g < v): continue
            bps = sorted(set([0, tw] + [t for t, _ in touch[g] if t <= tw] + [t + 1 for t, _ in touch[g] if t + 1 <= tw]
                             + htimes + [t + 1 for t in htimes if t + 1 <= tw]))
            seen = set()
            for p in bps:
                if p > tw: continue
                if p <= t1: hc, hn = E, F1
                else: hc, hn = frame_at(w, touch, h, p)
                gc, gn = frame_at(w, touch, g, p)
                opts = (hc, hn, gc, gn) if SPLIT else [F for F in (hc, hn) if F in (gc, gn)]
                F = next((F for F in opts if sub(hc, F) and sub(gc, F) and sub(F, hn) and sub(F, gn)), None)
                if F is None: continue
                a = alpha_at(hist, g, p)
                if not a or a in seen: continue
                seen.add(a); cands.append((a, g, p, F))
        sol = solve(k, [c[0] for c in cands])
        if sol is None: skipped['not in span'].append(h); continue
        ins = [cands[i][1:] for i in sol]
    # apply: insert gates at positions (raw seq index), latest first so earlier indices stay valid
    NA = len(w['A'])
    for g, p, F in sorted(ins, key=lambda x: -x[1]):
        gate = [F, g, [h]]
        if p <= NA: w['A'].insert(p, gate)
        else: w['B'].insert(p - NA - 1, gate)
    w['start'][h] = E
    done.append((h, fd[E], len(ins)))
    print('h %d: E %d (dim %d, F1 dim %d) insertions %d; done %d' % (h, E, fd[E], fd[F1], len(ins), len(done)), flush=True)

# recompute D and C
val = [1 << r for r in range(n)]
def run(gates):
    for f, d, srcs in gates:
        acc = 0
        for s in srcs: acc ^= val[s]
        val[d] ^= acc
run(w['A'])
copies = [val[q] for q in w['ret']]
for t, row in enumerate(w['scatter']):
    for k in row: val[v + t] ^= copies[k]
run(w['B'])
D = []
for t in range(v):
    K = [r for r in range(2 * v, n) if val[v + t] >> r & 1]
    if K: D.append([ZERO, v + t, K])
dread = set(x for g in D for x in g[2])
bad = [h for h, _, _ in done if h in dread]
print('converted', len(done), 'entrance rank total', sum(e for _, e, _ in done) + sum(fd[w['start'][h]] for h in range(2 * v, n) if h not in [x[0] for x in done] and w['start'][h] != ZERO),
      'insertions', sum(i for _, _, i in done), 'converted still in D (must be 0):', len(bad))
print('skipped', {k: len(x) for k, x in skipped.items()})
w['D'] = D
zg = [[FULL, g[1], list(g[2])] for sec in ('A', 'B') for g in w[sec] if not is_y(g[1])]
w['C'] = list(reversed(zg))
w['stats'] = dict(w.get('stats', {}), entrance_helpers=sorted(h - 2 * v for h in range(2 * v, n) if w['start'][h] != ZERO))
data = gzip.compress(json.dumps(w, sort_keys=True, separators=(',', ':')).encode(), compresslevel=9, mtime=0)
data = data[:9] + bytes([255]) + data[10:]
open(out, 'wb').write(data)
print('written', out, 'A', len(w['A']), 'B', len(w['B']), 'C', len(w['C']), 'D', len(w['D']))

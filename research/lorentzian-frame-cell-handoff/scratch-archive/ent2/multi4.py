"""Sequential multi-helper entrance conversion by dual-set dirt injection.
At any time p of the raw word W0 = (A, scatter, B) the register values are a basis of the column space, so the pure dirt
column e_h equals the sum of the current values of a unique register set S_h(p) (S_h(0) = {h}; a gate d += srcs with
d in S toggles srcs in S).  S never contains a target (H1).  An inserted gate X = [F, g, sorted(S_h(p))] (g a z register,
g not in S) adds exactly e_h to g, hence alpha_g(p) to k_h, and changes nothing else in W0 except the e_h column.
Frames: F listed, F contains the current frames of g and of every member of S, and is contained in all their next frames;
F in {gc, gn} (g: no split).  Solve k_h = sum alpha (F2); insert all X of h (latest first); start[h] = E.
E = frame of h's first touch if it has a live-root isometry (rank 1, or rank 2 spanned by orthogonal live roots), else a
rank-1 line inside it with one.  At the end D is recomputed and C rebuilt as the literal reverse.
usage: multi3.py IN.json.gz OUT.json.gz [--max N] [--maxS K] [--order first|rev]"""
import gzip, json, sys
from collections import defaultdict
import numpy as np

args = sys.argv[1:]
inp, out = args[0], args[1]
MAXN = int(args[args.index('--max') + 1]) if '--max' in args else 10 ** 9
MAXS = int(args[args.index('--maxS') + 1]) if '--maxS' in args else 6
w = json.load(gzip.open(inp, 'rt'))
v, R = w['v'], w['R']; n = 2 * v + R
FR = [frozenset(f) for f in w['frames']]
L = w['lines']; Lm = np.array(L, dtype=float)
fd = [int(np.linalg.matrix_rank(Lm[sorted(f)])) if f else 0 for f in FR]
FULL = fd.index(8); ZERO = fd.index(0)
fm = [sum(1 << q for q in f) for f in FR]          # line masks (v <= 120 bits)
fm_lo = np.array([m & ((1 << 64) - 1) for m in fm], dtype=np.uint64)
fm_hi = np.array([m >> 64 for m in fm], dtype=np.uint64)
dot = lambda a, b: sum(x * y for x, y in zip(a, b))
is_y = lambda r: v <= r < 2 * v
line_frame = {next(iter(f)): k for k, f in enumerate(FR) if fd[k] == 1}
RET = set(w['ret'])


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
        lines = sorted(FR[F]); ok = False
        if fd[F] == 1: ok = ortho_frame(lines) is not None
        elif fd[F] == 2: ok = any(dot(L[a], L[b]) == 0 and ortho_frame([a, b]) for a in lines for b in lines if a < b)
        iso_ok[F] = ok
    return iso_ok[F]


def seq_of(w):
    return [tuple((g[0], g[1], tuple(g[2]))) for g in w['A']] + [None] + [tuple((g[0], g[1], tuple(g[2]))) for g in w['B']]


def analyse(w):
    seq = seq_of(w); T = len(seq)
    touch = defaultdict(list)
    for t, g in enumerate(seq):
        if g is None: continue
        for r in (g[1],) + g[2]: touch[r].append((t, g[0]))
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
        for s in g[2]:
            alpha[s] ^= alpha[g[1]]; hist[s].append((t, alpha[s]))
    # per register: frame segments: list of (start_time p0, end_time p1 inclusive range of insertion times p in [p0,p1],
    # cur frame, next frame, alpha in segment)
    segs = {}
    for r in range(n):
        if is_y(r): continue
        tl = list(touch[r]); out = []
        if r in RET:   # the scatter reads retained totals (COPY at the current frame): a segment break at NA
            NA_ = len(w['A']); fr_ = w['start'][r]
            for t_, f_ in tl:
                if t_ < NA_: fr_ = f_
            tl = sorted(tl + [(NA_, fr_)])
        prev_t = -1; cur = w['start'][r]
        for (t, f) in tl + [(T, FULL)]:
            # insertion times p with prev_t < p <= t  (X placed before seq[p]); p ranges over (prev_t, t]
            p0, p1 = prev_t + 1, min(t, T)
            if p0 <= p1:
                a = None
                for tt, aa in hist[r]:
                    if tt >= p0: a = aa
                    else: break
                out.append((p0, p1, cur, f, a))
            prev_t = t; cur = f
        segs[r] = out
    return seq, touch, segs, alpha


def frame_of(w, touch, r, p):
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


def round_(h, E):
    seq, touch, segs, alpha = analyse(w)
    k = alpha[h]
    if k == 0: return 'done'
    T = len(seq)
    S = {h}; Ss = [None] * (T + 1)
    for p in range(T + 1):
        Ss[p] = frozenset(S)
        if p < T and seq[p] is not None:
            f, d, srcs = seq[p]
            if d in S:
                for s_ in srcs: S ^= {s_}
    LBlo = np.zeros(T + 1, dtype=np.uint64); LBhi = np.zeros(T + 1, dtype=np.uint64)
    UBlo = np.zeros(T + 1, dtype=np.uint64); UBhi = np.zeros(T + 1, dtype=np.uint64); okS = np.zeros(T + 1, dtype=bool)
    curf = list(w['start']); ptr = defaultdict(int); nextf = {}
    for r in range(n):
        tl = touch[r]; nextf[r] = tl[0][1] if tl else FULL
    for p in range(T + 1):
        if p > 0 and seq[p - 1] is not None:
            f, d, srcs = seq[p - 1]
            for r in (d,) + srcs:
                curf[r] = f; ptr[r] += 1
                tl = touch[r]; nextf[r] = tl[ptr[r]][1] if ptr[r] < len(tl) else FULL
        Sp = Ss[p]
        if len(Sp) > MAXS: continue
        lb = 0; ub = (1 << 128) - 1
        for r in Sp:
            lb |= fm[curf[r]]; ub &= fm[nextf[r]]
        if lb & ~ub: continue
        okS[p] = True
        LBlo[p] = lb & ((1 << 64) - 1); LBhi[p] = lb >> 64; UBlo[p] = ub & ((1 << 64) - 1); UBhi[p] = (ub >> 64) & ((1 << 64) - 1)
    NA = len(w['A'])
    okS[NA] = False
    # epochs: maximal runs of p with identical (S, LB, UB) and okS
    ep_start = []; ep = []
    prevkey = None
    for p in range(T + 1):
        if not okS[p]:
            prevkey = None; continue
        key = (Ss[p], int(LBlo[p]), int(LBhi[p]), int(UBlo[p]), int(UBhi[p]))
        if key != prevkey:
            ep_start.append(p); ep.append([p, p, Ss[p], (int(LBhi[p]) << 64) | int(LBlo[p]), (int(UBhi[p]) << 64) | int(UBlo[p])])
            prevkey = key
        else: ep[-1][1] = p
    import bisect
    cands = []; seen = set()
    for g in range(n):
        if is_y(g): continue
        for (p0, p1, gc, gn, a) in segs[g]:
            if not a or a in seen: continue
            i = max(0, bisect.bisect_right(ep_start, p0) - 1)
            found = None
            while i < len(ep) and ep[i][0] <= p1:
                e0, e1, Se, lb, ub = ep[i]; i += 1
                if e1 < p0 or g in Se: continue
                lo = lb | fm[gc]; hi = ub & fm[gn]
                if lo & ~hi: continue
                lo_lo, lo_hi = np.uint64(lo & ((1 << 64) - 1)), np.uint64(lo >> 64)
                hi_lo, hi_hi = np.uint64(hi & ((1 << 64) - 1)), np.uint64((hi >> 64) & ((1 << 64) - 1))
                mk = ((fm_lo & ~hi_lo) == 0) & ((fm_hi & ~hi_hi) == 0) & ((lo_lo & ~fm_lo) == 0) & ((lo_hi & ~fm_hi) == 0)
                idx = np.nonzero(mk)[0]
                if len(idx):
                    F = int(min(idx, key=lambda j: fd[j]))
                    found = (a, g, max(p0, e0), F); break
            if found:
                seen.add(a); cands.append(found)
    sol = solve(k, [c[0] for c in cands])
    if sol is None: return None
    ins = [cands[i] for i in sol]
    for a, g, p, F in sorted(ins, key=lambda x: -x[2]):
        gate = [F, g, sorted(Ss[p])]
        if p <= NA: w['A'].insert(p, gate)
        else: w['B'].insert(p - NA - 1, gate)
    return [len(Ss[p]) for _, _, p, _ in ins]


done = []; skipped = defaultdict(list)
order = [h for h in range(2 * v, n) if w['start'][h] == ZERO]
if '--order' in args and args[args.index('--order') + 1] == 'rev': order = order[::-1]
for h in order:
    if len(done) >= MAXN: break
    seq = seq_of(w)
    th = [(t, g[0]) for t, g in enumerate(seq) if g is not None and (g[1] == h or h in g[2])]
    if not th: skipped['untouched'].append(h); continue
    t1, F1 = th[0]
    if fd[F1] == 0: skipped['first touch at frame 0'].append(h); continue
    if has_iso(F1): E = F1
    else:
        subs = [line_frame[q] for q in sorted(FR[F1]) if q in line_frame and has_iso(line_frame[q])]
        if not subs: skipped['no isometry frame'].append(h); continue
        E = subs[0]
    old_start = w['start'][h]; w['start'][h] = E
    saveA, saveB = [list(g) for g in w['A']], [list(g) for g in w['B']]
    total_ins = []; ok = False
    for rnd in range(6):
        res = round_(h, E)
        if res is None: break
        if res == 'done': ok = True; break
        total_ins += res
    if not ok:
        w['start'][h] = old_start; w['A'], w['B'] = saveA, saveB; skipped['not in span'].append(h)
        print('h %d: not converted' % h, flush=True); continue
    done.append((h, fd[E], len(total_ins)))
    print('h %d: E %d (dim %d, F1 dim %d) insertions %d (|S| %s); done %d' % (
        h, E, fd[E], fd[F1], len(total_ins), sorted(x for x in total_ins), len(done)), flush=True)

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
    for kq in row: val[v + t] ^= copies[kq]
run(w['B'])
D = []
for t in range(v):
    K = [r for r in range(2 * v, n) if val[v + t] >> r & 1]
    if K: D.append([ZERO, v + t, K])
dread = set(x for g in D for x in g[2])
bad = [h for h in range(2 * v, n) if w['start'][h] != ZERO and h in dread]
ent = sum(fd[w['start'][h]] for h in range(2 * v, n))
print('converted', len(done), 'entrance rank total', ent, 'insertions', sum(i for _, _, i in done), 'converted still in D (must be 0):', len(bad))
print('skipped', {kk: len(x) for kk, x in skipped.items()})
w['D'] = D
zg = [[FULL, g[1], list(g[2])] for sec in ('A', 'B') for g in w[sec] if not is_y(g[1])]
w['C'] = list(reversed(zg))
w['stats'] = dict(w.get('stats', {}), entrance_helpers=sorted(h - 2 * v for h in range(2 * v, n) if w['start'][h] != ZERO))
data = gzip.compress(json.dumps(w, sort_keys=True, separators=(',', ':')).encode(), compresslevel=9, mtime=0)
data = data[:9] + bytes([255]) + data[10:]
open(out, 'wb').write(data)
print('written', out, 'A', len(w['A']), 'B', len(w['B']), 'C', len(w['C']), 'D', len(w['D']))

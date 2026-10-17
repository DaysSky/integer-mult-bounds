"""Sequential entrance conversion with rescheduled A (touch-DAG topological re-sort), regime S = {p} u Src.
For pivot p: E = frame of p's first touch.  For each segment j of p (p has read only sources so far; value d + sum Src_j),
an injection X = [F, g, sorted({p} u Src_j)] adds exactly e_p to g (g a helper, g not in S).  X needs, in the touch DAG of A:
preds {g_k, p_j, x_i (x in Src)}, succs {g_{k+1}, p_{j+1}, x_{i+1}}, frames nested at F for all, and no cycle.
Solve k_p = sum alpha_g (F2); insert all X of p; stable Kahn re-sort of A; exact forward replay must give k_p = 0
and keep every earlier pivot's column zero; otherwise revert.
usage: multi5.py IN OUT [--pivots a,b,c | --all] [--sources-as-g]"""
import gzip, json, sys, heapq, copy
from collections import defaultdict
import numpy as np

args = sys.argv[1:]
inp, out = args[0], args[1]
SRCG = '--sources-as-g' in args
w = json.load(gzip.open(inp, 'rt'))
v, R = w['v'], w['R']; n = 2 * v + R
FR = [frozenset(f) for f in w['frames']]
L = w['lines']; Lm = np.array(L, dtype=float)
fd = [int(np.linalg.matrix_rank(Lm[sorted(f)])) if f else 0 for f in FR]
FULL = fd.index(8); ZERO = fd.index(0)
RET = set(w['ret'])
is_y = lambda r: v <= r < 2 * v
dot = lambda a, b: sum(x * y for x, y in zip(a, b))
sub = lambda a, b: FR[a] <= FR[b]


def ortho_frame(base):
    def rec(cur, cands):
        if len(cur) == 8: return cur
        for k, c in enumerate(cands):
            r = rec(cur + [c], [d for d in cands[k + 1:] if dot(L[c], L[d]) == 0])
            if r: return r
        return None
    if any(dot(L[a], L[b]) for a in base for b in base if a != b): return None
    return rec(list(base), [i for i in range(len(L)) if i not in base and all(dot(L[i], L[b]) == 0 for b in base)])


def has_iso(F):
    lines = sorted(FR[F])
    if fd[F] == 1: return ortho_frame(lines) is not None
    if fd[F] == 2: return any(dot(L[a], L[b]) == 0 and ortho_frame([a, b]) for a in lines for b in lines if a < b)
    return False


def seq_of(w):
    return [tuple((g[0], g[1], tuple(g[2]))) for g in w['A']] + [None] + [tuple((g[0], g[1], tuple(g[2]))) for g in w['B']]


def raw_values(w):
    val = [1 << r for r in range(n)]
    for g in seq_of(w):
        if g is None:
            cop = [val[q] for q in w['ret']]
            for tt, row in enumerate(w['scatter']):
                for k in row: val[v + tt] ^= cop[k]
            continue
        f, d, srcs = g; a = 0
        for s in srcs: a ^= val[s]
        val[d] ^= a
    return val


def kcol(val, h):
    return sum(1 << t for t in range(v) if val[v + t] >> h & 1)


def analyse(w):
    seq = seq_of(w); T = len(seq); NA = len(w['A'])
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
    def alpha_at(r, p):
        best = None
        for tt, a in hist[r]:
            if tt >= p: best = a
            else: break
        return best
    succ = [set() for _ in range(NA)]
    for r, tl in touch.items():
        ta = [t for t, _ in tl if t < NA]
        for a_, b_ in zip(ta, ta[1:]): succ[a_].add(b_)
    desc = [0] * NA
    for t in range(NA - 1, -1, -1):
        d = 1 << t
        for s_ in succ[t]: d |= desc[s_]
        desc[t] = d
    return seq, touch, alpha, alpha_at, succ, desc, NA


def positions(w, touch, r):
    """(prev touch time or None, next touch time or None, cur frame, next frame); scatter splits ret registers"""
    NA = len(w['A'])
    tl = list(touch[r])
    if r in RET:
        fr_ = w['start'][r]
        for t_, f_ in tl:
            if t_ < NA: fr_ = f_
        tl = sorted(tl + [(NA, fr_)])
    out = []; prev = None; cur = w['start'][r]
    for t, f in tl + [(None, FULL)]:
        out.append((prev, t, cur, f))
        if t is None: break
        prev = t; cur = f
    return out


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


def try_pivot(w, p, E):
    seq, touch, alpha, alpha_at, succ, desc, NA = analyse(w)
    reach = lambda a, b: a is not None and b is not None and a < NA and b < NA and (desc[a] >> b) & 1
    k = alpha[p]
    if k == 0: return []
    th = touch[p]
    POS = {r: positions(w, touch, r) for r in range(n) if not is_y(r)}
    cands = {}; Src = set()
    for j in range(-1, len(th)):
        if j >= 0:
            t, f = th[j]
            if t >= NA: break
            g_ = seq[t]
            if g_[1] == p:
                if any(s >= v for s in g_[2]): break
                for s in g_[2]: Src ^= {s}
            pc, pj = f, t
        else: pc, pj = E, None
        if j + 1 >= len(th) or th[j + 1][0] >= NA: break
        pn, pq = th[j + 1][1], th[j + 1][0]
        S = {p} | Src
        for F in range(len(FR)):
            if not (FR[pc] <= FR[F] <= FR[pn]): continue
            spos = {}
            for x in Src:
                ps = [(a, b) for (a, b, c, d) in POS[x] if FR[c] <= FR[F] <= FR[d] and not reach(pq, a) and not reach(b, pj)
                      and (a is None or a < NA)]
                if not ps: spos = None; break
                spos[x] = ps
            if spos is None: continue
            for g in range(n):
                if is_y(g) or g in S or (g < v and not SRCG): continue
                for (gk, gn_t, gc, gn) in POS[g]:
                    if gk is not None and gk >= NA: break
                    if not (FR[gc] <= FR[F] <= FR[gn]): continue
                    if reach(pq, gk) or reach(gn_t, pj): continue
                    a = alpha_at(g, gk + 1 if gk is not None else 0)
                    if not a or a in cands: continue
                    choice = {}
                    for x, ps in spos.items():
                        c_ = next(((a_, b_) for a_, b_ in ps if not reach(gn_t, a_) and not reach(b_, gk)), None)
                        if c_ is None: choice = None; break
                        choice[x] = c_
                    if choice is None: continue
                    cands[a] = (g, gk, gn_t, j, pj, pq, F, frozenset(S), choice)
    keys = list(cands)
    sol = solve(k, keys)
    if sol is None: return None
    return [cands[keys[i]] for i in sol], NA, succ


def apply(w, p, ins, NA, succ0):
    A = w['A']
    succ = defaultdict(set)
    for a_ in range(NA):
        for b_ in succ0[a_]: succ[a_].add(b_)
    gate_of = {}
    for i, (g, gk, gn_t, j, pj, pq, F, S, choice) in enumerate(ins):
        x = NA + i; gate_of[x] = [F, g, sorted(S)]
        preds = [gk, pj] + [c[0] for c in choice.values()]
        succs = [gn_t, pq] + [c[1] for c in choice.values()]
        for q in preds:
            if q is not None and q < NA: succ[q].add(x)
        for q in succs:
            if q is not None and q < NA: succ[x].add(q)
    nodes = list(range(NA + len(ins)))
    indeg = defaultdict(int)
    for a_ in list(succ):
        for b_ in succ[a_]: indeg[b_] += 1
    pri = {i: (i, 0) for i in range(NA)}
    for i, c in enumerate(ins):
        s_ = [t for t in [c[2], c[5]] + [cc[1] for cc in c[8].values()] if t is not None and t < NA]
        pri[NA + i] = (min(s_) if s_ else NA, -1)
    heap = [(pri[x], x) for x in nodes if indeg[x] == 0]; heapq.heapify(heap); order = []
    while heap:
        _, x = heapq.heappop(heap); order.append(x)
        for s_ in succ[x]:
            indeg[s_] -= 1
            if indeg[s_] == 0: heapq.heappush(heap, (pri[s_], s_))
    if len(order) != len(nodes): return False
    w['A'] = [list(gate_of[x]) if x >= NA else A[x] for x in order]
    return True


pivots = None
if '--pivots' in args: pivots = [int(x) for x in args[args.index('--pivots') + 1].split(',')]
else: pivots = [h for h in range(2 * v, n) if w['start'][h] == ZERO]
done = []
for p in pivots:
    if w['start'][p] != ZERO: continue
    seq = seq_of(w)
    th = [(t, g[0]) for t, g in enumerate(seq) if g is not None and (g[1] == p or p in g[2])]
    E = th[0][1]
    if fd[E] == 0 or not has_iso(E): print('p %d: no usable entrance' % p); continue
    saved = copy.deepcopy(w)
    w['start'][p] = E
    ok = False
    for rnd in range(4):
        r = try_pivot(w, p, E)
        if r == []: ok = True; break
        if r is None: break
        ins, NA, succ0 = r
        if not apply(w, p, ins, NA, succ0): print('p %d: cycle' % p); break
    if ok:
        val = raw_values(w)
        bad = [q for q in [p] + [d_[0] for d_ in done] if kcol(val, q)]
        if bad: ok = False; print('p %d: replay shows nonzero columns %s' % (p, bad))
    if not ok:
        w.clear(); w.update(saved); print('p %d: not converted' % p, flush=True); continue
    nins = len(w['A']) - len(saved['A'])
    done.append((p, fd[E], nins))
    print('p %d CONVERTED: E %d dim %d, inserted %d gates; total converted %d' % (p, E, fd[E], nins, len(done)), flush=True)

val = raw_values(w)
D = []
for t in range(v):
    K = [r for r in range(2 * v, n) if val[v + t] >> r & 1]
    if K: D.append([ZERO, v + t, K])
dread = set(x for g in D for x in g[2])
bad = [h for h in range(2 * v, n) if w['start'][h] != ZERO and h in dread]
print('converted', len(done), [d_[0] for d_ in done], 'entrance rank total', sum(fd[w['start'][h]] for h in range(2 * v, n)), 'bad', bad)
w['D'] = D
FULLf = FULL
zg = [[FULLf, g[1], list(g[2])] for sec in ('A', 'B') for g in w[sec] if not is_y(g[1])]
w['C'] = list(reversed(zg))
w['stats'] = dict(w.get('stats', {}), entrance_helpers=sorted(h - 2 * v for h in range(2 * v, n) if w['start'][h] != ZERO))
data = gzip.compress(json.dumps(w, sort_keys=True, separators=(',', ':')).encode(), compresslevel=9, mtime=0)
data = data[:9] + bytes([255]) + data[10:]
open(out, 'wb').write(data)
print('written', out, 'A', len(w['A']), 'B', len(w['B']), 'C', len(w['C']), 'D', len(w['D']))

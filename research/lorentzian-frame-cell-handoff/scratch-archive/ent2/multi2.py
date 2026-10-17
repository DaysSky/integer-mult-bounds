"""Sequential multi-helper entrance conversion with A-section rescheduling.
A schedule of A is any topological order of the touch DAG (consecutive A-touches of every register are chained), so
every register keeps its own touch sequence (frames, values per register unchanged; the raw map is invariant).
For helper h (start 0, first A write w_h): E = frame of h's first touch (or a rank-1 line inside it with a live-root
isometry).  Candidate inserted gate X = [F, g, [h]] between g's touches k, k+1 and h's touches j, j+1 (j+1 <= w_h), with
F listed, hc,gc <= F <= hn,gn, acyclic iff no path h_{j+1} -> g_k and none g_{k+1} -> h_j.  X adds alpha_g(after g_k)
to k_h (h pure dirt at X).  Solve k_h = sum over F2; insert; stable topological re-sort of A; start[h] = E.
usage: multi2.py IN.json.gz OUT.json.gz [--max N] [--nosplit] [--no-sources] [--prefer-j0]"""
import gzip, json, sys, heapq
from collections import defaultdict
import numpy as np

args = sys.argv[1:]
inp, out = args[0], args[1]
MAXN = int(args[args.index('--max') + 1]) if '--max' in args else 10 ** 9
NOSPLIT = '--nosplit' in args; NOSRC = '--no-sources' in args
w = json.load(gzip.open(inp, 'rt'))
v, R = w['v'], w['R']; n = 2 * v + R
FR = [frozenset(f) for f in w['frames']]
L = w['lines']; Lm = np.array(L, dtype=float)
fd = [int(np.linalg.matrix_rank(Lm[sorted(f)])) if f else 0 for f in FR]
FULL = fd.index(8); ZERO = fd.index(0)
sub = lambda a, b: FR[a] <= FR[b]
dot = lambda a, b: sum(x * y for x, y in zip(a, b))
is_y = lambda r: v <= r < 2 * v
line_frame = {next(iter(f)): k for k, f in enumerate(FR) if fd[k] == 1}


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
        elif fd[F] == 2:
            ok = any(dot(L[a], L[b]) == 0 and ortho_frame([a, b]) for a in lines for b in lines if a < b)
        iso_ok[F] = ok
    return iso_ok[F]


def analyse(w):
    A = w['A']; NA = len(A)
    seq = [tuple((g[0], g[1], tuple(g[2]))) for g in A] + [None] + [tuple((g[0], g[1], tuple(g[2]))) for g in w['B']]
    T = len(seq)
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
    # DAG on A: successor lists by register chains; descendants bitsets
    succ = [set() for _ in range(NA)]
    for r, tl in touch.items():
        ta = [t for t, _ in tl if t < NA]
        for a, b in zip(ta, ta[1:]): succ[a].add(b)
    desc = [0] * NA
    for t in range(NA - 1, -1, -1):
        d = 1 << t
        for s in succ[t]: d |= desc[s]
        desc[t] = d
    return seq, touch, hist, alpha, desc, NA


def alpha_after(hist, r, t):
    """alpha_r just after raw time t (i.e. before t+1); t = -1 -> at time 0"""
    p = t + 1; best = None
    for tt, a in hist[r]:
        if tt >= p: best = a
        else: break
    return best


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


def topo(NA, succ_extra, nodes):
    """stable Kahn order over A gates (indices 0..NA-1) plus extra nodes; returns list of node ids"""
    pass


done = []; skipped = defaultdict(list)
order = [h for h in range(2 * v, n) if w['start'][h] == ZERO]
for h in order:
    if len(done) >= MAXN: break
    seq, touch, hist, alpha, desc, NA = analyse(w)
    th = touch[h]
    if not th or th[0][0] >= NA: skipped['no A touch'].append(h); continue
    t1, F1 = th[0]
    if fd[F1] == 0: skipped['first touch at frame 0'].append(h); continue
    if has_iso(F1): E = F1
    else:
        subs = [line_frame[q] for q in sorted(FR[F1]) if q in line_frame and has_iso(line_frame[q])]
        if not subs: skipped['no isometry frame'].append(h); continue
        E = subs[0]
    k = alpha[h]
    # h's touches up to its first write
    wi = next((i for i, (t, f) in enumerate(th) if seq[t][1] == h), len(th))
    if wi < len(th) and th[wi][0] >= NA: wi_a = None
    hslots = []   # (j, hj_time or None, hn_time, hc, hn)
    for j in range(-1, wi):
        if j + 1 >= len(th) or th[j + 1][0] >= NA: break
        hc = E if j == -1 else th[j][1]
        hn = th[j + 1][1]
        hslots.append((j, th[j][0] if j >= 0 else None, th[j + 1][0], hc, hn))
    ins = []
    if k:
        cands = []
        for g in range(n):
            if g == h or is_y(g) or (NOSRC and g < v): continue
            tg = touch[g]
            ga = [(t, f) for t, f in tg if t < NA]
            for kk in range(-1, len(ga)):
                gk_t = ga[kk][0] if kk >= 0 else None
                gc = ga[kk][1] if kk >= 0 else w['start'][g]
                if kk + 1 < len(tg):
                    nxt = tg[kk + 1]
                    gn = nxt[1]; gn_t = nxt[0] if nxt[0] < NA else None
                else: gn = FULL; gn_t = None
                a = alpha_after(hist, g, gk_t if gk_t is not None else -1)
                if not a: continue
                for (j, hj_t, hn_t, hc, hn) in hslots:
                    if gk_t is not None and desc[hn_t] >> gk_t & 1: continue
                    if hj_t is not None and gn_t is not None and desc[gn_t] >> hj_t & 1: continue
                    if gk_t is not None and gk_t == hn_t: continue
                    opts = [F for F in (hc, hn) if F in (gc, gn)] if NOSPLIT else [hc, hn, gc, gn]
                    F = next((F for F in opts if sub(hc, F) and sub(gc, F) and sub(F, hn) and sub(F, gn)), None)
                    if F is None: continue
                    cands.append((a, g, kk, gk_t, gn_t, j, hj_t, hn_t, F))
                    break
        # dedupe identical alpha vectors (keep first)
        seen = set(); cu = []
        for c in cands:
            if c[0] in seen: continue
            seen.add(c[0]); cu.append(c)
        sol = solve(k, [c[0] for c in cu])
        if sol is None: skipped['not in span'].append(h); continue
        ins = [cu[i] for i in sol]
    # build new A order: nodes 0..NA-1 plus extra X nodes NA.. ; edges: chains + X edges
    A = w['A']
    nodes = list(range(NA)) + [NA + i for i in range(len(ins))]
    succ = defaultdict(set); indeg = defaultdict(int)
    for r, tl in touch.items():
        ta = [t for t, _ in tl if t < NA]
        for a_, b_ in zip(ta, ta[1:]): succ[a_].add(b_)
    gate_of = {i: A[i] for i in range(NA)}
    for i, c in enumerate(ins):
        _, g, kk, gk_t, gn_t, j, hj_t, hn_t, F = c
        x = NA + i; gate_of[x] = [F, g, [h]]
        for p_ in (gk_t, hj_t):
            if p_ is not None: succ[p_].add(x)
        for s_ in (gn_t, hn_t):
            if s_ is not None: succ[x].add(s_)
    for a_ in list(succ):
        for b_ in succ[a_]: indeg[b_] += 1
    # priority: original position; X nodes just before their earliest successor
    pri = {i: (i, 0) for i in range(NA)}
    for i, c in enumerate(ins):
        x = NA + i; s_ = [t for t in (c[4], c[7]) if t is not None]
        pri[x] = (min(s_) if s_ else NA, -1)
    heap = [(pri[x], x) for x in nodes if indeg[x] == 0]; heapq.heapify(heap); neworder = []
    while heap:
        _, x = heapq.heappop(heap); neworder.append(x)
        for s_ in succ[x]:
            indeg[s_] -= 1
            if indeg[s_] == 0: heapq.heappush(heap, (pri[s_], s_))
    if len(neworder) != len(nodes): skipped['cycle'].append(h); continue
    w['A'] = [list(gate_of[x]) if x >= NA else A[x] for x in neworder]
    w['start'][h] = E
    moved = sum(1 for i, x in enumerate([y for y in neworder if y < NA]) if x != i)
    done.append((h, fd[E], len(ins)))
    print('h %d: E %d (dim %d, F1 dim %d) insertions %d (splits %d), A gates reordered %d; done %d' % (
        h, E, fd[E], fd[F1], len(ins), 0, moved, len(done)), flush=True)

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

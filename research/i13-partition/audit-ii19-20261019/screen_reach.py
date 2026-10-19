"""Slow-reach screen (2026-10-19).  For each line system: valid decoder bounds, reach retention, frame
sharing capacity, and the price it would get with a frontier-quality middle.

Decoder (flow-level definition, HANDOFF 1068): B_tt = 1, B_ts = 0 on non-orthogonal pairs, free otherwise.
  x_ub: exact minimum-cost star decoder for the B0 completion (B0_ts = 1 iff s = t or s _|_ t): the
        cost-ordered greedy basis of rowspace(B0) over F2 (exact for this matroid), frame cost = span dim +
        radical dim, enumerated when rank(B0) <= MAXRANK; otherwise the rref basis cost (an upper bound).
  x_lb: |S| / v for a pairwise non-orthogonal set S (B|SxS = I forces rank >= |S|; valid but weak).
Reach (proxy, line-spanned frames as a sharing middle uses them):
  r2: for each line s, max over lines u with <s,u> nondegenerate of |perp(s) & perp(u)| / |perp(s)|.
  cap: best (lines in F) x (targets _|_ F) over line-spanned frames F found by a small beam search.
Lifts: core (+) one special line of norm -2 orthogonal to everything (the 121 construction) is
  Lorentzian, adds 1 to v, h and cst (orthogonal-sum decoder), and keeps every core line's reach.
Price: the r434 frontier's climb shape transplanted to (v, h, cst, R = 3.91 v) -- a model, not a word."""
import itertools, json, os, random, sys, time
from fractions import Fraction as Fr
import numpy as np
from _common import FRONTIER, R434, COPY_R434, transplant, pct, I13

MAXRANK = 14
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

# ---------------------------------------------------------------- systems (integer coordinates, integer forms)
def e8_roots2():
    """2 x E8 roots in the even coordinate system (integer coordinates; form I8; norms 8)."""
    out = []
    for i, j in itertools.combinations(range(8), 2):
        for si, sj in itertools.product((2, -2), repeat=2):
            v = [0] * 8; v[i] = si; v[j] = sj; out.append(v)
    for s in itertools.product((1, -1), repeat=8):
        if s.count(-1) % 2 == 0: out.append(list(s))
    return out
def e8_norm4_2():
    """2 x E8 vectors of norm 4 (integer coordinates; form I8; norms 16): 2160 vectors."""
    out = []
    for idx in itertools.combinations(range(8), 4):
        for s in itertools.product((2, -2), repeat=4):
            v = [0] * 8
            for k, x in zip(idx, s): v[k] = x
            out.append(v)
    for i in range(8):
        for s in (4, -4):
            v = [0] * 8; v[i] = s; out.append(v)
    for i in range(8):
        for s in itertools.product((1, -1), repeat=8):
            v = list(s); v[i] *= 3
            if sum(v) % 4 == 0: out.append(v)          # half-integer coset: (sum of halves) even
    assert len(out) == 2160, len(out)
    return out
def lines_of(vecs):
    seen, out = set(), []
    for v in vecs:
        t = tuple(v); n = tuple(-x for x in v)
        if t in seen or n in seen: continue
        seen.add(t); out.append(list(v))
    return out
def D(n):
    out = []
    for i, j in itertools.combinations(range(n), 2):
        out += [[1 if k in (i, j) else 0 for k in range(n)], [1 if k == i else (-1 if k == j else 0) for k in range(n)]]
    return out, np.eye(n, dtype=np.int64)
def A(n):   # A_n roots e_i - e_j in R^{n+1}, projected to the n-dim sum-zero space via a basis
    pts = [[1 if k == i else (-1 if k == j else 0) for k in range(n + 1)] for i, j in itertools.combinations(range(n + 1), 2)]
    B = np.array([[1 if k == i else (-1 if k == i + 1 else 0) for k in range(n + 1)] for i in range(n)])   # simple roots
    # coordinates of each root in the simple-root basis (integers); form = Cartan matrix
    M = B.astype(float); coords = [list(np.rint(np.linalg.lstsq(M.T, np.array(p, float), rcond=None)[0]).astype(int)) for p in pts]
    C = (B @ B.T).astype(np.int64)
    return coords, C
def sub_e8(pred):
    L = lines_of(e8_roots2()); return [l for l in L if pred(l)], np.eye(8, dtype=np.int64)
def p111():
    w = json.load(open(os.path.join(I13, 'ii19_pub2_p111-r434.json')))
    return w['lines'], np.array(w['form']['num'], dtype=np.int64)
def lorentz_e8m2(levels):
    """E8 (+) <-2>, scaled by 2: vectors (2a, 2n), form diag(1^8, -2).  Norm-2 lines at |n| in levels."""
    out = []
    if 0 in levels: out += [l + [0] for l in lines_of(e8_roots2())]
    if 1 in levels: out += [v + [2] for v in e8_norm4_2()]                       # (a, 1), a.a = 4
    F = np.diag([1] * 8 + [-2]).astype(np.int64); return out, F
def lorentz_ii19(full):
    """E8 (+) U scaled by 2: (2a, 2x, 2y), form I8 (+) [[0,1],[1,0]].  Norm-2 lines with (x,y) small."""
    R = lines_of(e8_roots2()); allR = e8_roots2()
    out = [l + [0, 0] for l in R] + [v + [2, 0] for v in allR] + [v + [0, 2] for v in allR] + [[0] * 8 + [2, 2]]
    if full: out += [v + [2, -2] for v in e8_norm4_2()]                           # (a, 1, -1), a.a = 4
    F = np.zeros((10, 10), dtype=np.int64); F[:8, :8] = np.eye(8, dtype=np.int64); F[8, 9] = F[9, 8] = 1
    return out, F

SYSTEMS = []   # (name, builder, family note)
SYSTEMS.append(('E8', lambda: (lines_of(e8_roots2()), np.eye(8, dtype=np.int64)), 'pos-def core (frontier family)'))
SYSTEMS.append(('P111 (r434 lines)', p111, 'pos-def core (frontier)'))
SYSTEMS.append(('E7 (in E8)', lambda: sub_e8(lambda l: l[0] == l[1]), 'pos-def core; lift is h=8 Lorentzian in II_{1,9}'))
SYSTEMS.append(('E6 (in E8)', lambda: sub_e8(lambda l: l[0] == l[1] == l[2]), 'pos-def core'))
SYSTEMS.append(('D8 (in E8)', lambda: sub_e8(lambda l: abs(l[0]) in (0, 2) and all(abs(x) in (0, 2) for x in l)), 'pos-def core'))
SYSTEMS.append(('D7 (in E8)', lambda: sub_e8(lambda l: all(abs(x) in (0, 2) for x in l) and l[7] == 0), 'pos-def core; lift h=8'))
SYSTEMS.append(('A8', lambda: A(8), 'pos-def core'))
SYSTEMS.append(('A7', lambda: A(7), 'pos-def core; lift h=8'))
SYSTEMS.append(('D4+D4 (in E8)', lambda: sub_e8(lambda l: all(abs(x) in (0, 2) for x in l) and
                                                ((l[4:] == [0] * 4) or (l[:4] == [0] * 4))), 'pos-def core'))
def d8_plus_half(k, seed):
    L = lines_of(e8_roots2()); d8 = [l for l in L if all(abs(x) in (0, 2) for x in l)]
    half = [l for l in L if all(abs(x) == 1 for x in l)]
    return d8 + random.Random(seed).sample(half, k), np.eye(8, dtype=np.int64)
for k in (4, 8, 16, 32, 48):
    SYSTEMS.append(('D8+%d half-roots' % k, (lambda k=k: d8_plus_half(k, 7)), 'pos-def core, D8->E8 interpolation'))
for n in (9, 10, 12):
    SYSTEMS.append(('D%d' % n, (lambda n=n: D(n)), 'pos-def core (slow reach, twins)'))
SYSTEMS.append(('E8+<-2> levels 0,1', lambda: lorentz_e8m2({0, 1}), 'native Lorentzian, h=9, in II_{1,9}'))
SYSTEMS.append(('E8+<-2> level 1 only', lambda: lorentz_e8m2({1}), 'native Lorentzian, h=9, in II_{1,9}'))
SYSTEMS.append(('II_{1,9} levels 0-1 (601)', lambda: lorentz_ii19(False), 'native Lorentzian, h=10'))
SYSTEMS.append(('II_{1,9} incl (a,1,-1) (2761)', lambda: lorentz_ii19(True), 'native Lorentzian, h=10'))

# ---------------------------------------------------------------- exact linear algebra helpers
def rank_q(vecs):
    m = [[Fr(x) for x in r] for r in vecs]; rk = 0; n = len(m[0]) if m else 0
    for c in range(n):
        p = next((i for i in range(rk, len(m)) if m[i][c] != 0), None)
        if p is None: continue
        m[rk], m[p] = m[p], m[rk]
        for i in range(len(m)):
            if i != rk and m[i][c] != 0:
                f = m[i][c] / m[rk][c]; m[i] = [a - f * b for a, b in zip(m[i], m[rk])]
        rk += 1
    return rk, m[:rk]
def frame_cost(vecs, F):
    """smallest nondegenerate subspace containing the lines: span dim + radical dim
    = 2 rank(V) - rank(V F V^T), evaluated on an SVD basis of the span (small integer vectors)."""
    V = np.asarray(vecs, dtype=float)
    if V.size == 0: return 0
    U, S, Wt = np.linalg.svd(V, full_matrices=False)
    r = int((S > 1e-9 * max(1.0, S[0])).sum())
    if r == 0: return 0
    Rm = np.diag(S[:r]) @ Wt[:r]
    K = Rm @ np.asarray(F, dtype=float) @ Rm.T
    sk = np.linalg.svd(K, compute_uv=False)
    rk = int((sk > 1e-9 * max(1.0, sk[0])).sum())
    return 2 * r - rk
def gf2_basis(rows, nbits):
    piv = {}
    for r in rows:
        x = r
        while x:
            p = x.bit_length() - 1
            if p in piv: x ^= piv[p]
            else: piv[p] = x; break
    return list(piv.values())

# ---------------------------------------------------------------- per-system analysis
def analyze(name, Lraw, F):
    L = np.array(Lraw, dtype=np.int64); F = np.array(F, dtype=np.int64); v, h = L.shape
    G = L @ F @ L.T
    assert np.all(np.diag(G) != 0), 'null line'
    orth = (G == 0); np.fill_diagonal(orth, False)
    perp = [int(''.join('1' if orth[s, t] else '0' for t in range(v))[::-1], 2) for s in range(v)]
    psz = np.array([bin(p).count('1') for p in perp])
    span = int(np.linalg.matrix_rank(L.astype(float))); h = span
    # --- decoder upper bound: min-cost basis of rowspace(B0)
    B0 = [perp[s] | (1 << s) for s in range(v)]
    basis = gf2_basis(B0, v); rk = len(basis)
    Fl = F.tolist(); lines = L.tolist()
    def cost_of(mask):
        sup = [i for i in range(v) if (mask >> i) & 1]
        return frame_cost([lines[i] for i in sup], Fl)
    if rk <= MAXRANK:
        cws = [0]
        for b in basis: cws = cws + [c ^ b for c in cws]
        costed = sorted((cost_of(c), c) for c in cws if c)
        chosen, piv = [], {}
        for cst_c, c in costed:
            x = c
            while x:
                p = x.bit_length() - 1
                if p in piv: x ^= piv[p]
                else: piv[p] = x; chosen.append(cst_c); break
            if len(chosen) == rk: break
        cst_ub, how = sum(chosen), 'exact-B0'
        copies = {}
        for c in chosen: copies[c] = copies.get(c, 0) + 1
    else:
        costs = [cost_of(b) for b in basis]
        cst_ub, how = sum(costs), 'rref-UB'
        copies = {}
        for c in costs: copies[c] = copies.get(c, 0) + 1
    # --- decoder lower bound: pairwise non-orthogonal set (randomized greedy)
    rnd = random.Random(1); nonorth = ~orth; np.fill_diagonal(nonorth, True); best = 0
    for _ in range(300 if v <= 400 else 40):
        order = list(range(v)); rnd.shuffle(order); cand = np.ones(v, dtype=bool); n = 0
        for x in order:
            if cand[x]: n += 1; cand &= nonorth[x]
        best = max(best, n)
    # --- reach retention r2 over nondegenerate line pairs
    nd = (np.outer(np.diag(G), np.diag(G)) - G * G) != 0; np.fill_diagonal(nd, False)
    O = orth.astype(np.float32); M = O @ O; M[~nd] = -1
    r2 = np.where(psz > 0, M.max(axis=1) / np.maximum(psz, 1), 0.0)
    # --- sharing capacity: beam over line-spanned frames up to dim h-1 (small systems only)
    cap, capdim = None, None
    if v <= 400:
        best_cap = (0, 0)
        def audience(idx):
            m = (1 << v) - 1
            for i in idx: m &= perp[i]
            return bin(m).count('1')
        seeds = random.Random(2).sample(range(v), min(v, 25))
        for s0 in seeds:
            beam = [((s0,), None)]
            for d in range(2, h):
                nxt = []
                for idx, _ in beam:
                    for u in random.Random(d * 7 + s0).sample(range(v), min(v, 40)):
                        if u in idx: continue
                        cand = idx + (u,)
                        if np.linalg.matrix_rank(L[list(cand)].astype(float)) != len(cand): continue
                        aud = audience(cand)
                        nxt.append((aud, cand))
                nxt.sort(reverse=True)
                beam = [(c, None) for a, c in nxt[:4]]
                for idx, _ in beam:
                    # lines inside span(idx)
                    Bm = L[list(idx)].astype(float); P = Bm.T @ np.linalg.pinv(Bm @ Bm.T) @ Bm
                    res = np.linalg.norm(L - L @ P, axis=1)
                    val = int((res < 1e-7).sum()) * audience(idx)
                    if val > best_cap[0]: best_cap = (val, len(idx))
        cap, capdim = best_cap
    if cst_ub >= v: cst_ub, how, copies = v, 'trivial', {1: v}
    # relay proxy: targets of s lost at its best 2-frame, and the greedy number of extra 2-frames through s
    # (each = one register whose dim-1 frame is <s>) needed to keep them in reach
    lost_tot, relays = 0, 0
    if v <= 2400:
        for s in range(v):
            cand = np.nonzero(nd[s])[0]
            if not len(cand) or psz[s] == 0: continue
            ubest = int(cand[np.argmax(M[s, cand])])
            lost = perp[s] & ~perp[ubest]; lost_tot += bin(lost).count('1')
            while lost:
                gains = [(bin(lost & perp[u]).count('1'), u) for u in cand]
                g, u = max(gains)
                if g == 0: relays += bin(lost).count('1'); break
                relays += 1; lost &= ~perp[u]
    return dict(name=name, v=v, h=h, span=int(span), lost_per_line=lost_tot / v, relays_per_line=relays / v, perp_mean=float(psz.mean()), perp_min=int(psz.min()),
                rankB0=rk, cst_ub=cst_ub, how=how, copies=copies, x_ub=cst_ub / v, x_lb=best / v,
                r2_mean=float(r2.mean()), r2_min=float(r2.min()), cap=cap, capdim=capdim,
                demand_per_cap=(float(psz.sum()) / cap) if cap else None)

def frontier_quality_price(v, h, cst, copies):
    R = int(round(3.91 * v))
    if R > 4 * v: R = 4 * v
    cop = dict(copies) if copies else {h - 1: cst // (h - 1)}
    p, c = pct(transplant(R434, COPY_R434, v, h, R, cop), v, h, R)
    return p

if __name__ == '__main__':
    only = sys.argv[1:]
    rows = []
    for name, build, note in SYSTEMS:
        if only and not any(o in name for o in only): continue
        Lraw, F = build()
        log('building %s: %d lines' % (name, len(Lraw)))
        r = analyze(name, Lraw, F); r['note'] = note
        r['price_core'] = frontier_quality_price(r['v'], r['h'], r['cst_ub'], r['copies']) if r['x_ub'] < 8 / 9 else None
        lift_cop = dict(r['copies']); lift_cop[1] = lift_cop.get(1, 0) + 1
        r['price_lift'] = (frontier_quality_price(r['v'] + 1, r['h'] + 1, r['cst_ub'] + 1, lift_cop)
                           if (r['cst_ub'] + 1) / (r['v'] + 1) < 8 / 9 and 'native' not in note else None)
        rows.append(r)
        log('  v=%d h=%d perp %.1f | rank(B0) %d cst<=%d (%s) x in [%.3f, %.3f] | r2 %.3f (min %.3f) | cap %s@%s | lost %.1f relays %.2f | '
            'price core %s lift %s' % (r['v'], r['h'], r['perp_mean'], r['rankB0'], r['cst_ub'], r['how'], r['x_lb'],
                                        r['x_ub'], r['r2_mean'], r['r2_min'], r["cap"], r["capdim"], r["lost_per_line"], r["relays_per_line"],
                                        r['price_core'], r['price_lift']))
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'screen_reach_results.json')
    if not only:
        json.dump(rows, open(out, 'w'), indent=1, default=str)
        log('wrote', out)

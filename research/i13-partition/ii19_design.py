"""II19 coordinated full-361 stall-tail design: bulk rank-6 flat-totals + small-flat tails,
reuse-coordinated across all 361 targets.  Output: the full ledger (Sigma c_t, distinct
flats, content, projected R) vs the 15v budget.  RAM-safe (ints; ~361 x 20k samples
discarded per target)."""
import sys, time, random, itertools, resource, pickle
import numpy as np
t0 = time.time()
def log(*a): print('[%5.0fs rss=%dMB]' % (time.time() - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024), *a, flush=True)

roots = []
for i in range(8):
    for j in range(i + 1, 8):
        for si in (1, -1):
            for sj in (1, -1):
                v = np.zeros(8, dtype=int); v[i] = si; v[j] = sj
                roots.append(v)
half = [np.array(s, dtype=float) / 2 for s in itertools.product([1, -1], repeat=8) if s.count(-1) % 2 == 0]
def canon(v):
    for x in v:
        if x != 0:
            return tuple(v) if x > 0 else tuple(-v)
    return tuple(v)
lines8 = {}
for r in list(roots) + half: lines8[canon(r)] = r
R8 = list(lines8.values())
L = []
for al in R8:
    L.append((al, 0, 0)); L.append((al, 1, 0)); L.append((al, 0, 1))
L.append((None, 1, 1))
n = len(L)
coords = [list(al) + [a, b] if al is not None else [0.0] * 8 + [a, b] for al, a, b in L]
LA = np.array(coords)
def ip(x, y):
    (u, a1, b1), (w, a2, b2) = x, y
    gg = float(np.dot(u, w)) if u is not None and w is not None else 0.0
    return gg + a1 * b2 + b1 * a2
Gm = np.array([[ip(L[i], L[j]) for j in range(n)] for i in range(n)])
Z = np.abs(Gm) < 1e-9
Zint = [sum(1 << k for k in range(n) if Z[i, k]) for i in range(n)]
rng = random.Random(21)

use_count = {}  # flat mask -> reuse count
def sample_flats(R_lines, ntarget):
    tots, seen = [], set()
    tries = 0
    while len(tots) < ntarget and tries < ntarget * 60:
        tries += 1
        pick = rng.sample(R_lines, 6)
        if np.linalg.matrix_rank(LA[pick]) != 6: continue
        m = Z[pick[0]]
        for p in pick[1:]: m = m & Z[p]
        flat = np.ones(n, dtype=bool)
        for kk in [x for x in range(n) if m[x]]: flat = flat & Z[kk]
        fmask = sum(1 << k for k in range(n) if flat[k])
        if not fmask or fmask in seen: continue
        u = np.ones(n, dtype=bool)
        for k in range(n):
            if flat[k]: u = u & Z[k]
        if int(u.sum()) < 4: continue
        if int(flat.sum()) > 80: continue
        seen.add(fmask)
        tot = 0
        for k in range(n):
            if flat[k]: tot ^= (1 << k)
        tots.append((tot, fmask))
    return tots

def greedy_cover(R_t, band, maxw, restarts):
    """band: list of (total, fmask); reuse bonus: -0.5*use_count on ties"""
    best = None  # (residual_int, [fmasks])
    for _ in range(restarts):
        res = R_t; used = []
        order = list(band)
        while len(used) < maxw:
            rng.shuffle(order)
            bestp, bestt, bestf = 1 << 30, None, None
            for tt, fm in order:
                p = bin(res ^ tt).count('1') - 0.3 * use_count.get(fm, 0)
                if p < bestp: bestp, bestt, bestf = p, tt, fm
            if bestt is None or bin(res ^ bestt).count('1') >= bin(res).count('1'):
                break
            res ^= bestt; used.append(bestf)
            if bin(res).count('1') == 0: break
        rc = bin(res).count('1')
        if best is None or rc < best[0]: best = (rc, used, res)
        if best[0] == 0: break
    return best

ct_total = 0
solved = 0
all_design = {}
for t in range(n):
    R_t = Zint[t]
    R_lines = [k for k in range(n) if R_t >> k & 1]
    band = sample_flats(R_lines, 8000)
    rc, used, res = greedy_cover(R_t, band, 6, 3)
    w1 = len(used)
    # tail
    RL = [k for k in range(n) if res >> k & 1]
    small, sseen = [], set()
    for _ in range(6000):
        k = rng.choice((2, 3, 4))
        if len(RL) < k: break
        pick = rng.sample(RL, k)
        m = Z[pick[0]]
        for p in pick[1:]: m = m & Z[p]
        flat = np.ones(n, dtype=bool)
        for kk in [x for x in range(n) if m[x]]: flat = flat & Z[kk]
        fmask = sum(1 << k for k in range(n) if flat[k])
        if not fmask or fmask in sseen: continue
        sseen.add(fmask)
        tot = 0
        for x in range(n):
            if flat[x]: tot ^= (1 << x)
        small.append((tot, fmask))
    rc2, used2, res2 = greedy_cover(res, small, 5, 3)
    w2 = len(used2)
    for fm in used + used2: use_count[fm] = use_count.get(fm, 0) + 1
    ct = w1 + w2 + (1 if bin(res2).count('1') else 0)
    ct_total += ct
    solved += 1
    all_design[t] = (w1, w2, bin(res2).count('1'))
    if solved % 60 == 0:
        log('t=%d/%d solved: mean c_t so far %.2f, distinct flats %d' % (solved, n, ct_total / solved, len(use_count)))
log('DONE: %d targets, sum c_t = %d, mean c_t %.2f' % (solved, ct_total, ct_total / solved))
log('distinct flats used: %d' % len(use_count))
log('reuse histogram: %s' % dict(sorted({k: sum(1 for v in use_count.values() if v == k) for k in set(use_count.values())}.items())))
content = sum(bin(fm).count('1') for fm in use_count)
log('TOTAL CONTENT: %d slots' % content)
R_id = ct_total - n
log('R_identity = %d + dead (mids ~ content/16.7 = %d)' % (R_id, content // 17))
log('PROJECTED R = %d = %.1fv vs BUDGET 5414 (15v)' % (R_id + content // 17, (R_id + content // 17) / n))
pickle.dump({'design': all_design, 'use_count': use_count, 'ct_total': ct_total},
            open('ii19_design.pkl', 'wb'))
log('saved ii19_design.pkl')
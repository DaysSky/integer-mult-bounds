"""II19 flat-totals test: does E8's exact D6-total algebra live inside the level-0 target
perps?  II19's level-0 lines ARE E8 roots; their perps contain E8 quads/D6-flats.  If totals
of flats close R(t) EXACTLY at low weight here (unlike I11's stall), the E8 grammar
transplants.  Sampled rank-6 flats (RAM-safe), economical band, greedy trajectory."""
import sys, time, random, itertools, resource
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
# coordinate vectors for rank checks (11-dim ambient? use the (alpha, a, b) structure: 8+2 coords)
coords = []
for al, a, b in L:
    coords.append(list(al) + [a, b] if al is not None else [0.0] * 8 + [a, b])
LA = np.array(coords)
def ip(x, y):
    (u, a1, b1), (w, a2, b2) = x, y
    gg = float(np.dot(u, w)) if u is not None and w is not None else 0.0
    return gg + a1 * b2 + b1 * a2
Gm = np.array([[ip(L[i], L[j]) for j in range(n)] for i in range(n)])
Z = np.abs(Gm) < 1e-9
# ambient signature: last coord negative?  norm = (alpha^2) + 2ab: for (alpha,1,1): norm = alpha^2 + 2 = 2+... wait (a,b)=(1,1): 2ab=2: norm = |alpha|^2 + 2?? That gives 4 for unit alpha.  Hmm -- handled in census: all norms were 2.  (a,b) = (1,1): 2ab = 2: norm = |alpha|^2 + 2 > 2 unless alpha = 0.  But census showed norm 2 for the (None,1,1) line with alpha=None -> |alpha|^2 = 0: norm = 2.  OK consistent.
rng = random.Random(5)
for t in (0, 60, 200, 360, 121):
    R_mask = Z[t]
    R_lines = [k for k in range(n) if R_mask[k]]
    R_t = sum(1 << k for k in R_lines)
    totals, uszs, users = [], [], []
    seen = set()
    tries = 0
    while len(totals) < 2500 and tries < 120000:
        tries += 1
        pick = rng.sample(R_lines, 6)
        if np.linalg.matrix_rank(LA[pick]) != 6: continue
        m = Z[pick[0]]
        for p in pick[1:]:
            m = m & Z[p]
        flat = np.ones(n, dtype=bool)
        mk = [k for k in range(n) if m[k]]
        for k in mk:
            flat = flat & Z[k]
        fi = int(np.where(flat)[0].sum())  # placeholder
        fmask = sum(1 << k for k in range(n) if flat[k])
        if not fmask or fmask in seen: continue
        u = np.ones(n, dtype=bool)
        for k in range(n):
            if flat[k]:
                u = u & Z[k]
        nu = int(u.sum())
        seen.add(fmask)
        tot = 0
        for k in range(n):
            if flat[k]: tot ^= (1 << k)
        totals.append(tot); uszs.append(int(flat.sum())); users.append(nu)
    sizes_hist, users_hist = {}, {}
    for s in uszs: sizes_hist[s] = sizes_hist.get(s, 0) + 1
    for u in users: users_hist[u] = users_hist.get(u, 0) + 1
    inR = sum(1 for tt in totals if (tt & ~R_t) == 0)
    log('t=%d |R|=%d: %d rank-6 flats, size hist %s' % (t, bin(R_t).count('1'), len(totals), dict(sorted(sizes_hist.items()))))
    log('   users hist %s ; inside R(t): %d/%d' % (dict(sorted(users_hist.items())), inR, len(totals)))
    band = [(tt, u, s) for tt, u, s in zip(totals, users, uszs) if u >= 5 and s <= 80]
    log('   band (u>=5, s<=80): %d' % len(band))
    res = R_t
    hist = [bin(res).count('1')]
    for _ in range(8):
        best, bp = None, 1 << 30
        for tt, u, s in band:
            p = bin(res ^ tt).count('1')
            if p < bp: bp, best = p, tt
        if best is None: break
        res ^= best
        hist.append(bin(res).count('1'))
        if hist[-1] == 0: break
    log('   greedy trajectory: %s' % hist)
log('DONE')
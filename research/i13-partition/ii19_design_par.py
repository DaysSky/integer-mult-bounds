"""II19 coordinated full-361 stall-tail design — PARALLEL (4 workers, round-robin shards).
Same algorithm as ii19_design.py: bulk rank-6 flat-totals + small-flat tails, reuse bonus
within each shard, merged ledger at the end.  Checkpoint pickles per shard every 20 targets."""
import sys, time, random, itertools, resource, pickle
import numpy as np
import multiprocessing as mp
t0 = time.time()

# ---- system build (runs in each worker under spawn; ~2s) ----
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

def sample_flats(rng, R_lines, ntarget):
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

def greedy_cover(rng, use_count, R_t, band, maxw, restarts):
    best = None
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

def run_shard(arg):
    shard_id, seed, targets = arg
    rng = random.Random(seed)
    use_count = {}
    design = {}
    ct_total = 0
    t_st = time.time()
    for t in targets:
        R_t = Zint[t]
        R_lines = [k for k in range(n) if R_t >> k & 1]
        band = sample_flats(rng, R_lines, 8000)
        rc, used, res = greedy_cover(rng, use_count, R_t, band, 6, 3)
        w1 = len(used)
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
        rc2, used2, res2 = greedy_cover(rng, use_count, res, small, 5, 3)
        w2 = len(used2)
        for fm in used + used2: use_count[fm] = use_count.get(fm, 0) + 1
        ct = w1 + w2 + (1 if bin(res2).count('1') else 0)
        ct_total += ct
        design[t] = (w1, w2, bin(res2).count('1'))
        if len(design) % 20 == 0:
            print('[shard %d %4.0fs rss=%dMB] %d/%d done: mean c_t %.2f, flats %d' %
                  (shard_id, time.time() - t_st, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024,
                   len(design), len(targets), ct_total / len(design), len(use_count)), flush=True)
            pickle.dump((design, use_count, ct_total), open('ii19_shard_%d.pkl' % shard_id, 'wb'))
    pickle.dump((design, use_count, ct_total), open('ii19_shard_%d.pkl' % shard_id, 'wb'))
    return (design, use_count, ct_total)

if __name__ == '__main__':
    NPROC = 10
    shards = [(i, 21 + i, [t for t in range(n) if t % NPROC == i]) for i in range(NPROC)]
    print('parallel design: %d shards of sizes %s' % (NPROC, [len(s[2]) for s in shards]), flush=True)
    ctx = mp.get_context('spawn')
    with ctx.Pool(NPROC) as pool:
        results = pool.map(run_shard, shards)
    design, use_count, ct_total = {}, {}, 0
    for d, u, c in results:
        design.update(d)
        for fm, cnt in u.items(): use_count[fm] = use_count.get(fm, 0) + cnt
        ct_total += c
    print('DONE: %d targets, sum c_t = %d, mean c_t %.2f' % (len(design), ct_total, ct_total / len(design)), flush=True)
    print('distinct flats used: %d' % len(use_count), flush=True)
    hist = {}
    for v in use_count.values(): hist[v] = hist.get(v, 0) + 1
    print('reuse histogram: %s' % dict(sorted(hist.items())), flush=True)
    content = sum(bin(fm).count('1') for fm in use_count)
    print('TOTAL CONTENT: %d slots' % content, flush=True)
    R_id = ct_total - n
    print('R_identity = %d + dead (mids ~ content/17 = %d)' % (R_id, content // 17), flush=True)
    R = R_id + content // 17
    print('PROJECTED R = %d = %.1fv vs BUDGET 5414 (15.0v) / 4846 (13.4v)' % (R, R / n), flush=True)
    pickle.dump({'design': design, 'use_count': use_count, 'ct_total': ct_total},
                open('ii19_design.pkl', 'wb'))
    print('saved ii19_design.pkl', flush=True)
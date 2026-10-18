"""II19 assembly builder — PARALLEL (two-phase, 10 workers).
Phase A: each design flat (rank-6) built from rank-5 sub-flats, sharded round-robin.
Merge lvl5 dicts (distinct masks + counts).
Phase B: each DISTINCT lvl5 built from rank-4 sub-flats, sharded round-robin over the
MERGED lvl5 key set (avoids double-building lvl5s seen by multiple workers).
Ledger: true middle = distinct lvl5 + distinct lvl4 + gates/8; R vs budget."""
import sys, time, random, itertools, resource, pickle
import numpy as np
import multiprocessing as mp
t0 = time.time()

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

def total_of(mask):
    tot = 0
    for k in range(n):
        if mask >> k & 1: tot ^= (1 << k)
    return tot

def subflats(rng, mask, rank, nsample):
    lines = [k for k in range(n) if mask >> k & 1]
    out, seen = [], set()
    tries = 0
    while len(out) < nsample and tries < nsample * 40:
        tries += 1
        pick = rng.sample(lines, min(rank, len(lines)))
        if np.linalg.matrix_rank(LA[pick]) != len(pick): continue
        m = Z[pick[0]]
        for p in pick[1:]: m = m & Z[p]
        flat = np.ones(n, dtype=bool)
        for kk in [x for x in range(n) if m[x]]: flat = flat & Z[kk]
        fmask = sum(1 << k for k in range(n) if flat[k])
        if not fmask or fmask in seen: continue
        if fmask & ~mask: continue  # stay inside parent
        seen.add(fmask)
        out.append(fmask)
    return out

def passA(arg):
    shard_id, seed, masks = arg
    rng = random.Random(seed)
    lvl5 = {}
    gates = 0
    t_st = time.time()
    for i, fmask in enumerate(masks):
        ftot = total_of(fmask)
        subs = subflats(rng, fmask, 5, 300)
        if not subs:
            gates += bin(fmask).count('1') - 1
            continue
        res = ftot
        used = []
        for _ in range(6):
            best, bp = None, 1 << 30
            for sm in subs:
                p = bin(res ^ total_of(sm)).count('1')
                if p < bp: bp, best = p, sm
            if best is None or bp >= bin(res).count('1'): break
            res ^= total_of(best); used.append(best)
            if bin(res).count('1') == 0: break
        for sm in used:
            lvl5[sm] = lvl5.get(sm, 0) + 1
        if bin(res).count('1') > 0:
            gates += bin(res).count('1') + len(used)
        else:
            gates += len(used)
        if (i + 1) % 50 == 0:
            print('[A%d %3.0fs rss=%dMB] %d/%d flats: lvl5 %d gates %d' %
                  (shard_id, time.time() - t_st, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024,
                   i + 1, len(masks), len(lvl5), gates), flush=True)
    return (lvl5, gates)

def passB(arg):
    shard_id, seed, masks = arg
    rng = random.Random(seed)
    lvl4 = {}
    gates = 0
    t_st = time.time()
    for i, sm in enumerate(masks):
        stot = total_of(sm)
        subs = subflats(rng, sm, 4, 150)
        if not subs:
            gates += bin(sm).count('1') - 1
            continue
        res = stot
        used = []
        for _ in range(5):
            best, bp = None, 1 << 30
            for s4 in subs:
                p = bin(res ^ total_of(s4)).count('1')
                if p < bp: bp, best = p, s4
            if best is None or bp >= bin(res).count('1'): break
            res ^= total_of(best); used.append(best)
            if bin(res).count('1') == 0: break
        for s4 in used:
            lvl4[s4] = lvl4.get(s4, 0) + 1
        gates += len(used) + (bin(res).count('1') if bin(res).count('1') else 0)
        if (i + 1) % 100 == 0:
            print('[B%d %3.0fs rss=%dMB] %d/%d lvl5s: lvl4 %d gates %d' %
                  (shard_id, time.time() - t_st, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024,
                   i + 1, len(masks), len(lvl4), gates), flush=True)
    return (lvl4, gates)

if __name__ == '__main__':
    NPROC = 10
    d = pickle.load(open('ii19_design.pkl', 'rb'))
    use_count = d['use_count']
    ct_total = d['ct_total']
    print('design: %d distinct flats, sum c_t %d' % (len(use_count), ct_total), flush=True)
    flats = list(use_count.keys())
    ctx = mp.get_context('spawn')
    # phase A
    shardsA = [(i, 33 + i, [f for j, f in enumerate(flats) if j % NPROC == i]) for i in range(NPROC)]
    with ctx.Pool(NPROC) as pool:
        resA = pool.map(passA, shardsA)
    lvl5, gatesA = {}, 0
    for u5, g in resA:
        for m, c in u5.items(): lvl5[m] = lvl5.get(m, 0) + c
        gatesA += g
    print('PHASE A DONE: distinct lvl5 %d, gates %d' % (len(lvl5), gatesA), flush=True)
    # phase B over merged lvl5
    l5keys = list(lvl5.keys())
    shardsB = [(i, 53 + i, [m for j, m in enumerate(l5keys) if j % NPROC == i]) for i in range(NPROC)]
    with ctx.Pool(NPROC) as pool:
        resB = pool.map(passB, shardsB)
    lvl4, gatesB = {}, 0
    for u4, g in resB:
        for m, c in u4.items(): lvl4[m] = lvl4.get(m, 0) + c
        gatesB += g
    print('PHASE B DONE: distinct lvl4 %d, gates %d' % (len(lvl4), gatesB), flush=True)
    h5 = {}
    for v in lvl5.values(): h5[v] = h5.get(v, 0) + 1
    h4 = {}
    for v in lvl4.values(): h4[v] = h4.get(v, 0) + 1
    print('lvl5 reuse histogram: %s' % dict(sorted(h5.items())), flush=True)
    print('lvl4 reuse histogram: %s' % dict(sorted(h4.items())), flush=True)
    gates = gatesA + gatesB
    mid_regs = len(lvl5) + len(lvl4) + gates // 8
    print('TRUE MIDDLE: distinct lvl5 %d + distinct lvl4 %d + gates/8 %d = %d registers' %
          (len(lvl5), len(lvl4), gates // 8, mid_regs), flush=True)
    R_id = ct_total - n
    R = R_id + mid_regs
    print('R = %d + %d = %d (%.1fv) vs BUDGET 5414 (15.0v) / 4846 (13.4v)' %
          (R_id, mid_regs, R, R / n), flush=True)
    fits = R <= 5414
    print('VERDICT: %s (needs mids <= %d for 15v budget; %d for 13.4v)' %
          ('FITS the 15v budget' if fits else 'OVER the 15v budget',
           5414 - R_id - 0, 4846 - R_id - 0), flush=True)
    pickle.dump({'lvl5': lvl5, 'lvl4': lvl4, 'gates': gates, 'mid_regs': mid_regs},
                open('ii19_assembly.pkl', 'wb'))
    print('saved ii19_assembly.pkl', flush=True)
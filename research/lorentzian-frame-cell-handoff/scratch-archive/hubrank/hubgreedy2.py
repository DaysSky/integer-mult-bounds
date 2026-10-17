# Relaxed hub cover of the E-set incidences on partA: lazy greedy, cost of a hub = F2 rank of the residual rows
# (consumer c takes E_c n Z n uncovered_c).  Ignores chain nesting and the cost of building parked contents, so the
# total is an optimistic estimate of the hub-register count (not a bound: greedy).
import sys, pickle, itertools, heapq, time
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V, bits, closure, dim, nondegenerate
exec(open('hubrank.py').read().split("pairs = [")[0].split("print('consumers'")[0])   # reuse setup (cons, f2rank)
def f2rank(rows):
    piv = {}; r = 0
    for x in rows:
        while x:
            hb = x.bit_length() - 1
            if hb in piv: x ^= piv[hb]
            else: piv[hb] = x; r += 1; break
    return r
def perp(W):
    m = LIVE
    for s in bits(W): m &= g.HYP[s]
    return m
cand = pickle.load(open('hubrank.pkl', 'rb'))
hubs = []
for W, v in cand.items():
    if len(v) < 3 or v[1] < float(sys.argv[1]) if len(sys.argv) > 1 else 1.5: continue
    Zc = closure(perp(W))
    users = [i for i, c in enumerate(cons) if ((W >> c[1]) & 1) and ((W >> c[2]) & 1)]
    if v[0] == 1 or len(users) < 2: continue
    hubs.append((Zc, users))
print('hubs considered', len(hubs), flush=True)
unc = [c[3] for c in cons]
def score(h):
    Zc, users = hubs[h]
    rows = [unc[i] & Zc for i in users]; rows = [r for r in rows if r]
    if len(rows) < 2: return 0, 0, 0
    ones = sum(bin(r).count('1') for r in rows); rk = f2rank(rows)
    return ones / rk, ones, rk
pq = [(-score(h)[0], h) for h in range(len(hubs))]; heapq.heapify(pq)
total_rank = 0; covered = 0; picks = 0; t0 = time.time()
TOT = sum(bin(x).count('1') for x in unc)
log = []
while pq:
    negs, h = heapq.heappop(pq)
    s, ones, rk = score(h)
    if s <= 0: continue
    if pq and s < -pq[0][0] - 1e-9: heapq.heappush(pq, (-s, h)); continue
    if s < 2: break                       # below 2 incidences per register: leave to private arrivals
    Zc, users = hubs[h]
    for i in users: unc[i] &= ~Zc
    total_rank += rk; covered += ones; picks += 1
    log.append((s, ones, rk))
    if picks % 50 == 0: print('picks', picks, 'hub registers', total_rank, 'covered', covered, 'of', TOT, 'last ratio %.1f' % s, '%.0fs' % (time.time() - t0), flush=True)
left = sum(bin(x).count('1') for x in unc)
print('FINAL picks', picks, 'hub registers', total_rank, 'covered', covered, 'left', left)
# residual per consumer: lines left to private arrivals
from collections import Counter
print('residual lines per consumer histogram', sorted(Counter(bin(x).count('1') for x in unc).items()))

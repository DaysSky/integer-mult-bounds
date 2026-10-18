"""Minimal out-of-span carriers per target: how many {t,e}-sections are algebraically
unavoidable after using all rooms (12-user pieces) available to t.  Greedy over
section-residuals.  Output flushed directly."""
import pickle, sys, time
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(13); V = g.V; HYP = g.HYP; G = g.G
full = (1 << V) - 1
t0 = time.time()
frames = pickle.load(open('goodframes13.pkl', 'rb'))[:30000]
rooms_by_t = {}
for F in frames:
    room = full
    for s in [x for x in range(V) if F >> x & 1]: room &= HYP[s]
    for s in [x for x in range(V) if F >> x & 1]:
        if room & ~HYP[s] == 0: rooms_by_t.setdefault(s, set()).add(room)
print('frames scanned', len(frames), 'targets with rooms', len(rooms_by_t), flush=True)
def reduce_vec(v, basis):
    while v:
        b = v & -v
        if b not in basis: return v
        v ^= basis[b][0]
    return 0
for t in (g.P(0,1), g.T(0,1,2)):
    R_t = HYP[t] & ~(1 << t)
    cand = list(rooms_by_t.get(t, ()))
    basis = {}
    for c in cand:
        v = c
        while v:
            b = v & -v
            if b in basis: v ^= basis[b][0]
            else: basis[b] = (v, c); break
    res = reduce_vec(R_t, basis)
    print(g.kind[t], g.supp[t], 'rooms', len(cand), 'basis dim', len(basis),
          'residual after rooms:', bin(res).count('1'), flush=True)
    secs = [HYP[t] & HYP[e] for e in range(V) if e != t and G[t, e] == 0]
    reds = [reduce_vec(s, basis) for s in secs]
    used = 0
    while res:
        best, gain = None, -1
        for r in reds:
            c = bin(res & r).count('1') - bin(r & ~res).count('1')
            if c > gain: gain, best = c, r
        if best is None or gain <= 0: break
        res ^= best; used += 1
        if used % 5 == 0: print('   %d sections used, residual %d' % (used, bin(res).count('1')), flush=True)
    print('FINAL %s: greedy sections to close residual: %d, residual left: %d, %.0fs' % (
        g.kind[t] + str(g.supp[t]), used, bin(res).count('1'), time.time() - t0), flush=True)

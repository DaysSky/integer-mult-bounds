"""Is each {t,e}-section a small XOR of rooms (12-user pieces)?
For target t and mate e: section S = perp(t) & perp(e).  Rooms available: perp(M) for D4-flats
M containing t (or containing e -- a room readable by t must have supp inside R(t), i.e. flats
M with t in M).  Test: minimum #rooms XORing to S (after reducing S against the room basis,
greedy match over reduced rooms).  If sections are small room-XORs, the build tree of every
section is shared 12-way and the incidence economy changes completely."""
import pickle, sys, time
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(13); V = g.V; HYP = g.HYP; G = g.G
full = (1 << V) - 1
t0 = time.time()
print('scanning frames...', flush=True)
frames = pickle.load(open('goodframes13.pkl', 'rb'))[:30000]
rooms_by_t = {}
for F in frames:
    room = full
    for s in [x for x in range(V) if F >> x & 1]: room &= HYP[s]
    for s in [x for x in range(V) if F >> x & 1]:
        if room & ~HYP[s] == 0: rooms_by_t.setdefault(s, set()).add(room)
print('done %.0fs; targets %d' % (time.time()-t0, len(rooms_by_t)), flush=True)
def basis_of(cands):
    basis = {}
    for c in cands:
        v = c
        while v:
            b = v & -v
            if b in basis: v ^= basis[b][0]
            else: basis[b] = (v, c); break
    return basis
def reduce_vec(v, basis):
    while v:
        b = v & -v
        if b not in basis: return v
        v ^= basis[b][0]
    return 0
for t in (g.P(0,1), g.T(0,1,2)):
    R_t = HYP[t] & ~(1 << t)
    cand = list(rooms_by_t.get(t, ()))
    basis = basis_of(cand)
    # reduced rooms (their component outside the basis for matching): use reduced forms
    red_rooms = [reduce_vec(c, basis) for c in cand]
    red_rooms = [r for r in red_rooms if r]  # 0 = room already in span of others
    stats = []
    n_test = 0
    for e in range(V):
        if e == t or G[t, e] != 0: continue
        S = HYP[t] & HYP[e]
        r_S = reduce_vec(S, basis)
        if r_S == 0:
            stats.append(('in-span-of-rooms', 0)); n_test += 1
            continue
        # greedy min #rooms to kill r_S
        res = r_S; used = 0
        while res and used < 40:
            best, gain = None, -1
            for r in red_rooms:
                c = bin(res & r).count('1') - bin(r & ~res).count('1')
                if c > gain: gain, best = c, r
            if best is None or gain <= 0: break
            res ^= best; used += 1
        stats.append(('greedy', used if res == 0 else -1)); n_test += 1
        if n_test >= 40: break
    ok = [u for k, u in stats if u >= 0]
    print('%s: %d sections tested; in-room-span: %d; greedy-closed with mean %.1f rooms; unclosed: %d' % (
        g.kind[t] + str(g.supp[t]), n_test, sum(1 for k, u in stats if k == 'in-span-of-rooms'),
        (sum(ok)/len(ok) if ok else 0), sum(1 for k, u in stats if u < 0 and k == 'greedy')), flush=True)
    from collections import Counter
    print('   room-count histogram:', dict(sorted(Counter(u for k, u in stats if k == 'greedy' and u >= 0).items())), flush=True)

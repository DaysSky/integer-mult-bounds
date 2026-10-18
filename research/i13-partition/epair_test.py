"""E-pair XOR pieces: is E(t,e) XOR E(t,e') shared by >= 4-5 targets?
For target t in good frames, the frame identity: R(t) = Q + E(t,e1) + E(t,e2) + E(t,e3) + corr.
E-sets are 2-user pieces (the load bottleneck, 24.4k of PG's 28.8k).  But the XOR of two E-sets
is a different vector: users = lines of perp(supp) -- count them.  If >= 4-5, the E-content can
ride pair-XOR pieces shared 4-5x and the architecture closes under capacity."""
import pickle, sys, time, collections
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(13); V = g.V; HYP = g.HYP; G = g.G
full = (1 << V) - 1
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
frames = pickle.load(open('goodframes13.pkl', 'rb'))[:8000]
log('frames', len(frames))
# collect good frames containing representative targets; compute E-sets from the frame structure
# frame F (4 lines), Q = perp(frame), section {a,b} = perp(a)&perp(b); E(a,b|F) = sec(a,b) minus (Q plus content ⊥ other mates)
by_t = collections.defaultdict(list)
for F in frames:
    for s in [x for x in range(V) if F >> x & 1]: by_t[s].append(F)
log('frames per target mean %.0f' % (sum(len(v) for v in by_t.values()) / V))
def perp_lines(mask):
    r = full
    for s in [x for x in range(V) if mask >> x & 1]: r &= HYP[s]
    return r
users_hist = collections.Counter()
sizes = collections.Counter()
n_tested = 0
for t in (g.P(0,1), g.T(0,1,2), g.P(2,3), g.T(3,4,5), g.P(5,6)):
    for F in by_t[t][:12]:
        fs = [x for x in range(V) if F >> x & 1]
        if t not in fs: continue
        mates = [x for x in fs if x != t]
        if len(mates) != 3: continue
        Q = perp_lines(F)
        secs = {}
        Es = {}
        for a in fs:
            for b in fs:
                if a < b: secs[(a, b)] = HYP[a] & HYP[b]
        # E(a,b) relative to frame = lines in sec(a,b) not in Q and not in other mates' perps
        for (a, b), sec in secs.items():
            others = [x for x in fs if x != a and x != b]
            o = full
            for u in others: o &= HYP[u]
            Es[(a, b)] = sec & ~Q & ~o
        # pair-XORs of E-sets involving t
        pairs = [(a, b) for (a, b) in Es if t in (a, b)]
        for i in range(len(pairs)):
            for j in range(i + 1, len(pairs)):
                p = Es[pairs[i]] ^ Es[pairs[j]]
                if not p: continue
                pl = perp_lines(p)
                u = bin(pl).count('1')
                users_hist[u] += 1
                sizes[bin(p).count('1')] += 1
                n_tested += 1
log('E-pair XOR pieces tested:', n_tested)
log('users histogram:', dict(sorted(users_hist.items())))
log('size histogram (top):', dict(sorted(sizes.items())[:12]))
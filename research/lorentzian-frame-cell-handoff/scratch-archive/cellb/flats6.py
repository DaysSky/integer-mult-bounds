"""All closed flats of rank 6 inside t-perp (E8, t = 0) by closure BFS; classify by whether the flat is a plane-perp."""
import sys, pickle, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
V = e8.V; pc = lambda m: bin(m).count('1')
def perp(mask):
    m = (1 << V) - 1
    for s in e8.bits(mask): m &= e8.HYP[s]
    return m
t = int(sys.argv[1]) if len(sys.argv) > 1 else 0
H = e8.HYP[t]; Hl = list(e8.bits(H))
level = {1 << s for s in Hl}
for r in range(2, 7):
    nxt = set()
    for F in level:
        for x in Hl:
            if F >> x & 1: continue
            G, rk = e8.closure(F | (1 << x))
            if rk == r: nxt.add(G)
    level = nxt; print('rank', r, 'flats', len(level), flush=True)
planeperps = set(perp(e8.closure((1 << t) | (1 << u))[0]) for u in range(V) if u != t)
cnt = collections.Counter((pc(F), F in planeperps) for F in level)
print(sorted(cnt.items()))
pickle.dump(sorted(level), open('flats6_t%d.pkl' % t, 'wb'))

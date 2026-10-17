"""Cell alignment of E-set sign halves: for every half H (and every Q-part) and every partition frame f', the parity of
|H n f'|.  A half is a union of cells (pairs inside partition frames) iff every intersection is even.
usage: halfalign.py e8 | i11 PART.pkl"""
import sys, collections, itertools, pickle
mode = sys.argv[1]
if mode == 'e8':
    sys.path.insert(0, '/home/user/integer-mult-bounds/research/subspace16-r420/vendor/e8-bit-carrier-skeleton/code/skeleton')
    import e8
    from geom import Geom as GE
    frames = GE().frames4; GI = e8.GI; V = e8.V; live = list(range(V))
else:
    sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
    from geom import Geom
    g = Geom(11); V = g.V; GI = g.G
    frames, pun = pickle.load(open(sys.argv[2], 'rb')); live = [u for u in range(V) if u not in set(pun)]
orth = lambda a, b: a != b and GI[a, b] == 0
halves = set(); Qs = set()
for f in frames:
    Qs.add(frozenset(u for u in live if all(orth(u, x) for x in f)))
    for t, e in itertools.combinations(f, 2):
        k, l = [x for x in f if x not in (t, e)]
        E = [u for u in live if orth(u, t) and orth(u, e) and not orth(u, k) and not orth(u, l)]
        halves.add(frozenset(u for u in E if GI[u, k] == GI[u, l])); halves.add(frozenset(u for u in E if GI[u, k] == -GI[u, l]))
def odd(S): return sum(1 for f in frames if len(S & set(f)) % 2)
oh = collections.Counter(odd(H) for H in halves); oq = collections.Counter(odd(Q) for Q in Qs)
print(mode, 'halves: #odd frame intersections -> #halves', sorted(oh.items()), '| Q-parts:', sorted(oq.items()))
print('aligned halves', oh[0], 'of', len(halves), '; aligned Q', oq[0], 'of', len(Qs))

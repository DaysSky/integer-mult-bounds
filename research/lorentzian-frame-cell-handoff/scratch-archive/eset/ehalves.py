"""Split each E-set E(t,e) of a 4-frame partition by sign pattern: E+ = {u : <u,k> = <u,l>}, E- = {u : <u,k> = -<u,l>}
(k, l the other two frame members).  Each half lies in the rank-(h-3) pencil room f-perp + u.  Report sizes, ranks of
halves, and rank of half + Q-part.  Usage: ehalves.py e8 | i11 | i13"""
import sys, pickle, collections, itertools, numpy as np
mode = sys.argv[1]
if mode == 'e8':
    sys.path.insert(0, '/home/user/integer-mult-bounds/research/subspace16-r420/vendor/e8-bit-carrier-skeleton/code/skeleton')
    import e8
    from geom import Geom as GE
    frames = GE().frames4; LA = np.array(e8.LA, dtype=float); GI = e8.GI; V = e8.V; live = list(range(V))
else:
    sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
    from geom import Geom
    g = Geom(11 if mode == 'i11' else 13); V = g.V; GI = g.G; LA = np.array(g.LA, dtype=float)
    if mode == 'i11':
        frames, pun = pickle.load(open('/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/goodframe/goodpart.pkl', 'rb'))
        live = [u for u in range(V) if u not in set(pun)]
    else:
        frames = pickle.load(open('../i13a/pg23_partition.pkl', 'rb')); live = list(range(V))
orth = lambda a, b: a != b and GI[a, b] == 0
rk = lambda S: int(np.linalg.matrix_rank(LA[sorted(S)])) if S else 0
st = collections.Counter()
for f in frames:
    for t, e in itertools.combinations(f, 2):
        k, l = [x for x in f if x not in (t, e)]
        E = [u for u in live if orth(u, t) and orth(u, e) and not orth(u, k) and not orth(u, l)]
        Ep = [u for u in E if GI[u, k] == GI[u, l]]; Em = [u for u in E if GI[u, k] == -GI[u, l]]
        st[(len(E), rk(E), len(Ep), rk(Ep), len(Em), rk(Em))] += 1
print(mode, 'h', LA.shape[1], '(|E|, rk E, |E+|, rk E+, |E-|, rk E-): count')
for k_, c in sorted(st.items()): print('  ', k_, c)

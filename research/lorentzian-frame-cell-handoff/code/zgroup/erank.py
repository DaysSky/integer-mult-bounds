"""Rank structure of E-sets (I11 good partition vs E8 R420 skeleton): rank of E(sigma), rank of Sigma, and greedy
2-hub covers: H1 = best rank-r closed subset of E (greedy by lines gained), check rank(E minus H1) <= r."""
import sys, pickle, collections, itertools, numpy as np
mode = sys.argv[1]
if mode == 'i11':
    sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
    from geom import Geom
    g = Geom(11); V = g.V; G = g.G; LA = g.LA
    frames, pun = pickle.load(open('../part/goodpart.pkl', 'rb'))
    live = [u for u in range(V) if u not in set(pun)]
    orth = lambda a, b: a != b and G[a, b] == 0
else:
    sys.path.insert(0, '/home/user/integer-mult-bounds/research/subspace16-r420/vendor/e8-bit-carrier-skeleton/code/skeleton')
    import e8
    from geom import Geom as GE
    GG = GE(); V = e8.V
    # e8 line vectors
    LA = e8.LA
    frames = GG.frames4; live = list(range(V)); orth = lambda a, b: a != b and e8.GI[a, b] == 0
rk = lambda S: int(np.linalg.matrix_rank(LA[sorted(S)])) if S else 0
E = {}
for f in frames:
    for i, t in enumerate(f):
        for e in f[i + 1:]:
            o = [x for x in f if x not in (t, e)]
            E[(t, e)] = [u for u in live if orth(u, t) and orth(u, e) and not orth(u, o[0]) and not orth(u, o[1])]
stat = collections.Counter()
for k, S in list(E.items())[: int(sys.argv[2]) if len(sys.argv) > 2 else 10**9]:
    r = rk(S)
    res = [len(S), r]
    for hr in (4, 5, 6, 7):
        # greedy H1: grow a basis inside S choosing lines that maximise closure coverage
        basis = []; cov = set()
        for _ in range(hr):
            best = None
            for u in S:
                if u in cov: continue
                B = basis + [u]
                if rk(B) <= len(basis): continue
                c = [x for x in S if rk(B + [x]) == len(B)]
                if best is None or len(c) > len(best[1]): best = (u, c)
            if best is None: break
            basis.append(best[0]); cov = set(best[1])
        rest = [x for x in S if x not in cov]
        res.append((len(cov), rk(rest)))
    stat[tuple(res[:2])] += 1
    print(k, 'E size', res[0], 'rank', res[1], 'greedy hub (covered, rank of rest) for r=4..7:', res[2:], flush=True)

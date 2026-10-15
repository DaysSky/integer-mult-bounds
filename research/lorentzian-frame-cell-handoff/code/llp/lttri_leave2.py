"""Can a target that leaves TWO of its 4 M11 triangle nodes release anything?  T(X) keeps triangle nodes n2, n3 and
replaces n0, n1 by two sections F'-perp, F''-perp (F', F'' rank-3 frames through t = T(X)).  Those must cover
Need = R(t) n (n0-perp u n1-perp) minus (n2-perp u n3-perp) (no other section holds these lines).  A release at
n2/n3 is a line of R(t) lying in n2-perp or n3-perp only (the forced memberships of lttri_rho5_minrel.py are among
these); it must then also lie in F'-perp u F''-perp.  Enumerates all rank-3 frames through t and all frame pairs
covering Need, and reports which can also hold a release line.  usage: lttri_leave2.py [target_index ...]"""
import sys, json, itertools, collections
from lgeo import *
sol = [tuple(tuple(T) for T in node) for node in json.load(open('lttri_design_z11.json'))]
nodes_of = collections.defaultdict(list)
for ni, node in enumerate(sol):
    for T in node: nodes_of[T].append(ni)
def Ln(k, pts): return IDX[(k, tuple(sorted(pts)))]
targets = sorted(nodes_of)
for xi in (map(int, sys.argv[1:]) if len(sys.argv) > 1 else [0]):
    X = targets[xi]; t = Ln('T', X); R = HYP[t]
    nperp = [pm(pp(sum(1 << Ln('T', T) for T in sol[nj]))) & R for nj in nodes_of[X]]
    assert nperp[0] | nperp[1] | nperp[2] | nperp[3] == R
    frames = set()
    for a, b in itertools.combinations([s for s in range(V) if s != t], 2):
        m = (1 << t) | (1 << a) | (1 << b)
        if rank(m) == 3: frames.add(pp(m))
    fperp = {F: pm(F) & R for F in frames}
    print('target', X, '| frames through t:', len(frames), flush=True)
    for i0, i1 in itertools.combinations(range(4), 2):
        i2, i3 = [i for i in range(4) if i not in (i0, i1)]
        need = (nperp[i0] | nperp[i1]) & ~(nperp[i2] | nperp[i3])
        rel = (nperp[i2] | nperp[i3]) & ~(nperp[i0] | nperp[i1])
        rel2 = (nperp[i2] & ~nperp[i3]) | (nperp[i3] & ~nperp[i2])   # lines in exactly one retained node
        rel &= rel2
        cand = [F for F in frames if fperp[F] & need]
        ok = []; okrel = []
        for F1, F2 in itertools.combinations_with_replacement(cand, 2):
            u = fperp[F1] | fperp[F2]
            if need & ~u == 0:
                ok.append((F1, F2))
                if u & rel: okrel.append((F1, F2, pc(u & rel)))
        orig = {pp(sum(1 << Ln('T', T) for T in sol[nodes_of[X][i]])) for i in (i0, i1)}
        others = [p for p in ok if set(p[:2]) != orig]
        print(' leave', (nodes_of[X][i0], nodes_of[X][i1]), '| |Need|', pc(need), 'rank', rank(need), '| covering frame pairs:', len(ok),
              '(other than the original pair:', len(others), ') | pairs also holding a release line:', len(okrel),
              ('max release lines %d' % max(k for _, _, k in okrel)) if okrel else '', flush=True)

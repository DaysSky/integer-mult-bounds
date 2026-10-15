"""Shareability of 2-piece covers of exclusive parts: for each top type (first occurrence per signature), enumerate all
2-covers E = P1 u P2 with P_i = E & HYP[x_i] (x_i lines outside the plane); node frame N_i = pp(P_i); sinks = number of
plane sections containing N_i; need = ceil(|P_i|/2) input registers (cell registers carry <= 2 lines).
Report the best (max over covers of min_i sinks_i/need_i) per top type."""
import itertools, collections
from lgeo import *
VEC = {}
for s in range(V):
    VEC[tuple(int(x) for x in g.L[s])] = s; VEC[tuple(-int(x) for x in g.L[s])] = s
def plane_of(a, b):
    m = (1 << a) | (1 << b)
    if G[a][b] != 0:
        for sg in (1, -1):
            c = VEC.get(tuple(int(x) for x in (g.L[a] - sg * g.L[b])))
            if c is not None and c not in (a, b): m |= 1 << c
    return m
NS = {}
def sinks(N):
    if N not in NS:
        P = bits(pm(N)); NS[N] = len(set(plane_of(a, b) for i, a in enumerate(P) for b in P[i + 1:]))
    return NS[N]
for t in (0, 100):
    R = HYP[t]
    pl = sorted(set(plane_of(t, e) for e in range(V) if e != t))
    S = {p: pm(p) for p in pl}
    done = set()
    for i, j, k in itertools.combinations(pl, 3):
        D = S[i] ^ S[j] ^ S[k] ^ R; d = pc(D)
        if not (d == 1 or (d == 3 and all(G[x][y] == 0 for x, y in itertools.combinations(bits(D) + [t], 2)))): continue
        for a, b, c in ((i, j, k), (j, i, k), (k, i, j)):
            E = S[a] & ~S[b] & ~S[c]
            sig = (d, pc(a), pc(S[a]), pc(E))
            if sig in done: continue
            done.add(sig)
            parts = set()
            for x in range(V):
                if a >> x & 1: continue
                P = E & HYP[x]
                if P and P != E: parts.add(P)
            best = None
            for P1 in parts:
                rest = E & ~P1
                for P2 in parts:
                    if rest & ~P2: continue
                    Q2 = rest                          # assign shared lines to P1
                    N1, N2 = pp(P1), pp(Q2)
                    r1 = sinks(N1) / ((pc(P1) + 1) // 2); r2 = sinks(N2) / ((pc(Q2) + 1) // 2)
                    score = min(r1, r2)
                    if best is None or score > best[0]:
                        best = (round(score, 2), pc(P1), pc(N1), sinks(N1), pc(Q2), pc(N2), sinks(N2))
            print('target', KIND[t], 'top sig (defect, plane, |S|, |E|):', sig, ' best 2-cover (min sinks/need, |P1|, |N1|, sinks1, |P2|, |N2|, sinks2):', best, flush=True)

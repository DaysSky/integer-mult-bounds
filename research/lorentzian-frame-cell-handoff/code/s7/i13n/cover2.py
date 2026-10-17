"""2-covers of sections / Q-frames of the PG partition by two proper flats (A = S cap n-perp for line normals n in S)."""
from part13 import *
import collections, random
random.seed(1)
frames = {}
for d in DEM: frames.setdefault((d[0], pc(d[1])), []).append(d[1])
for key, lst in sorted(frames.items()):
    S = lst[0]; rS = rk(S)
    best = None; n2 = 0
    for u in bits(S):
        A = S & HYP[u]
        B = cl(S & ~A)
        if B != S:
            n2 += 1
            if best is None or pc(A) + pc(B) < best[0]: best = (pc(A) + pc(B), pc(A), rk(A), pc(B), rk(B), pc(A & B))
    print(key, 'rank', rS, 'line-normal 2-covers:', n2, 'best (sum, |A|, rkA, |B|, rkB, |AnB|):', best, flush=True)

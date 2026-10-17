"""Cover numbers of E-sets / Q-parts by proper flats of their frames (heuristic: hyperplanes S cap n-perp for
normals n = lines of S and sums/differences of two lines of S)."""
from part13 import *
import collections
res = collections.Counter(); ex = {}
seen = set()
for d in DEM:
    kind, S, E, fi, users = d
    key = (kind, pc(E), pc(S))
    if (key, E) in seen: continue
    seen.add((key, E))
    if sum(1 for k in res if k[0] == key) and sum(v for k, v in res.items() if k[0] == key) >= 6: continue
    rS = rk(S); rE = rk(E)
    if rE < rS or cl(E) != S:
        res[(key, 1)] += 1; continue
    Sl = bits(S)
    # candidate hyperplanes: lines of S perp to n, n in lines of S
    hyps = set()
    for u in Sl:
        A = S & HYP[u]
        if rk(A) < rS: hyps.add(cl(A))
    best2 = None
    for A in hyps:
        B = cl(E & ~A)
        if B != S and rk(B) < rS:
            best2 = (pc(A & E), pc(B & E)); break
    if best2: res[(key, 2)] += 1; continue
    # greedy 3
    hl = sorted(hyps, key=lambda A: -pc(A & E))
    ok3 = False
    for A in hl[:40]:
        R1 = E & ~A
        for B in hl[:200]:
            C = cl(R1 & ~B)
            if C != S and rk(C) < rS: ok3 = True; break
        if ok3: break
    res[(key, 3 if ok3 else 4)] += 1
    print(key, 'cover', 3 if ok3 else '>=4(heur)', 'max|A cap E|', pc(hl[0] & E) if hl else 0, flush=True)
print(sorted(res.items()))

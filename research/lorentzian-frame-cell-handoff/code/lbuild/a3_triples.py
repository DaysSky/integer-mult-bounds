"""Step 1 of the A3-parity word build (I_{11,1}): for every target t, all triples of PLANE sections (perps of
nondegenerate rank-2 flats through t: pairs or A2 triangles, nondegenerate sections) whose perps XOR to R(t) + D with
|D| <= 1.  Exact, vectorised: for each plane pair (a,b), popcount(R^Sa^Sb^Sc) over all c.
Output a3_triples.pkl {t: [(plane_a, plane_b, plane_c, defect line or -1)]}.  usage: python3 a3_triples.py"""
import sys, os, pickle, collections, itertools, time
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lmid'))
import lw
from lw import V, g, bits, nondegenerate
from fastcl import fclosure
HYP = g.HYP; NW = (V + 63) // 64
t0 = time.time()
def words(m): return [(m >> (64 * w)) & ((1 << 64) - 1) for w in range(NW)]
POP = np.array([bin(i).count('1') for i in range(1 << 16)], dtype=np.uint8)
def popc(arr):   # arr uint64 [..., NW]
    tot = np.zeros(arr.shape[:-1], dtype=np.int32)
    for sh in (0, 16, 32, 48):
        tot = tot + POP[((arr >> np.uint64(sh)) & np.uint64(0xFFFF)).astype(np.int64)].sum(axis=-1, dtype=np.int32)
    return tot
PM = {}
def pm(m):
    r = PM.get(m)
    if r is None:
        r = (1 << V) - 1
        for s in bits(m): r &= HYP[s]
        PM[m] = r
    return r
out = {}; stat = collections.Counter()
for t in range(V):
    planes = {}
    for u in range(V):
        if u == t: continue
        Q = fclosure((1 << t) | (1 << u))
        if Q not in planes and nondegenerate(Q):
            S = pm(Q)
            if nondegenerate(S): planes[Q] = S
    QL = list(planes); SL = [planes[Q] for Q in QL]; R = HYP[t]; nq = len(QL)
    W = np.array([words(S) for S in SL], dtype=np.uint64); Rw = np.array(words(R), dtype=np.uint64)
    res = []
    for a in range(nq):
        Ya = Rw ^ W[a]
        Yab = Ya[None, :] ^ W[a + 1:]                       # pairs (a, b>a)
        Z = Yab[:, None, :] ^ W[None, :, :]                 # (b, c)
        pcnt = popc(Z)
        bb, cc = np.nonzero(pcnt <= 1)
        for b0, c in zip(bb, cc):
            b = a + 1 + int(b0); c = int(c)
            if c <= b: continue
            d = -1
            if pcnt[b0, c] == 1:
                rest = R ^ SL[a] ^ SL[b] ^ SL[c]; d = rest.bit_length() - 1
            res.append((QL[a], QL[b], QL[c], d))
    out[t] = res
    stat[(g.kind[t], len(res) > 0)] += 1
    if t % 20 == 0: print('[%4.0fs] t=%d %s planes %d triples %d (defect0 %d)' % (time.time() - t0, t, g.kind[t], nq, len(res), sum(1 for r in res if r[3] < 0)), flush=True)
pickle.dump(out, open('a3_triples.pkl', 'wb'))
print('targets with >= 1 triple of defect <= 1, by (kind, has):', dict(stat))
print('targets with a defect-0 triple:', sum(1 for t in out if any(r[3] < 0 for r in out[t])))

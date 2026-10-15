"""Is 1[R(t)] in the F2 span of the routable-section-total vectors rt(S) (planes S through t)?  Also the span of
FULL section totals tot(S) (all lines, routable or not), for comparison.  usage: lparspan.py SYSTEM.json"""
import sys, os, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lw import V, g, bits, closure, FULL
HYP = g.HYP
cov = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}
cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in bits(cov[a])))
cells_of = {s: [C for C in cells if C >> s & 1] for s in range(V)}
def pm(m):
    r = FULL
    for s in bits(m): r &= HYP[s]
    return r
def rt(S):
    r = 0
    for u in bits(S):
        if any(C & ~S == 0 for C in cells_of[u]): r |= 1 << u
    return r
def in_span(vecs, target):
    red = {}
    for v0 in vecs:
        v1 = v0
        while v1:
            hb = v1.bit_length() - 1
            if hb in red: v1 ^= red[hb]
            else: red[hb] = v1; break
    x = target
    while x:
        hb = x.bit_length() - 1
        if hb not in red: return False, len(red)
        x ^= red[hb]
    return True, len(red)
res = collections.Counter()
for t in range(V):
    planes = sorted(set(closure((1 << t) | (1 << e)) for e in range(V) if e != t))
    secs = [pm(Q) for Q in planes]
    a, ra = in_span([rt(S) for S in secs], HYP[t])
    b, rb = in_span(secs, HYP[t])
    res[(g.kind[t], 'routable-span' if a else 'NOT', ra, 'full-span' if b else 'NOT', rb)] += 1
for k, n in sorted(res.items(), key=str): print(n, k)

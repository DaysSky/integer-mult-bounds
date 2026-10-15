"""Independent geometric check of a T-triangle design (lttri_design*.json) with lgeo: every node frame
{T(A),T(B),T(C)} is a rank-3 frame whose perp has 37 lines; every T line lies in exactly 4 nodes and the perps of
those 4 nodes cover R(t) = HYP[t]; reports overlap statistics.  usage: lttri_check.py design.json"""
import sys, json, collections
from lgeo import *
sol = [tuple(tuple(T) for T in node) for node in json.load(open(sys.argv[1]))]
frames = {}
for node in sol:
    m = 0
    for T in node: m |= 1 << IDX[('T', tuple(T))]
    assert rank(m) == 3, node
    F = pp(m); assert pc(pm(F)) == 37, (node, pc(pm(F)))
    frames[node] = F
use = collections.defaultdict(list)
for node, F in frames.items():
    for T in node: use[IDX[('T', tuple(T))]].append(F)
ov = collections.Counter()
for t in range(V):
    if KIND[t] != 'T': continue
    Fs = use[t]; assert len(Fs) == 4, (t, len(Fs))
    U = 0; tot = 0
    for F in Fs:
        assert F >> t & 1
        P = pm(F) & HYP[t]; assert P == pm(F); U |= P; tot += pc(P)
    assert U == HYP[t], 'not a cover'
    ov[tot - pc(HYP[t])] += 1
print('CHECK OK: %d nodes, all 165 T lines covered by exactly 4 triangle nodes; overlap histogram' % len(frames), sorted(ov.items()))

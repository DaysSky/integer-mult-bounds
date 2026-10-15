"""Faithful node cost of a rank-8 frame-section top (Z11-equivariant solution from lr8z11 det JSON).
At each section node F-perp: k = #delivered users (one register each); S = GF(2) span of all delivered parts and all
in-chain parts on F (in-chain users read combinations of the node's registers).  The node's registers arrive from
the last middle stop, each with content supported in a closed set of rank <= RHO.  m = min #registers whose
(rank <= RHO)-supported contents span a space containing S:
  m = dim S if the good vectors of S (support rank <= RHO) span S; otherwise dim S + 1 <= m <= dim S + (dim S - g).
Registers at the node = k + (m - d), d = dim span(delivered parts) (= max(m, k) when delivered parts are
independent); extra = m - d.  R = 440 + sum of extras (sum k = 660).
usage: lr8nodecost.py det.json RHO [AUTO]  (AUTO = input rank used at rank-7 nodes, chain ...,AUTO,7 -> node)"""
import sys, json, collections, pickle
from lgeo import *
D = json.load(open(sys.argv[1])); RHO = int(sys.argv[2])
AUTO = int(sys.argv[3]) if len(sys.argv) > 3 else 0   # e.g. 5: rank-7 nodes get inputs from rank-5 stops
sel = {int(k): v for k, v in D['sel'].items()}; det = D['det']
rot = [img_line(s, [(i + 1) % n for i in range(n)]) for s in range(V)]
rotp = [list(range(V))]
for k in range(1, n): rotp.append([rot[x] for x in rotp[-1]])
def rotm(m, k):
    r = 0
    for s in bits(m): r |= 1 << rotp[k % n][s]
    return r
orb = {}; reps = []
for s in range(V):
    if s in orb: continue
    reps.append(s); x = s
    for k in range(n): orb[x] = (len(reps) - 1, k); x = rot[x]
cov = pickle.load(open(__import__('os').environ.get('POOL', 'r8covers.pkl'), 'rb'))
# rep parts
asg = collections.defaultdict(int)
for key, v in det['assign'].items():
    ri, i, u = map(int, key.split(','))
    if v: asg[(ri, i)] |= 1 << u
def part(t, j):
    o, k = orb[t]; return rotm(asg[(o, j)], k)
def secs(t):
    o, k = orb[t]; return [rotm(F, k) for F in cov[reps[o]][sel[reps[o]]]]
def cin(t):
    o, k = orb[t]; return det['cin'][o].index(1)
# sanity: parts partition R(t), part j inside perp of frame j
for t in range(V):
    S = secs(t); tot = 0
    for j in range(4):
        p = part(t, j); assert p & ~pm(S[j]) == 0; assert tot & p == 0; tot |= p
    assert tot == HYP[t]
users = collections.defaultdict(list)
for t in range(V):
    for j, F in enumerate(secs(t)): users[F].append((t, j))
def gf2_basis(vs):
    basis = []
    for v in vs:
        for b in basis:
            if v ^ b < v: v ^= b
        if v:
            basis.append(v); basis.sort(reverse=True)
    return basis
def reduce(v, basis):
    for b in basis:
        if v ^ b < v: v ^= b
    return v
RK = {}
def srank(v):
    if v not in RK: RK[v] = rank(v)
    return RK[v]
extra = 0; lo = hi = 0; hist = collections.Counter(); unhost = 0
for F, us in users.items():
    dl = [part(t, j) for t, j in us if cin(t) != j]; ic = [part(t, j) for t, j in us if cin(t) == j]
    k = len(dl)
    Bd = gf2_basis(dl)
    for q in ic:
        if reduce(q, Bd): unhost += 1
    B = gf2_basis(dl + ic); s = len(B)
    # enumerate span
    vecs = [0]
    for b in B: vecs = vecs + [v ^ b for v in vecs]
    rho = RHO
    if AUTO and rank(pm(F)) <= 7: rho = AUTO      # rank-7 node: the stop before it is the rank-AUTO stop (e.g. 5)
    good = [v for v in vecs if v and srank(v) <= rho]
    g = len(gf2_basis(good))
    mlo = s if g == s else s + 1; mhi = s if g == s else 2 * s - g
    d = len(Bd)                       # dim span of delivered contents
    # registers = k + (m - d): the final contents span the m arriving dimensions; delivered registers cover d of
    # them, dead registers the rest (copies of an assembled vector are free empties)
    lo += mlo - d; hi += mhi - d
    hist[(k, len(ic), s, g)] += 1
print('sections', len(users), '| unhosted in-chain (not in delivered span)', unhost)
print('RHO=%d  extra registers: %d .. %d  ->  R = %d .. %d' % (RHO, lo, hi, 440 + lo, 440 + hi))
print('(k delivered, in-chain users, dim S, good dim) histogram:')
for key, c in sorted(hist.items()): print('  ', key, c)

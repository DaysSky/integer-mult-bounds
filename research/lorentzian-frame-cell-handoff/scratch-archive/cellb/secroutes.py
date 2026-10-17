"""For target t: every plane Q ∋ t (orthogonal pair or A2), number of R420 cells inside Q-perp and the lines of R(t)
routable through Q (a cell of u inside Q-perp)."""
import sys, json, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
V = e8.V; pc = lambda m: bin(m).count('1')
def perp(mask):
    m = (1 << V) - 1
    for s in e8.bits(mask): m &= e8.HYP[s]
    return m
cells = [int(h, 16) for h in json.load(open('../sec4/r420cells.json'))['planes']]
t = 0
frame = 1 << t
for C in cells:
    if C >> t & 1: frame |= C
stat = collections.Counter()
for u in range(V):
    if u == t: continue
    Q = e8.closure((1 << t) | (1 << u))[0]
    if u != min(x for x in e8.bits(Q) if x != t): continue
    P = perp(Q)
    inside = [C for C in cells if C & ~P == 0]
    rout = 0
    for C in inside: rout |= C
    kind = ('frame-pair' if Q & ~frame == 0 else 'pair') if pc(Q) == 2 else 'A2'
    stat[(kind, pc(P), len(inside), pc(rout))] += 1
for k, n in sorted(stat.items()): print(k, n)

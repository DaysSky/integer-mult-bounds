"""FREE-TOP version of the cell bottleneck: targets may read anywhere inside t-perp.  Doubly forced targets of C={s,e}:
t ⊥ s,e such that no other cell of s and no other cell of e lies in t-perp.  A stream node N ⊋ C serves t iff
N ⊂ t-perp.  k_C = |T_C| - max_N #{t in T_C : N ⊂ t-perp}  (the rest must read C in-chain, <= 1 rank-2 read each)."""
import sys, json, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
V = e8.V
cells = [int(h, 16) for h in json.load(open('../sec4/r420cells.json'))['planes']]
cells_of = {s: [C for C in cells if C >> s & 1] for s in range(V)}
CL = {}
def closure(m):
    if m not in CL: CL[m] = e8.closure(m)[0]
    return CL[m]
hist = collections.Counter(); rk = collections.Counter(); tsz = collections.Counter()
for C in cells:
    s, e = e8.bits(C)
    T = [t for t in range(V) if C & ~e8.HYP[t] == 0
         and not any(c != C and c & ~e8.HYP[t] == 0 for c in cells_of[s] + cells_of[e])]
    tsz[len(T)] += 1
    m = 0
    for t in T: m |= 1 << t
    rk[e8.dim(m)] += 1
    best = 0
    for x in range(V):
        if C >> x & 1: continue
        N = closure(C | (1 << x))
        best = max(best, sum(1 for t in T if N & ~e8.HYP[t] == 0))
    hist[len(T) - best] += 1
print('|T_C|', dict(tsz), ' rank span T_C', dict(rk), ' k_C', dict(hist))

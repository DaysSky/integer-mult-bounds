"""Frame-top cell bottleneck for an E8 frame graph (targets read only inside their own 3 frame D6s)."""
import sys, json, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
V = e8.V
def perp(m):
    r = (1 << V) - 1
    for s in e8.bits(m): r &= e8.HYP[s]
    return r
CL = {}
def closure(m):
    if m not in CL: CL[m] = e8.closure(m)[0]
    return CL[m]
adj = json.load(open(sys.argv[1]))
cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in adj[a]))
cells_of = {s: [C for C in cells if C >> s & 1] for s in range(V)}
D6 = {t: [perp(C) for C in cells_of[t]] for t in range(V)}
hT = collections.Counter(); hk = collections.Counter(); single = collections.Counter()
for C in cells:
    s, a = e8.bits(C); T = []; S = []
    for t in range(V):
        if C & ~e8.HYP[t]: continue
        rs = [(D, c) for D in D6[t] for c in cells_of[s] if c & ~D == 0]
        ra = [(D, c) for D in D6[t] for c in cells_of[a] if c & ~D == 0]
        fs = rs and all(c == C for _, c in rs); fa = ra and all(c == C for _, c in ra)
        if fs and fa: T.append([D for D, _ in rs])
        elif fs or fa: S.append(t)
    best = 0
    for x in range(V):
        if C >> x & 1: continue
        N = closure(C | (1 << x))
        best = max(best, sum(1 for Ds in T if any(N & ~D == 0 for D in Ds)))
    hT[len(T)] += 1; hk[len(T) - best] += 1; single[len(S)] += 1
print(sys.argv[1], 'frame top: |T_C|', dict(hT), 'k_C', dict(hk), 'singly forced per cell', dict(single))

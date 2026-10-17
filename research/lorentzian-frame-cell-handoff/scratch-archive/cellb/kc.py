"""Refinement: a doubly forced target may instead read the cell C in-chain (frame C on its chain; each target's chain
holds at most one rank-2 frame).  k_C = |T_C| - max over N ⊋ C of #targets in T_C with N inside a C-containing D6.
Also the 2-stream variant (streams s and e with nodes N1, N2: a target is served iff both nodes fit its D6s)."""
import sys, json, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
V = e8.V
def perp(mask):
    m = (1 << V) - 1
    for s in e8.bits(mask): m &= e8.HYP[s]
    return m
cells = [int(h, 16) for h in json.load(open('../sec4/r420cells.json'))['planes']]
cells_of = {s: [C for C in cells if C >> s & 1] for s in range(V)}
D6s_of = {t: [perp(C) for C in cells_of[t]] for t in range(V)}
CL = {}
def closure(m):
    if m not in CL: CL[m] = e8.closure(m)[0]
    return CL[m]
kc = collections.Counter(); best_sizes = collections.Counter(); ranks = collections.Counter()
for C in cells:
    s, e = e8.bits(C); T = []
    for t in range(V):
        if not (e8.HYP[t] >> s & 1 and e8.HYP[t] >> e & 1): continue
        rs = [(D, c) for D in D6s_of[t] for c in cells_of[s] if c & ~D == 0]
        re = [(D, c) for D in D6s_of[t] for c in cells_of[e] if c & ~D == 0]
        if rs and re and all(c == C for _, c in rs) and all(c == C for _, c in re): T.append((t, [D for D, _ in rs]))
    # candidate nodes: all closed flats N ⊋ C inside some C-containing D6 of some t: enumerate closures of C+x, C+x+y
    cand = set()
    for x in range(V):
        if C >> x & 1: continue
        N1 = closure(C | (1 << x))
        if any(any(N1 & ~D == 0 for D in Ds) for t, Ds in T): cand.add(N1)
    best = 0; bestN = None
    for N in cand:
        k = sum(1 for t, Ds in T if any(N & ~D == 0 for D in Ds))
        if k > best: best, bestN = k, N
    # bigger N only serve subsets of what a minimal sub-node serves, so minimal nodes give the max
    kc[len(T) - best] += 1; best_sizes[best] += 1; ranks[e8.dim(bestN) if bestN else 0] += 1
    # two-stream: max over pairs (N1,N2) of targets served by both (<= best) -> sum-stream dominates
print('k_C histogram (cell readers needed if C keeps 2 registers):', dict(kc))
print('max targets served by one stream node:', dict(best_sizes), ' rank of best node:', dict(ranks))

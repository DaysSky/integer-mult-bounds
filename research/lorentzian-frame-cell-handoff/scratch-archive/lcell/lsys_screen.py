"""Screen a Lorentzian source system (json: line -> cover mask of its 3 partners): cells, defects, own-cover frame top
(t's sections = perps of its own cells) no-route count, doubly forced T_C and k_C for frame and free tops."""
import sys, json, collections
from lbase import *
cov = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}
defects = sum(1 for a in range(V) for b in bits(cov[a]) if not cov[b] >> a & 1)
cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in bits(cov[a])))
cells_of = {s: [C for C in cells if C >> s & 1] for s in range(V)}
own = {t: [perp((1 << t) | (1 << f)) for f in bits(cov[t])] for t in range(V)}
nr = sum(1 for t in range(V) for u in bits(HYP[t]) if not any(c & ~D == 0 for D in own[t] for c in cells_of[u]))
print('cells', len(cells), 'defects', defects, 'own-cover frame top no-route pairs', nr, flush=True)
res = {'free': collections.Counter(), 'frame': collections.Counter()}; tsz = {'free': collections.Counter(), 'frame': collections.Counter()}
for C in cells:
    s, a = list(bits(C))
    Ns = set()
    for x in range(V):
        if C >> x & 1: continue
        N = closure(C | (1 << x))
        if nondeg_span(N): Ns.add(N)
    Tf = [t for t in range(V) if C & ~HYP[t] == 0 and not any(c != C and c & ~HYP[t] == 0 for c in cells_of[s] + cells_of[a])]
    best = max([sum(1 for t in Tf if N & ~HYP[t] == 0) for N in Ns] + [0])
    res['free'][len(Tf) - best] += 1; tsz['free'][len(Tf)] += 1
    Tr = []
    for t in range(V):
        if C & ~HYP[t]: continue
        rs = [(D, c) for D in own[t] for c in cells_of[s] if c & ~D == 0]
        ra = [(D, c) for D in own[t] for c in cells_of[a] if c & ~D == 0]
        if rs and ra and all(c == C for _, c in rs) and all(c == C for _, c in ra): Tr.append([D for D, _ in rs])
    bestr = max([sum(1 for Ds in Tr if any(N & ~D == 0 for D in Ds)) for N in Ns] + [0])
    res['frame'][len(Tr) - bestr] += 1; tsz['frame'][len(Tr)] += 1
for k in res: print(k, 'top: |T_C|', dict(tsz[k]), 'k_C', dict(res[k]))

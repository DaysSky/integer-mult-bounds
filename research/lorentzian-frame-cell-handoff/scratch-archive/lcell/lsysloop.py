"""Generate several Z11 good-frame systems (random tie-breaks, short solves) and score each by the free-top
doubly-forced counting bound: R_lb = 440 + defects + sum_j_lb.  Keeps all systems; prints scores."""
import sys, os, json, random, collections, itertools, subprocess
os.environ['GRP'] = '11'; os.environ['NOPPP'] = '1'
from lbase import *
def score(cov):
    defects = sum(1 for a in range(V) for b in bits(cov[a]) if not cov[b] >> a & 1)
    cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in bits(cov[a])))
    cells_of = {s: [C for C in cells if C >> s & 1] for s in range(V)}
    ks = []
    reps = {}
    for C in cells:
        key = min(act(C, p) for p in PERMS)
        if key in reps: ks.append(reps[key]); continue
        s, a = list(bits(C))
        T = [t for t in range(V) if C & ~HYP[t] == 0 and not any(c != C and c & ~HYP[t] == 0 for c in cells_of[s] + cells_of[a])]
        best = 0
        if T:
            for x in range(V):
                if C >> x & 1: continue
                N = closure(C | (1 << x))
                if not nondeg_span(N): continue
                best = max(best, sum(1 for t in T if N & ~HYP[t] == 0))
        k = len(T) - best; reps[key] = k; ks.append(k)
    free0 = sum(1 for k in ks if k == 0); pool = V; cnt = 0
    for k in sorted(k for k in ks if k > 0):
        if pool >= k: pool -= k; cnt += 1
    jlb = len(cells) - free0 - cnt
    return defects, jlb, 440 + defects + jlb
if __name__ == '__main__':
    for fn in sys.argv[1:]:
        cov = {int(k): v for k, v in json.load(open(fn)).items()}
        print(fn, 'defects, sum_j_lb, R_lb =', score(cov), flush=True)

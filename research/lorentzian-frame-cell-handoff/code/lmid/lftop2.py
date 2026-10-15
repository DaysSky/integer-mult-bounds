"""Frame top with the top frame chosen freely: for each target t, over ALL good frames Phi through t, the correction
c(t) = sum_i tot_u(S_i) + mates; report min |c(t)| and whether some Phi has c(t) routable inside one extra plane
section (4-section frame top with shared totals).  usage: lftop2.py SYSTEM.json"""
import sys, os, json, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lcell'))
os.environ['GRP'] = '11'
from lbase import V, bits, HYP, closure, perp, g, goodframes
pc = lambda m: bin(m).count('1')
cov = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}
cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in bits(cov[a])))
co = {s: [C for C in cells if C >> s & 1] for s in range(V)}
RT = {}
def rt(S):
    if S not in RT:
        m = 0
        for u in bits(S):
            if any(C & ~S == 0 for C in co[u]): m |= 1 << u
        RT[S] = m
    return RT[S]
fr = goodframes()
SEC = {}
for t in range(V):
    SEC[t] = []
    for e in range(V):
        if e != t: SEC[t].append(rt(perp(closure((1 << t) | (1 << e)))))
mins = []; fits = 0; fitsn = collections.Counter()
for t in range(V):
    best = None; nfit = 0
    for F in fr:
        if not F >> t & 1: continue
        mates = [e for e in bits(F) if e != t]
        c = 0
        for e in mates: c ^= (1 << e) ^ ((HYP[t] & HYP[e]) & ~rt(HYP[t] & HYP[e]))
        if best is None or pc(c) < best: best = pc(c)
        if any(c & ~r == 0 for r in SEC[t]): nfit += 1
    mins.append(best); fitsn[min(nfit, 5)] += 1
    if nfit: fits += 1
    print(t, g.kind[t], 'min |c|', best, 'frames whose c fits one section', nfit, flush=True)
print('min |c| distribution', sorted(collections.Counter(mins).items()))
print('targets with a fitting frame top:', fits, 'of', V, ' (#fitting frames capped at 5):', dict(fitsn))

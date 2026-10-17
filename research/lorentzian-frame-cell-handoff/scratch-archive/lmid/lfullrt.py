"""Fully routable plane sections (every line of S has a system cell inside S) per target, and the deficit
distribution |S| - |rt(S)| over all plane sections.  usage: lfullrt.py SYSTEM.json"""
import sys, os, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lw import V, g, bits, closure, FULL
HYP = g.HYP; pc = lambda m: bin(m).count('1')
cov = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}
cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in bits(cov[a])))
cells_of = {s: [C for C in cells if C >> s & 1] for s in range(V)}
def pm(m):
    r = FULL
    for s in bits(m): r &= HYP[s]
    return r
RT = {}
def rt(S):
    if S not in RT:
        r = 0
        for u in bits(S):
            if any(C & ~S == 0 for C in cells_of[u]): r |= 1 << u
        RT[S] = r
    return RT[S]
planes = set()
for t in range(V):
    for e in range(V):
        if e != t: planes.add(closure((1 << t) | (1 << e)))
defi = collections.Counter(); full_per_t = collections.Counter(); sizes = collections.Counter()
for Q in planes:
    S = pm(Q); d = pc(S) - pc(rt(S)); defi[min(d, 30)] += 1; sizes[pc(S)] += 1
    if d == 0:
        for t in bits(Q): full_per_t[t] += 1
print('plane sections', len(planes), 'section sizes', sorted(sizes.items()))
print('deficit |S|-|rt(S)| distribution', sorted(defi.items()))
print('targets with >=1 fully routable section', len(full_per_t), 'distribution', sorted(collections.Counter(full_per_t.values()).items()))

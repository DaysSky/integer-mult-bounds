"""For a system: per cell, the optimal 2-stream configuration of the refined screen (node choices), and statistics
of the chosen nodes: rank, #lines, #system cells inside, #targets served."""
import sys, os, json, collections
os.environ['GRP'] = '11'
import lsa3
from lbase import *
cov = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}
cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in bits(cov[a])))
cells_of = {s: [C for C in cells if C >> s & 1] for s in range(V)}
pc_ = lambda m: bin(m).count('1')
stat = collections.Counter(); nodes_used = collections.Counter()
for C in cells:
    s, a = list(bits(C))
    os_ = 0; oa_ = 0
    for c in cells_of[s]:
        if c != C: os_ |= lsa3.perpm(c)
    for c in cells_of[a]:
        if c != C: oa_ |= lsa3.perpm(c)
    PC = lsa3.perpm(C); Fs = PC & ~os_; Fa = PC & ~oa_
    D = Fs & Fa; S = Fs & ~Fa; A = Fa & ~Fs
    if not (D | S | A): stat['no forced'] += 1; continue
    best = None
    nodes = {}
    for x in range(V):
        if C >> x & 1: continue
        N = closure(C | (1 << x)); nodes[lsa3.perpm(N)] = N
    for q1, N1 in nodes.items():
        for q2, N2 in nodes.items():
            u = min((pc_(D & ~q1) + pc_(S & ~(q1 | q2)) + pc_(A & ~q1), 'sum+s'), (pc_(D & ~q1) + pc_(S & ~q1) + pc_(A & ~(q1 | q2)), 'sum+a'),
                    (pc_(D & ~(q1 & q2)) + pc_(S & ~q1) + pc_(A & ~q2), 's+a'))
            if best is None or u[0] < best[0]: best = (u[0], u[1], N1, N2)
    r, kind, N1, N2 = best
    nodes_used[N1] += 1
    stat[(kind, 'r=%d' % r, 'N1 lines %d rank %d cells %d nondeg %s' % (pc_(N1), g.closure(N1)[1], sum(1 for c in cells if c & ~N1 == 0), nondeg_span(N1)))] += 1
for k, v in sorted(stat.items(), key=lambda kv: -kv[1])[:20]: print(v, k)
print('distinct N1 nodes', len(nodes_used), 'max cells sharing one N1', max(nodes_used.values()))

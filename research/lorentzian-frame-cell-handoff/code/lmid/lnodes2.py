"""Node census for a one-level middle: candidate nodes N = closure(C u C') for pairs of system cells (and of triples
from the best pairs).  For each N: c = #system cells inside N (max one-level inputs = 2c registers), a = #lines covered
by those cells, b = #lines in perp(N) (the only targets N's content can ever reach), rank.  A one-level node with k
input registers emits k outputs, each serving <= 3 targets in perp(N) and carrying content on <= a lines.
Prints the joint distribution and the best nodes by min(2c, 3b)*a-type usefulness.
usage: lnodes2.py SYSTEM.json"""
import sys, os, json, collections, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lcell'))
os.environ['GRP'] = '11'
from lbase import V, bits, HYP, closure, perp, g
pc = lambda m: bin(m).count('1')
cov = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}
cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in bits(cov[a])))
cellset = set(cells)
nodes = {}
for i, C in enumerate(cells):
    for D in cells[i + 1:]:
        N = closure(C | D)
        if N not in nodes: nodes[N] = None
print('distinct pair-closure nodes', len(nodes), flush=True)
rows = []
for N in nodes:
    ins = [C for C in cells if C & ~N == 0]
    a = 0
    for C in ins: a |= C
    b = pc(perp(N))
    rows.append((N, len(ins), pc(a), b, g.dim(N)))
dist = collections.Counter((r[4], min(r[1], 20) // 2 * 2, min(r[3], 60) // 5 * 5) for r in rows)
print('rank, cells(binned), perp lines(binned) -> count:')
for k in sorted(dist): print('  ', k, dist[k])
# usefulness: incidences per register upper bound with k = 2c inputs: min(a, 2k?) ...
best = sorted(rows, key=lambda r: -min(r[2], 2 * 2 * r[1]) * min(r[3], 3 * 2 * r[1]) / (2 * r[1]))[:15]
print('top nodes by per-register incidence bound (cells, lines, perp, rank, bound/reg):')
for N, c, a, b, rk in best: print('  ', c, a, b, rk, round(min(a, 4 * c) * min(b, 6 * c) / (2 * c), 1))
json.dump([[hex(N), c, a, b, rk] for N, c, a, b, rk in rows], open('lnodes2_rows.json', 'w'))

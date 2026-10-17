"""Group covers for I_{n,1}: vectors z (non-null, in the ambient w-perp) whose perps T_z = {lines perp z} cover all lines.
Candidates: z = (b; c) with b in small integer patterns (symmetry-reduced by sorted multiplicities), c = sum(b)/3.
Lines: P(ij) perp z iff b_i = b_j; T(ijk) perp z iff b_i+b_j+b_k = c.  norm(z) = sum b^2 - c^2."""
import itertools, sys
from fractions import Fraction as Fr
n = int(sys.argv[1]) if len(sys.argv) > 1 else 11
vals = [-2, -1, 0, 1, 2, 3]
P = list(itertools.combinations(range(n), 2)); T = list(itertools.combinations(range(n), 3))
L = len(P) + len(T)
cands = {}
# patterns: value multiset assignments up to S_n -> we need actual labelled vectors for covers; use composition by blocks
# enumerate b as non-decreasing sequences (canonical), store coverage as frozenset of line ids after applying all
# permutations is too costly; instead for covers we will later permute.  Here: evaluate canonical b only.
def cover_of(b):
    c = Fr(sum(b), 3)
    s = set()
    for k, (i, j) in enumerate(P):
        if b[i] == b[j]: s.add(k)
    for k, (i, j, l) in enumerate(T):
        if b[i] + b[j] + b[l] == c: s.add(len(P) + k)
    nrm = sum(x*x for x in b) - c*c
    return s, nrm, c
best = []
for b in itertools.combinations_with_replacement(vals, n):
    if len(set(b)) == 1: continue
    s, nrm, c = cover_of(b)
    if nrm == 0: continue
    best.append((len(s), b, nrm, c))
best.sort(reverse=True)
print('top canonical z by coverage (n=%d, %d lines):' % (n, L))
seen = set()
for cnt, b, nrm, c in best[:25]:
    print(cnt, b, 'norm', nrm, 'c', c)

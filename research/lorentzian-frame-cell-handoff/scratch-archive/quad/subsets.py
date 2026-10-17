"""F2^10 = even subsets of [11] with w(A,B) = |A cap B| mod 2.  Test orthogonal representability in C^h of the
graph {A != B : |A cap B| even} on a chosen family of even subsets."""
import itertools, sys, numpy as np
from orthrep import solve
fam = [int(k) for k in sys.argv[1].split(',')]; h = int(sys.argv[2]); seeds = int(sys.argv[3]); iters = int(sys.argv[4])
S = [frozenset(c) for k in fam for c in itertools.combinations(range(11), k)]
n = len(S)
E = [(i, j) for i in range(n) for j in range(i+1, n) if len(S[i] & S[j]) % 2 == 0]
print('family sizes', fam, 'n', n, 'edges', len(E), 'h', h, flush=True)
for sd in range(seeds):
    r, x, t = solve(n, E, h, seed=sd, iters=iters)
    print('seed', sd, 'residual %.3e' % r, '%.0fs' % t, flush=True)

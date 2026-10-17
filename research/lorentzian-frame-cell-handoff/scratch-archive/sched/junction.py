"""Schedules with bridges only at block junctions (pair j finished, pair j+1 about to start: both at the same level,
both wires at existing vertices -> no idle split), plus free bridges at the start/end.  Symplectic structure: start/end
bridges diag(A, A^-T) can complete the identity iff the middle product W has zero X->X and Y->Y blocks.
Search: block lengths (n_0..n_3) summing to 9, F/R sequences per block, junction bridge words (pairs j, j+1 only)."""
import itertools, numpy as np, sys
from edgebridge import op_local, op_bridge, compose, K
X = [0, 2, 4, 6]; Y = [1, 3, 5, 7]
def ok(W):
    return not W[np.ix_(X, X)].any() and not W[np.ix_(Y, Y)].any()
maxj = int(sys.argv[1]) if len(sys.argv) > 1 else 2
jgen = lambda j: [(j, j + 1, 1), (j, j + 1, -1), (j + 1, j, 1), (j + 1, j, -1)]
def jwords(j):
    out = []
    for L in range(maxj + 1):
        for w in itertools.product(jgen(j), repeat=L): out.append(w)
    return out
JW = [jwords(j) for j in range(K - 1)]
sols = []
for lens in itertools.product(range(1, 5), repeat=K):
    if sum(lens) != 9: continue
    for orients in itertools.product(*[list(itertools.product((False, True), repeat=n)) for n in lens]):
        blocks = [compose([op_local(p, r) for r in orients[p]]) for p in range(K)]
        # incremental: W = S3 J23 S2 J12 S1 J01 S0
        for w01 in JW[0]:
            A1 = compose([op_bridge(*b) for b in w01]) @ blocks[0]
            A1 = blocks[1] @ A1
            for w12 in JW[1]:
                A2 = blocks[2] @ compose([op_bridge(*b) for b in w12]) @ A1
                for w23 in JW[2]:
                    W = blocks[3] @ compose([op_bridge(*b) for b in w23]) @ A2
                    if ok(W):
                        sols.append((lens, orients, w01, w12, w23))
                        if len(sols) <= 5: print('SOLUTION', lens, ['%s' % ''.join('R' if r else 'F' for r in o) for o in orients], w01, w12, w23, flush=True)
print('solutions', len(sols), 'maxj', maxj)

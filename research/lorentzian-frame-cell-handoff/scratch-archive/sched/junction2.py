"""Focused: block lengths (3,1,2,3) and (3,2,1,3); end blocks must be signed swaps (FRF or RFR, proven necessary);
junction bridge words up to length maxj between pairs j, j+1 (coefficients in {-2..2}).  Condition: middle product
has zero X->X and Y->Y blocks."""
import itertools, numpy as np, sys
from edgebridge import op_local, op_bridge, compose, K
X = [0, 2, 4, 6]; Y = [1, 3, 5, 7]
ok = lambda W: not W[np.ix_(X, X)].any() and not W[np.ix_(Y, Y)].any()
maxj = int(sys.argv[1]); C = [c for c in range(-2, 3) if c]
jgen = lambda j: [(j, j + 1, c) for c in C] + [(j + 1, j, c) for c in C]
def jw(j):
    seen = {}
    for L in range(maxj + 1):
        for w in itertools.product(jgen(j), repeat=L):
            M = compose([op_bridge(*b) for b in w]); seen.setdefault(M.tobytes(), M)
    return list(seen.values())
JW = [jw(j) for j in range(K - 1)]
print('distinct junction matrices', [len(x) for x in JW], flush=True)
sw = [(False, True, False), (True, False, True)]
n = 0
for lens in ((3, 1, 2, 3), (3, 2, 1, 3)):
    mids = [list(itertools.product((False, True), repeat=l)) for l in lens[1:3]]
    for o0 in sw:
        for o3 in sw:
            for o1 in mids[0]:
                for o2 in mids[1]:
                    S = [compose([op_local(p, r) for r in o]) for p, o in enumerate((o0, o1, o2, o3))]
                    for J0 in JW[0]:
                        A1 = S[1] @ J0 @ S[0]
                        for J1 in JW[1]:
                            A2 = S[2] @ J1 @ A1
                            for J2 in JW[2]:
                                W = S[3] @ J2 @ A2
                                if ok(W):
                                    n += 1
                                    if n <= 5: print('SOLUTION', lens, o0, o1, o2, o3, flush=True)
print('solutions', n, flush=True)

"""Double-star condition in F2 terms: centres c_1..c_9 nonsingular, affinely independent, sum c_k = 0; B-dual vectors
b_j (B(b_j, c_k) = 1 + delta_jk) all nonsingular -> partners p'_j.  Construct directly and evaluate."""
import sys, random, numpy as np
from e8dec import G, v, A
from dstar import N, evaluate, aff_indep
ORTH = (G == 0)
rng = random.Random(int(sys.argv[1])); found = 0; best = None; tries = 0
# class of a line = its row of N (affine function); sums of classes <-> XOR of (N rows + all-ones)?  Work with lines:
# c_9 = c_1 + ... + c_8 : find line x whose N-row equals the XOR of the 8 N-rows (odd count of affine fns -> affine fn)
rowkey = {N[t].tobytes(): t for t in range(v)}
for tries in range(int(sys.argv[2])):
    Z = rng.sample(range(v), 8)
    acc = np.zeros(v, np.uint8)
    for z in Z: acc ^= N[z]
    acc ^= 1   # sum of 8 (even) affine functions ell_z = (c_z, 1) is (sum c, 0); ell of the sum class = 1 + that
    x = rowkey.get(acc.tobytes())
    if x is None or x in Z: continue
    Z9 = Z + [x]
    if not aff_indep(Z9): continue
    # partners: lines y with y _|_ p_j and y non-orth to the other centres
    Pp = []
    for j, pj in enumerate(Z9):
        cand = [y for y in range(v) if ORTH[y, pj] and y != pj and all(G[y, pk] != 0 for k, pk in enumerate(Z9) if k != j)]
        if len(cand) != 1: break
        Pp.append(cand[0])
    if len(Pp) < 9: continue
    found += 1
    ok, nl, costs = evaluate(Z9, Pp)
    val = 8 * nl - 9 * sum(costs)
    if best is None or val > best[0]:
        best = (val, Z9, Pp)
        print('double star: live %d, piece costs %s = %d, decomposition ok %s, value %d (P111 321)' % (nl, costs, sum(costs), ok, val), flush=True)
        np.save('dstar_best.npy', np.array([Z9, Pp]))
print('tries', tries + 1, 'found', found)

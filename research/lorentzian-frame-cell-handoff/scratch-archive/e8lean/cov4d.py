"""Structure of the E8 4-covers (D5,D5,D5,A5) of R(t): the perps X1,X2,X3 (A3s through t) and Z (A2xA1 through t).
Reports intersections, the 6 triple-covered lines, how the lines of the X's and Z relate, and the span of X1+X2+X3+Z."""
import sys, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
V = e8.V; GI = e8.GI; t = 0; P = e8.HYP[t]
pc = lambda m: bin(m).count('1')
def perpmask(F):
    m = (1 << V) - 1
    for s in e8.bits(F): m &= e8.HYP[s]
    return m
# rank-3 flats through t with 6 lines (A3) or 4 lines (A2xA1)
X6, X4 = set(), set()
for a in range(1, V):
    for b in range(a + 1, V):
        F, d = e8.closure((1 << t) | (1 << a) | (1 << b))
        if d == 3:
            if pc(F) == 6: X6.add(F)
            elif pc(F) == 4: X4.add(F)
X6 = sorted(X6); X4 = sorted(X4)
print('A3s through t', len(X6), ' A2xA1 through t', len(X4))
c6 = {F: perpmask(F) & P for F in X6}; c4 = {F: perpmask(F) & P for F in X4}
print('D5 sizes', set(pc(v) for v in c6.values()), 'A5 sizes', set(pc(v) for v in c4.values()))
covers = []
for i, j, k in itertools.combinations(range(len(X6)), 3):
    m = c6[X6[i]] | c6[X6[j]] | c6[X6[k]]
    rem = P & ~m
    if pc(rem) > 15: continue
    for Z in X4:
        if rem & ~c4[Z] == 0:
            covers.append((X6[i], X6[j], X6[k], Z))
print('covers (all D5 triples):', len(covers))
stat = collections.Counter()
for X1, X2, X3, Z in covers:
    Xs = [X1, X2, X3]
    inter = tuple(sorted(pc(A & B) for A, B in itertools.combinations(Xs, 2)))
    zx = tuple(sorted(pc(Z & A) for A in Xs))
    tri = c6[X1] & c6[X2] & c6[X3]
    allx = X1 | X2 | X3 | Z
    stat[(inter, zx, pc(tri), pc(allx), e8.dim(allx), e8.dim(X1 | X2 | X3))] += 1
for k, n in stat.items():
    print('  Xi^Xj lines', k[0], ' Z^Xi lines', k[1], ' triple-covered', k[2], ' |union of flats|', k[3], ' rank', k[4], ' rank X1+X2+X3', k[5], ':', n)
X1, X2, X3, Z = covers[0]
print('example: X lines', [e8.bits(X) for X in (X1, X2, X3)], 'Z', e8.bits(Z))
print('  pairwise Gram between X1-lines and X2-lines:', [[int(GI[a, b]) for b in e8.bits(X2)] for a in e8.bits(X1)])
print('  Z lines Gram:', [[int(GI[a, b]) for b in e8.bits(Z)] for a in e8.bits(Z)])

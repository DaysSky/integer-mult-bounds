"""Role of t inside Z (= perp of the A5 in its 4-cover): A1 factor (t perp the other 3 lines of Z) or A2 part?"""
import sys, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
V = e8.V; GI = e8.GI; t = 0; P = e8.HYP[t]
pc = lambda m: bin(m).count('1')
def perpmask(F):
    m = (1 << V) - 1
    for s in e8.bits(F): m &= e8.HYP[s]
    return m
X6, X4 = set(), set()
for a in range(1, V):
    for b in range(a + 1, V):
        F, d = e8.closure((1 << t) | (1 << a) | (1 << b))
        if d == 3:
            if pc(F) == 6: X6.add(F)
            elif pc(F) == 4: X4.add(F)
X6 = sorted(X6); X4 = sorted(X4)
role = lambda Z: 'A1' if all(GI[t, s] == 0 for s in e8.bits(Z) if s != t) else 'A2'
print('A2xA1 through t by role:', collections.Counter(role(Z) for Z in X4))
c6 = {F: perpmask(F) & P for F in X6}; c4 = {F: perpmask(F) & P for F in X4}
cnt = collections.Counter()
for i, j, k in itertools.combinations(range(len(X6)), 3):
    m = c6[X6[i]] | c6[X6[j]] | c6[X6[k]]
    rem = P & ~m
    if pc(rem) > 15: continue
    for Z in X4:
        if rem & ~c4[Z] == 0: cnt[role(Z)] += 1
print('covers by role of t in Z:', dict(cnt))

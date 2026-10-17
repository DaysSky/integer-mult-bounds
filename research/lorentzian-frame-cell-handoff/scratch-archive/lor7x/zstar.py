"""Cover the star of point 0 in I_{11,1} (P(0x), T(0xy)) by perps of non-null ambient vectors z = (b; sum(b)/3)."""
import itertools
from fractions import Fraction as Fr
n = 11; vals = [-3, -2, -1, 0, 1, 2, 3]
star = [('P', x) for x in range(1, n)] + [('T', x, y) for x, y in itertools.combinations(range(1, n), 2)]
def cov(b):
    c = Fr(sum(b), 3); nrm = sum(x*x for x in b) - c*c
    if nrm == 0: return None
    s = 0
    for k, l in enumerate(star):
        if l[0] == 'P': ok = b[l[1]] == b[0]
        else: ok = b[0] + b[l[1]] + b[l[2]] == c
        if ok: s |= 1 << k
    return s
res = {}
for b0 in vals:
    for rest in itertools.combinations_with_replacement(vals, n - 1):
        b = (b0,) + rest
        s = cov(b)
        if s is None: continue
        res[b] = s
print('patterns', len(res))
top = sorted(res.items(), key=lambda kv: -bin(kv[1]).count('1'))[:15]
for b, s in top: print(bin(s).count('1'), b)
# pairs of labelled vectors covering star: permute the 10 rest-coordinates of the second vector freely.
# Approach: for first vector b (canonical), the uncovered set U; need second labelled vector covering U.
full = (1 << len(star)) - 1
import random
found = 0
cands = sorted(res.items(), key=lambda kv: -bin(kv[1]).count('1'))[:400]
def permuted_cover(b, perm):
    bb = (b[0],) + tuple(b[1 + perm[i]] for i in range(n - 1))
    return cov(bb), bb
for b1, s1 in cands[:60]:
    U = full & ~s1
    for b2, _ in cands:
        # try random relabelings of b2's rest coordinates
        for _ in range(300):
            perm = list(range(n - 1)); random.shuffle(perm)
            s2, bb2 = permuted_cover(b2, perm)
            if s2 is not None and (s2 & U) == U:
                print('PAIR covers star:', b1, bb2); found += 1; break
        if found: break
    if found: break
print('found', found)

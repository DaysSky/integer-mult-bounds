"""Integral non-root-like realisation attempt of the O^-(8,2) singular quadric (119) in L = E8 (+) <-2>.
Points: q'(x) = q(x) + B(r,x) = 0 with r a root class: 56 root classes y (y.r odd) and 63 norm-4 classes x
(B(r,x)=0, q(x)=0).  Realise the 56 as roots (m=0).  A norm-4 class x needs e_x in x + 2E8 orthogonal to every root y
of the 56 collinear with x (B(x,y) = 0).  Report the span of those roots and the allowed lifts."""
import itertools, numpy as np
from fractions import Fraction
def e8_vectors(norm):
    out = []; target = 4 * norm
    def rec(pre, s):
        if len(pre) == 8:
            if s == target and (all(x % 2 == 0 for x in pre) or all(x % 2 for x in pre)) and sum(pre) % 4 == 0: out.append(tuple(pre))
            return
        for x in range(-6, 7):
            if s + x*x <= target: rec(pre + [x], s + x*x)
    rec([], 0); return out
R = [v for v in e8_vectors(2) if v > tuple(-a for a in v)]   # 120 lines, doubled coords
dot = lambda a, b: sum(x*y for x, y in zip(a, b)) // 4
r = R[0]
Y = [y for y in R if dot(y, r) % 2]            # 56 roots with odd product with r
print('root r', r, '| 56 roots:', len(Y))
N4 = e8_vectors(4)
# class of a vector mod 2E8: doubled coords v ~ v' iff (v - v')/2 in 2E8 doubled... use representation: v mod 2E8 <-> (v/2 mod E8)
def in_E8(v):   # doubled coords v (=2*true); true vector v/2 in E8 iff v/2... use: w = v (doubled of true t): t in E8 iff entries all even or all odd and sum%4==0
    return (all(x % 2 == 0 for x in v) or all(x % 2 for x in v)) and sum(v) % 4 == 0
def same_class(a, b):   # true a - b in 2E8  <=>  (a-b)/2 in E8 (true coords): doubled of (a-b)/2 is (a-b)/2 in doubled units
    d = tuple(x - y for x, y in zip(a, b))
    if any(x % 2 for x in d): return False
    return in_E8(tuple(x // 2 for x in d))
# norm-4 classes with B(r,x) = 0 (r.x even): group N4 by class
cls = []
for v in N4:
    if dot(v, r) % 2: continue
    for c in cls:
        if same_class(v, c[0]): c.append(v); break
    else: cls.append([v])
print('norm-4 classes with B(r,x)=0:', len(cls), 'sizes', set(len(c) for c in cls))
# for each class: roots y in Y collinear (B = dot mod 2 = 0)
B = lambda a, b: dot(a, b) % 2
spans = []
for c in cls:
    x = c[0]
    col = [y for y in Y if B(x, y) == 0]
    M = np.array(col, float); rk = np.linalg.matrix_rank(M) if col else 0
    ok = [v for v in c if all(dot(v, y) == 0 for y in col)]
    spans.append((len(col), rk, len(ok)))
import collections
print('per class (#collinear 56-roots, their rank, #norm-4 lifts orthogonal to all):', collections.Counter(spans))

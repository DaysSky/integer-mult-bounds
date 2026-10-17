import time, random, itertools
from lgeo import *
random.seed(1)
# test: random masks and random permutations give the same canonical form
for trial in range(30):
    m = 0
    for s in random.sample(range(V), random.randint(1, 30)): m |= 1 << s
    m2 = 0
    for s in random.sample(range(V), 5): m2 |= 1 << s
    perm = list(range(11)); random.shuffle(perm)
    a = canon((m, m2))[0]; b = canon((act(m, perm), act(m2, perm)))[0]
    assert a == b, trial
# symmetric: D5 hub
P = lambda i, j: g.P(i, j); T = lambda *a: g.T(*a)
A = [0, 1, 2, 3, 4]; p = 10
h = 0
for i, j in itertools.combinations(A, 2): h |= (1 << P(i, j)) | (1 << T(i, j, p))
t0 = time.time(); c = canon((h,)); print('D5 hub canon %.3fs' % (time.time() - t0))
t0 = time.time(); c = canon((pm(h),)); print('perp canon %.3fs' % (time.time() - t0))
t0 = time.time(); c = canon((FULL,)); print('FULL canon %.3fs' % (time.time() - t0))
print('ok')

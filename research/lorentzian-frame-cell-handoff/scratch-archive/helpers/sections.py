import sys, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
V = e8.V
subs = e8.all_subspaces()
print({d: len(s) for d, s in subs.items()})
t = 0
Ht = e8.HYP[t]
sec = [m for m in subs[6] if m & ~Ht == 0]
types = collections.Counter()
for m in sec:
    nl = e8.popcount(m)
    share = e8.popcount(e8.perp(m))      # lines orthogonal to the whole section = targets that can use it
    types[(nl, share)] += 1
print('6-dim flats inside t^perp (lines, #targets sharing):', dict(types))
# 5-dim flats inside t^perp
sec5 = [m for m in subs[5] if m & ~Ht == 0]
t5 = collections.Counter((e8.popcount(m), e8.popcount(e8.perp(m))) for m in sec5)
print('5-dim flats inside t^perp:', dict(t5))

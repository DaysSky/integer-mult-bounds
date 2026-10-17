"""6-dim root-spanned flats inside t^perp, grown level by level from the 63 lines of t^perp."""
import sys, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
V = e8.V
t = 0
H = e8.bits(e8.HYP[t])
level = {1: {1 << s for s in H}}
for d in range(2, 7):
    nxt = set()
    for m in level[d-1]:
        for s in H:
            if m >> s & 1: continue
            cm, k = e8.closure(m | (1 << s))
            if k == d: nxt.add(cm)
    level[d] = nxt
    print('dim', d, 'flats inside t^perp:', len(nxt), flush=True)
types = collections.Counter((e8.popcount(m), e8.popcount(e8.perp(m))) for m in level[6])
print('6-dim sections (lines, #targets sharing):', dict(types))

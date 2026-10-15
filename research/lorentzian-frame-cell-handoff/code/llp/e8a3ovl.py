import sys, json, itertools, collections
exec(open('e8a3quad.py').read().split('# candidate nodes')[0])
srcA3 = {int(k): int(v, 16) for k, v in sol['src'].items()}
def planes_t(t):
    X = srcA3[t]
    tris = [T for T in tri if T >> t & 1 and T & ~X == 0]
    prs = [P for P in pair if P >> t & 1]
    return tris + prs
ov = collections.Counter(); bl = collections.Counter()
for t in range(V):
    pls = planes_t(t)
    cnt = collections.Counter()
    for P in pls:
        for C in pieces[P]: cnt[C] += 1
    ov[tuple(sorted(collections.Counter(cnt.values()).items()))] += 1
    # complementary-block content: B' of t's block in all three sections?
    i = blk[t]
    bl[sum(1 for P in pls if blocks[comp[i]] & ~pm(P) == 0)] += 1
print('per target: multiplicity distribution of pieces over its 3 sections (mult -> #pieces):')
for k, v in ov.most_common(6): print('   ', k, v)
print('B-complement contained in how many of t sections:', bl)
t = 0
pls = planes_t(t)
mult = collections.Counter()
for P in pls:
    for u in bits(pm(P)): mult[u] += 1
print('target 0: section sizes', [pc(pm(P)) for P in pls], 'line multiplicity dist', collections.Counter(mult.values()),
      '|R(t)|', pc(HYP[t]), 'lines of R(t) not covered', [u for u in bits(HYP[t]) if mult[u] == 0])
X = 0
for P in pls: X ^= pm(P)
print('XOR == R(t) + one line:', pc(X ^ HYP[t]))

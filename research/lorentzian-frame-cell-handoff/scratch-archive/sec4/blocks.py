"""Structure of the design relative to its 10 'full' D4s (12 cells inside, 12 sections in the perp)."""
from common import *
D4 = load_d4()
full = []
for W in D4:
    Wp = perpmask(W)
    ci = [P for P in planes if P & ~W == 0]; so = [Q for Q in planes if Q & ~Wp == 0]
    if len(ci) == 12 and len(so) == 12: full.append(W)
print('full D4s', len(full), 'disjoint?', all(a & b == 0 for i, a in enumerate(full) for b in full[i+1:]),
      'union all lines?', bin(sum(full)).count('1') if all(a & b == 0 for i, a in enumerate(full) for b in full[i+1:]) else None)
print('perp pairs:', sorted(set(tuple(sorted((full.index(W), full.index(perpmask(W) & ((1<<V)-1)))) ) for W in full if perpmask(W) in full)))
blk = {s: k for k, W in enumerate(full) for s in e8.bits(W)}
inside = collections.Counter(); cross = collections.Counter()
for P in planes:
    bs = set(blk[s] for s in e8.bits(P))
    if len(bs) == 1: inside[pc(P)] += 1
    else: cross[(pc(P), len(bs))] += 1
print('planes inside a block by size', dict(inside), ' crossing (size, #blocks):', dict(cross))
# per block: inside planes types
for k, W in enumerate(full[:2]):
    ci = [P for P in planes if P & ~W == 0]
    print('block', k, 'inside planes sizes', collections.Counter(pc(P) for P in ci))

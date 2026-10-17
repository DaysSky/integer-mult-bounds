"""Block structure of sections and private sets for the D4-partition design."""
from common import *
D4 = load_d4()
full = [W for W in D4 if len([P for P in planes if P & ~W == 0]) == 12 and len([Q for Q in planes if Q & ~perpmask(W) == 0]) == 12]
blk = {s: k for k, W in enumerate(full) for s in e8.bits(W)}
comp = {k: full.index(perpmask(W)) for k, W in enumerate(full)}
for t in [0, 2]:
    B = blk[t]; Bc = comp[B]
    mine = [Q for Q in planes if Q >> t & 1]
    secs = [perpmask(Q) & e8.HYP[t] for Q in mine]
    print('target', t, 'block', B, 'comp', Bc, ' R(t) by block:', dict(collections.Counter(blk[s] for s in e8.bits(e8.HYP[t]))))
    for k, Q in enumerate(mine):
        oth = 0
        for j in range(4):
            if j != k: oth |= secs[j]
        priv = secs[k] & ~oth
        print('  sec', 'pair' if pc(Q) == 2 else 'A2  ', 'users blocks', [blk[u] for u in e8.bits(Q)],
              'lines by block', dict(sorted(collections.Counter(blk[s] for s in e8.bits(secs[k])).items())),
              'priv by block', dict(collections.Counter(blk[s] for s in e8.bits(priv))), 'priv rank', e8.dim(priv))
    # multiplicity of each line of R(t) across t's 4 sections, by block
    mult = collections.Counter()
    for s in e8.bits(e8.HYP[t]):
        mult[(('own' if blk[s] == B else 'comp' if blk[s] == Bc else 'other'), sum(1 for x in secs if x >> s & 1))] += 1
    print('  (block kind, #sections containing line):', dict(sorted(mult.items())))

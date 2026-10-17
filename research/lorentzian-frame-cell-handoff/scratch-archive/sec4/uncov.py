"""Which (t,s) pairs are uncovered in the best symmetric exact routing, and their structural type."""
import json
from common import *
D4 = load_d4()
full = [W for W in D4 if len([P for P in planes if P & ~W == 0]) == 12 and len([Q for Q in planes if Q & ~perpmask(W) == 0]) == 12]
blk = {s: k for k, W in enumerate(full) for s in e8.bits(W)}
comp = {k: full.index(perpmask(W)) for k, W in enumerate(full)}
rt = json.load(open('routing_s1_k0.json'))
Y = [(int(P, 16), int(W, 16)) for P, W in rt['Y']]; Z = [(int(W, 16), int(Q, 16)) for W, Q in rt['Z']]
ins = collections.defaultdict(list); outs = collections.defaultdict(list)
for P, W in Y: ins[W].append(P)
for W, Q in Z: outs[W].append(Q)
print('quads used', len(ins), 'n_W', collections.Counter(len(v) for v in ins.values()),
      'full-block quads used', sum(1 for W in ins if W in full))
kinds = collections.Counter(); tot = collections.Counter()
for t in reps:
    mine = [Q for Q in planes if Q >> t & 1]
    secs = {Q: perpmask(Q) & e8.HYP[t] for Q in mine}
    avail = collections.defaultdict(int)
    for W, Ps in ins.items():
        lines = 0
        for P in Ps: lines |= P
        for Q in outs[W]:
            if Q in secs: avail[Q] |= lines & W
    for s in e8.bits(e8.HYP[t]):
        nsec = [Q for Q in mine if secs[Q] >> s & 1]
        kind = ('own' if blk[s] == blk[t] else 'comp' if blk[s] == comp[blk[t]] else 'other', len(nsec),
                'priv-pair' if len(nsec) == 1 and pc(nsec[0]) == 2 else 'priv-A2' if len(nsec) == 1 else 'shared')
        tot[kind] += 1
        if not any(avail[Q] >> s & 1 for Q in mine): kinds[kind] += 1
print('uncovered by kind:', dict(kinds)); print('totals by kind:', dict(tot))

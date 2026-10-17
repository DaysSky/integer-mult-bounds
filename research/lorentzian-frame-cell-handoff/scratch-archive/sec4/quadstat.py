"""For the Z15 4-plane design: verify every line's 4 sections are an all-proper cover; then for every D4 W of E8
count design planes inside W (cells) and inside W-perp (sections), and the lines of W covered by inner cells."""
import sys, json, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
V = e8.V; GI = e8.GI
pc = lambda m: bin(m).count('1')
planes = [int(h, 16) for h in json.load(open('design.json'))['planes']]
def perpmask(F):
    m = (1 << V) - 1
    for s in e8.bits(F): m &= e8.HYP[s]
    return m
bad = 0; priv = collections.Counter()
for t in range(V):
    mine = [F for F in planes if F >> t & 1]
    assert len(mine) == 4
    secs = [perpmask(F) & e8.HYP[t] for F in mine]
    u = 0
    for s in secs: u |= s
    if u != e8.HYP[t]: bad += 1; continue
    for k in range(4):
        oth = 0
        for j in range(4):
            if j != k: oth |= secs[j]
        P = secs[k] & ~oth
        if not P or e8.dim(P) == e8.dim(secs[k]): bad += 1
        priv[(pc(mine[k]), pc(P))] += 1
print('lines with invalid covers:', bad, ' private sizes by plane size:', dict(priv))
orth = [set(e8.ORTH[a]) for a in range(V)]
D4 = set()
for a in range(V):
    for b in orth[a]:
        if b <= a: continue
        for c in orth[a] & orth[b]:
            if c <= b: continue
            for d in orth[a] & orth[b] & orth[c]:
                if d <= c: continue
                F, r = e8.closure((1 << a) | (1 << b) | (1 << c) | (1 << d))
                if pc(F) == 12: D4.add(F)
D4 = sorted(D4)
stat = collections.Counter(); rows = []
for W in D4:
    Wp = perpmask(W)
    cells = [P for P in planes if P & ~W == 0]
    secs = [Q for Q in planes if Q & ~Wp == 0]
    covered = 0
    for P in cells: covered |= P
    stat[(len(cells), len(secs), pc(covered))] += 1
    rows.append((len(cells), len(secs), pc(covered)))
for k, n in sorted(stat.items(), key=lambda kv: -kv[0][0] * kv[0][1])[:15]: print('  (#cells in W, #sections fed possible, lines covered by cells):', k, n)

# Verify: R(t) = XOR over hubs h with t in D10(h) of (D10(h) n t-perp), for every target t.
import sys
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, bits, V
D10 = []
for h in range(11):
    m = 0
    for u in range(V):
        s = g.supp[u]
        if (g.kind[u] == 'P' and h not in s) or (g.kind[u] == 'T' and h in s): m |= 1 << u
    D10.append(m)
ok = 0
for t in range(V):
    acc = 0; hubs = [h for h in range(11) if D10[h] >> t & 1]
    for h in hubs: acc ^= D10[h] & g.HYP[t]
    ok += acc == g.HYP[t]
    assert len(hubs) == (9 if g.kind[t] == 'P' else 3)
print('targets with R(t) = XOR of D10 pieces:', ok, 'of', V, '| D10 sizes', set(bin(m).count('1') for m in D10))

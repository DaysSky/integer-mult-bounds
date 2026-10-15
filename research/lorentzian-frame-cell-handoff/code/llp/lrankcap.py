"""EXHAUSTIVE rank capacity lemma.  For t = T(0,1,2): U = the 84 lines T(x,y,z) of R(t) with x in {0,1,2}, y,z in D.
For t = P(0,1): U = the 84 lines T(xyz) with xyz inside the 9-set.  Enumerate all span-closed subsets of U of rank
<= K (closure growth, lclosed.py) and report the maximum size per rank.  If 4 * max(rank <= 6) < 84, every line has
a part of rank >= 7 in any 4-section design (parts partition, or odd-cover, R(t)).  usage: lrankcap.py K"""
import sys
from lgeo import *
from lclosed import closed_sets
K = int(sys.argv[1])
for kind in (__import__('os').environ.get('KINDS', 'TP')):
    if kind == 'T':
        t = IDX[('T', (0, 1, 2))]
        U = sum(1 << s for s in bits(HYP[t]) if KIND[s] == 'T')
    else:
        t = IDX[('P', (0, 1))]
        U = sum(1 << s for s in bits(HYP[t]) if KIND[s] == 'T' and not ({0, 1} & set(SUPP[s])))
    lv = closed_sets(U, K)
    print(kind, 'U lines', pc(U), 'rank', rank(U), '| max lines in closed subsets of rank k:', {k: max(pc(S) for S in lv[k]) for k in lv}, flush=True)

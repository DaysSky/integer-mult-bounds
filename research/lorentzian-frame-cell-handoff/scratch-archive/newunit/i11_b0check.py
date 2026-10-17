import sys, itertools, numpy as np, time
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V
from codescore import System, independent
S = System(g.G)
lab = np.array([[(g.binlabel(t) >> i) & 1 for i in range(11)] for t in range(V)])
D10 = [sum(1 << t for t in range(V) if lab[t, i]) for i in range(11)]
t0 = time.time(); r = S.rows(D10)
print('B0 code: feasible', all(x is not None for x in r), 'row weights min/max', min(r), max(r), 'load', sum(x - 1 for x in r), '%.1fs' % (time.time() - t0))

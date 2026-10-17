import pickle, numpy as np
from dfam import LINES, IDX, NO, n, v, check
from flats import shift
flats = pickle.load(open('flats.pkl', 'rb'))
for rmax in range(3, 10):
    pcs = {}
    for f in flats:
        if f[0] > rmax: continue
        for a in range(n):
            p = shift(f[1], a); pcs[tuple(sorted(p))] = p
    pcs = list(pcs.values())
    ok, bad, _ = check(pcs, want_rows=False)
    print('all structured flats of rank <= %d (%d pieces): served all %s, unserved targets %d' % (rmax, len(pcs), ok, bad), flush=True)

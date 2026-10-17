import gzip, json, sys, numpy as np
from collections import defaultdict
w = json.load(gzip.open(sys.argv[1], 'rt'))
v, R = w['v'], w['R']; n = 2*v + R
L = np.array(w['lines'], dtype=float); fr = w['frames']
fdim = [int(np.linalg.matrix_rank(L[f])) if f else 0 for f in fr]
def rk(fids):
    idx = sorted(set(i for f in fids for i in fr[f])); return int(np.linalg.matrix_rank(L[idx])) if idx else 0
def sub(a, b): return rk([a, b]) == fdim[b]
role = lambda r: 'x%d' % r if r < v else ('y%d' % (r-v) if r < 2*v else 'h%d' % r)
# per-register event timeline: (phase, idx, frame, kind, other)
ev = defaultdict(list)
for name in ('D', 'A', 'B'):
    for k, (f, d, srcs) in enumerate(w[name]):
        ev[d].append((name, k, f, 'write', srcs))
        for s in srcs: ev[s].append((name, k, f, 'read-by', d))
for q in w['ret']:
    print('=== total', role(q))
    for e in ev[q]:
        print('   ', e[0], e[1], 'frame', e[2], 'rank', fdim[e[2]], e[3], [role(x) for x in (e[4] if isinstance(e[4], list) else [e[4]])])
    # what happens to the registers tau read, after the read
    for e in ev[q]:
        if e[3] != 'write': continue
        for s in e[4]:
            later = [x for x in ev[s] if (x[0], x[1]) > (e[0], e[1]) or (x[0] == 'B' and e[0] == 'A')]
            later = [x for x in ev[s] if ('DAB'.index(x[0]), x[1]) > ('DAB'.index(e[0]), e[1])]
            print('      after tau read', role(s), 'at', e[0], e[1], ': later events', [(x[0], x[1], fdim[x[2]], x[3][0]) for x in later][:8], '... total', len(later))

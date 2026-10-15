"""Node side + target side of the one-level LP.  Reads sec_*.pkl.  For every node orbit (distinct canonical N among
section reps): concrete rep N0, multiset of (pi, N0) Y-keys over all concrete planes pi inside pm(N0), Z-keys of
lines.  Plane orbit sizes.  Target side for t0 = P line 0 and T line 100: (t,pi), (t,u,pi), (t,u) keys and the
mapping of each concrete plane through t0 to its orbit rep.  -> side.pkl"""
import pickle, glob, time, collections
from lgeo import *
t0_ = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0_), *a, flush=True)
planes = pickle.load(open('planes.pkl', 'rb'))
VEC = {}
for s in range(V):
    VEC[tuple(int(x) for x in g.L[s])] = s; VEC[tuple(-int(x) for x in g.L[s])] = s
def plane_of(a, b):
    m = (1 << a) | (1 << b)
    if G[a][b] != 0:
        for sg in (1, -1):
            c = VEC.get(tuple(int(x) for x in (g.L[a] - sg * g.L[b])))
            if c is not None and c not in (a, b): m |= 1 << c
    return m
# plane orbit sizes
allp = set()
for a in range(V):
    for b in range(a + 1, V): allp.add(plane_of(a, b))
psize = collections.Counter()
pidx = {p: i for i, p in enumerate(planes)}
for p in allp: psize[pidx[canon((p,))[0][0]]] += 1
log('planes', len(allp), 'orbit sizes', dict(psize))
secs = {}
for f in sorted(glob.glob('sec_*.pkl')):
    i = int(f.split('_')[1].split('.')[0]); secs[i] = pickle.load(open(f, 'rb'))
log('sections loaded', sorted(secs))
nodes = {}
for i, s in secs.items():
    for yk, r in s['reps'].items():
        if r['nkey'] not in nodes: nodes[r['nkey']] = dict(N0=r['N'], lam=r['lam'], rank=r['rank'], size=r['size'], perp=r['perp'])
log('node orbits', len(nodes))
for k, (nk, d) in enumerate(nodes.items()):
    N0 = d['N0']; P = pm(N0); pl = set()
    b = bits(P)
    for x in range(len(b)):
        for y in range(x + 1, len(b)): pl.add(plane_of(b[x], b[y]))
    yc = collections.Counter(canon((p, N0))[0] for p in pl)
    d['ykeys'] = dict(yc); d['nplanes'] = len(pl)
    d['zkeys'] = collections.Counter(canon((N0, 1 << u))[0] for u in bits(N0))
    if k % 25 == 0: log('node', k, d['rank'], d['size'], d['perp'], 'planes', len(pl))
# target side
tgt = {}
for t0 in (0, 100):
    pl = set(plane_of(t0, e) for e in range(V) if e != t0)
    tp = []
    for p in pl:
        key, sig = canon((p,))
        i = pidx[key[0]]
        inkey = canon((p, 1 << t0))[0]
        covs = {}
        for u in bits(pm(p)):
            covs[u] = (canon((p, 1 << t0, 1 << u))[0], img_line(u, sig))
        tp.append(dict(plane=p, sec=i, inkey=inkey, covs=covs))
    ck = {u: canon((1 << t0, 1 << u))[0] for u in bits(HYP[t0])}
    tgt[t0] = dict(planes=tp, ckeys=ck)
    log('target', t0, 'planes through it', len(tp))
# user (t, pi0) keys for each section rep
users = {}
for i, p in enumerate(planes):
    users[i] = [canon((p, 1 << t))[0] for t in bits(p)]
pickle.dump(dict(psize=dict(psize), nodes=nodes, tgt=tgt, users=users), open('side.pkl', 'wb'))
log('saved side.pkl')

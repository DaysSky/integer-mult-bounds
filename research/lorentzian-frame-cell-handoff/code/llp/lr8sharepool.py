"""Pool of 4-covers whose four nodes all have >= MINU usable users (lines of the frame that can use it in some 4-cover;
see lr8usable.py), rebuilt from the exhaustive lists, mapped to the 20 Z11 reps and rotated; sampled <= NMAX per rep.
Output r8share.pkl ({t: [covers]}, r8covers format).  usage: lr8sharepool.py MINU NMAX"""
import sys, pickle, itertools, random, collections, time
from lgeo import *
MINU = int(sys.argv[1]); NMAX = int(sys.argv[2]); random.seed(11); t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
def inv(p):
    q = [0] * n
    for i, x in enumerate(p): q[x] = i
    return q
tabs = {}; full = {}
for kind in ('P', 'T'):
    D = pickle.load(open('lr8allcovers_%s.pkl' % kind, 'rb')); t = D['t']
    fr = set()
    for a, b in itertools.combinations([x for x in range(V) if x != t], 2):
        m = (1 << t) | (1 << a) | (1 << b)
        if rank(m) != 3: continue
        fr.add(pp(m))
    canon_of = {F: canon((1 << t, F)) for F in fr}
    tabs[kind] = {canon_of[F1][0]: len(c) for F1, c in D['covers'].items()}
    for F in fr: tabs[kind].setdefault(canon_of[F][0], 0)
    full[kind] = (t, D, fr, canon_of)
usable = {}
for kind in ('P', 'T'):
    t, D, fr, canon_of = full[kind]
    for F1 in D['covers']:
        u = sum(1 for b in bits(F1) if tabs[KIND[b]][canon((1 << b, F1))[0]] > 0)
        usable[canon_of[F1][0]] = u
out = {}
pools = {}
for kind in ('P', 'T'):
    t, D, fr, canon_of = full[kind]
    rep_of = {canon_of[F1][0]: F1 for F1 in D['covers']}
    allc = set()
    for F in fr:
        cf, pF = canon_of[F]; F1 = rep_of.get(cf)
        if F1 is None: continue
        p1 = canon_of[F1][1]; ipF = inv(pF); g = [ipF[p1[x]] for x in range(n)]
        for c in D['covers'][F1]: allc.add(tuple(sorted(act(X, g) for X in c)))
    good = [c for c in allc if all(usable.get(canon_of[F][0], 0) >= MINU for F in c)]
    log(kind, 'covers', len(allc), 'with all nodes usable >=', MINU, ':', len(good))
    tc = collections.Counter(tuple(sorted(usable[canon_of[F][0]] for F in c)) for c in good)
    log('   usable-count types', tc.most_common(6))
    pools[kind] = (t, good)
rot = [img_line(s, [(i + 1) % n for i in range(n)]) for s in range(V)]
orb = {}; reps = []
for s in range(V):
    if s in orb: continue
    reps.append(s); x = s
    for k in range(n): orb[x] = (len(reps) - 1, k); x = rot[x]
for r in reps:
    t, good = pools[KIND[r]]
    src = list(SUPP[t]); dst = list(SUPP[r])
    rest_s = [x for x in range(n) if x not in src]; rest_d = [x for x in range(n) if x not in dst]
    perm = [None] * n
    for a, b in zip(src + rest_s, dst + rest_d): perm[a] = b
    smp = random.sample(good, min(NMAX, len(good)))
    out[r] = [tuple(sorted(act(X, perm) for X in c)) for c in smp]
def rotm(m, k):
    for _ in range(k):
        m2 = 0
        for s in bits(m): m2 |= 1 << rot[s]
        m = m2
    return m
allc = {t: [tuple(sorted(rotm(F, orb[t][1]) for F in c)) for c in out[reps[orb[t][0]]]] for t in range(V)}
pickle.dump(allc, open('r8share.pkl', 'wb')); log('saved r8share.pkl')

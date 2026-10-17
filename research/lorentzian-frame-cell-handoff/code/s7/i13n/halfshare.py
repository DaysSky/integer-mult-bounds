"""For every good frame of I13 that a target can use, the 6 E-sets split into sign halves.  How many distinct
good frames produce a given half (max possible sharing of that half), over all good frames (not a partition)."""
from part13 import *
import collections
# enumerate good frames: PPTT {P(ab),P(cd),T(abx),T(cdx)} and TTTT Pasch
frames = set()
for x in range(13):
    others = [i for i in range(13) if i != x]
    for Q in itertools.combinations(others, 4):
        a, b, c, d = Q
        for (p, q), (r, s) in (((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c))):
            f = tuple(sorted((g.P(p, q), g.P(r, s), g.T(p, q, x), g.T(r, s, x))))
            frames.add(f)
for S6 in itertools.combinations(range(13), 6):
    trs = [g.T(*t) for t in itertools.combinations(S6, 3)]
    for q in itertools.combinations(trs, 4):
        if all(len(set(g.supp[x]) & set(g.supp[y])) == 1 for x, y in itertools.combinations(q, 2)) and good(q):
            frames.add(tuple(sorted(q)))
frames = sorted(frames)
print('good frames', len(frames), collections.Counter(''.join(sorted(g.kind[x] for x in f)) for f in frames))
cnt = collections.Counter(); per_frame = []
for f in frames:
    hs = []
    for a, b in itertools.combinations(range(4), 2):
        o = [z for z in range(4) if z not in (a, b)]
        E = HYP[f[a]] & HYP[f[b]] & ~HYP[f[o[0]]] & ~HYP[f[o[1]]]
        k, l = f[o[0]], f[o[1]]
        Ep = sum(1 << u for u in bits(E) if G[u, k] == G[u, l]); Em = E & ~Ep
        for hh in (Ep, Em):
            if hh: cnt[hh] += 1; hs.append(hh)
    per_frame.append(hs)
print('distinct halves', len(cnt), 'occurrence distribution', sorted(collections.Counter(cnt.values()).items()))
pickle.dump((frames, per_frame, cnt), open('halfshare.pkl', 'wb'))

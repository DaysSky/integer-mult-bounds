"""Anatomy of I_{11,1} halves that occur in several good frames: are those frames pairwise disjoint?  Kinds."""
import sys, collections, itertools, pickle
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(11); V = g.V; G = g.G
d = pickle.load(open('halfglobal_11.pkl', 'rb')); frames = d['frames']; where = d['where']
kind = lambda f: ''.join(sorted(g.kind[u] for u in f))
st = collections.Counter(); ex = {}
for H, fs in where.items():
    fs = sorted(set(fs)); fr = [frames[i] for i in fs]
    disj = all(not (set(a) & set(b)) for a, b in itertools.combinations(fr, 2))
    key = (len(fs), disj, tuple(sorted(kind(f) for f in fr)), bin(H).count('1'))
    st[key] += 1; ex.setdefault(key, (H, fr))
for k, c in sorted(st.items()): print(k, c)
for k, (H, fr) in list(ex.items())[:6]:
    print(k, [[(g.kind[u], g.supp[u]) for u in f] for f in fr])

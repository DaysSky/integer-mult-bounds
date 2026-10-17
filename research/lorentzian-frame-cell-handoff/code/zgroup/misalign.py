"""Misalignment of an I_{11,1} good-frame partition: number of (E-set, partition frame) pairs with odd intersection
(E8 R420: 0; each odd pair forces a single-line input or a correction).  usage: misalign.py PART.pkl"""
import sys, itertools, collections, pickle
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(11); V = g.V; G = g.G
frames, pun = pickle.load(open(sys.argv[1], 'rb')); live = [u for u in range(V) if u not in set(pun)]
orth = lambda a, b: a != b and G[a, b] == 0
tot = 0; per = collections.Counter(); qodd = 0
for f in frames:
    Q = set(u for u in live if all(orth(u, x) for x in f)); qodd += sum(1 for f2 in frames if len(Q & set(f2)) % 2)
    for t, e in itertools.combinations(f, 2):
        k, l = [x for x in f if x not in (t, e)]
        E = set(u for u in live if orth(u, t) and orth(u, e) and not orth(u, k) and not orth(u, l))
        o = sum(1 for f2 in frames if len(E & set(f2)) % 2); tot += o; per[o] += 1
print(sys.argv[1].split('/')[-1], 'frames', len(frames), 'odd (E-set, frame) pairs', tot, 'per E-set', sorted(per.items()), '| odd (Q, frame) pairs', qodd)

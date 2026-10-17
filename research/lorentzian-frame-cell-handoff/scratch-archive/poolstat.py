import pickle, collections, sys
sys.path.insert(0, '.')
from lgeo import *
cov = pickle.load(open('r8covers.pkl', 'rb'))
print('covers per target', collections.Counter(len(cov[t]) for t in range(V)))
inpool = {t: set(F for c in cov[t] for F in c) for t in range(V)}
print('distinct frames per target', collections.Counter(len(inpool[t]) for t in (0, 60)))
# shareable frames: F in pool of t and of some other line b in F
sh = collections.Counter(); tot = collections.Counter()
for t in range(V):
    for F in inpool[t]:
        k = sum(1 for b in bits(F) if b != t and F in inpool[b])
        sh[(KIND[t], k)] += 1
print(sorted(sh.items()))
# covers with number of shareable frames
cs = collections.Counter()
for t in range(V):
    for c in cov[t]:
        k = sum(1 for F in c if any(b != t and F in inpool[b] for b in bits(F)))
        cs[(KIND[t], k)] += 1
print('covers by #shareable frames', sorted(cs.items()))

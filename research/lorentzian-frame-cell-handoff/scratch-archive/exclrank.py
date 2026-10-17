import sys, pickle, collections
sys.path.insert(0, '.')
from lgeo import *
cov = pickle.load(open('r8covers.pkl', 'rb'))
rot = [img_line(s, [(i + 1) % n for i in range(n)]) for s in range(V)]
orb = {}; reps = []
for s in range(V):
    if s in orb: continue
    reps.append(s); x = s
    for k in range(n): orb[x] = (len(reps) - 1, k); x = rot[x]
st = collections.Counter(); secrank = collections.Counter()
for r in reps[:20:3]:
    R = HYP[r]
    for c in cov[r][:150]:
        P = [pm(F) & R for F in c]
        for i, F in enumerate(c):
            ex = P[i] & ~(P[(i+1)%4] | P[(i+2)%4] | P[(i+3)%4])
            st[(KIND[r], rank(P[i]), rank(ex) if ex else 0)] += 1
print(sorted(st.items()))

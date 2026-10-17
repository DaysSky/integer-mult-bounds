"""Add rank-5 candidate flats: G = perp(closure(Q + line)) for design planes Q (so G feeds Q); keep those with cells."""
import pickle
from common import *
out = pickle.load(open('flats.pkl', 'rb'))
have = set(F for F, r, c, s in out)
add = set()
for Q in planes:
    for s in range(V):
        H = e8.closure(Q | (1 << s))[0]
        if e8.dim(H) != 3: continue
        G = perpmask(H)
        if e8.dim(G) == 5: add.add(G)
for G in add:
    if G in have: continue
    Gp = perpmask(G)
    cells = [P for P in planes if P & ~G == 0]
    secs = [Q for Q in planes if Q & ~Gp == 0]
    if cells and secs: out.append((G, 5, cells, secs))
print('candidate flats', len(out), collections.Counter((r, pc(F)) for F, r, c, s in out).most_common(30))
st = collections.Counter((r, pc(F), len(c), len(s)) for F, r, c, s in out if r == 5)
print('rank5 (lines, #cells, #secs):', st.most_common(10))
pickle.dump(out, open('flats.pkl', 'wb'))

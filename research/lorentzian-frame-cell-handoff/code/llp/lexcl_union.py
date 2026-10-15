"""Exclusive-part closures for ALL exact 3-section union covers (covers3.pkl) of the P and T representatives: for each
cover (mates e1,e2,e3) and each section S_i = {t,e_i}-perp, E_i = lines of R(t) only in S_i; test whether some proper
rank-8 node S_i & x-perp (x not in the pair plane) contains E_i.  If no cover has all three E_i inside proper nodes,
R(t) has no cover by 3 perps of rank-3 frames through t (each such perp lies in a pair section {t,a}-perp, so a
3-cover refines an exact union cover and must contain each exclusive part in one rank-8 node)."""
import pickle, collections
from lgeo import *
cov = pickle.load(open('covers3.pkl', 'rb'))
for kind in ('P', 'T'):
    t = next(s for s in range(V) if KIND[s] == kind)
    R = HYP[t]; st = collections.Counter(); allin = 0
    for ms, gd in cov[t]:
        S = [HYP[t] & HYP[e] for e in ms]
        okc = 0
        for i in range(3):
            E = S[i] & ~S[(i + 1) % 3] & ~S[(i + 2) % 3]
            pl = (1 << t) | (1 << ms[i])
            inside = any(E & ~(S[i] & HYP[x]) == 0 for x in range(V) if not (pl >> x & 1) and (S[i] & HYP[x]) != S[i])
            okc += inside
        st[(gd, okc)] += 1
        if okc == 3: allin += 1
    print(kind, 'covers', len(cov[t]), '(good frame?, #sections whose exclusive part fits a proper node):', sorted(st.items()), '| covers with all three fitting:', allin, flush=True)

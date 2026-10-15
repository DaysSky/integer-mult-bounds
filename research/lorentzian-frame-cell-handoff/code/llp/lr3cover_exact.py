"""Exhaustive: is R(t) covered by 3 perps of rank-3 frames through t?  Every such perp is a rank-8 node
S_a & x-perp of a pair section S_a = {t,a}-perp, and a 3-cover refines an exact 3-section union cover (covers3.pkl),
so: for each exact cover (S_1,S_2,S_3) and each choice of nodes N_i = S_i & x_i-perp containing the exclusive part
E_i, test N_1 u N_2 u N_3 == R(t).  Prints the number of 3-covers found per line type (and an example)."""
import pickle, itertools
from lgeo import *
cov = pickle.load(open('covers3.pkl', 'rb'))
for kind in ('P', 'T'):
    t = next(s for s in range(V) if KIND[s] == kind)
    R = HYP[t]; found = 0; ex = None; checked = 0
    for ms, gd in cov[t]:
        S = [HYP[t] & HYP[e] for e in ms]
        cand = []
        for i in range(3):
            E = S[i] & ~S[(i + 1) % 3] & ~S[(i + 2) % 3]
            pl = (1 << t) | (1 << ms[i])
            Ns = set()
            for x in range(V):
                if pl >> x & 1: continue
                N = S[i] & HYP[x]
                if N != S[i] and E & ~N == 0: Ns.add(N)
            cand.append(sorted(Ns))
        for N1 in cand[0]:
            for N2 in cand[1]:
                rem = R & ~(N1 | N2)
                for N3 in cand[2]:
                    checked += 1
                    if rem & ~N3 == 0:
                        found += 1
                        if ex is None: ex = (ms, gd, pc(N1), pc(N2), pc(N3))
    print(kind, 'node triples checked', checked, '| 3-covers of R(t) by rank-8 nodes:', found, '| example (mates, good, node sizes):', ex, flush=True)

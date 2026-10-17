import sys, pickle, collections, random
sys.path.insert(0, '.')
from lgeo import *
random.seed(1)
cov = pickle.load(open('r8covers.pkl', 'rb'))
PM = {}
def pmc(F):
    if F not in PM: PM[F] = pm(F)
    return PM[F]
RK = {}
def rk(m):
    if m not in RK: RK[m] = rank(m)
    return RK[m]
# exclusive parts per (t, F) over pool covers (distinct)
EX = collections.defaultdict(set)
for t in range(0, V):
    R = HYP[t]
    for c in cov[t][:300]:
        P = [pmc(F) & R for F in c]
        for i, F in enumerate(c):
            ex = P[i] & ~(P[(i + 1) % 4] | P[(i + 2) % 4] | P[(i + 3) % 4])
            EX[(t, F)].add(ex)
stats = collections.Counter(); n = 0
frames = collections.defaultdict(list)
for (t, F) in EX: frames[F].append(t)
for F, us in frames.items():
    if len(us) < 2 or rk(pmc(F)) != 8: continue
    for a in range(len(us)):
        for b in range(a + 1, len(us)):
            t, s = us[a], us[b]
            ok7 = any(rk(e1 | e2) <= 7 for e1 in EX[(t, F)] for e2 in EX[(s, F)])
            r1 = min(rk(e) for e in EX[(t, F)]); r2 = min(rk(e) for e in EX[(s, F)])
            stats[(ok7, min(r1, 7) == 7 and min(r2, 7) == 7)] += 1; n += 1
print('rank-8 node user pairs (pool, first 300 covers/target):', n)
print('(some exclusive pair fits one hyperplane, both users forced rank-7 exclusives) ->', sorted(stats.items()))

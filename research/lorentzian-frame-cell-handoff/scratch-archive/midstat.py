import sys, json, collections, pickle
sys.path.insert(0, '.')
from lgeo import *
D = json.load(open(sys.argv[1]))
sel = {int(k): v for k, v in D['sel'].items()}; det = D['det']
rot = [img_line(s, [(i + 1) % n for i in range(n)]) for s in range(V)]
rotp = [list(range(V))]
for k in range(1, n): rotp.append([rot[x] for x in rotp[-1]])
def rotm(m, k):
    r = 0
    for s in bits(m): r |= 1 << rotp[k % n][s]
    return r
orb = {}; reps = []
for s in range(V):
    if s in orb: continue
    reps.append(s); x = s
    for k in range(n): orb[x] = (len(reps) - 1, k); x = rot[x]
cov = pickle.load(open('r8covers.pkl', 'rb'))
asg = collections.defaultdict(int)
for key, v in det['assign'].items():
    ri, i, u = map(int, key.split(','))
    if v: asg[(ri, i)] |= 1 << u
clos = collections.Counter(); rk = collections.Counter(); sizes = []
for t in range(V):
    o, k = orb[t]; ci = det['cin'][o].index(1)
    for j in range(4):
        if j == ci: continue
        P = rotm(asg[(o, j)], k); r = rank(P); rk[r] += 1; sizes.append(pc(P))
        if r <= 7: clos[pp(P)] += 1
print('delivered parts', sum(rk.values()), 'rank hist', sorted(rk.items()), 'mean size %.1f' % (sum(sizes) / len(sizes)))
print('rank<=7 parts', sum(clos.values()), 'distinct closures', len(clos), 'multiplicity hist', sorted(collections.Counter(clos.values()).items()))
print('closure sizes (lines) hist', sorted(collections.Counter(pc(M) for M in clos).items()))

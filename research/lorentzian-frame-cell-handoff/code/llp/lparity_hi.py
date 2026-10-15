"""Parity tops with higher-user sections: sections = pm(Phi) for closed flats Phi containing t (rank 2..4); users = lines
of Phi.  Search combinations of up to 4 sections through t whose totals XOR to 1_{R(t)} + D with |D| <= 2, and report
the per-target 'section cost' sum (users-sharing) for the best ones.  usage: lparity_hi.py n maxrank"""
import sys, os, itertools, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lword'))
from geom import Geom
import numpy as np
n = int(sys.argv[1]); MR = int(sys.argv[2])
g = Geom(n); V = g.V; G = g.G; HYP = g.HYP; bits = g.bits
pc = lambda m: bin(m).count('1')
FM = (1 << V) - 1
def pm(m):
    r = FM
    for s in bits(m): r &= HYP[s]
    return r
def pp(m): return pm(pm(m))
def rank(m):
    b = bits(m)
    if not b: return 0
    M = g.LA[b]
    if n == 9: M = np.vstack([M, np.array([1.0] * 9 + [3.0])])
    return int(np.linalg.matrix_rank(M)) - (1 if n == 9 else 0)
for t in sorted({0, [s for s in range(V) if g.kind[s] == 'T'][0]}):
    R = HYP[t]
    flats = {}
    fr = [pp(1 << t)]
    seen = set(fr)
    while fr:
        nf = []
        for F in fr:
            for y in bits(R | pm(1 << t) & 0):
                pass
            for y in range(V):
                if F >> y & 1: continue
                F2 = pp(F | (1 << y))
                if F2 in seen: continue
                seen.add(F2)
                r = rank(F2)
                if r <= MR and pc(pm(F2)) > 0: nf.append(F2); flats[F2] = r
        fr = nf
    secs = [(F, pm(F), pc(F), flats[F]) for F in flats]
    print('target', t, g.kind[t], '|R|', pc(R), 'flats through t (rank 2..%d):' % MR, len(secs),
          collections.Counter((r, u) for F, S, u, r in secs).most_common(12), flush=True)
    # combinations of 2..4 sections
    best = {}
    S_list = sorted(secs, key=lambda x: -pc(x[1]))
    idx = {x[1]: x for x in S_list}
    for k in (2, 3, 4):
        cnt = collections.Counter(); found = 0
        for combo in itertools.combinations(range(len(S_list)), k - 1):
            X = R
            for i in combo: X ^= S_list[i][1]
            # need one more section S with |X ^ S| <= 2: search candidates by size
            for j in range(combo[-1] + 1, len(S_list)):
                d = pc(X ^ S_list[j][1])
                if d <= 2:
                    sig = tuple(sorted((S_list[i][3], S_list[i][2]) for i in combo + (j,)))
                    cnt[(d, sig)] += 1; found += 1
            if found > 200000: break
        print('  k =', k, 'parity combos with defect <= 2:', sum(cnt.values()))
        for key, v in sorted(cnt.items(), key=lambda kv: (kv[0][0], -sum(u for r, u in kv[0][1])))[:12]:
            print('     defect', key[0], 'sections (rank, users):', key[1], 'x', v)

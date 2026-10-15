"""E8 version: parity tops mixing plane sections (D6 cells / E6 A2) and A3-perp sections (D5, 20 lines, 6 users),
combinations of <= 4 with defect <= 1."""
import sys, os, itertools, collections, pickle
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
V = e8.V; G = e8.GI; HYP = e8.HYP; bits = e8.bits
pc = lambda m: bin(m).count('1')
def pm(m):
    r = e8.FULL
    for s in bits(m): r &= HYP[s]
    return r
A2 = set()
for a in range(V):
    for b in e8.NEIGH[a]:
        F, r = e8.closure((1 << a) | (1 << b))
        if pc(F) == 3: A2.add(F)
tri_of = collections.defaultdict(list)
for T in A2:
    for s in bits(T): tri_of[s].append(T)
A3 = set()
for t in range(V):
    for T1, T2 in itertools.combinations(tri_of[t], 2):
        if pc(T1 & T2) != 1: continue
        F, r = e8.closure(T1 | T2)
        if r == 3 and pc(F) == 6: A3.add(F)
A3 = sorted(A3)
print('A3', len(A3), 'A3-perp sizes', collections.Counter(pc(pm(X)) for X in A3[:200]))
def planes_through(t):
    out = set()
    for e in range(V):
        if e == t: continue
        F, r = e8.closure((1 << t) | (1 << e))
        out.add(F)
    return out
for t in (0,):
    R = HYP[t]
    secs = [('pl%d' % pc(p), pm(p)) for p in sorted(planes_through(t))] + [('A3', pm(X)) for X in A3 if X >> t & 1]
    print('target', t, 'sections', collections.Counter(k for k, S in secs), flush=True)
    N = len(secs)
    pairs = collections.defaultdict(list)
    for i in range(N):
        for j in range(i + 1, N): pairs[secs[i][1] ^ secs[j][1]].append((i, j))
    res = collections.Counter()
    for X, lst in pairs.items():
        Y = X ^ R
        for D in [0] + [1 << s for s in bits(R)]:
            for (k, l) in pairs.get(Y ^ D, []):
                for (i, j) in lst:
                    if len({i, j, k, l}) == 4 and i < k:
                        res[(pc(D), tuple(sorted(secs[x][0] for x in (i, j, k, l))))] += 1
    for k in range(len(secs)):
        Y = secs[k][1] ^ R
        for D in [0] + [1 << s for s in bits(R)]:
            for (i, j) in pairs.get(Y ^ D, []):
                if k > j: res[(pc(D), tuple(sorted(secs[x][0] for x in (i, j, k))))] += 1
    for key, v in sorted(res.items()): print('   defect %d' % key[0], key[1], 'x', v)

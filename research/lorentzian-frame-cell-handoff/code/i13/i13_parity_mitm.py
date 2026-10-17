"""EXACT minimum-weight parity covers of R(t) inside a chosen set of frame types (meet in the middle over a hash
table of pairwise perp XORs; first frame up to Stab(t) for k >= 5).  k <= KMAX (<= 6).  Distinctness enforced.
usage: python3 i13_parity_mitm.py KIND KMAX 'type1' ['type2' ...]   (types named by a representative's lines)"""
import sys, pickle, collections, itertools, time
from lgeo13 import *
kind, KMAX = sys.argv[1], int(sys.argv[2]); tnames = sys.argv[3:]
t0 = time.time()
t, FL, PL = pickle.load(open('i13_frames_%s.pkl' % kind, 'rb'))
R = HYP[t]
def mask_of(tn):
    m = 0
    for w in tn.split():
        m |= 1 << IDX[(w[0], tuple(int(c, 16) for c in w[1:]))]
    return m
want = {canon((1 << t, mask_of(tn)))[0] for tn in tnames}
idx = []; key = {}
for i in range(len(FL)):
    k = canon((1 << t, FL[i]))[0]
    if k in want: idx.append(i); key[i] = k
C = [PL[i] for i in idx]; n = len(C)
reps = {}
for j, i in enumerate(idx):
    reps.setdefault(key[i], j)
print(kind, tnames, '| candidate frames', n, '| reps', len(reps), '%.0fs' % (time.time() - t0), flush=True)
single = {}
for j, P in enumerate(C): single.setdefault(P, []).append(j)
pairs = collections.defaultdict(list)
for a in range(n):
    Pa = C[a]
    for b in range(a + 1, n): pairs[Pa ^ C[b]].append((a, b))
print('  pair table', len(pairs), '%.0fs' % (time.time() - t0), flush=True)
def found(sol):
    sol = sorted(sol); tot = 0
    for j in sol: tot ^= C[j]
    assert tot == R and len(set(sol)) == len(sol)
    print('  k=%d FOUND: %s' % (len(sol), [' '.join(KIND[s] + ''.join('%x' % q for q in SUPP[s]) for s in bits(FL[idx[j]])) for j in sol]), flush=True)
    return True
def search(k):
    if k == 1: return R in single and found(single[R][:1])
    if k == 2:
        for a in range(n):
            for b in single.get(R ^ C[a], []):
                if b != a: return found([a, b])
        return False
    if k == 3:
        for a in range(n):
            for (b, c) in pairs.get(R ^ C[a], []):
                if a not in (b, c): return found([a, b, c])
        return False
    if k == 4:
        for X, lst in pairs.items():
            for (c, d) in pairs.get(R ^ X, []):
                for (a, b) in lst:
                    if len({a, b, c, d}) == 4: return found([a, b, c, d])
        return False
    if k == 5:
        for a in reps.values():
            Ra = R ^ C[a]
            for X, lst in pairs.items():
                for (c, d) in pairs.get(Ra ^ X, []):
                    for (p, q) in lst:
                        if len({a, p, q, c, d}) == 5: return found([a, p, q, c, d])
        return False
    if k == 6:
        for a in reps.values():
            for b in range(n):
                if b == a: continue
                Rab = R ^ C[a] ^ C[b]
                for X, lst in pairs.items():
                    l2 = pairs.get(Rab ^ X)
                    if not l2: continue
                    for (c, d) in l2:
                        for (p, q) in lst:
                            if len({a, b, p, q, c, d}) == 6: return found([a, b, p, q, c, d])
        return False
for k in range(1, KMAX + 1):
    r = search(k)
    print('  k=%d: %s  %.0fs' % (k, 'yes' if r else 'none', time.time() - t0), flush=True)
    if r: break

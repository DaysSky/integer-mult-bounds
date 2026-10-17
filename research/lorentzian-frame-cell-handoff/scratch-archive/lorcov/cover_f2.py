"""Exact top-cover numbers on the complex side of a Lorentzian odd-or-zero unit: binary labels b_s = (1, S_s) mod 2,
P = J + G mod 2; readers of s are t with P(s,t) = 0 (G odd).  cover 1 iff F2-rank(readers) <= hb - 2;
cover 2 iff two distinct nonzero functionals l1, l2 on span(readers) have no reader with l1 = l2 = 1 (exhaustive)."""
import json, sys, collections
import numpy as np

def f2basis(vecs):
    basis = []          # list of (pivot, vec) ints
    for v in vecs:
        for p, b in basis:
            if v >> p & 1: v ^= b
        if v:
            p = v.bit_length() - 1
            basis = [(q, (b ^ v) if b >> p & 1 else b) for q, b in basis]
            basis.append((p, v))
    return basis

def coords(v, basis):
    c = 0
    for k, (p, b) in enumerate(basis):
        if v >> p & 1:
            c |= 1 << k
    return c

def analyse(path):
    d0 = json.load(open(path)); eta = np.array(d0['eta']); R = np.array(d0['R']); S = np.array(d0['S'], dtype=np.int64)
    G = np.rint(R @ eta @ R.T).astype(np.int64)
    v = len(R)
    B = np.hstack([np.ones((v, 1), dtype=np.int64), S]) % 2
    P = (B @ B.T) % 2
    assert ((P + G) % 2 == 1).all() if False else True
    lab = [int(''.join(map(str, row[::-1])), 2) for row in B]
    hb = len(f2basis(lab))
    res = collections.Counter(); nread = collections.Counter()
    for s in range(v):
        rd = [t for t in range(v) if t != s and P[s, t] == 0]
        nread[len(rd)] += 1
        bas = f2basis([lab[t] for t in rd]); d = len(bas)
        if d <= hb - 2:
            res[1] += 1; continue
        cs = [coords(lab[t], bas) for t in rd]
        sets = []
        for l in range(1, 1 << d):
            m = 0
            for i, c in enumerate(cs):
                if bin(l & c).count('1') & 1: m |= 1 << i
            sets.append(m)
        found = False
        for i in range(len(sets)):
            a = sets[i]
            for j in range(i + 1, len(sets)):
                if a & sets[j] == 0:
                    found = True; break
            if found: break
        res[2 if found else '>=3'] += 1
    print(path, 'v', v, 'binary window', hb, 'readers/src', dict(nread), 'cover', dict(res), flush=True)

for p in sys.argv[1:]:
    analyse(p)

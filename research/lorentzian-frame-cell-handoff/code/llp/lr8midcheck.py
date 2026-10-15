"""Necessary node condition for rank-8 frame sections (zero waste): at each section node F-perp the delivered parts
{A_b : b delivered on F} (independent) must be the span of k = #delivered inputs, each input carrying a vector
supported inside a rank-<=5 closed set (its mid M inside F-perp).  So span{A_b} must have a basis of vectors whose
supports have closure rank <= MAXR.  Checks all 2^k - 1 span vectors.  usage: lr8midcheck.py parts.json [MAXR]
parts.json: {"F_hex": {"b": "part_hex", ...}, ...} (delivered parts per section)"""
import sys, json, itertools
from lgeo import *
P = json.load(open(sys.argv[1])); MAXR = int(sys.argv[2]) if len(sys.argv) > 2 else 5
def gf2_rank(vs):
    rows = list(vs); r = 0
    for bit in range(V):
        piv = next((i for i in range(r, len(rows)) if rows[i] >> bit & 1), None)
        if piv is None: continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i] >> bit & 1: rows[i] ^= rows[r]
        r += 1
    return r
ok = bad = dep = 0
for Fh, parts in P.items():
    A = [int(v, 16) for v in parts.values()]
    k = len(A)
    if gf2_rank(A) < k: dep += 1; continue
    good = []
    for mask in range(1, 1 << k):
        v = 0
        for i in range(k):
            if mask >> i & 1: v ^= A[i]
        if v and rank(pp(v)) <= MAXR: good.append(v)
    if gf2_rank(good) == k: ok += 1
    else: bad += 1
print('sections: ok', ok, '| fail (no mid-supported basis, rank <= %d)' % MAXR, bad, '| dependent delivered parts', dep)

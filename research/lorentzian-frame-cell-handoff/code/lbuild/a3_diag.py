"""Diagnostic for a cached A3-parity selection (a3_choice.pkl): sections (perps of chosen planes), users per section,
largest pairwise intersection per section (perp of a rank-3 frame), remainder sizes, and how much of each remainder is
covered by flats (pair/triple closures, fixed fclosure) that lie inside >= 2 sections' remainders.  usage: python3 a3_diag.py"""
import sys, os, pickle, collections, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lmid'))
import lw
from lw import V, g, bits, nondegenerate
from fastcl import fclosure
HYP = g.HYP; pc = lambda m: bin(m).count('1')
def pm(m):
    r = (1 << V) - 1
    for s in bits(m): r &= HYP[s]
    return r
choice = pickle.load(open('a3_choice.pkl', 'rb'))
users = collections.defaultdict(list)
for t, (a, b, c, d) in choice.items():
    for Q in (a, b, c): users[Q].append(t)
SEC = {Q: pm(Q) for Q in users}
print('sections', len(SEC), '| users per section', dict(collections.Counter(len(u) for u in users.values())),
      '| defects', len({c[3] for c in choice.values() if c[3] >= 0}))
best = {}
QL = list(SEC)
for Q in QL:
    bi = 0
    for Q2 in QL:
        if Q2 == Q: continue
        I = SEC[Q] & SEC[Q2]
        if pc(I) > pc(bi): bi = I
    best[Q] = bi
print('section size hist', dict(sorted(collections.Counter(pc(S) for S in SEC.values()).items())))
print('largest shared intersection size hist', dict(sorted(collections.Counter(pc(b) for b in best.values()).items())))
rem = {Q: SEC[Q] & ~best[Q] for Q in QL}
print('remainder size hist', dict(sorted(collections.Counter(pc(r) for r in rem.values()).items())), '| total remainder lines', sum(pc(r) for r in rem.values()))
where = collections.defaultdict(set)
for Q in QL:
    L = bits(rem[Q])
    for a, b in itertools.combinations(L, 2):
        X = fclosure((1 << a) | (1 << b))
        if X & ~rem[Q] == 0: where[X].add(Q)
shared = {X: w for X, w in where.items() if len(w) >= 2 and nondegenerate(X)}
print('flats inside >= 2 remainders:', len(shared), '| size hist', dict(sorted(collections.Counter(pc(X) for X in shared).items())),
      '| multiplicity hist', dict(sorted(collections.Counter(min(len(w), 10) for w in shared.values()).items())))

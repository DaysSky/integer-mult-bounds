"""Transversal lower nodes for the raw-line D5 architecture: flats X (closure of 2 or 3 lines from distinct blocks) and
the set of D5 nodes G_A (A = block A3 with 3 design A2s) containing X; also pair-section perps containing X."""
from common import *
import itertools
D4 = load_d4()
full = [W for W in D4 if len([P for P in planes if P & ~W == 0]) == 12 and len([Q for Q in planes if Q & ~perpmask(W) == 0]) == 12]
blk = {s: k for k, W in enumerate(full) for s in e8.bits(W)}
comp = {k: full.index(perpmask(W)) for k, W in enumerate(full)}
A2s = [P for P in planes if pc(P) == 3]; pairs = [P for P in planes if pc(P) == 2]
A3s = set()
for i, P in enumerate(A2s):
    for P2 in A2s[i+1:]:
        F, r = e8.closure(P | P2)
        if r == 3 and pc(F) == 6: A3s.add(F)
A3s = sorted(A3s); G = {A: perpmask(A) for A in A3s}
L = {A: G[A] & ~full[comp[blk[e8.bits(A)[0]]]] for A in A3s}
# line -> A3s with s in L_A
inL = collections.defaultdict(list)
for A in A3s:
    for s in e8.bits(L[A]): inL[s].append(A)
print('each line in L_A for', collections.Counter(len(v) for v in inL.values()), 'A3s')
# pairs of lines co-occurring in L_A
co = collections.Counter()
for A in A3s:
    for a, b in itertools.combinations(e8.bits(L[A]), 2): co[(a, b)] += 1
print('co-occurrence multiplicities of line pairs within L-sets:', collections.Counter(co.values()))
tri = collections.Counter()
for A in A3s:
    for c in itertools.combinations(e8.bits(L[A]), 3): tri[c] += 1
print('triples co-occurrence:', collections.Counter(tri.values()))
# flats: closure of a co-occurring pair/triple; which D5 nodes contain the closure
st = collections.Counter()
for (a, b), n in co.items():
    X, r = e8.closure((1 << a) | (1 << b))
    cont = [A for A in A3s if X & ~G[A] == 0]
    st[('pair', int(GI[a, b]) != 0, r, pc(X), len(cont))] += 1
for (a, b, c), n in tri.items():
    X, r = e8.closure((1 << a) | (1 << b) | (1 << c))
    cont = [A for A in A3s if X & ~G[A] == 0]
    st[('triple', r, pc(X), len(cont))] += 1
for k, n in sorted(st.items()): print(k, n)
# L_A structure: inner products among the 8 lines
A = A3s[0]
ls = e8.bits(L[A]); print('L_A gram (|ip|):'); print([[abs(int(GI[x, y])) for y in ls] for x in ls])
print('blocks of L_A lines', [blk[x] for x in ls], 'comp pairs', [(blk[x], comp[blk[x]]) for x in ls])

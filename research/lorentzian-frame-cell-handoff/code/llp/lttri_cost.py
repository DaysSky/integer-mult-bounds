"""Node cost of the T-triangle top (lttri_design*.json).  Parts: at node (A,B,C,E) user T(A) receives f_A = A2(B) +
A2(C) + P(E), its own A2(A) at its first node, and the A-fibres {T(a,b,c): a in A} of the crossing pairs (b,c)
assigned to this node (each crossing pair of D_A assigned to exactly one node where it crosses; tie-break by a
seeded random choice).  In-chain node per T line chosen to minimise cost (greedy).  Node registers = k + m - d with
m = min #rank-<=RHO-supported vectors spanning S (bounds as in lr8nodecost).  Reports total extra registers.
usage: lttri_cost.py design.json RHO seed"""
import sys, json, itertools, random, collections
from lgeo import *
sol = [tuple(tuple(T) for T in node) for node in json.load(open(sys.argv[1]))]; RHO = int(sys.argv[2]); random.seed(int(sys.argv[3]))
def L(kind, pts): return IDX[(kind, tuple(sorted(pts)))]
def A2(T): return sum(1 << L('P', p) for p in itertools.combinations(T, 2))
nodes_of = collections.defaultdict(list)
for ni, node in enumerate(sol):
    for T in node: nodes_of[T].append(ni)
part = {}   # (T, ni) -> mask
for A, nis in nodes_of.items():
    D = [x for x in range(11) if x not in A]
    # crossing-pair assignment
    asg = {}
    for p in itertools.combinations(D, 2):
        opts = []
        for ni in nis:
            B, C = [T for T in sol[ni] if T != A]
            if (p[0] in B and p[1] in C) or (p[0] in C and p[1] in B): opts.append(ni)
        asg[p] = random.choice(opts)
    for j, ni in enumerate(nis):
        B, C = [T for T in sol[ni] if T != A]
        E = tuple(x for x in D if x not in B and x not in C)
        m = A2(B) | A2(C) | (1 << L('P', E))
        if j == 0: m |= A2(A)
        for p, nj in asg.items():
            if nj == ni:
                for a in A: m |= 1 << L('T', (a,) + p)
        part[(A, ni)] = m
    tot = 0
    for ni in nis: assert tot & part[(A, ni)] == 0; tot |= part[(A, ni)]
    assert tot == HYP[L('T', A)], 'parts do not partition R(t)'
def gf2_basis(vs):
    basis = []
    for v in vs:
        for b in basis:
            if v ^ b < v: v ^= b
        if v: basis.append(v); basis.sort(reverse=True)
    return basis
RK = {}
def srank(v):
    if v not in RK: RK[v] = rank(v)
    return RK[v]
def node_m(vecs):
    B = gf2_basis(vecs); s = len(B)
    span = [0]
    for b in B: span = span + [v ^ b for v in span]
    g = len(gf2_basis([v for v in span if v and srank(v) <= RHO]))
    return (s if g == s else s + 1), (s if g == s else 2 * s - g), B
# in-chain choice: greedy per T line, pick the node where its part is in the span of the other users' parts
inch = {}
for A, nis in nodes_of.items():
    best = nis[0]
    for ni in nis:
        others = [part[(T, ni)] for T in sol[ni] if T != A]
        Bo = gf2_basis(others); v = part[(A, ni)]
        for b in Bo:
            if v ^ b < v: v ^= b
        if v == 0: best = ni; break
    inch[A] = best
lo = hi = 0; hist = collections.Counter()
for ni, node in enumerate(sol):
    deliv = [part[(T, ni)] for T in node if inch[T] != ni]; allp = [part[(T, ni)] for T in node]
    k = len(deliv); d = len(gf2_basis(deliv))
    mlo, mhi, B = node_m(allp)
    lo += mlo - d; hi += mhi - d; hist[(k, len(B), mlo - d)] += 1
print('RHO=%d  T-triangle top: extra registers %d .. %d over 495 T deliveries' % (RHO, lo, hi))
print('(delivered k, dim S, extra lo) histogram', sorted(hist.items()))

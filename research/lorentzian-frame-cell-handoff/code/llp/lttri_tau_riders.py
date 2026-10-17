"""Riders for the triple-sum register at an M11 triangle node (any RHO).  A basis of the node span S = <p_A,p_B,p_C>
must contain tau = p_A + p_B + p_C (the three pairwise sums only span 2 dimensions).  The tau register shares a stop M
(a closed set containing supp(tau)) with another register only if (i) a co-user register stops there -- impossible:
the pairwise sums close at the hub M_n, which lacks P(E), and P(E) is in tau (forced in all three parts) -- or (ii) a
register of another node F' with M inside F'-perp, i.e. F' inside pm(M), which lies inside pm(supp tau).  F' != F needs a line
l outside F with supp(tau) inside M_l = F-perp n l-perp.  tau's lines: P(E) = 1; A2(X) lines = delta_X (free);
a transversal = XOR of the three users' memberships (1 if forced, free otherwise).  So a rider is locally possible
for l iff P(E) is in M_l and no transversal with all three memberships forced lies outside M_l.
usage: lttri_tau_riders.py node_index ..."""
import sys, json, itertools, collections
from lgeo import *
sol = [tuple(tuple(T) for T in node) for node in json.load(open('lttri_design_z11.json'))]
nodes_of = collections.defaultdict(list)
for ni, node in enumerate(sol):
    for T in node: nodes_of[T].append(ni)
def Ln(k, pts): return IDX[(k, tuple(sorted(pts)))]
def mult(X, pair):
    k = 0
    for nj in nodes_of[X]:
        B, C = [T for T in sol[nj] if T != X]
        if (pair[0] in B and pair[1] in C) or (pair[0] in C and pair[1] in B): k += 1
    return k
for ni in map(int, sys.argv[1:]):
    A, B, C = sol[ni]; users = (A, B, C)
    E = tuple(x for x in range(11) if x not in A + B + C); pE = Ln('P', E)
    F = pp(sum(1 << Ln('T', T) for T in users)); perp = pm(F)
    allforced = 0; nfree = collections.Counter()
    for s in bits(perp):
        if KIND[s] != 'T': continue
        f = 0
        for X in users:
            pair = tuple(sorted(x for x in SUPP[s] if x not in X))
            if mult(X, pair) == 1: f += 1
        nfree[3 - f] += 1
        if f == 3: allforced |= 1 << s
    cand = []; rk = collections.Counter()
    for l in range(V):
        if F >> l & 1: continue
        Ml = perp & HYP[l]
        r = rank(Ml); rk[r] += 1
        if (Ml >> pE & 1) and allforced & ~Ml == 0: cand.append((l, r, pc(Ml)))
    print('node', ni, '| transversals by #free memberships', dict(nfree), '| all-forced transversals', pc(allforced),
          'rank', rank(allforced) if allforced else 0, '| rank(M_l) histogram over lines l outside F', dict(rk),
          '| lines l allowing a tau rider:', len(cand), cand[:10], flush=True)

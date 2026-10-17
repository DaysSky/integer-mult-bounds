"""All 220 nodes: lines l allowing a tau rider (lttri_tau_riders.py criterion), the frames F' != F inside pm(M_l), and
whether any such F' is a frame of the design (a node that could actually send the rider).  usage: lttri_tau_riders_all.py"""
import json, itertools, collections
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
design_frames = {pp(sum(1 << Ln('T', T) for T in node)) for node in sol}
stats = collections.Counter(); hit = 0
for ni, (A, B, C) in enumerate(sol):
    users = (A, B, C); E = tuple(x for x in range(11) if x not in A + B + C); pE = Ln('P', E)
    F = pp(sum(1 << Ln('T', T) for T in users)); perp = pm(F)
    allforced = 0
    for s in bits(perp):
        if KIND[s] != 'T': continue
        if all(mult(X, tuple(sorted(x for x in SUPP[s] if x not in X))) == 1 for X in users): allforced |= 1 << s
    nl = 0; nfr = 0; types = set()
    for l in range(V):
        if F >> l & 1: continue
        Ml = perp & HYP[l]
        if not (Ml >> pE & 1 and allforced & ~Ml == 0): continue
        nl += 1; P = pm(Ml); types.add((KIND[l], perp >> l & 1, pc(P), rank(P)))
        for a, b, c in itertools.combinations(bits(P), 3):
            m = (1 << a) | (1 << b) | (1 << c)
            if rank(m) != 3: continue
            Fp = pp(m)
            if Fp == F: continue
            nfr += 1
            if Fp in design_frames: hit += 1
    stats[(nl, nfr, tuple(sorted(types)))] += 1
print('per-node (#rider lines, #candidate rider frames, {(kind of l, l in perp, |pm(M_l)|, rank)}):', dict(stats))
print('candidate rider frames that are design frames:', hit)

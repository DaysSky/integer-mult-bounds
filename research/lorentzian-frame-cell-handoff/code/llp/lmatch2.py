"""Union in-chain frame top evaluation for a good-frame system (own-frame tops).
1. weak routability: (t,u) routable iff some e in M(t), f in M(u): e _|_ u, f _|_ t, e _|_ f.
2. sharing: per line u, max matching of R(u) by reciprocal u-routable sections {t,e}; matched pairs get u through
   the shared section; unmatched targets get u through a non-shared routable own section (if any) -> 'private'
   incidences; targets with no routable own section for u -> 'unroutable'.
3. parts: A_S (shared part of each reciprocal section, from the matchings) and per-user private additions; kappa test:
   is A_S inside the union of two rank-8 nodes S & x-perp (x not in the plane)?
4. register estimate (model A): reciprocal sections 2 pieces (+1 copy if both users delivered; +1 if the users' parts
   differ and need a third piece), non-reciprocal sections 2 pieces for 1 user; each target 1 in-chain section.
usage: lmatch2.py system.json"""
import sys, json, collections, itertools
import networkx as nx
from lgeo import *
sysm = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}
M = {s: [x for x in bits(sysm[s]) if x != s] for s in range(V)}
O = lambda a, b: G[a][b] == 0
recip = set((min(t, e), max(t, e)) for t in range(V) for e in M[t] if t in M[e])
def routable_secs(t, u):
    return [e for e in M[t] if O(e, u) and any(O(f, t) and O(f, e) for f in M[u])]
part = collections.defaultdict(int)       # (t, e) directed: lines t receives through section {t,e}
unr = 0; priv = 0; shared_inc = 0
for u in range(V):
    Ru = bits(HYP[u])
    H = nx.Graph(); H.add_nodes_from(Ru)
    for t in Ru:
        for e in routable_secs(t, u):
            if (min(t, e), max(t, e)) in recip and O(e, u): H.add_edge(t, e)
    mt = nx.max_weight_matching(H, maxcardinality=True)
    matched = set()
    for a, b in mt:
        part[(a, b)] |= 1 << u; part[(b, a)] |= 1 << u; matched |= {a, b}; shared_inc += 2
    for t in Ru:
        if t in matched: continue
        rs = routable_secs(t, u)
        if rs: part[(t, rs[0])] |= 1 << u; priv += 1
        else: unr += 1
# section-level analysis
def plane_lines(t, e): return (1 << t) | (1 << e)
def two_node(S, A, pl):
    xs = [x for x in range(V) if not (pl >> x & 1)]
    Ns = [S & HYP[x] for x in xs]
    for i, Ni in enumerate(Ns):
        rem = A & ~Ni
        if rem == 0: return 1
        for Nj in Ns:
            if rem & ~Nj == 0: return 2
    return 3
stats = collections.Counter(); regs = 0.0
for (a, b) in sorted(recip):
    S = HYP[a] & HYP[b]; pl = plane_lines(a, b)
    Aa, Ab = part[(a, b)], part[(b, a)]
    ka, kb = two_node(S, Aa, pl) if Aa else 0, two_node(S, Ab, pl) if Ab else 0
    same = Aa == Ab
    kU = two_node(S, Aa | Ab, pl) if (Aa | Ab) else 0
    stats[('recip', 'same' if same else 'diff', ka, kb)] += 1
    # pieces: same -> max(ka,kb); differ -> need span containing both: <= ka + kb, >= max + 1
    regs += (max(ka, kb) if same else min(ka + kb, kU + 1))
for t in range(V):
    for e in M[t]:
        if (min(t, e), max(t, e)) in recip: continue
        S = HYP[t] & HYP[e]; A = part[(t, e)]
        k = two_node(S, A, plane_lines(t, e)) if A else 0
        stats[('nonrecip', k)] += 1; regs += k
# deliveries: each target 3 sections, 1 in-chain -> 2 dedicated deliveries; copies counted as the
# deliveries not covered by distinct pieces (crude): add 220*2 - (pieces usable as deliveries) later
print('weak routability: unroutable (t,u) %d of 26070 ; private (non-shared) incidences %d ; shared %d' % (unr, priv, shared_inc))
for k, v in sorted(stats.items(), key=str): print('  ', k, v)
print('pieces (kappa sum over sections) %.0f ; reciprocal sections %d ; non-reciprocal %d' % (regs, len(recip), sum(1 for t in range(V) for e in M[t] if (min(t, e), max(t, e)) not in recip)))

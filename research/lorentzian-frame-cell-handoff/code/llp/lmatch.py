"""Union-top sharing test for a good-frame system (own-frame tops, in-chain union reads, kappa = 2 shared parts).
For each line u: targets R(u) must receive x_u through exactly one of their frame sections {t,e}-perp; a SHARED
section (e in mates(t) and t in mates(e)) delivers the same part to both users, so the shared deliveries of u form a
matching in H_u = {edges {t,e} reciprocal, t,e in R(u), section u-routable: some mate f of u with f _|_ t, e}.
Reports per system: sum over u of the deficiency |R(u)| - 2 nu(H_u) (targets needing a non-shared delivery of u),
and the number of (t,u) with no routable section at all (own frame).  usage: lmatch.py system.json [system2 ...]"""
import sys, json, collections
import networkx as nx
from lgeo import *
def run(path):
    sysm = {int(k): v for k, v in json.load(open(path)).items()}
    mates = {s: [x for x in bits(sysm[s]) if x != s] for s in range(V)}
    recip = set()
    for t in range(V):
        for e in mates[t]:
            if t in mates[e]: recip.add((min(t, e), max(t, e)))
    defic = 0; unr = 0; oddmin = 0; nonrec_sec = sum(1 for t in range(V) for e in mates[t] if t not in mates[e])
    for u in range(V):
        Ru = set(bits(HYP[u]))
        fm = mates[u]
        H = nx.Graph(); H.add_nodes_from(Ru)
        for (t, e) in recip:
            if t in Ru and e in Ru and any(G[f][t] == 0 and G[f][e] == 0 for f in fm):
                H.add_edge(t, e)
        nu = len(nx.max_weight_matching(H, maxcardinality=True))
        defic += len(Ru) - 2 * nu
        oddmin += len(Ru) % 2
        for t in Ru:
            if not any((G[u][e] == 0) and any(G[f][t] == 0 and G[f][e] == 0 for f in fm) for e in mates[t]): unr += 1
    print('%-40s reciprocal sections %d, non-reciprocal %d | sharing deficiency %d (parity minimum %d) | (t,u) with no routable own section %d'
          % (path.split('/')[-1], len(recip), nonrec_sec, defic, oddmin, unr), flush=True)
for p in sys.argv[1:]: run(p)

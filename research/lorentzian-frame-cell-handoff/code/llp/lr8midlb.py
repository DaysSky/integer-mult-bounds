"""Design-specific LOWER BOUND on middle waste at the rank-7 stop (chains ...,5,7 -> 8 or ...,3,7 -> 8).
At a node F-perp, each arriving register carries c with rank(supp c) <= 7 and stops before at the rank-7 closed set
M = closure(c) when rank(c) = 7 (forced).  At M with j registers, contents arrive from rank-<=5 stops, so
j >= kappa5(W_M) >= 2 whenever W_M has rank 7 (W_M = union of supports at M).  Nodes with dim S = 1 whose vector has
rank 7 force c (and M).  LB = #forced closures holding exactly one forced c - #all other registers (any of which could
be a free rider at such an M).  usage: lr8midlb.py det.json"""
import sys, json, collections, pickle
from lgeo import *
D = json.load(open(sys.argv[1]))
sel = {int(k): v for k, v in D['sel'].items()}; det = D['det']
rot = [img_line(s, [(i + 1) % n for i in range(n)]) for s in range(V)]
rotp = [list(range(V))]
for k in range(1, n): rotp.append([rot[x] for x in rotp[-1]])
def rotm(m, k):
    r = 0
    for s in bits(m): r |= 1 << rotp[k % n][s]
    return r
orb = {}; reps = []
for s in range(V):
    if s in orb: continue
    reps.append(s); x = s
    for k in range(n): orb[x] = (len(reps) - 1, k); x = rot[x]
cov = pickle.load(open(__import__('os').environ.get('POOL', 'r8covers.pkl'), 'rb'))
asg = collections.defaultdict(int)
for key, v in det['assign'].items():
    ri, i, u = map(int, key.split(','))
    if v: asg[(ri, i)] |= 1 << u
users = collections.defaultdict(list)
for t in range(V):
    o, k = orb[t]; ci = det['cin'][o].index(1)
    for j, F in enumerate(cov[reps[o]][sel[reps[o]]]):
        users[rotm(F, k)].append((rotm(asg[(o, j)], k), j == ci))
def span_closure(v):
    """lines in span(v)"""
    r = rank(v); out = v
    for x in range(V):
        if not out >> x & 1 and rank(v | (1 << x)) == r: out |= 1 << x
    return out
forced = collections.Counter(); flexible = 0; forced_node = {}; regs = {}
for F, us in users.items():
    vecs = []
    for p, inch in us: vecs.append(p)
    # dim of S
    basis = []
    for v in vecs:
        for b in basis:
            if v ^ b < v: v ^= b
        if v: basis.append(v); basis.sort(reverse=True)
    k = sum(1 for p, inch in us if not inch)
    if len(basis) == 1 and rank(basis[0]) == 7 and max(k, 1) == 1:
        Mc = span_closure(basis[0]); forced[Mc] += 1; forced_node[Mc] = F; regs[F] = 0
    else:
        regs[F] = max(k, 2 * len(basis))
        # registers at this node: at most max(k, 2*dim) (generous upper count of flexible registers)
        flexible += max(k, 2 * len(basis))
single = sum(1 for M, c in forced.items() if c == 1)
print('forced rank-7 c (dim-1 nodes):', sum(forced.values()), 'distinct closures', len(forced), 'closures with one forced c', single)
print('flexible registers (generous)', flexible, '-> LB middle waste at rank-7 stop >=', max(0, single - flexible))

# refined: a free rider at forced M must come from another used node F' with F' inside pm(M) (its register's c lies in
# M, which lies in F'-perp).  Bipartite matching: forced singleton closures <-> registers of such nodes.
import networkx as nx
G2 = nx.Graph(); Ms = [M for M, c in forced.items() if c == 1]
for a, M in enumerate(Ms):
    P = pm(M)
    for F2, r in regs.items():
        if F2 == forced_node[M] or r == 0: continue
        if F2 & ~P == 0:
            for q in range(r): G2.add_edge(('M', a), ('R', F2, q))
mt = nx.bipartite.maximum_matching(G2, top_nodes=[n for n in G2 if n[0] == 'M']) if G2.number_of_edges() else {}
matched = sum(1 for n in mt if n[0] == 'M')
iso = sum(1 for a in range(len(Ms)) if ('M', a) not in G2)
print('forced singleton closures', len(Ms), '| with no possible rider node', iso, '| max rider matching', matched,
      '-> RIGOROUS LB middle waste (this top) >=', len(Ms) - matched)

"""Full top-level evaluation of a union in-chain frame design (own covers: each line's 3 mates; sections {t,e}-perp).
Per line u: serve every target t in R(u) through exactly one routable section of t.  Shared (reciprocal) sections
give the same part to both users (kappa = 2 rule), so shared deliveries of u form a matching; a target may instead
take u through a single-user (non-reciprocal) routable section ('free private'); leftovers need a differing part in a
reciprocal section ('diff', +1 piece for that section) or are unroutable.  Max-weight matching maximises service.
Then: parts per section, 2-node (kappa <= 2) test per part, in-chain orientation (bipartite matching), model-A
register count: reciprocal 2 (+1 if both users delivered, +1 if parts differ), single-user 2, kappa-3 parts +1,
+1 private register per target with unroutable lines.  usage: lmatch3.py system.json [parts_out.json] [blocks.json]
With blocks.json (A3 packing), matching edges {t, opp_X(t)} carrying a line u of X-perp get weight 3 (prefer
routing each block's A3-perp through its 3 opposite-pair sections -> shared A3-perp node)."""
import sys, json, collections
import networkx as nx
from lgeo import *
sysm = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}
M = {s: [x for x in bits(sysm[s]) if x != s] for s in range(V)}
BL = json.load(open(sys.argv[3])) if len(sys.argv) > 3 else []
blk = {t: i for i, X in enumerate(BL) for t in X}
Xperp = [HYP[X[0]] & HYP[X[1]] & HYP[X[2]] & HYP[X[3]] & HYP[X[4]] & HYP[X[5]] for X in BL]
O = lambda a, b: G[a][b] == 0
recip = set((min(t, e), max(t, e)) for t in range(V) for e in M[t] if t in M[e])
single = set((t, e) for t in range(V) for e in M[t] if (min(t, e), max(t, e)) not in recip)
def rsecs(t, u): return [e for e in M[t] if O(e, u) and any(O(f, t) and O(f, e) for f in M[u])]
part = collections.defaultdict(int)     # directed (t,e): lines t takes through section {t,e}
diffsec = collections.Counter(); unr_t = collections.Counter(); nfree = ndiff = nunr = nshared = 0
for u in range(V):
    Ru = bits(HYP[u])
    H = nx.Graph()
    opts = {t: rsecs(t, u) for t in Ru}
    for t in Ru:
        for e in opts[t]:
            if (min(t, e), max(t, e)) in recip and e in opts and t in rsecs(e, u):
                w = 3 if (t in blk and blk.get(e) == blk[t] and Xperp[blk[t]] >> u & 1) else 2
                H.add_edge(t, e, weight=w)
        if any((t, e) in single for e in opts[t]): H.add_edge(t, ('free', t), weight=1)
    mt = nx.max_weight_matching(H)
    served = set()
    for a, b in mt:
        if isinstance(a, tuple) or isinstance(b, tuple):
            t = b if isinstance(a, tuple) else a
            e = next(e for e in opts[t] if (t, e) in single); part[(t, e)] |= 1 << u; served.add(t); nfree += 1
        else:
            part[(a, b)] |= 1 << u; part[(b, a)] |= 1 << u; served |= {a, b}; nshared += 2
    for t in Ru:
        if t in served: continue
        if opts[t]:
            e = opts[t][0]; part[(t, e)] |= 1 << u; ndiff += 1
            if (min(t, e), max(t, e)) in recip: diffsec[(min(t, e), max(t, e))] += 1
        else: nunr += 1; unr_t[t] += 1
def kap(S, A, pl):
    if A == 0: return 0
    Ns = [S & HYP[x] for x in range(V) if not (pl >> x & 1)]
    for Ni in Ns:
        rem = A & ~Ni
        if rem == 0: return 1
        for Nj in Ns:
            if rem & ~Nj == 0: return 2
    return 3
kst = collections.Counter(); regs_pieces = 0; extra = 0
for (a, b) in recip:
    S = HYP[a] & HYP[b]; pl = (1 << a) | (1 << b)
    A1, A2 = part[(a, b)], part[(b, a)]
    k = kap(S, A1 | A2, pl)
    kst[('recip', k, 'same' if A1 == A2 else 'diff')] += 1
    regs_pieces += max(2, k) + (1 if A1 != A2 else 0)
for (t, e) in single:
    S = HYP[t] & HYP[e]; k = kap(S, part[(t, e)], (1 << t) | (1 << e))
    kst[('single', k)] += 1; regs_pieces += max(2, k) if part[(t, e)] else 0
# in-chain orientation: maximise reciprocal sections with an in-chain user
B = nx.Graph()
for t in range(V):
    for e in M[t]:
        key = (min(t, e), max(t, e))
        if key in recip: B.add_edge(('t', t), ('s',) + key)
mb = nx.bipartite.maximum_matching(B, top_nodes=[n for n in B if n[0] == 't']) if B.number_of_edges() else {}
covered = len([k for k in mb if k[0] == 's'])
deldel = len(recip) - covered
total = regs_pieces + deldel + len(unr_t)
print('system', sys.argv[1].split('/')[-1])
print('  reciprocal sections %d, single-user %d' % (len(recip), len(single)))
print('  incidences: shared %d, free private %d, differing-part %d (in %d reciprocal sections), unroutable %d (%d targets)'
      % (nshared, nfree, ndiff, len(diffsec), nunr, len(unr_t)))
print('  kappa of parts:', sorted(kst.items(), key=str))
print('  in-chain covers %d reciprocal sections -> (del,del) %d' % (covered, deldel))
print('  model-A registers: pieces/diff %d + copies %d + unroutable privates %d = %d -> R ~ %d' % (regs_pieces, deldel, len(unr_t), total, total - 220))
if len(sys.argv) > 2 and sys.argv[2] != '-':
    json.dump({'%d,%d' % k: hex(v) for k, v in part.items() if v}, open(sys.argv[2], 'w'))

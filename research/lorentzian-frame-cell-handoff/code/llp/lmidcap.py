"""Middle capacity screen for a union in-chain frame design (necessary conditions, zero-waste two-level middle).
Input: system + parts (lmatch3 output).  For each section S (shared part = union of its users' parts) pick a 2-node
decomposition A = P1 + P2, P_i inside N_i = S & x_i-perp (rank-8 nodes), preferring nodes already used (sharing).
Per node N: k_N pieces, U_N = union of piece supports.  Zero-waste needs k_N inputs, each from a rank-3 first frame
(<= 6 lines) -> U_N <= 6 k_N; inputs total = sum k_N <= cell registers (3 per line = 660) + extra.
Reports: pieces, distinct nodes, node-sharing histogram, nodes violating U_N <= 6 k_N (and the extra inputs they
need), total extra registers estimate.  usage: lmidcap.py system.json parts.json"""
import sys, json, collections
from lgeo import *
sysm = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}
parts = {tuple(int(x) for x in k.split(',')): int(v, 16) for k, v in json.load(open(sys.argv[2])).items()}
M = {s: [x for x in bits(sysm[s]) if x != s] for s in range(V)}
secpart = collections.defaultdict(int)
for (t, e), A in parts.items(): secpart[(min(t, e), max(t, e))] |= A
usage = collections.Counter()
def decomp(S, A, pl):
    xs = [x for x in range(V) if not (pl >> x & 1)]
    best = None
    for x in xs:
        N1 = S & HYP[x]; rem = A & ~N1
        if rem == 0:
            sc = (1, -usage[N1]); cand = ((N1, A),)
        else:
            cand = None
            for y in xs:
                N2 = S & HYP[y]
                if rem & ~N2 == 0:
                    sc = (2, -(usage[N1] + usage[N2])); cand = ((N1, A & N1), (N2, rem)); break
            if cand is None: continue
        if best is None or sc < best[0]: best = (sc, cand)
    return best[1] if best else None
pieces = []; fails = 0
for (a, b), A in sorted(secpart.items()):
    S = HYP[a] & HYP[b]; pl = (1 << a) | (1 << b)
    d = decomp(S, A, pl)
    if d is None: fails += 1; continue
    for N, P in d:
        usage[N] += 1; pieces.append((N, P))
byN = collections.defaultdict(list)
for N, P in pieces: byN[N].append(P)
viol = 0; extra = 0; hist = collections.Counter()
for N, Ps in byN.items():
    k = len(Ps); U = 0
    for P in Ps: U |= P
    hist[k] += 1
    if pc(U) > 6 * k: viol += 1; extra += -(-pc(U) // 6) - k
print('sections', len(secpart), 'no 2-node decomposition', fails, 'pieces', len(pieces), 'distinct nodes', len(byN))
print('pieces per node histogram', sorted(hist.items()))
print('nodes with support > 6 x pieces:', viol, ' extra inputs needed', extra)
print('cell registers 660 vs pieces + extra inputs', len(pieces) + extra)

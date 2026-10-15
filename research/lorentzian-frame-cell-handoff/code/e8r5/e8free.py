"""Free-riding screen for E8 4-cover tops.  For an A3 X and each of its 6 lines b: over b's covers containing X and all
assignments of b's multiply-covered lines, the achievable parts A_b(X) (lines b takes from section X-perp).
Reports per pair (t,b) in X whether some part is achievable by both (identical parts -> t in-chain rides free on b),
and whether a part of t is the XOR of parts of two other users (span with 2 co-users)."""
import sys, itertools, collections, pickle
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
V = e8.V; HYP = e8.HYP; bits = e8.bits
pc = lambda m: bin(m).count('1')
def pm(m):
    r = e8.FULL
    for s in bits(m): r &= HYP[s]
    return r
cov = pickle.load(open('covers.pkl', 'rb'))['covers']
def parts_on(t, X):
    """all achievable parts of t on X-perp over t's covers containing X"""
    R = HYP[t] & ~(1 << t); out = set(); ncov = 0
    for Xs, Z in cov[t]:
        if X not in Xs: continue
        ncov += 1
        sets = [pm(Y) & R for Y in Xs] + [pm(Z) & R]
        i = list(Xs).index(X)
        mult = [u for u in bits(R) if sum(S >> u & 1 for S in sets) > 1]
        excl = sets[i]
        for j, S in enumerate(sets):
            if j != i: excl &= ~S
        flex = [u for u in mult if sets[i] >> u & 1]
        for k in range(len(flex) + 1):
            for sub in itertools.combinations(flex, k):
                A = excl
                for u in sub: A |= 1 << u
                out.add(A)
    return out, ncov
X = cov[0][0][0][0]
users = bits(X)
P = {}
for b in users:
    P[b], nc = parts_on(b, X)
    print('user', b, 'covers containing X', nc, 'achievable parts', len(P[b]), 'part sizes', sorted(set(pc(A) for A in P[b])), flush=True)
for t in users:
    same = [b for b in users if b != t and P[t] & P[b]]
    xor2 = 0
    for b, c in itertools.combinations([x for x in users if x != t], 2):
        Pb = P[b]; Pc = P[c]
        if any((A ^ B) in P[t] for A in Pb for B in Pc): xor2 += 1
    print('target', t, 'identical part with users', same, '| pairs (b,c) with part_t = part_b XOR part_c:', xor2, flush=True)

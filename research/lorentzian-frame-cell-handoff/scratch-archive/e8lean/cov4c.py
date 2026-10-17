"""E8 4-covers of R(t) by rank-5 flats, using the fact that every 4-cover contains a D5 (only flats of >= 16 lines).
Fix one D5 representative W1 (the stabiliser of t acts transitively on the 378 D5s of t-perp -- checked by orbit
size under the stabiliser below via Gram invariants is not attempted; we simply loop over ALL D5s if --all).
Remaining 3 flats: branch on the lowest uncovered line, last flat found by bitset intersection."""
import sys, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
V = e8.V; t = 0; P = e8.HYP[t]; Pl = e8.bits(P)
pc = lambda m: bin(m).count('1')
flats = {0: 0}; fr = [0]
while fr:
    nf = []
    for F in fr:
        if flats[F] >= 5: continue
        for s in Pl:
            if F >> s & 1: continue
            Fc, d = e8.closure(F | (1 << s))
            if Fc not in flats: flats[Fc] = d; nf.append(Fc)
    fr = nf
top = [F for F, d in flats.items() if d == 5]
size = [pc(F) for F in top]
n = len(top)
member = collections.defaultdict(int)        # line -> bitmask over flat indices
for i, F in enumerate(top):
    for s in e8.bits(F): member[s] |= 1 << i
ALL = (1 << n) - 1
def perplines(F):
    m = (1 << V) - 1
    for s in e8.bits(F): m &= e8.HYP[s]
    return pc(m)
def containing(U):
    m = ALL
    for s in e8.bits(U):
        m &= member[s]
        if not m: break
    return m
def covers_k(U, k):
    """all sets of k flats (indices) covering U"""
    out = []
    if k == 1:
        m = containing(U)
        while m:
            b = m & -m; out.append((b.bit_length() - 1,)); m ^= b
        return out
    s = (U & -U).bit_length() - 1
    need = pc(U)
    m = member[s]
    while m:
        b = m & -m; i = b.bit_length() - 1; m ^= b
        if pc(top[i] & U) + 20 * (k - 1) < need: continue
        for rest in covers_k(U & ~top[i], k - 1):
            out.append((i,) + rest)
    return out
d5 = [i for i in range(n) if size[i] == 20]
reps = d5 if '--all' in sys.argv else d5[:1]
res = set()
for i in reps:
    for rest in covers_k(P & ~top[i], 3):
        res.add(tuple(sorted((i,) + rest)))
print('covers containing the chosen D5(s):', len(res), '(over', len(reps), 'D5 reps)', flush=True)
pl = {}
types = collections.Counter(); mult = collections.Counter()
for cv in res:
    for i in cv:
        if i not in pl: pl[i] = perplines(top[i])
    types[tuple(sorted(((size[i], pl[i]) for i in cv), reverse=True))] += 1
    mm = collections.Counter(sum(1 for i in cv if top[i] >> s & 1) for s in Pl)
    mult[tuple(sorted(mm.items()))] += 1
for k, c in sorted(types.items(), key=lambda kv: -kv[1]): print('  type (lines, perp lines):', k, c)
for k, c in sorted(mult.items(), key=lambda kv: -kv[1])[:12]: print('  multiplicity profile {mult: #lines}:', k, c)

"""E8: all 3-covers of R(t) by flats of rank <= 6 inside t-perp (rank-6 = hyperplanes of t-perp), classified by
(rank, #lines, #users = lines in W-perp).  Exact: every 3-cover has a flat of >= 21 lines."""
import sys, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
V = e8.V; t = 0; P = e8.HYP[t]; Pl = e8.bits(P)
pc = lambda m: bin(m).count('1')
flats = {0: 0}; fr = [0]
while fr:
    nf = []
    for F in fr:
        if flats[F] >= 6: continue
        for s in Pl:
            if F >> s & 1: continue
            Fc, d = e8.closure(F | (1 << s))
            if Fc not in flats: flats[Fc] = d; nf.append(Fc)
    fr = nf
print('flats by rank', dict(sorted(collections.Counter(flats.values()).items())), flush=True)
cand = [F for F, d in flats.items() if d in (5, 6)]
def users(F):
    m = (1 << V) - 1
    for s in e8.bits(F): m &= e8.HYP[s]
    return pc(m)
info = {F: (flats[F], pc(F), users(F)) for F in cand}
print('rank-6 types (lines, users):', dict(collections.Counter((pc(F), info[F][2]) for F in cand if flats[F] == 6)))
print('rank-5 types (lines, users):', dict(collections.Counter((pc(F), info[F][2]) for F in cand if flats[F] == 5)))
big = [F for F in cand if pc(F) >= 21]
member = collections.defaultdict(int); idx = {F: i for i, F in enumerate(cand)}
for i, F in enumerate(cand):
    for s in e8.bits(F): member[s] |= 1 << i
ALL = (1 << len(cand)) - 1
def containing(U):
    m = ALL
    for s in e8.bits(U):
        m &= member[s]
        if not m: break
    return m
types = collections.Counter()
seen = set()
for F1 in big:
    U = P & ~F1
    s = (U & -U).bit_length() - 1
    m = member[s]
    while m:
        b = m & -m; i = b.bit_length() - 1; m ^= b
        F2 = cand[i]
        U2 = U & ~F2
        mm = containing(U2) if U2 else ALL
        while mm:
            bb = mm & -mm; j = bb.bit_length() - 1; mm ^= bb
            key = tuple(sorted((idx[F1], i, j)))
            if key in seen or len(set(key)) < 3: continue
            seen.add(key)
            types[tuple(sorted((info[cand[k]] for k in key), reverse=True))] += 1
print('3-covers:', len(seen))
for k, n in sorted(types.items(), key=lambda kv: -kv[1]): print('  ', k, n)

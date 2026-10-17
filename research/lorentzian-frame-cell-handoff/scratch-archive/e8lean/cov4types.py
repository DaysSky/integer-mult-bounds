"""E8: all 4-covers of R(t) (63 lines) by rank-<=5 flats inside t-perp (maximal ones), classified by flat types
(#lines) and sharing (#lines in W-perp = targets that could use W).  Exact branching search."""
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
def perplines(F):
    m = (1 << V) - 1
    for s in e8.bits(F): m &= e8.HYP[s]
    return pc(m)
by_line = collections.defaultdict(list)
for i, F in enumerate(top):
    for s in e8.bits(F): by_line[s].append(i)
covers = set()
def rec(m, chosen, k):
    if m == P: covers.add(tuple(sorted(chosen))); return
    if k == 0: return
    u = P & ~m; s = (u & -u).bit_length() - 1
    for i in by_line[s]:
        if i in chosen: continue
        rec(m | top[i], chosen + [i], k - 1)
rec(0, [], 4)
print('4-covers by rank-5 flats:', len(covers))
info = {}
types = collections.Counter()
for cv in covers:
    key = []
    for i in cv:
        if i not in info: info[i] = (pc(top[i]), perplines(top[i]))
        key.append(info[i])
    types[tuple(sorted(key))] += 1
for k, n in sorted(types.items(), key=lambda kv: -kv[1])[:20]:
    print('  ', n, '(lines, perp lines) x4:', k)

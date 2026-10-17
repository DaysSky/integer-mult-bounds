"""E8 4-covers of R(t) by rank-5 flats, exact: flats sorted by size; recursion with the bound
(largest remaining flat size) * k >= #uncovered.  Classify by (lines, perp-lines) and line multiplicity."""
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
top = sorted([F for F, d in flats.items() if d == 5], key=pc, reverse=True)
size = [pc(F) for F in top]
print('rank-5 flats', len(top), flush=True)
def perplines(F):
    m = (1 << V) - 1
    for s in e8.bits(F): m &= e8.HYP[s]
    return pc(m)
covers = []
def rec(unc, k, start, chosen):
    if unc == 0:
        covers.append(tuple(chosen)); return
    if k == 0: return
    need = pc(unc)
    for i in range(start, len(top)):
        if size[i] * k < need: break
        g = pc(top[i] & unc)
        if g == 0: continue
        # the chosen flats are in decreasing size order; the remaining k-1 flats have size <= size[i]
        if g + size[i] * (k - 1) < need: continue
        rec(unc & ~top[i], k - 1, i + 1, chosen + [i])
rec(P, 4, 0, [])
print('4-covers:', len(covers), flush=True)
pl = {}
types = collections.Counter(); mult = collections.Counter()
for cv in covers:
    for i in cv:
        if i not in pl: pl[i] = perplines(top[i])
    types[tuple(sorted(((size[i], pl[i]) for i in cv), reverse=True))] += 1
    m = collections.Counter(sum(1 for i in cv if top[i] >> s & 1) for s in Pl)
    mult[tuple(sorted(m.items()))] += 1
for k, n in sorted(types.items(), key=lambda kv: -kv[1]): print('  type (lines, perp lines):', k, n)
for k, n in sorted(mult.items(), key=lambda kv: -kv[1])[:10]: print('  multiplicity profile:', k, n)

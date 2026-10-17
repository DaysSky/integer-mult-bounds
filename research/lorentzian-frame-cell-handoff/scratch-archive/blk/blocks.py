# Group partition frames into blocks (frames sharing the cell-sum plane pi), compute W, layers, sharing, frames.
import sys, pickle, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, bits, V, nondegenerate, closure, dim
HYP = g.HYP
def vec(x):
    m = 0
    for i in g.supp[x]: m |= 1 << i
    if g.kind[x] == 'T': m |= 1 << 11
    return m
vv = [vec(x) for x in range(V)]
dot = lambda a, b: bin(a & b).count('1') & 1
def span(gens):
    S = {0}
    for x in gens: S |= {s ^ x for s in S}
    return S
def N(Vs): return sum(1 << l for l in range(V) if all(dot(vv[l], u) == 0 for u in Vs))
def pm(m):
    r = g.FULL
    for s in bits(m): r &= HYP[s]
    return r
frames, pun = pickle.load(open(sys.argv[1], 'rb'))
pis = collections.defaultdict(list)
for q in frames:
    t, a, b, c = q
    pi = frozenset({vv[t] ^ vv[a], vv[t] ^ vv[b], vv[t] ^ vv[c]})
    pis[pi].append(q)
print('frames', len(frames), '| blocks by pi:', collections.Counter(len(v) for v in pis.values()))
lineof = {vv[x]: x for x in range(V)}
for pi, fs in list(pis.items())[:6]:
    Wv = span([vv[x] for q in fs for x in q])
    Wd = len(Wv).bit_length() - 1
    wl = [lineof[x] for x in Wv if x in lineof]
    kinds = ''.join(sorted(g.kind[x] for x in wl))
    NW = N(Wv)
    # hyperplanes of W not containing pi
    pil = sorted(pi)
    hyps = set()
    gens = list(Wv - {0})
    for a, b, c in itertools.combinations(gens, 3):
        S = span([a, b, c])
        if len(S) == 8 and S <= Wv: hyps.add(frozenset(S))
    nonpi = [S for S in hyps if not set(pi) <= S]
    lay = []
    for S in nonpi:
        L = N(S) & ~NW
        lines_in = [lineof[x] for x in S if x in lineof]
        realF = pm(sum(1 << x for x in lines_in))
        cells = sum(1 for q in fs for x, y in itertools.combinations(q, 2) if vv[x] in S and vv[y] in S)
        lay.append((bin(L).count('1'), len(lines_in), cells, bin(L & ~realF).count('1'), dim(realF), nondegenerate(realF)))
    print('block', len(fs), 'frames | dim W', Wd, '| lines in W', len(wl), kinds, '| |N(W)|', bin(NW).count('1'),
          '| real pm(W) lines', bin(pm(sum(1 << x for x in wl))).count('1'), '| layers', len(nonpi))
    print('   layers (size, lines in V, cells in V, lines outside real pm(V), rank pm(V), nd):', sorted(lay))

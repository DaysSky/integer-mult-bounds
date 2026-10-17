def vec(x):
    m = 0
    for i in g.supp[x]: m |= 1 << i
    if g.kind[x] == 'T': m |= 1 << 11
    return m
vv = [vec(x) for x in range(V)]
lineof = {vv[x]: x for x in range(V)}
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

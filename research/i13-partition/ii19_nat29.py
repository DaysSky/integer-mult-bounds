"""THE ONE-STATION FEASIBILITY CENSUS (ii19_nat29.py) — the redesign's core constraint measured.

The one-station design (each helper read ONCE, at its station F(h); every register ONE climb):
  - station F(h) ⊇ span(value(h)), and F(h) ⊆ I(h) := (span{L_t : t in T(h)})^⊥, where T(h) =
    the targets whose delivered value depends on h (the DAG reachability) — because the reader
    chain nests: F(h) ⊆ F(h2) ⊆ ... ⊆ perp(t) at the B-read leaves;
  - the sources' crux: every source's fed stations {F(h) : h reads s} must form ONE nested
    chain (the source climbs it once) — the cross-constraint: value(h1) ⊆ I(h2)-compatibility.

Measures: (1) the dep-DAG (int-bitmask propagation through D/A/scatter/B); (2) T(h), dim I(h),
span-rank(value(h)), the value ⊆ I verification; (3) per source: the fed helpers and their
pairwise nesting compatibility -> the minimal forced chain length (greedy).
"""
import json, os, sys
from collections import Counter, defaultdict
from fractions import Fraction

sys.argv = ['ii19_nat20.py']
exec(open('ii19_nat20.py').read().split('# (1) chain-shape census')[0])

BF = [[Fraction(x, w['form']['den']) for x in row] for row in w['form']['num']]
def ip(x, y): return sum(x[i] * BF[i][j] * y[j] for i in range(H) for j in range(H) if BF[i][j])

# ---- the atom-dep propagation (atom i <-> bit i; UNION = read-incidence, not XOR-parity:
# ---- the delivery's value-parity cancels by design (the dirt-doubling), so T(h) must count READS) ----
nreg = len(w['start'])
def atom(r): return r if r < V else r - V          # helper 2V+i -> atom V+i
dep = [0] * nreg
for r in range(nreg):
    if r < V or r >= 2 * V: dep[r] = 1 << atom(r)   # sources and helpers start as their own atom
W = w
# (D excluded: it reads self-bits pre-A, no value-flow)
for F, d, srcs in W['A']:
    x = 0
    for s in srcs: x |= dep[s]
    dep[d] |= x
for t in range(V):
    for k in W['scatter'][t]:
        dep[V + t] |= dep[W['ret'][k]]
for F, d, srcs in W['B']:
    x = 0
    for s in srcs: x |= dep[s]
    dep[d] |= x

T = defaultdict(set)          # helper atom -> {targets}
for t in range(V):
    x = dep[V + t]
    i = 0
    while x:
        b = x & -x; a = b.bit_length() - 1; x ^= b
        if a >= V: T[a].add(t)          # helper atoms only (V..V+R-1)
log('(1) helper atoms reaching targets: %d | |T(h)| hist %s' % (
    len(T), dict(sorted(Counter(len(v) for v in T.values()).items()))))

# ---- I(h) dims and value spans ----
def rank_lines(ls):
    m = [list(L[i]) for i in ls]; r = 0
    for c in range(H):
        p = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if p is None: continue
        m[r], m[p] = m[p], m[r]
        iv = Fraction(1) / m[r][c]; m[r] = [x * iv for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]; m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
    return r

def perp_dim(ts):
    return H - rank_lines(list(ts))

# values: simulate A-final values (line bitmasks)
val = [1 << r for r in range(nreg)]
for F, d, srcs in W['D']:
    for s in srcs: val[d] ^= val[s]
for F, d, srcs in W['A']:
    for s in srcs: val[d] ^= val[s]

rankI, slack, badval = Counter(), Counter(), 0
Iof = {}
for h, ts in T.items():
    r = 2 * V + (h - V)
    dI = perp_dim(ts)
    Iof[h] = (ts, dI)
    vlines = []
    x = val[r] & ((1 << V) - 1)
    while x:
        b = x & -x; vlines.append(b.bit_length() - 1); x ^= b
    vr = rank_lines(vlines) if vlines else 0
    rankI[dI] += 1
    slack[dI - vr] += 1
    # verify value ⊆ I: every value line ⊥ to every L_t
    for s in vlines:
        for t in ts:
            if ip([Fraction(x) for x in L[s]], [Fraction(x) for x in L[t]]) != 0:
                badval += 1; break
log('(2) dim I(h) hist %s | slack (dimI - spanrank(value)) hist %s | value⊂I violations: %d' % (
    dict(sorted(rankI.items())), dict(sorted(slack.items())), badval))

# ---- per source: the fed helpers and the chain feasibility ----
fed = defaultdict(list)       # source -> [helper atoms reading it]
for F, d, srcs in W['A']:
    for s in srcs:
        if s < V and d >= 2 * V: fed[s].append(atom(d))
Tsizes = Counter(len(v) for v in fed.values())
log('(3) sources fed by A-gates: %d | fed-count hist %s' % (len(fed), dict(sorted(Tsizes.items()))))

def val_lines(h):
    r = 2 * V + (h - V)
    out, x = [], val[r] & ((1 << V) - 1)
    while x:
        b = x & -x; out.append(b.bit_length() - 1); x ^= b
    return out

# nesting compatibility: h1 -> h2 iff value(h1) ⊆ I(h2) (h1's station can nest inside h2's)
def nests(h1, h2):
    ts2, dI2 = Iof[h2]
    for s in val_lines(h1):
        for t in ts2:
            if ip([Fraction(x) for x in L[s]], [Fraction(x) for x in L[t]]) != 0:
                return False
    return True

chainlen = Counter()
examples = {}
for s, hs in fed.items():
    hs = sorted(set(hs))
    if len(hs) <= 1:
        chainlen[max(len(hs), 1)] += 1; continue
    # greedy chain cover: order by |T| ascending (big I first, low stations first)
    order = sorted(hs, key=lambda h: len(Iof[h][0]))
    chains = []
    for h in order:
        placed = False
        for c in chains:
            if c[-1] != h and nests(c[-1], h):
                c.append(h); placed = True; break
        if not placed:
            chains.append([h])
    chainlen[len(chains)] += 1
    if len(chains) >= 3 and 'worst' not in examples:
        examples['worst'] = (s, [tuple(x) for x in chains])
log('(4) per-source minimal fed-chain length (greedy, big-I-first): %s' % dict(sorted(chainlen.items())))
log('    a worst example (source %s): %s' % examples.get('worst', ('-', '-')))

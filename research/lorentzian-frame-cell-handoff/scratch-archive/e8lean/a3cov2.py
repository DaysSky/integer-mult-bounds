"""E8: count 4-covers of R(t) by D5 flats X-perp (X an A3 through t), by branching on uncovered lines (exact), and
describe their structure (pairwise relations of the four A3s)."""
import sys, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
V = e8.V; GI = e8.GI
pc = lambda m: bin(m).count('1')
perp = e8.HYP
t = 0; R = perp[t]
X = set()
for a in range(1, V):
    for b in range(a + 1, V):
        F, d = e8.closure((1 << t) | (1 << a) | (1 << b))
        if d == 3 and pc(F) == 6: X.add(F)
X = sorted(X)
def pm(F):
    m = (1 << V) - 1
    for s in e8.bits(F): m &= perp[s]
    return m
cov = [pm(F) & R for F in X]
idx_by_line = collections.defaultdict(list)
for i, c in enumerate(cov):
    for s in e8.bits(c): idx_by_line[s].append(i)
covers = set()
def rec(m, chosen, k):
    if m == R:
        covers.add(tuple(sorted(chosen))); return
    if k == 0: return
    u = R & ~m; s = (u & -u).bit_length() - 1
    for i in idx_by_line[s]:
        if i in chosen: continue
        rec(m | cov[i], chosen + [i], k - 1)
rec(0, [], 4)
print('A3s through t:', len(X), ' 4-covers by D5s:', len(covers))
types = collections.Counter()
for cv in covers:
    Fs = [X[i] for i in cv]
    inter = tuple(sorted(pc(Fs[a] & Fs[b]) for a, b in itertools.combinations(range(4), 2)))
    ov = tuple(sorted(collections.Counter(sum((cov[i] >> s) & 1 for i in cv) for s in e8.bits(R)).items()))
    types[(inter, ov)] += 1
for k, n in types.items(): print('  ', n, 'pairwise A3 intersections (#lines):', k[0], ' line multiplicities:', k[1])

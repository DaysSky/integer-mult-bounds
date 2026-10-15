"""Anatomy of the E8 A3-parity design (e8a3_sol_0.json): section decomposition into source cells (by block), how many
used sections contain each cell, complementary-block structure, keeper reads."""
import sys, os, json, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
V = e8.V; G = e8.GI; HYP = e8.HYP; bits = e8.bits
pc = lambda m: bin(m).count('1')
def pm(m):
    r = e8.FULL
    for s in bits(m): r &= HYP[s]
    return r
sol = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'e8a3_sol_0.json'))
tri = [int(h, 16) for h in sol['tri']]; pair = [int(h, 16) for h in sol['pair']]
cells_l = tri + pair
src = {int(k): int(v, 16) for k, v in sol['src'].items()}
cells = [int(h, 16) for h in json.load(open('../sec4/r420cells.json'))['planes']]
adj = collections.defaultdict(set)
for C in cells:
    a, b = bits(C); adj[a].add(b); adj[b].add(a)
frames = sorted(set(frozenset({s} | adj[s]) for s in range(V)), key=min)
blocks = sorted(set(e8.closure(sum(1 << x for x in f))[0] for f in frames))
blk = {s: i for i, B in enumerate(blocks) for s in bits(B)}
comp = {}
for i, B in enumerate(blocks):
    for j, B2 in enumerate(blocks):
        if all(G[a][b] == 0 for a in bits(B) for b in bits(B2)) and i != j: comp[i] = j
print('blocks', len(blocks), 'complementary pairs', sorted(set(tuple(sorted((i, j))) for i, j in comp.items())))
# per-line A3 and its planes
def planes_of_line(s):
    X = src[s]
    tris = [T for T in tri if T >> s & 1 and T & ~X == 0]
    prs = [P for P in pair if P >> s & 1]
    return tris, prs
# verify each line has 2 chosen tri + 1 chosen pair inside its A3
for s in range(V):
    tris, prs = planes_of_line(s)
    assert len(tris) == 2 and len(prs) == 1 and prs[0] & ~src[s] == 0
# A3 sharing: do the lines' A3s form a partition?
a3s = collections.Counter(src.values())
print('distinct source A3s', len(a3s), 'lines per A3', collections.Counter(a3s.values()))
# triangle / pair cells per block
print('tri cells per block', collections.Counter(blk[bits(T)[0]] for T in tri).most_common(3), 'pairs per block', collections.Counter(blk[bits(P)[0]] for P in pair).most_common(3))
# frames vs pairs: are the chosen pairs frame pairs (R420 cells)?
print('chosen pairs that are R420 cells', sum(1 for P in pair if P in set(cells)), 'of', len(pair))
# sections
secs = tri + pair
inc = collections.Counter()
for P in secs:
    S = pm(P); i = blk[bits(P)[0]]
    parts = collections.Counter()
    for j, B in enumerate(blocks):
        X = S & B
        if not X: continue
        if j == comp[i]: parts['Bcomp%d' % pc(X)] += 1; continue
        if j == i: parts['own%d' % pc(X)] += 1; continue
        k = 'T' if X in set(tri) else ('P' if X in set(pair) else 'other%d' % pc(X))
        parts[k] += 1
    inc[(pc(P), tuple(sorted(parts.items())))] += 1
print('section anatomy (plane size, pieces):')
for k, v in inc.items(): print('  ', k, v)
# how many used sections contain each cell
cont = collections.Counter()
for C in cells_l:
    cont[(pc(C), sum(1 for P in secs if C & ~pm(P) == 0))] += 1
print('cells: (size, #sections containing it):', sorted(cont.items()))

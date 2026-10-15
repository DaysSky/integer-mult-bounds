"""Quad search for the E8 A3-parity design: candidate nodes N = closure of two pieces of a common section; for each N:
the design cells (pieces) inside N and the used sections S containing N together with the pieces of S inside N.
A 'quad' is a node whose piece set P_N (design cells inside N, from blocks other than the section's own/complement) is the
same for every section it serves.  Report nodes covering 4 pieces of every section they serve, and the best 2-cover
of each section's 8 pieces by such nodes."""
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
dcells = tri + pair
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
        if i != j and all(G[a][b] == 0 for a in bits(B) for b in bits(B2)): comp[i] = j
secs = dcells[:]                      # section of plane P = pm(P)
pieces = {}
for P in secs:
    S = pm(P); i = blk[bits(P)[0]]
    pieces[P] = [C for C in dcells if C & ~S == 0 and blk[bits(C)[0]] not in (i, comp[i])]
    assert len(pieces[P]) in (8, 9), len(pieces[P])
print('pieces per section', collections.Counter(len(v) for v in pieces.values()))
# candidate nodes: closures of unions of 2 pieces of a common section
cand = set()
for P in secs:
    for c1, c2 in itertools.combinations(pieces[P], 2):
        cand.add(e8.closure(c1 | c2)[0])
print('candidate 2-piece closures', len(cand))
# extend: closures of 3 and 4 pieces (within a section) -- the quad level
cand4 = set()
for P in secs:
    for grp in itertools.combinations(pieces[P], 4):
        F, r = e8.closure(grp[0] | grp[1] | grp[2] | grp[3])
        if r <= 5: cand4.add((F, r))
print('4-piece closures of rank <= 5:', len(cand4), collections.Counter(r for F, r in cand4))
# for each such node: sections served and pieces inside per section
good = []
for F, r in cand4:
    served = [P for P in secs if F & ~pm(P) == 0]
    pin = {P: tuple(sorted(C for C in pieces[P] if C & ~F == 0)) for P in served}
    sizes = collections.Counter(len(v) for v in pin.values())
    good.append((F, r, len(served), sizes, len(set(pin.values()))))
good.sort(key=lambda x: -x[2])
for F, r, ns, sizes, nd in good[:15]:
    print('node rank', r, 'lines', pc(F), 'sections served', ns, 'pieces-inside sizes', dict(sizes), 'distinct piece sets', nd)
# which sections are served by the 20 quads, by type
cov = collections.Counter()
for F, r in cand4:
    for P in secs:
        if F & ~pm(P) == 0: cov[P] += 1
print('sections served by >=1 quad by plane size:', collections.Counter((pc(P), cov[P]) for P in secs))
# piece type inside quads
for F, r in list(cand4)[:3]:
    inside = [C for C in dcells if C & ~F == 0]
    print('quad: design cells inside', [pc(C) for C in inside], 'blocks', sorted(set(blk[bits(C)[0]] for C in inside)))

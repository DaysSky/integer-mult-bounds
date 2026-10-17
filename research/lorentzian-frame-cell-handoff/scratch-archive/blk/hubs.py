# Layer-assembly hubs for a block partition.  Layers L_B(V) (frame pm(V)) and block Q's (frame pm(W)) are the demands.
# A hub frame F serves demand D if F lies inside D's frame; it supplies |F n content(D)| lines to D.
# Candidates F: closures of pairs and triples of lines (rank <= 5, nondegenerate).  Report the incidence potential.
import sys, pickle, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, bits, V, nondegenerate, closure, dim
HYP = g.HYP
exec(open('/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/blk/f2lib.py').read())
blocks, pun = pickle.load(open(sys.argv[1], 'rb'))
dem = []    # (frame, content, tag)
for bi, fs in enumerate(blocks):
    Wv = span([vv[x] for q in fs for x in q])
    if len(Wv) != 16: continue
    NW = N(Wv); Wl = sum(1 << lineof[w] for w in Wv if w in lineof)
    dem.append((pm(Wl), NW, ('Q', bi)))
    pi = {vv[fs[0][0]] ^ vv[x] for x in fs[0][1:]}
    hyps = set()
    for a, b, c in itertools.combinations(list(Wv - {0}), 3):
        S = frozenset(span([a, b, c]))
        if len(S) == 8 and not pi <= S: hyps.add(S)
    for S in hyps:
        Sl = sum(1 << lineof[w] for w in S if w in lineof)
        # only layers used by some section of a used frame
        used = any(all(vv[u] in S for u in (x, y)) for q in fs for x, y in itertools.combinations(q, 2))
        if used: dem.append((pm(Sl), N(S) & ~NW, ('L', bi)))
print('demands', len(dem), '| incidences', sum(bin(c).count('1') for _, c, _ in dem))
inc_line = collections.Counter()
for F, c, t in dem:
    for u in bits(c): inc_line[u] += 1
print('layer/Q memberships per line: min %d mean %.1f max %d' % (min(inc_line.values()), sum(inc_line.values()) / V, max(inc_line.values())))
cand = {}
for a, b in itertools.combinations(range(V), 2):
    F, d = g.closure((1 << a) | (1 << b))
    if F not in cand: cand[F] = d
print('rank<=2 closures', len(cand))
res = []
for F, d in cand.items():
    if not nondegenerate(F): continue
    srv = [(t, bin(F & c).count('1')) for (Fr, c, t) in dem if F & ~Fr == 0 and F & c]
    tot = sum(k for _, k in srv)
    res.append((tot, len(srv), d, bin(F).count('1')))
res.sort(reverse=True)
print('best rank-2 hubs (incidences, demands served, rank, lines):', res[:8])
print('distribution of demands served by a rank-2 frame:', sorted(collections.Counter(r[1] for r in res).items())[:20])

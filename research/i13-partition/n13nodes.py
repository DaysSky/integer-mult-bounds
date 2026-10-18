"""I_{13,1} node census: perps of small line sets (candidate middle hubs).  For each rank r = 2..5, enumerate
perps of spans of r lines (canonical, S13), record (rank of perp, #lines in perp, #users = lines of the frame).
Key I11 numbers: pair-closure nodes rank 3-4 with <= 8 covered lines; D5 apex hubs (rank 5): 20 lines, perp 20,
kappa5 >= 3.  For I13 the analogue matters for whether rank-5/6 hubs can feed rank-11 section nodes.
usage: n13nodes.py"""
import sys, itertools, collections, pickle, time
from lgeo13 import *
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

# enumerate all perps of spans of up to 4 lines, canonical per (frame lines, perp lines)
seen = {}
rows = collections.Counter()
examples = {}
t_rep = {'P': g.P(0, 1), 'T': g.T(0, 1, 2)}
for k1 in range(V):
    for k2 in range(k1 + 1, V):
        for r in (2, 3, 4):
            pass
    # smarter: iterate pairs/triples/quads that are pairwise orthogonal OR arbitrary?
    # I11 census enumerated ALL flats containing a cell (closed sets).  Here: all spans of <= 4 lines.
    break
# implement: for each size s in 1..4, spans of s lines (any lines), canonicalise (span lines, perp)
def enum_spans(smax=4):
    res = {}
    # seed with single lines
    cur = [(1 << s) for s in range(V)]
    for s in range(1, smax + 1):
        nxt = set()
        for m in cur:
            F = pp(m)
            if F in res: continue
            res[F] = m
            hi = max(bits(m))
            for x in range(hi + 1, V):
                nxt.add(m | (1 << x))
        cur = sorted(nxt)
        log('size', s, 'spans', len(cur), 'flats so far', len(res), '%.0fs' % (time.time() - t0))
    return res
flats = enum_spans(4)
log('total flats of <= 4 lines:', len(flats))
# census of their perps
census = collections.Counter()
ex = {}
for F, m in flats.items():
    pF = pm(F)
    key = (rank(F), pc(F), rank(pF), pc(pF))
    census[key] += 1
    if key not in ex: ex[key] = (m, F)
log('distinct (rank,lines,perp rank,perp lines) keys:', len(census))
big = sorted(census.items(), key=lambda kv: -kv[0][3])[:25]
for k, c in big:
    print('rank', k[0], 'lines', k[1], '| perp rank', k[2], 'lines', k[3], 'x', c, 'example mask', hex(ex[k][0]), flush=True)
pickle.dump({'flats': flats, 'census': dict(census), 'examples': {k: v for k, v in ex.items()}},
            open('n13nodes.pkl', 'wb'))
log('saved')

"""Replay R420's shipped word: track each register's x-content (bitset over 120 lines) and frame; record every
phase-B target read (target, register, frame dim, content).  Then compare reads with frame-D6 totals."""
import gzip, json, sys, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
from geom import Geom
G = Geom()
c = json.load(gzip.open('/home/user/integer-mult-bounds/research/e8-bit-r420/data/bitE8mut-r420.json.gz', 'rt'))
v, R = c['v'], c['R']; nreg = 2 * v + R
fr = c['frames']; fmask = [sum(1 << s for s in f) for f in fr]
fdim = [e8.dim(m) if m else 0 for m in fmask]
xc = [0] * nreg
for s in range(v): xc[s] = 1 << s
cur = list(c['start'])
reads = collections.defaultdict(list)
def run(gates, ph):
    for f, d, srcs in gates:
        for x in [d] + srcs: cur[x] = f
        if v <= d < 2 * v and ph == 'B':
            for s in srcs: reads[d - v].append((s, fdim[f], xc[s], fmask[f]))
        for s in srcs:
            if not (v <= s < 2 * v): xc[d] ^= xc[s]
run(c['D'], 'D'); run(c['A'], 'A'); run(c['B'], 'B')
pc = lambda m: bin(m).count('1')
st = collections.Counter()
for t in range(v):
    rs = reads[t]
    st[tuple((dim, pc(cont)) for (s, dim, cont, fm) in rs)] += 1
print('read patterns (frame dim, content size) per target, top:')
for k, n in st.most_common(6): print('  ', n, k)
# compare with D6 totals
t = 0
f = G.phi[t]; mates = [e for e in f if e != t]
print('target 0 frame', f)
for (s, dim, cont, fm) in reads[t]:
    desc = []
    for e in mates:
        D6 = e8.perp((1 << t) | (1 << e))
        desc.append('D6{%d,%d}: in=%d out=%d' % (t, e, pc(cont & D6), pc(cont & ~D6)))
    B_ = G.blocks[G.comp[G.blk[t]]]
    print('  read reg', s, 'frame dim', dim, 'content', pc(cont), 'lines; B\'-part', pc(cont & B_), '; mates in content', [e for e in mates if cont >> e & 1], ';', '; '.join(desc))

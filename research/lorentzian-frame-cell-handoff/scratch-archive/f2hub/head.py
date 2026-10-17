"""BUILD (good-frame top, partner sources as accumulating deliveries).  Partition of the lines into good orthogonal
4-frames Phi = {t,a,b,c} (pairing (t,a),(b,c)) plus punctured lines.  For a good frame, with Q = lines _|_ Phi and
E_xy = lines _|_ x,y (not in Q, not frame lines):  R(t) = Q + E_ta + E_tb + E_tc + a + b + c  (disjoint).
Top registers per frame (6, + Q shared by every frame with the same Q):
  Q      at pm(Phi)   read in-chain by the 4 targets (and by every frame with the same pm, e.g. a star D4 block)
  IN_ta  at pm(t,a)   = E_ta + b + c, read in-chain by t and a;  IN_bc likewise
  X_tb, X_tc, X_ab, X_ac at pm(x,y) = E_xy.
Deliveries (sources accumulate in phase A):  source a reads X_tb at pm(t,b) -> t;  source t reads X_ac -> a;
  source c reads X_ab -> b;  source b reads X_tc -> c.  Final reads:  t: [a, X_tc]  a: [t, X_ab]  b: [c, X_tb]
  c: [b, X_ac].  Target chains: 0 -> pm(Phi) -> pm(t,a) -> t-perp.  Punctured targets: one R(t) register.
Middle as in build_a3g.py (Paar pieces, quad merges, piece chains, line chains).
usage: build_f2hub.py PART.pkl OUT.json.gz   (PART = (frames, punctured), frames as 4-tuples of line indices)"""
import sys, os, pickle, collections, itertools, time, heapq
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lmid'))
import lw
from lw import V, g, bits, LWord, frame_alg, FULL, nondegenerate
from fastcl import fclosure
HYP = g.HYP; G = g.G
pc = lambda m: bin(m).count('1')
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
PARTF, OUT = sys.argv[1], sys.argv[2]
part = pickle.load(open(PARTF, 'rb'))
frames0, punct = part[0], list(part[1])
pairsel = part[2] if len(part) > 2 else None          # optional per-frame pairing index 0..2
PM = {}
def pm(m):
    r = PM.get(m)
    if r is None:
        r = FULL
        for s in bits(m): r &= HYP[s]
        PM[m] = r
    return r
B2 = lambda x, y: (1 << x) | (1 << y)
PAIR = int(os.environ.get('PAIR', '0'))
FR = []                                              # (t, a, b, c) with in-chain pairs (t,a), (b,c)
for i, q in enumerate(frames0):
    q = list(q); k = pairsel[i] if pairsel is not None else PAIR
    t = q[0]; others = q[1:]; a = others[k]; b, c = [x for x in others if x != a]
    FR.append((t, a, b, c))
E = {}
for (t, a, b, c) in FR:
    U = B2(t, a) | B2(b, c); Q = pm(U)
    for x, y in itertools.combinations((t, a, b, c), 2):
        E[(x, y)] = E[(y, x)] = pm(B2(x, y)) & ~Q & ~U
    for x in (t, a, b, c):
        o = [y for y in (t, a, b, c) if y != x]
        parts = [Q, E[(x, o[0])], E[(x, o[1])], E[(x, o[2])], B2(o[0], o[1]) | (1 << o[2])]
        acc = 0
        for p in parts: assert acc & p == 0, 'not a partition (frame not good?)'; acc |= p
        assert acc == HYP[x], 'parts do not cover R(t)'
for F in set(pm(B2(t, a) | B2(b, c)) for (t, a, b, c) in FR) | set(pm(B2(x, y)) for (t, a, b, c) in FR for x, y in itertools.combinations((t, a, b, c), 2)):
    assert nondegenerate(F), 'degenerate top frame'
log('frames', len(FR), '| punctured', len(punct), '| distinct Q frames', len(set(pm(B2(t, a) | B2(b, c)) for (t, a, b, c) in FR)))
# ---- top demands
demand = collections.Counter(); content = {}
def dkey(F, Y): content[(F, Y)] = Y; return (F, Y)
INQ = os.environ.get('INQ', '0') == '1'             # 1: IN_ta holds the whole pm(t,a) (no separate Q register)
topQ = {}; topIN = {}; topX = {}
for (t, a, b, c) in FR:
    U = B2(t, a) | B2(b, c); Q = pm(U)
    if not INQ:
        topQ[(t, a, b, c)] = dkey(Q, Q); demand[topQ[(t, a, b, c)]] = 1
    for (x, y, p, q) in ((t, a, b, c), (b, c, t, a)):
        Y = E[(x, y)] | B2(p, q) | (Q if INQ else 0)
        topIN[(x, y)] = dkey(pm(B2(x, y)), Y); demand[topIN[(x, y)]] = 1
    for (x, y) in ((t, b), (t, c), (a, b), (a, c)):
        topX[(x, y)] = dkey(pm(B2(x, y)), E[(x, y)]); demand[topX[(x, y)]] = 1
topP = {}
for t in punct:
    topP[t] = dkey(HYP[t], HYP[t]); demand[topP[t]] += 1
# accumulating deliveries: source -> (frame, X key, target)
acc = {}; deliv = {}
for (t, a, b, c) in FR:
    for (s, x, y, tgt, cons) in ((a, t, b, t, (t, c)), (t, a, c, a, (a, b)), (c, a, b, b, (t, b)), (b, t, c, c, (a, c))):
        acc[s] = (pm(B2(x, y)), topX[(x, y)] if (x, y) in topX else topX[(y, x)], tgt)
        deliv[tgt] = (s, topX[cons])
for s, (F, D, tgt) in acc.items(): assert (1 << s) & ~F == 0 and F & ~HYP[tgt] == 0
TOPSET = set(demand)
log('top demands', len(demand), '| copies', sum(demand.values()), '| content lines', sum(pc(k[1]) for k in demand))

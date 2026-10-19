"""nat167: THE MERGE AT THE W4 (the never-tuned word's frame-raising at fixed R).

The shape map: the W4's hist (55% mass at rank 2) prices -23.4%; the all-at-6 row
prices +3.7% - the shape headroom at FIXED R=472 is the frontier-crossing lever.
The merge: the backward bounds (the participants' next-gates), then the forward
frame-raising to the highest legal candidates (the nat125-machinery, W4 format).
"""
import json
from collections import Counter, defaultdict

W4 = json.load(open('ii19_own_word4.json'))
v = W4['v']; h = W4['h']; R = W4['R']
nreg = 2*v + R

frames = W4['frames']
LCDIM = {0: 0, 1: 1, 2: 2, 3: 3, 12: 4, 13: 5, 30: 6, 64: 8, 120: 8, 121: 9}
dims = [LCDIM[len(fr)] for fr in frames]

# the containment: the W4's frames are root-closed (their line-sets = the spans' closures!)
# -> span i ⊆ span j iff lineset(i) ⊆ lineset(j) (the fast set test)
lidx = {}
for i, l in enumerate(W4['lines']):
    lidx[tuple(int(c) for c in l)] = i
    lidx[tuple(-int(c) for c in l)] = i
fsets = []
for fr in frames:
    s = set()
    for x in fr:
        t = tuple(int(c) for c in x)
        if t in lidx:
            s.add(lidx[t])
    fsets.append(s)
NF = len(frames)
print('the frames: %d' % NF, flush=True)

sub = [[False]*NF for _ in range(NF)]
for i in range(NF):
    si = fsets[i]
    for j in range(NF):
        sub[i][j] = True if i == j else (si <= fsets[j])
print('the containment matrix built (the closure test)', flush=True)

start = list(W4['start']); final = list(W4['final'])

# the gates in gcheck order: D, A, B, C
gates = []
for F, d, ss in W4['D']:
    gates.append((F, d, list(ss), 'D'))
for F, d, ss in W4['A']:
    gates.append((F, d, list(ss), 'A'))
for F, d, ss in W4['B']:
    gates.append((F, d, list(ss), 'B'))
for F, d, ss in W4['C']:
    gates.append((F, d, list(ss), 'C'))
# the finals: the pseudo-gates
fin_gates = []
for r in range(nreg):
    fin_gates.append((final[r], r, [], 'fin'))

# THE BACKWARD BOUNDS: the participants' next-touch frames
seqg = gates + fin_gates
cur_b = list(final)
bounds = [None]*len(seqg)
for gi in range(len(seqg)-1, -1, -1):
    F, d, ss, ph = seqg[gi]
    parts = [d] + list(ss)
    bounds[gi] = {p: cur_b[p] for p in parts}
    for p in parts:
        cur_b[p] = F

# THE FORWARD RE-FRAMING: raise each gate's frame to the highest legal
cur = list(start)
nmoved = 0
newgates = []
hist = Counter()
mass = [0]

def climb(r, F):
    if cur[r] != F:
        assert dims[cur[r]] < dims[F], 'down-climb r=%d' % r
        hist[dims[F] - dims[cur[r]]] += 1
        mass[0] += dims[F] - dims[cur[r]]
        cur[r] = F

for gi, (F, d, ss, ph) in enumerate(gates):
    parts = [d] + list(ss)
    bd = bounds[gi]
    # the ret-gates: freeze (the scatter invariant)
    if d in W4['ret']:
        newgates.append((F, d, ss, ph))
        for p in parts:
            climb(p, F)
        continue
    # the candidates: G with cur[p] ⊆ G ⊆ bd[p] ∀p, dims[G] > max-cur-dims (or no-op)
    ok_frames = []
    for G in range(NF):
        if all(sub[cur[p]][G] for p in parts):
            gd = dims[G]
            if all(dims[cur[p]] < gd or cur[p] == G for p in parts):
                if all(sub[G][bd[p]] for p in parts):
                    ok_frames.append(G)
    if not ok_frames:
        newgates.append((F, d, ss, ph))
        for p in parts:
            climb(p, F)
        continue
    # the highest-dim candidate (the max-jump!)
    best = max(ok_frames, key=lambda G: dims[G])
    if best != F:
        nmoved += 1
    newgates.append((best, d, ss, ph))
    for p in parts:
        climb(p, best)

for F, r, ss, ph in fin_gates:
    climb(r, F)

print('the gates re-framed: %d of %d' % (nmoved, len(gates)))
print('THE MERGED HIST:', dict(sorted(hist.items())))
print('the mass: %d | the identity: %d' % (mass[0], h*R + 73 + 2*v*(h-1)))

# the price
import sys
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
import pricer
# the copies: the ret-frames' dims
rf = W4['ret_frames']
hh = dict(hist)
for k in rf:
    hh[dims[k]] = hh.get(dims[k], 0) + 1
res = pricer.price(hh, v, h, R)
print('THE MERGED PRICE:', str(res[0]), flush=True)
pub = 0.001733052823330162099157
try:
    print('  vs frontier: %+.2f%%' % (100*(float(res[0])/pub - 1)))
except Exception as e:
    print('  (no root or error: %s)' % res[2] if len(res) > 2 else e)

json.dump({'nmoved': nmoved, 'hist': dict(hist)}, open('ii19_nat167_w4merge.json', 'wt'))
print('SAVED ii19_nat167_w4merge.json')

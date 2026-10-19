"""nat174: THE PIECES' ONE-GATE-BUILD FEASIBILITY at the 121.
The real construction question: the W4's 180 pieces are built through {2,2}-chains;
a one-gate build at the dim-4 content-span puts their 1,620 mass at {4,5}-ranks.
The binding: the pieces' 4-11 consumers read them at (possibly incomparable) dim-6
wire-build-frames -- the dup-law (the r434's version: 471 dups).
(1) the pieces' consumer-frames census;
(2) the dup-count for the one-gate builds;
(3) the net: the shape-gain vs the dup-cost at the measured sensitivities.
"""
import json
from collections import Counter, defaultdict

w = json.load(open('ii19_own_word4.json'))
v = w['v']
nreg = 2 * v + w['R']
LCDIM = {0: 0, 1: 1, 2: 2, 3: 3, 12: 4, 13: 5, 30: 6, 64: 8, 120: 8, 121: 9}
dims = [LCDIM[len(fr)] for fr in w['frames']]

def lineset(fr):
    return frozenset(tuple(int(c) for c in vec) for vec in w['frames'][fr])

# the helpers: the A-dests
a_dest = set(d for F, d, ss in w['A'] if d >= 2 * v)
b_wires = set()
for F, d, ss in w['B']:
    for s in ss:
        if s >= 2 * v:
            b_wires.add(s)
pieces = sorted(a_dest - b_wires)
print('the pieces (A-built, not B-read): %d | the B-wires: %d' % (len(pieces), len(b_wires)))

# (1) the pieces' consumers + their read-frames
cons = defaultdict(list)
for F, d, ss in w['A']:
    for s in ss:
        if s in set(pieces):
            cons[s].append((d, F))
for F, d, ss in w['B']:
    for s in ss:
        if s in set(pieces):
            cons[s].append((d, F))
print('the pieces with consumers: %d | the consumers-per-piece: %s' % (
    len(cons), dict(sorted(Counter(len(c) for c in cons.values()).items()))))

# (2) the dup-count: the one-gate build at the content-span (dim-4), then the consumers'
#     reads at THEIR frames: incomparable -> a dup per incomparable read.
dup_total = 0
for p, cs in cons.items():
    frames = [F for d, F in cs]
    ls = {}
    clusters = []
    for f in frames:
        s = lineset(f)
        placed = False
        for cl in clusters:
            if s <= ls[cl[0]] or ls[cl[0]] <= s:
                cl.append(f)
                ls[f] = s
                placed = True
                break
        if not placed:
            ls[f] = s
            clusters.append([f])
    dup_total += len(clusters) - 1
print('THE DUP-COUNT (the pieces\' one-gate builds): %d extra copies' % dup_total)
print('the R-impact: %d + %d = %d vs the wall 591' % (w['R'], dup_total, w['R'] + dup_total))

# (3) the net: the pieces' mass at {4,5} vs the dup-cost
# the pieces' current mass (the {2,2}-chains: 0->2->4->6->8->9-ish) vs the one-gate {4,5}
# the hist delta: the pieces' ~1,620 mass: from {2,2,2,2,1}-ish to {4,5}
# the price sensitivities (measured): the shape +4-8 points (the partial mid-shifts), the dup -0.092/each
print('the net: the shape gain ~+4-8 points vs the dup cost ~-%.1f points' % (dup_total * 0.092))

"""Cell bottleneck screen for the E8 frame architecture (3 branches per source at the cells of its frame, targets read
only inside their 3 frame-D6s).  For each target t and u in R(t): routes = {(D6 of t, cell of u) : cell inside D6}.
Doubly forced targets of cell C={s,e}: every route of s and every route of e uses C.  If no frame N ⊋ C lies inside a
C-containing D6 of every doubly forced target, a 2-register cell cannot serve them (one stream carries s+e at most,
or two streams s,e both need nodes inside a D6 of each such t) -> C needs a 3rd register.
env FRAMES: json list of 4-frames (line index lists); default = R420 partition frames from r420cells (pairs -> frames)."""
import sys, os, json, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
V = e8.V; pc = lambda m: bin(m).count('1')
def perp(mask):
    m = (1 << V) - 1
    for s in e8.bits(mask): m &= e8.HYP[s]
    return m
cells = [int(h, 16) for h in json.load(open('../sec4/r420cells.json'))['planes']]
# frames: union of cells sharing lines within a frame (each line in 3 cells, all inside its frame)
frame_of = {}
for s in range(V):
    m = 1 << s
    for C in cells:
        if C >> s & 1: m |= C
    frame_of[s] = m
assert all(pc(frame_of[s]) == 4 for s in range(V))
cells_of = {s: [C for C in cells if C >> s & 1] for s in range(V)}
D6s_of = {t: [perp(C) for C in cells_of[t]] for t in range(V)}     # t's 3 frame D6s (perp of its 3 cells)
def routes(t, u):
    return [(i, C) for i, D in enumerate(D6s_of[t]) for C in cells_of[u] if C & ~D == 0]
# flats strictly above a cell inside a D6: candidate first nodes = closures of C + one more line (minimal), enough to
# test existence (if a frame N ⊋ C fits inside D6s, so does a minimal one: closure(C ∪ {x}) for some x in N)
def closure(m): return e8.closure(m)[0]
stats = collections.Counter(); bad = []
for C in cells:
    s, e = e8.bits(C)
    T = []
    for t in range(V):
        if not (e8.HYP[t] >> s & 1 and e8.HYP[t] >> e & 1): continue
        rs, re = routes(t, s), routes(t, e)
        if rs and all(c == C for _, c in rs) and re and all(c == C for _, c in re):
            T.append((t, [D6s_of[t][i] for i, _ in rs]))
    stats[len(T)] += 1
    # existence of N ⊋ C inside a C-containing D6 of each t in T
    cand = set()
    for x in range(V):
        if C >> x & 1: continue
        N = closure(C | (1 << x))
        if all(any(N & ~D == 0 for D in Ds) for t, Ds in T): cand.add(N)
    if T and not cand: bad.append(C)
print('doubly-forced targets per cell:', dict(stats))
print('cells with NO common first node for their doubly-forced targets:', len(bad), 'of', len(cells))

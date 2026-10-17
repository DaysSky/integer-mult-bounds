"""Block-structured good-frame systems for I_{11,1} (E8/R420 analogue).
Blocks:  apex D4 block D(A,x) (|A| = 4, apex x not in A): lines P(ij), T(ijx) for ij in A; 3 PPTT frames (one per
         perfect matching of A).  Cube block for a pairing {(a,a'),(b,b'),(c,c')}: 8 transversal T lines in 2 TTTT
         frames (even / odd transversals) (+3 matching P lines, not framed inside the cube).
Construction (randomised): pack edge-disjoint K4's (P lines) with apexes whose T lines are unclaimed, then pack cubes
on unclaimed T lines, then give every leftover line the good frame maximising overlap with already-framed lines.
Output system JSON (line -> frame mask) and its own-frame-top routability U (unroutable (section, line) pairs) and
defects.  usage: blocks.py trials seed OUTPREFIX"""
import sys, os, json, random, itertools, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lcell'))
os.environ['GRP'] = '11'
from lbase import V, bits, HYP, goodframes, g
pc = lambda m: bin(m).count('1')
TR, SEED, OUT = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
random.seed(SEED)
FR = goodframes(); FRS = set(FR)
frames_of = collections.defaultdict(list)
for F in FR:
    for s in bits(F): frames_of[s].append(F)
P = lambda i, j: g.P(i, j); T = lambda i, j, k: g.T(i, j, k)
def evaluate(F):
    cells = set()
    for a in range(V):
        for b in bits(F[a]):
            if b != a: cells.add((1 << a) | (1 << b))
    cells_of = collections.defaultdict(list)
    for C in cells:
        for s in bits(C): cells_of[s].append(C)
    U = 0
    for C in cells:
        a, b = bits(C); S = HYP[a] & HYP[b]
        for u in bits(S):
            if not any(D & ~S == 0 for D in cells_of[u]): U += 1
    dfc = sum(1 for a in range(V) for b in bits(F[a]) if b != a and not F[b] >> a & 1)
    return U, dfc, len(cells)
def build():
    F = {}
    usedP = set(); usedT = set()
    # 1) apex D4 blocks
    quads = list(itertools.combinations(range(11), 4)); random.shuffle(quads)
    nd4 = 0
    for A in quads:
        pairs = list(itertools.combinations(A, 2))
        if any(P(i, j) in usedP for i, j in pairs): continue
        xs = [x for x in range(11) if x not in A and not any(T(i, j, x) in usedT for i, j in pairs)]
        if not xs: continue
        x = random.choice(xs)
        for (i, j) in pairs: usedP.add(P(i, j)); usedT.add(T(i, j, x))
        a, b, c, d = A
        for m in (((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c))):
            (i, j), (k, l) = m
            fr = (1 << P(i, j)) | (1 << P(k, l)) | (1 << T(i, j, x)) | (1 << T(k, l, x))
            assert fr in FRS
            for s in bits(fr): F[s] = fr
        nd4 += 1
    # 2) cube blocks on unclaimed T lines
    ncube = 0
    pts = list(range(11))
    tries = 0
    while tries < 4000:
        tries += 1
        six = random.sample(pts, 6)
        pr = [(six[0], six[1]), (six[2], six[3]), (six[4], six[5])]
        trans = [T(a, b, c) for a in pr[0] for b in pr[1] for c in pr[2]]
        if any(t in usedT for t in trans): continue
        even = [T(a, b, c) for ia, a in enumerate(pr[0]) for ib, b in enumerate(pr[1]) for ic, c in enumerate(pr[2]) if (ia + ib + ic) % 2 == 0]
        odd = [t for t in trans if t not in even]
        ok = True
        for grp in (even, odd):
            fr = sum(1 << t for t in grp)
            if fr not in FRS: ok = False
        if not ok: continue
        for grp in (even, odd):
            fr = sum(1 << t for t in grp)
            for t in grp: F[t] = fr; usedT.add(t)
        ncube += 1
    # 3) leftovers: frame maximising overlap with frames of its mates (prefer frames whose other lines are leftovers too)
    left = [s for s in range(V) if s not in F]
    random.shuffle(left)
    for s in left:
        best = max(frames_of[s], key=lambda X: (sum(1 for y in bits(X) if y != s and y not in F), random.random()))
        for y in bits(best):
            if y not in F: F[y] = best
    return F, nd4, ncube, len(left)
best = None
for tr in range(TR):
    F, nd4, nc, nl = build()
    U, dfc, nc_ = evaluate(F)
    print('trial', tr, 'D4 blocks', nd4, 'cubes', nc, 'leftover lines', nl, '-> U', U, 'defects', dfc, 'cells', nc_, flush=True)
    if best is None or U + dfc < best[0]:
        best = (U + dfc, F)
        json.dump({str(k): v for k, v in F.items()}, open(OUT + '.json', 'w'))
print('best U+defects', best[0])

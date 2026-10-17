"""Paar-style shared pieces for the lbuild builders (cancellation-free XOR common-subexpression elimination).
Variables start as the lines; repeatedly the pair of variables co-occurring in the most rows (top demands and pieces
made so far) is merged into a new piece P = A u B (disjoint union) at frame closure(P) (skipped if degenerate).
Each piece has exactly two inputs and, when made, >= 2 users, so pieces carry no junk; a top demand's junk is its
number of remaining terms minus its copies.  Returns (children, covered) in the genpieces format; lines left as terms
are delivered by the builder's line chains."""
import collections
import numpy as np
import lw
from lw import bits, nondegenerate, V
from fastcl import fclosure
pc = lambda m: bin(m).count('1')

def paar_pieces(demand, content, log, mincount=2, maxpieces=100000, seed=None, seeds=None):
    import random, os
    if seed is None: seed = int(os.environ.get('PAARSEED', '0'))
    rnd = random.Random(seed)
    jit = (lambda: rnd.random()) if seed else (lambda: 0.0)
    tops = list(demand)
    var_content = [1 << u for u in range(V)]          # variable index -> line set
    var_key = [None] * V                                # piece key for non-line variables
    rows = [set(bits(content[D])) for D in tops]        # each row: set of variable indices (initially lines)
    piece_rows = {}                                      # piece var -> its two child vars
    seeded = {}                                          # seeded var -> its line set (assembled from lines)
    for B in (seeds or []):
        F = fclosure(B)
        if not nondegenerate(F): continue
        rs = [r for r in range(len(rows)) if all(u in rows[r] for u in bits(B))]
        if len(rs) < 2: continue
        v = len(var_content); var_content.append(B); var_key.append((F, B)); seeded[v] = B
        content[(F, B)] = B
        for r in rs:
            for u in bits(B): rows[r].discard(u)
            rows[r].add(v)
    if seeds: log('paar seeds applied', len(seeded), 'of', len(seeds))
    # co-occurrence via incidence sets
    occ = collections.defaultdict(set)                  # var -> rows (index into allrows) containing it
    allrows = list(range(len(rows)))
    for r, row in enumerate(rows):
        for v in row: occ[v].add(r)
    bad = set()
    made = 0
    import heapq
    def pair_count(a, b): return len(occ[a] & occ[b])
    # initial candidate heap over all co-occurring pairs (line pairs)
    heap = []
    cnt = collections.Counter()
    for row in rows:
        L = sorted(row)
        for i in range(len(L)):
            for j in range(i + 1, len(L)): cnt[(L[i], L[j])] += 1
    for (a, b), c in cnt.items():
        if c >= mincount: heap.append((-c, jit(), a, b))
    heapq.heapify(heap); del cnt
    while heap and made < maxpieces:
        negc, jj, a, b = heapq.heappop(heap)
        if (a, b) in bad: continue
        rs = occ[a] & occ[b]; c = len(rs)
        if c < mincount: continue
        if c < -negc: heapq.heappush(heap, (-c, jit(), a, b)); continue
        C = var_content[a] | var_content[b]
        F = fclosure(C)
        if not nondegenerate(F): bad.add((a, b)); continue
        v = len(var_content); var_content.append(C); var_key.append((F, C)); piece_rows[v] = (a, b)
        content[(F, C)] = C
        for r in rs:
            rows[r].discard(a); rows[r].discard(b); rows[r].add(v)
            occ[a].discard(r); occ[b].discard(r); occ[v].add(r)
        # the new piece is itself a row only through its parents; new candidate pairs (v, w) for w in those rows
        nc = collections.Counter()
        for r in rs:
            for w in rows[r]:
                if w != v: nc[w] += 1
        for w, cc in nc.items():
            if cc >= mincount: heapq.heappush(heap, (-cc, jit(), min(v, w), max(v, w)))
        made += 1
    # assemble children/covered: piece children are its two child vars if they are pieces; tops: their piece terms
    children = collections.defaultdict(list); covered = collections.defaultdict(int)
    uses = collections.Counter()
    for v, (a, b) in piece_rows.items():
        K = var_key[v]
        for x in (a, b):
            if x >= V:
                children[K].append(var_key[x]); covered[K] |= var_content[x]; uses[x] += 1
    for r, D in enumerate(tops):
        for x in rows[r]:
            if x >= V and var_key[x] != D:          # a piece equal to the whole top IS the top
                children[D].append(var_key[x]); covered[D] |= var_content[x]; uses[x] += 1
    for v in list(piece_rows) + list(seeded):
        demand[var_key[v]] += uses[v]
    nterm = [len(rows[r]) for r in range(len(tops))]
    log('paar: pieces', len(piece_rows), '| terms per top: mean %.2f max %d' % (np.mean(nterm), max(nterm)),
        '| top junk estimate', sum(max(0, nterm[r] - demand[D]) for r, D in enumerate(tops)),
        '| pieces with 1 use', sum(1 for v in piece_rows if uses[v] == 1), '| degenerate pairs skipped', len(bad),
        '| seeded used', sum(1 for v in seeded if uses[v] > 0))
    return children, covered

EXCL = set()
def mp_refine(tops, demand, content, children, covered, log):
    """Matching-pursuit refinement with cancellation: each top demand is re-expressed as an XOR of shared pieces
    (Paar pieces and other top demands earlier in build order, any content inside its frame) plus residual lines,
    greedily maximising the weight drop; kept if it has fewer terms.  covered[D] becomes the XOR of the children
    (the builder delivers content ^ covered as lines).  Piece copy counts are recomputed from the final references."""
    order = lambda K: (lw.dim(K[0]), pc(content[K]))
    allp = [K for K in content if pc(content[K]) >= 2]
    def nterms(D): return len(children[D]) + pc(content[D] ^ covered[D])
    before = sum(nterms(D) for D in tops); improved = 0
    for D in tops:
        F = D[0]; oD = order(D)
        cands = [K for K in allp if K != D and content[K] & ~F == 0 and K[0] & ~F == 0 and order(K) < oD and K not in EXCL]
        r = content[D]; chosen = []
        while True:
            best = None; bw = pc(r) - 1
            for K in cands:
                w = pc(r ^ content[K])
                if w < bw: bw = w; best = K
            if best is None: break
            chosen.append(best); r ^= content[best]
        if len(chosen) + pc(r) < nterms(D):
            children[D] = chosen; cv = 0
            for K in chosen: cv ^= content[K]
            covered[D] = cv; improved += 1
    # recompute copy counts: tops keep their read copies; pieces get one copy per reference
    topset = set(tops); base = {D: demand[D] for D in tops}
    refs = collections.Counter()
    for P, ch in children.items():
        for K in ch: refs[K] += 1
    # drop pieces no longer referenced (transitively)
    alive = set(tops); stack = list(tops)
    while stack:
        X = stack.pop()
        for K in children.get(X, []):
            if K not in alive: alive.add(K); stack.append(K)
    for K in list(demand):
        if K not in alive: del demand[K]
    refs = collections.Counter()
    for X in alive:
        for K in children.get(X, []): refs[K] += 1
    for K in alive:
        demand[K] = (base[K] if K in topset else 0) + refs[K]
    log('mp_refine: tops improved', improved, '| terms before', before, '| after', sum(nterms(D) for D in tops),
        '| pieces alive', len(alive) - len(tops))
    return children, covered

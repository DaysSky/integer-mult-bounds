"""Multi-output QUAD plan for the lbuild tops.  A quad is a small nondegenerate frame X lying inside several
demand frames; it receives (copies of) its lines and outputs, to each demand using it, a DIFFERENT part
p = (demand content) n X n (still uncovered).  Junk at a quad = #distinct lines it receives - rank(parts); a top demand
with k parts (quad parts + residual lines) has junk k - 1.  R = reads - 220 + total junk, exactly.
plan_quads(demand, content, log) -> (parts: demand -> list of (X, part)), qjunk, tjunk."""
import collections, itertools
import lw
from lw import bits, nondegenerate
from fastcl import fclosure
pc = lambda m: bin(m).count('1')

def rank2(vs):
    red = {}
    for v in vs:
        while v:
            hb = v.bit_length() - 1
            if hb in red: v ^= red[hb]
            else: red[hb] = v; break
    return len(red)

def candidates(tops, content, maxrank=5, minuse=2):
    frames = sorted(set(D[0] for D in tops))
    cand = set()
    for A, B in itertools.combinations(frames, 2):
        I = A & B
        if pc(I) < 3: continue
        X = fclosure(I)
        if X & ~I: X = I if fclosure(I) == I else None
        if X is None: continue
        cand.add(X)
    # also small closures of pairs/triples of lines inside frames are implied by intersections; keep rank-bounded
    out = {}
    for X in cand:
        d = lw.dim(X)
        if d < 2 or d > maxrank or not nondegenerate(X): continue
        users = [D for D in tops if X & ~D[0] == 0 and pc(content[D] & X) >= 2]
        if len(users) >= minuse: out[X] = users
    return out

def plan_quads(tops, content, log, maxrank=5, minpart=2, minscore=1):
    cand = candidates(tops, content, maxrank)
    log('quad candidates', len(cand))
    unc = {D: content[D] for D in tops}
    parts = collections.defaultdict(list)
    quads = {}
    import heapq
    def score(X):
        return sum(pc(unc[D] & X) - 1 for D in cand[X] if pc(unc[D] & X) >= minpart)
    heap = [(-score(X), X) for X in cand]; heapq.heapify(heap)
    while heap:
        ns, X = heapq.heappop(heap)
        sc = score(X)
        if sc < minscore: continue
        if sc < -ns: heapq.heappush(heap, (-sc, X)); continue
        got = []
        for D in cand[X]:
            p = unc[D] & X
            if pc(p) >= minpart: got.append((D, p))
        # junk check: parts must span the lines they use, else drop the weakest users until they do (or skip)
        lines = 0
        for _, p in got: lines |= p
        r = rank2([p for _, p in got])
        if pc(lines) - r > 0 and len(got) >= 1:
            pass   # accept with junk; recorded below
        for D, p in got:
            parts[D].append((X, p)); unc[D] &= ~p
        quads[X] = got
    qjunk = {}
    for X, got in quads.items():
        lines = 0
        for _, p in got: lines |= p
        qjunk[X] = pc(lines) - rank2([p for _, p in got])
    tjunk = {D: len(parts[D]) + pc(unc[D]) - 1 for D in tops}
    log('quads used', len(quads), '| quad junk', sum(qjunk.values()), '| top junk', sum(tjunk.values()),
        '| parts per top %.2f' % (sum(len(parts[D]) for D in tops) / len(tops)),
        '| residual lines', sum(pc(unc[D]) for D in tops))
    return parts, unc, qjunk, tjunk

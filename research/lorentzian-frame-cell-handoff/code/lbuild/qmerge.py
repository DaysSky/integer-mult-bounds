"""Multi-output quad merges on top of a piece circuit (Paar).  A quad is a closed nondegenerate frame X lying
inside several top frames; every top D using X replaces its terms (pieces / residual lines) whose frames lie inside
X by ONE part = XOR of those terms, and the quad node at X turns the distinct incoming terms into the distinct parts.
Junk change: -sum_D (#terms_D inside X - 1) + (#distinct terms - rank(parts)).  Greedy over candidate frames
(pairwise intersections of top frames).  Returns a list of quads (X, in_pieces, in_lines, outs=[(D, vec)])."""
import collections, itertools, heapq
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

def plan(tops, children, covered, content, frame_of, log, maxq=100000, strict=()):
    """tops: list of top keys; children[D]: piece keys; covered[D]: XOR of children contents (residual lines =
    content ^ covered); frame_of(K): assembly frame of piece/top K."""
    terms = {}
    for D in tops:
        T = [('P', C) for C in children.get(D, [])]
        for u in bits(content[D] ^ covered[D]): T.append(('L', u))
        terms[D] = T
    def tframe(t): return frame_of(t[1]) if t[0] == 'P' else (1 << t[1])
    def tvec(t): return content[t[1]] if t[0] == 'P' else (1 << t[1])
    tidx = {D: i for i, D in enumerate(tops)}
    strict = set(strict)
    inframe = collections.defaultdict(int)          # line -> bitset of tops whose frame contains it
    for D in tops:
        b = 1 << tidx[D]
        for u in bits(frame_of(D)): inframe[u] |= b
    frames = sorted(set(frame_of(D) for D in tops))
    cand = set()
    for A, B in itertools.combinations(frames, 2):
        I = A & B
        if pc(I) >= 3 and fclosure(I) == I and nondegenerate(I): cand.add(I)
    log('qmerge: candidate frames', len(cand))
    def users_of(X):
        m = -1
        for u in bits(X):
            m &= inframe[u]
            if not m: return []
        out = []
        while m:
            lb = m & -m; j = lb.bit_length() - 1; m ^= lb; out.append(tops[j])
        return out
    def gain(X):
        us = []
        for D in users_of(X):
            if D in strict and frame_of(D) == X: continue      # a piece at frame X could also feed the quad
            ins = [t for t in terms[D] if t[0] != 'Q' and tframe(t) & ~X == 0]
            if len(ins) >= 2: us.append((D, ins))
        if len(us) < 2: return 0, us
        distinct = set(t for _, ins in us for t in ins)
        parts = []
        for D, ins in us:
            v = 0
            for t in ins: v ^= tvec(t)
            parts.append(v)
        return sum(len(ins) - 1 for _, ins in us) - (len(distinct) - rank2(parts)), us
    heap = [(-gain(X)[0], X) for X in cand]; heapq.heapify(heap)
    quads = []; total = 0
    while heap and len(quads) < maxq:
        ng, X = heapq.heappop(heap)
        gn, us = gain(X)
        if gn <= 0: continue
        if gn < -ng: heapq.heappush(heap, (-gn, X)); continue
        distinct = []
        for _, ins in us:
            for t in ins:
                if t not in distinct: distinct.append(t)
        outs = []
        for D, ins in us:
            v = 0
            for t in ins: v ^= tvec(t)
            outs.append((D, v, list(ins)))
            terms[D] = [t for t in terms[D] if t not in ins] + [('Q', len(quads), v)]
        quads.append((X, [t[1] for t in distinct if t[0] == 'P'], [t[1] for t in distinct if t[0] == 'L'], outs))
        total += gn
    log('qmerge: quads', len(quads), '| estimated junk saved', total,
        '| terms per top %.2f' % (sum(len(terms[D]) for D in tops) / max(1, len(tops))))
    return quads, terms

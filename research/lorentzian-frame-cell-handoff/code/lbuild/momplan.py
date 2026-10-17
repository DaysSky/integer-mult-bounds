"""Multi-output-node (MOM) planner: top-down choice of node arrivals.
Every needed vector v (a read content, or an arrival requested by a higher node) is produced at the node
X = closure(v).  A node with distinct outputs O_X (span rank r) needs arrivals A_X, each of LOWER rank (closure a
proper subflat of X), with span(A_X) >= span(O_X); its junk is |A_X| - r.  Total junk over all nodes is exactly the
register excess over the reads (R = reads - 220 + junk).  Heuristic per node: a basis of lower-rank vectors inside
span(O_X) (preferring vectors already needed at lower nodes, then light ones); a missing dimension is supplied by
splitting an output along a proper subflat (junk +1 per split).  plan(needed) -> arrivals per node and junk."""
import collections, itertools
import lw
from lw import bits, nondegenerate
from fastcl import fclosure
pc = lambda m: bin(m).count('1')
CL = {}
def clo(v):
    r = CL.get(v)
    if r is None: r = fclosure(v); CL[v] = r
    return r
def dim(F): return lw.dim(F)

def reduce_basis(vecs):
    """GF(2) row-echelon: returns dict pivot -> (vector, combination-tag)"""
    red = {}
    for i, v in enumerate(vecs):
        tag = 1 << i
        while v:
            hb = v.bit_length() - 1
            if hb in red: v ^= red[hb][0]; tag ^= red[hb][1]
            else: red[hb] = (v, tag); break
    return red
def in_span(red, v):
    while v:
        hb = v.bit_length() - 1
        if hb not in red: return False
        v ^= red[hb][0]
    return True
def add_vec(red, v):
    while v:
        hb = v.bit_length() - 1
        if hb in red: v ^= red[hb][0]
        else: red[hb] = (v, 0); return True
    return False

def plan(needed, log, maxenum=12, verbose=False):
    """needed: dict frame X -> Counter(vector -> uses).  Mutated: arrivals are added as needs at lower nodes.
    Returns arrivals: dict X -> list of vectors; junk: dict X -> int."""
    arrivals = {}; junk = {}
    done = set()
    by_dim = collections.defaultdict(set)
    for X in needed: by_dim[dim(X)].add(X)
    stats = collections.Counter()
    while True:
        ds = [d for d in by_dim if by_dim[d] - done]
        if not ds: break
        d = max(ds)
        if d <= 1:
            for X in by_dim[d]: done.add(X)
            continue
        X = next(iter(by_dim[d] - done)); done.add(X)
        O = [v for v, u in needed[X].items() if u > 0]
        red = reduce_basis(O); r = len(red)
        # candidate lower-rank vectors inside span(O)
        cands = []
        # (a) vectors already needed at lower nodes (proper subflats of X)
        for Y, cnt in needed.items():
            if Y == X or Y & ~X or dim(Y) >= dim(X): continue
            for v in cnt:
                if in_span(red, v): cands.append((0, pc(v), v))
        # (b) enumeration of span(O)
        if r <= maxenum:
            basis = [red[h][0] for h in red]
            for k in range(1, 1 << r):
                v = 0
                for i in range(r):
                    if k >> i & 1: v ^= basis[i]
                if clo(v) != X: cands.append((1, pc(v), v))
        cands.sort()
        chosen = []; cred = {}
        for _, _, v in cands:
            if len(cred) == r: break
            if add_vec(cred, v): chosen.append(v)
        deficit = r - len(cred)
        extra = 0
        # supply missing dimensions by splitting outputs along proper subflats
        while deficit > 0:
            o = next(v for v in O if not in_span(cred, v))
            # candidate subflats: lower needed frames inside X, and closures of large parts of o
            best = None
            Ys = [Y for Y in needed if Y != X and Y & ~X == 0 and dim(Y) < dim(X)]
            for Y in Ys:
                a = o & Y; b = o & ~Y
                if not a or not b: continue
                if clo(b) == X: continue
                sc = (pc(a) * pc(b) > 0, pc(a), )
                if best is None or sc > best[0]: best = (sc, a, b)
            if best is None:
                # greedy: peel lines of o into a subflat until the remainder is lower rank
                L = bits(o); a = 0
                for u in L:
                    if clo(a | (1 << u)) != X: a |= 1 << u
                b = o ^ a
                if clo(b) == X or not b:
                    # split b again: take its maximal lower-rank prefix
                    b1 = 0
                    for u in bits(b):
                        if clo(b1 | (1 << u)) != X: b1 |= 1 << u
                    parts = [a, b1, b ^ b1]
                else: parts = [a, b]
            else:
                parts = [best[1], best[2]]
            parts = [p for p in parts if p]
            for p in parts:
                assert clo(p) != X, 'split part not lower rank'
            new = 0
            for p in parts:
                if add_vec(cred, p): chosen.append(p); new += 1
                else: chosen.append(p); new += 1
            extra += new - 1
            deficit = r - len(cred) if len(cred) <= r else 0
            # recompute: chosen span may exceed r (that is the junk)
            if all(in_span(cred, v) for v in O): deficit = 0
        arrivals[X] = chosen
        junk[X] = len(chosen) - r
        stats['nodes'] += 1; stats['junk'] += junk[X]; stats['arrivals'] += len(chosen); stats['rank'] += r
        for a in chosen:
            Y = clo(a)
            if Y not in needed: needed[Y] = collections.Counter(); by_dim[dim(Y)].add(Y)
            needed[Y][a] += 1
        if verbose and stats['nodes'] % 200 == 0: log('mom nodes', stats['nodes'], dict(stats))
    log('MOM plan', dict(stats), '| line nodes', sum(1 for X in needed if dim(X) == 1))
    return arrivals, junk

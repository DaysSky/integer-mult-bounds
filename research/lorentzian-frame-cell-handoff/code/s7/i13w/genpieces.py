"""General shared pieces for the lbuild builders: a piece is (F, C) with C any line set and F = closure(C) a
nondegenerate flat; it is assembled once (C at frame F), copied once per use, and XORed into each parent's content.
Candidates are pairwise intersections of parents' RESIDUAL contents (content minus pieces already taken), so
non-flat remainders such as stars St_x(U) become shareable.  Greedy by incidences saved (uses-1)*(|C|-1), re-run
on the updated residuals until nothing scores; new pieces are decomposed at the next level the same way."""
import itertools, heapq, collections
import lw
from lw import bits, nondegenerate
from fastcl import fclosure
pc = lambda m: bin(m).count('1')

def find_pieces(demand, content, log, minsize=3, maxlevel=8, rounds=6, minscore=1):
    children = collections.defaultdict(list); covered = collections.defaultdict(int)
    clos = {}
    def closure(C):
        F = clos.get(C)
        if F is None: F = fclosure(C); clos[C] = F
        return F
    frontier = list(demand); level = 0
    while frontier and level < maxlevel:
        par = sorted(set(frontier), key=lambda k: -pc(content[k]))
        idx = {P: i for i, P in enumerate(par)}
        res = {P: content[P] & ~covered[P] for P in par}
        newf = []
        for rnd in range(rounds):
            dres = collections.defaultdict(int)
            for P in par:
                b = 1 << idx[P]
                for u in bits(res[P]): dres[u] |= b
            # candidates: pairwise residual intersections (only pairs sharing >= minsize lines)
            cand = set()
            nbr = collections.defaultdict(int)
            for P in par:
                if pc(res[P]) < minsize: continue
                m = 0
                for u in bits(res[P]): m |= dres[u]
                m &= ~((1 << (idx[P] + 1)) - 1)
                while m:
                    lb = m & -m; j = lb.bit_length() - 1; m ^= lb
                    I = res[P] & res[par[j]]
                    if pc(I) >= minsize: cand.add(I)
            def uses_of(C):
                m = -1
                for u in bits(C):
                    m &= dres[u]
                    if not m: return 0
                return m
            heap = []
            for C in cand:
                k = pc(uses_of(C))
                sc = (k - 1) * (pc(C) - 1)
                if sc >= minscore: heap.append((-sc, -pc(C), C))
            heapq.heapify(heap)
            took = 0
            while heap:
                negs, nsz, C = heapq.heappop(heap)
                um = uses_of(C); k = pc(um); sc = (k - 1) * (pc(C) - 1)
                if sc < minscore: continue
                if sc < -negs: heapq.heappush(heap, (-sc, nsz, C)); continue
                F = closure(C)
                if not nondegenerate(F): continue
                K = (F, C)
                content[K] = C
                us = []
                while um:
                    lb = um & -um; j = lb.bit_length() - 1; um ^= lb
                    if par[j] != K: us.append(par[j])
                if len(us) < 2 and not (len(us) == 1 and K in demand): continue
                for P in us:
                    covered[P] |= C; res[P] &= ~C; children[P].append(K)
                    b = 1 << idx[P]
                    for u in bits(C): dres[u] &= ~b
                demand[K] += len(us); newf.append(K); took += 1
            if not took: break
        log('gen level', level, '| parents', len(par), '| new pieces', len(newf), '| sizes',
            dict(sorted(collections.Counter(pc(content[k]) for k in newf).items(), reverse=True)[:10]),
            '| residual lines', sum(pc(res[P]) for P in par))
        frontier = newf; level += 1
    return children, covered

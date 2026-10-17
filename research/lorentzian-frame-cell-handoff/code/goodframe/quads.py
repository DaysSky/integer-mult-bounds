# Hub (quad) candidates for a frame partition: X = closure of two partition cells (pairs inside partition frames),
# nondegenerate, X a union of partition cells.  Owners: sections (x,y) of partition frames with X inside pm(x,y).
# For each owner, E-part = X n E_xy; it is "aligned" if it is a union of the cells of X.  Report the best hubs.
import sys, pickle, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, bits, V, nondegenerate, closure, dim
HYP = g.HYP
def pm(m):
    r = g.FULL
    for s in bits(m): r &= HYP[s]
    return r
B2 = lambda x, y: (1 << x) | (1 << y)
part = pickle.load(open(sys.argv[1], 'rb'))
frames = [tuple(f) for b in part[0] for f in (b if isinstance(b[0], (tuple, list)) else [b])]
print('frames', len(frames))
cells = [B2(x, y) for f in frames for x, y in itertools.combinations(f, 2)]
cellset = set(cells)
cells_of = collections.defaultdict(list)
for c in cells:
    for u in bits(c): cells_of[u].append(c)
sec = []   # (frame, x, y, pm(x,y), E_xy)
for f in frames:
    U = 0
    for u in f: U |= 1 << u
    Q = pm(U)
    for x, y in itertools.combinations(f, 2):
        sec.append((f, x, y, pm(B2(x, y)), pm(B2(x, y)) & ~Q & ~U))
def cover_by_cells(m):
    """partition line set m into partition cells (exact cover, small); returns list or None"""
    if m == 0: return []
    u = bits(m)[0]
    for c in cells_of[u]:
        if c & ~m == 0:
            r = cover_by_cells(m & ~c)
            if r is not None: return [c] + r
    return None
seen = {}
for c1, c2 in itertools.combinations(cells, 2):
    if c1 & c2: continue
    X, d = g.closure(c1 | c2)
    if X in seen: continue
    if d > 6 or not nondegenerate(X): seen[X] = None; continue
    cov = cover_by_cells(X)
    if cov is None: seen[X] = None; continue
    owners = []; tot = 0
    for (f, x, y, P_, Exy) in sec:
        if X & ~P_ == 0:
            part_ = X & Exy
            if part_ == 0: continue
            ok = cover_by_cells(part_) is not None
            owners.append((ok, bin(part_).count('1')))
            if ok: tot += bin(part_).count('1')
    seen[X] = (d, bin(X).count('1'), len(cov), owners, tot)
good = [(v[4], X, v) for X, v in seen.items() if v is not None and v[4] > 0]
good.sort(key=lambda z: -z[0])
print('hub candidates', len(good), '| closures examined', len(seen))
for tot, X, (d, nl, nc, owners, _) in good[:15]:
    print('rank %d lines %d cells %d | owners %d aligned %d | aligned E-lines %d | part sizes %s' % (
        d, nl, nc, len(owners), sum(1 for o in owners if o[0]), tot, sorted(o[1] for o in owners if o[0])))
dist = collections.Counter(min(10, sum(1 for o in v[3] if o[0])) for _, _, v in good)
print('aligned-owner count distribution', sorted(dist.items()))

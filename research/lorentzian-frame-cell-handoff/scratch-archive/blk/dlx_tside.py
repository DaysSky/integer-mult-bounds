# Exhaustive exact cover (Algorithm X) of the remaining T lines of the (6,3,3) P side by octets and at most F lone
# TTTT frames, with exactly 3 punctured T lines whose supports partition {1..9}.  Exhaustive => "none" is a proof.
import sys, itertools, pickle, collections, time
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V
sys.setrecursionlimit(10000)
P, T = g.P, g.T
tri = lambda a, b, c: T(*sorted((a, b, c)))
X = 10
D = '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/blk/'
hubs, stars2, singles, punP = pickle.load(open(D + 'pside633.pkl', 'rb'))
pack6 = [(0, 1, 2, 3), (0, 4, 5, 6), (0, 7, 8, 9), (1, 4, 7, X), (2, 5, 8, X), (3, 6, 9, X)]
blocks = []
for h, F4 in zip(hubs, pack6):
    p, q, r, s = F4
    blocks.append([(P(a, b), P(c, d), tri(h, a, b), tri(h, c, d)) for (a, b), (c, d) in (((p, q), (r, s)), ((p, r), (q, s)), ((p, s), (q, r)))])
for h, F4, es in stars2:
    e1, e2, e3, e4 = [tuple(sorted(e)) for e in es]
    blocks.append([(P(*e1), P(*e2), tri(h, *e1), tri(h, *e2)), (P(*e3), P(*e4), tri(h, *e3), tri(h, *e4))])
for h, e1, e2 in singles:
    e1, e2 = tuple(sorted(e1)), tuple(sorted(e2))
    blocks.append([(P(*e1), P(*e2), tri(h, *e1), tri(h, *e2))])
pun = [P(*sorted(e)) for e in punP]
used = set(u for b in blocks for f in b for u in f) | set(pun)
remT = [u for u in range(V) if u not in used]
rem = set(remT)
rows = {}
def octet_frames(m):
    (a1, a2), (b1, b2), (c1, c2) = m
    tr = [(x, y, z) for x in (a1, a2) for y in (b1, b2) for z in (c1, c2)]
    f0 = tuple(tri(*t) for t in tr if (int(t[0] == a2) + int(t[1] == b2) + int(t[2] == c2)) % 2 == 0)
    f1 = tuple(tri(*t) for t in tr if (int(t[0] == a2) + int(t[1] == b2) + int(t[2] == c2)) % 2 == 1)
    return f0, f1
seen = set()
for a1, a2 in itertools.combinations(range(11), 2):
    for b1, b2 in itertools.combinations(range(11), 2):
        if len({a1, a2, b1, b2}) < 4 or (b1, b2) < (a1, a2): continue
        for c1, c2 in itertools.combinations(range(11), 2):
            if len({a1, a2, b1, b2, c1, c2}) < 6 or (c1, c2) < (b1, b2): continue
            f0, f1 = octet_frames(((a1, a2), (b1, b2), (c1, c2)))
            if all(u in rem for u in f0 + f1): rows[('O', f0, f1)] = set(f0 + f1)
            for f in (f0, f1):
                k = tuple(sorted(f))
                if k not in seen and all(u in rem for u in f): seen.add(k); rows[('F', k)] = set(f)
for u in remT:
    s = g.supp[u]
    if 0 not in s and X not in s: rows[('X', u)] = {u} | {('pt', p) for p in s}
cols = set(remT) | {('pt', p) for p in range(1, 10)}
Fmax = int(sys.argv[1])
colrows = collections.defaultdict(set)
for r, cs in rows.items():
    for c in cs: colrows[c].add(r)
print('rows', len(rows), '| cols', len(cols), '| F max', Fmax, flush=True)
sol = []; nodes = [0]; t0 = time.time()
def search(nf):
    if not colrows_active: return True
    nodes[0] += 1
    c = min(colrows_active, key=lambda c: len(colrows_active[c]))
    cand = sorted(colrows_active[c], key=lambda r: (r[0] == 'F', r[0] == 'X'))
    for r in cand:
        if r[0] == 'F' and nf >= Fmax: continue
        removed = cover(r)
        sol.append(r)
        if search(nf + (r[0] == 'F')): return True
        sol.pop(); uncover(removed)
    return False
colrows_active = {c: set(colrows[c]) for c in cols}
def cover(r):
    removed = []
    for c in rows[r]:
        for r2 in list(colrows_active[c]):
            for c2 in rows[r2]:
                if c2 != c and c2 in colrows_active: colrows_active[c2].discard(r2)
        removed.append((c, colrows_active.pop(c)))
    return removed
def uncover(removed):
    for c, rs in reversed(removed):
        colrows_active[c] = rs
        for r2 in rs:
            for c2 in rows[r2]:
                if c2 != c and c2 in colrows_active: colrows_active[c2].add(r2)
ok = search(0)
print('F <= %d: %s | nodes %d | %.0fs' % (Fmax, 'FOUND' if ok else 'NONE (exhaustive)', nodes[0], time.time() - t0), flush=True)
if ok:
    for r in sol:
        if r[0] == 'O': blocks.append([r[1], r[2]])
        elif r[0] == 'F': blocks.append([r[1]])
        else: pun.append(r[1])
    assert sorted([u for b in blocks for f in b for u in f] + pun) == list(range(V))
    pickle.dump((blocks, pun), open(D + 'partF%d.pkl' % Fmax, 'wb'))
    print('saved: blocks', len(blocks), collections.Counter(len(b) for b in blocks), 'lone', sum(1 for r in sol if r[0] == 'F'))

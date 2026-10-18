"""Dead-minimizer menus v2: content-piece semantics.
A piece is (frame F, content c) with F closed nondegenerate rank <= 10, c any nonempty subset of L(F).
A demand E (frame S) is served by pieces (F_i, c_i) with c_i partitioning E (disjoint, union E) and F_i a
closed flat with cl(c_i) = F_i <= S.  Cost of a piece = 1 register (it exists once, shared across demands);
leaves (|c| = 1) are the branch copies, free.  Merge/pool costs are added at the ILP stage via pool variables.
So the v2 menu for E = all partitions of E into <= KMAX groups (groups of size 1 allowed = leaves),
canonical on the (F, c) pairs.  Piece identity = (F, c); sharing = same (F, c) reused.
"""
import os, pickle, sys, time, collections
HERE = os.path.dirname(os.path.abspath(__file__))
t0 = time.time()
def log(*a, **kw): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

D = pickle.load(open(os.path.join(HERE, 'deadmin_instance.pkl'), 'rb'))
cand_set = set(D['cand']); dem_cand = D['dem_cand']; DEM = D['DEM_kind']
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g13 = Geom(13); V = g13.V
def rkof(A): return g13.closure(A)[1] if A else 0
def clof(A): return g13.closure(A)[0] if A else 0

ddem = sorted(set(E for k, S, E in DEM))
frame_of = {}
for k, S, E in DEM: frame_of.setdefault(E, S)
log('distinct demands', len(ddem), 'candidate flats', len(cand_set), flush=True)

# piece vocabulary per demand: (F, c) with c <= E, cl(c) = F in cand_set (rank <= 10, nondegenerate),
# c nonempty.  For the partition DFS we need, for each demand E, the set of usable (c, F) pairs with
# c <= E.  Build by scanning E's sub-multisets?  No: for each candidate flat F <= S (in dem_cand[E] ∪ {S}),
# the usable contents are subsets c <= E with cl(c) = F.  For the partition search we only need c values;
# enumerate candidate c as: all candidate flats' line sets intersected... simpler: candidate contents are
# line sets of the form (any candidate flat's lines) <= E, plus singletons.  But subsets of a flat that
# close to a DIFFERENT flat are also pieces (frame = closure).  The closure of c is what matters.
# For v2 partition menus we track c (content) and F = cl(c) at use time; a c is *allowed* if rank(cl(c)) <= 10.
KMAX = 4
def piece_options(E, S):
    """usable contents c <= E with rk(cl(c)) <= 10, as (c, F) pairs.  Enumerate: all closed flats F <= S
    (candidates), contents = F & E plus sub-candidates... v2 fast path: contents are (F & E) for F in
    dem_cand[E] + {S}, and singletons, and (candidate flat ∩ E) of any candidate flat of the FULL frame.
    Also arbitrary subsets of F & E close to something <= F; we include the power-set only at sizes <= 2
    beyond F & E (fallback pieces)."""
    Fs = list(dem_cand[E])
    if S in cand_set: Fs.append(S)
    seen = set()
    out = []
    for F in Fs:
        c = F & E
        if c and c not in seen:
            cf = clof(c)
            if rkof(cf) <= 10:
                seen.add(c); out.append((c, cf))
        # one-line-each subcontents are leaves; two-line subcontents:
        # (skip: leaves cover everything at cost 0, menus would explode; leaves are always available)
    # singletons are leaves (free): handled implicitly at ILP time
    return out

# partition DFS over contents with closure-rank guard
LEAF = 'LEAVES'
def covers_of(E, opts, kmax=KMAX, limit=200):
    out = []
    ol = sorted(opts, key=lambda t: -bin(t[0]).count('1'))
    def rec(rem, chosen):
        if len(out) >= limit: return
        if rem == 0:
            out.append(tuple(chosen)); return
        if len(chosen) >= kmax:
            # remainder served by leaves (free) -- allowed: leaf fill
            out.append(tuple(chosen) + ((LEAF, rem),)); return
        u = (rem & -rem).bit_length() - 1
        for c, F in ol:
            if c >> u & 1 and c & ~rem == 0 and all(c != cc for cc, _ in chosen):
                rec(rem & ~c, chosen + [(c, F)])
                if len(out) >= limit: return
        # no piece covers u: leaf fill
        out.append(tuple(chosen) + ((LEAF, rem),))
    rec(E, [])
    return out

menus = {}
piece_of = {}   # global piece registry: (c, F) -> id
t1 = time.time()
for n, E in enumerate(ddem):
    S = frame_of[E]
    opts = piece_options(E, S)
    cv = covers_of(E, opts)
    menus[E] = cv
    for cover in cv:
        for item in cover:
            if isinstance(item, tuple) and item and item[0] == LEAF: continue
            c, F = item
            if (c, F) not in piece_of: piece_of[(c, F)] = len(piece_of)
    if n % 150 == 0: log('menu %d/%d covers %d pieces %d %.0fs' % (n, len(ddem), len(cv), len(piece_of), time.time() - t1))
log('menus done: total covers', sum(len(v) for v in menus.values()), 'distinct pieces', len(piece_of), '%.0fs' % (time.time()-t1))
pickle.dump({'menus': menus, 'piece_of': piece_of, 'frame_of': frame_of},
            open(os.path.join(HERE, 'deadmin_menus2.pkl'), 'wb'))
cnt = collections.Counter(len(v) for v in menus.values())
log('covers per demand: min %d max %d mean %.1f' % (min(cnt), max(cnt), sum(len(v) for v in menus.values())/len(menus)))
# piece reuse potential: how many demands can use each piece
use = collections.Counter()
for E, cv in menus.items():
    for cover in cv:
        for item in cover:
            if isinstance(item, tuple) and item and item[0] == LEAF: continue
            use[piece_of[item]] += 1
hist = collections.Counter(use.values())
log('piece use-count histogram (top 12):', sorted(hist.items(), reverse=True)[:12])
log('pieces used >= 2 demands:', sum(1 for v in use.values() if v >= 2))

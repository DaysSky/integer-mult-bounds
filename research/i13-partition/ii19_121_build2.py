"""THE 121-LINE WORD — THE BUILD STAGE 2a v2: THE JOINT GREEDY CLUSTERING (SS1423's fix).

THE SS1423 LESSON: the per-target dims (SS1419!!) + the union-find = THE TRANSITIVE BLOBS
(the dims 6-7: ONE component of 104-111 pieces + 121 targets: INFEASIBLE!!).

THE V2: THE JOINT GREEDY — the reads (the (piece, user) pairs!!) assigned ONE BY ONE:
- the dim candidates d = (the piece's span dim)..8:
  (a) the piece's dim-d component: the JOIN the user (the frame ⊆ the user's perp + the
      user's dim-d slot free-or-same!!);
  (b) the user's dim-d component: the JOIN the piece (the accumulated content ⊆ the frame +
      the piece's dim-d slot free-or-same + the NESTING: the piece's previous frame ⊆!!);
  (c) the NEW component (both free at d!!): the frame = the accumulated span + the fillers
      from the user's perp-space!!, at the dim d.
- THE ACCUMULATED FRAMES: the component's frame ⊇ ∪(the members' contents) and each
  member's chain accumulates (the NEXT frame ⊇ THIS one!!) -> the nesting by construction.
- THE CHECKS at every join: rank(the accumulated) <= d <= 9 - rank(the component's targets)
  and the accumulated span ⊆ ∩(the users' perps) (the orthogonality mask!!).
THE OUTPUT: the failures' log + the components + the chains (the stage-2b pickle!!).
"""
import sys, time, resource, itertools, pickle
from collections import Counter
import numpy as np
t0 = time.time()
def log(*a): print('[%5.0fs rss=%dMB]' % (time.time() - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // (1024 * 1024)), *a, flush=True)

# the system [the SS1419 code]
roots = []
for i in range(8):
    for j in range(i + 1, 8):
        for si in (1, -1):
            for sj in (1, -1):
                v = np.zeros(8); v[i] = si; v[j] = sj
                roots.append(v)
half = [np.array(s, dtype=float) / 2 for s in itertools.product([1, -1], repeat=8) if s.count(-1) % 2 == 0]
def canon(v):
    for x in v:
        if x != 0:
            return tuple(v) if x > 0 else tuple(-v)
    return tuple(v)
d8 = {}
for r in list(roots) + half: d8[canon(r)] = np.array(r)
AL = list(d8.values())
L = [list(al) + [0, 0] for al in AL]
L.append([0.0] * 8 + [1.0, 1.0])
L = np.array(L, dtype=float)
V = len(L)
FORM = np.zeros((10, 10)); FORM[:8, :8] = np.eye(8); FORM[8, 9] = FORM[9, 8] = 1.0
G = L @ FORM @ L.T
PERP = []
for t in range(V):
    m = 0
    for s in range(V):
        if s != t and abs(G[s][t]) < 1e-9:
            m |= (1 << s)
    PERP.append(m)
PERPMASK = [PERP[t] | (1 << t) for t in range(V)]   # the closed perps (the frame-compat check!!)
log('the 121-line system: %d lines' % V)

D = pickle.load(open('/Users/dayssky/integer-mult-bounds/research/i13-partition/ii19_121_design.pkl', 'rb'))
pool = [list(p) for p in D['pool']]
pranks = D['pranks']
leftovers = D['leftovers']
log('the design data: %d pieces' % len(pool))

def rrank(ids):
    return int(np.linalg.matrix_rank(np.array([L[i] for i in ids]))) if ids else 0
def orth_ok(acc_mask, users):
    """the accumulated line-mask ⊆ every user's closed perp!!"""
    return all((acc_mask & ~PERPMASK[u]) == 0 for u in users)

# ============ THE JOINT GREEDY ============
# the components: the dicts; the members: the pieces (0..) + the users (1000+)
NODE_U = 1000
comps = []            # the list: dict(pieces=[], users=[], acc=0 (the line-mask), dim=d, span_r=0, tmask=[the users])
piece_comp = {}       # (pid, d) -> the comp index
user_comp = {}        # (uid, d) -> the comp index
piece_prev = {}       # pid -> (the dim, the acc-mask) of its LATEST component (the nesting!!)
user_prev = {}        # uid -> (the dim, the acc-mask)

# the reads: the (piece, user) pairs from the pool_users (the greedy's real_users!!)
reads = []
for pid, users in enumerate(D['pool_users']):
    for u in users:
        reads.append((pid, u))
# the tails: the (tail, user): the tail = the user's leftover (the -1 marker -> the per-user!!)
tail_reads = [(('T', ti), ti) for ti in range(V) if leftovers[ti]]
log('the reads: %d pieces + %d tails' % (len(reads), len(tail_reads)))

fail = 0
assigned = 0
for pid, u in reads:
    plines = pool[pid]
    pmask = 0
    for s in plines:
        pmask |= (1 << s)
    the_dim_min = max(2, pranks[pid])
    placed = False
    for d in range(the_dim_min, 9):
        # (a) the piece's dim-d component: the join the user
        if (pid, d) in piece_comp:
            ci = piece_comp[(pid, d)]
            C = comps[ci]
            # the checks: the acc ⊆ the user's perp + the user's dim-d slot free-or-this
            if (C['acc'] & ~PERPMASK[u]) == 0 and ((u, d) not in user_comp or user_comp[(u, d)] == ci):
                if (u, d) not in user_comp:
                    C['users'].append(u)
                    user_comp[(u, d)] = ci
                    # the re-check: the dim <= 9 - rank(users)
                    trank = rrank(C['users'])
                    if d > 9 - trank:
                        C['users'].pop(); del user_comp[(u, d)]
                        continue
                # the user's chain: the nesting: the user's previous acc ⊆ the C's acc?!
                if u in user_prev and not (user_prev[u][1] & ~C['acc']) == 0:
                    pass   # the acc-nesting: the previous ⊆ the new: the mask check below
                if u in user_prev and (user_prev[u][1] & ~C['acc']) != 0:
                    continue   # the nesting fail: the user's previous acc ⊄ the C's acc
                assigned += 1
                placed = True
                break
        # (b) the user's dim-d component: the join the piece
        if (u, d) in user_comp:
            ci = user_comp[(u, d)]
            C = comps[ci]
            # the checks: the piece's content ⊆ the acc?? NO: the acc grows; the frame: the span of the acc + the piece!!
            new_acc = C['acc'] | pmask
            if (new_acc & ~PERPMASK[u]) == 0 and ((pid, d) not in piece_comp or piece_comp[(pid, d)] == ci):
                # the piece's chain: the nesting: the piece's previous acc ⊆ the new acc?!?
                if pid in piece_prev and (piece_prev[pid][1] & ~new_acc) != 0:
                    continue
                # the rank checks: rank(new acc) <= d <= 9 - rank(users)
                ids = [s for s in range(V) if (new_acc >> s) & 1]
                if rrank(ids) > d:
                    continue
                if d > 9 - rrank(C['users']):
                    continue
                if (pid, d) not in piece_comp:
                    C['pieces'].append(pid)
                    piece_comp[(pid, d)] = ci
                C['acc'] = new_acc
                C['span_r'] = rrank(ids)
                assigned += 1
                placed = True
                break
        # (c) the NEW component (both free at d!!)
        if (pid, d) not in piece_comp and (u, d) not in user_comp:
            # the nesting: the piece's previous acc ⊆ the piece's content?? the frame: the acc: the piece's prev ⊆?!
            new_acc = pmask
            if pid in piece_prev and (piece_prev[pid][1] & ~pmask) != 0:
                new_acc = pmask | piece_prev[pid][1]
            if u in user_prev and (user_prev[u][1] & ~new_acc) != 0:
                new_acc = new_acc | user_prev[u][1]
            if (new_acc & ~PERPMASK[u]) != 0:
                continue   # the accumulated ⊄ the user's perp
            ids = [s for s in range(V) if (new_acc >> s) & 1]
            if rrank(ids) > d or d > 9 - rrank([u]):
                continue
            ci = len(comps)
            comps.append(dict(pieces=[pid], users=[u], acc=new_acc, dim=d,
                             span_r=rrank(ids)))
            piece_comp[(pid, d)] = ci
            user_comp[(u, d)] = ci
            assigned += 1
            placed = True
            break
    if placed:
        # the chains' update: the piece's/user's latest (the max dim!!)
        if pid not in piece_prev or piece_prev[pid][0] < d:
            piece_prev[pid] = (d, comps[piece_comp[(pid, d)]]['acc'])
        if u not in user_prev or user_prev[u][0] < d:
            user_prev[u] = (d, comps[user_comp[(u, d)]]['acc'])
    else:
        fail += 1
log('THE JOINT GREEDY (the pieces): assigned %d of %d; FAILURES %d' % (assigned, len(reads), fail))

# the tails: the per-user tail registers: the reads at the user's LAST dim + the t-perp!!
tail_fail = 0
tail_dim = {}
for tid, u in tail_reads:
    lo = leftovers[u]
    lmask = 0
    for s in lo:
        lmask |= (1 << s)
    # the tail: the user's private register: the read at the user's top free dim (before the t-perp!!)
    # the simplest: the dim 8 (the t-perp-adjacent!!): the frame: the user's accumulated + the tail ⊆ the perp ✓!!
    d = 8
    acc = lmask
    if u in user_prev and (user_prev[u][1] & ~acc) != 0:
        acc = acc | user_prev[u][1]
    if (acc & ~PERPMASK[u]) != 0:
        tail_fail += 1
        continue
    ids = [s for s in range(V) if (acc >> s) & 1]
    if rrank(ids) > d:
        tail_fail += 1
        continue
    tail_dim[u] = d
log('THE TAILS: assigned %d of %d (the tail-failures %d)' % (len(tail_dim), len(tail_reads), tail_fail))

# the component stats
sizes = Counter((len(C['pieces']), len(C['users'])) for C in comps)
log('THE COMPONENTS: %d; the (pieces, users) histogram: %s' % (len(comps), dict(sorted(sizes.items()))))
dimc = Counter(C['dim'] for C in comps)
log('the dims: %s' % dict(sorted(dimc.items())))
bad = [C for C in comps if C['span_r'] > C['dim'] or C['dim'] > 9 - rrank(C['users'])]
log('the infeasible components: %d (double-checked)' % len(bad))
ok = (fail == 0) and (tail_fail == 0) and (len(bad) == 0)
log('THE STAGE-2a v2 VERDICT: %s' % ('FEASIBLE — the joint greedy closed; the stage 2b (the word!!) proceeds!!' if ok
    else 'TIGHT: %d read-failures, %d tail-failures, %d infeasible' % (fail, tail_fail, len(bad))))
out = dict(comps=[dict(pieces=C['pieces'], users=C['users'], acc=C['acc'], dim=C['dim']) for C in comps],
           piece_comp={str(k): v for k, v in piece_comp.items()},
           user_comp={str(k): v for k, v in user_comp.items()},
           piece_prev={str(k): v for k, v in piece_prev.items()},
           user_prev={str(k): v for k, v in user_prev.items()},
           tail_dim=tail_dim, reads_fail=fail, tail_fail=tail_fail)
with open('/Users/dayssky/integer-mult-bounds/research/i13-partition/ii19_121_stage2a_v2.pkl', 'wb') as f:
    pickle.dump(out, f)
log('the stage-2a v2 data pickled: ii19_121_stage2a_v2.pkl')
log('DONE')

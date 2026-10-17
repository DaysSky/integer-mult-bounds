# Constructive block partition: 6 complete star blocks (max K4 packing) + partial star frames for the 19 leftover P
# lines + T-octets / TTTT frames; randomized with restarts, exact-cover backtracking for the T part.
import sys, itertools, random, collections, pickle
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V
P, T = g.P, g.T
K4s = [[0, 1, 2, 3], [0, 4, 5, 6], [0, 7, 8, 9], [1, 4, 7, 10], [2, 5, 8, 10], [3, 6, 9, 10]]
seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
rng = random.Random(seed)
def star_frames(h, F4):
    p, q, r, s = F4
    return [(P(a, b), P(c, d), T(h, a, b), T(h, c, d)) for (a, b), (c, d) in (((p, q), (r, s)), ((p, r), (q, s)), ((p, s), (q, r)))]
used_edges = set(frozenset(e) for b in K4s for e in itertools.combinations(b, 2))
left = [e for e in itertools.combinations(range(11), 2) if frozenset(e) not in used_edges]
print('leftover P edges', len(left), left)
def tri(a, b, c): return T(*sorted((a, b, c)))
for attempt in range(200000):
    usedT = set(); blocks = []; ok = True
    hubs = []
    for F4 in K4s:
        hs = [h for h in range(11) if h not in F4]; rng.shuffle(hs)
        for h in hs:
            ts = [tri(h, a, b) for a, b in itertools.combinations(F4, 2)]
            if not any(t in usedT for t in ts):
                usedT |= set(ts); blocks.append(('star', h, F4, star_frames(h, F4))); break
        else: ok = False; break
    if not ok: continue
    # partial star frames on leftover P edges: perfect-ish matching of edges into disjoint pairs + hub
    E = list(left); rng.shuffle(E)
    frames = []; usedP = set()
    def pfr(E, frames):
        if len([e for e in E if e not in usedP]) <= 1: return True
        e1 = next(e for e in E if e not in usedP)
        cand = [e2 for e2 in E if e2 not in usedP and e2 != e1 and not set(e1) & set(e2)]
        rng.shuffle(cand)
        for e2 in cand:
            hs = [h for h in range(11) if h not in e1 and h not in e2]; rng.shuffle(hs)
            for h in hs:
                t1, t2 = tri(h, *e1), tri(h, *e2)
                if t1 in usedT or t2 in usedT: continue
                usedP.add(e1); usedP.add(e2); usedT.add(t1); usedT.add(t2); frames.append((h, e1, e2))
                if pfr(E, frames): return True
                usedP.discard(e1); usedP.discard(e2); usedT.discard(t1); usedT.discard(t2); frames.pop()
        return False
    if not pfr(E, frames): continue
    punP = [e for e in E if e not in usedP]
    # T part: exact cover of remaining triples by octets / TTTT frames, 3 punctured T lines allowed
    remT = set(tri(*c) for c in itertools.combinations(range(11), 3)) - usedT
    supp = {t: g.supp[t] for t in remT}
    # all TTTT frames (half octets) inside remT and octets
    def octet_frames(m):
        (a1, a2), (b1, b2), (c1, c2) = m
        tr = [(x, y, z) for x in (a1, a2) for y in (b1, b2) for z in (c1, c2)]
        f0 = tuple(tri(*x) for x in tr if (int(x[0] == a2) + int(x[1] == b2) + int(x[2] == c2)) % 2 == 0)
        f1 = tuple(tri(*x) for x in tr if (int(x[0] == a2) + int(x[1] == b2) + int(x[2] == c2)) % 2 == 1)
        return f0, f1
    # randomized greedy octets then frames, with retries
    best = None
    for rr in range(30):
        R = set(remT); octs = []; tf = []
        order = list(R); rng.shuffle(order)
        for t in order:
            if t not in R: continue
            a, b, c = supp[t]
            others = [x for x in range(11) if x not in (a, b, c)]
            opts = []
            for a2, b2, c2 in itertools.permutations(others, 3):
                f0, f1 = octet_frames(((a, a2), (b, b2), (c, c2)))
                if all(x in R for x in f0 + f1): opts.append(('O', f0, f1))
            if opts:
                o = rng.choice(opts); octs.append(o[1:]); R -= set(o[1] + o[2]); continue
            for a2, b2, c2 in itertools.permutations(others, 3):
                f0, f1 = octet_frames(((a, a2), (b, b2), (c, c2)))
                f = f0 if t in f0 else f1
                if all(x in R for x in f): opts.append(f)
            if opts:
                f = rng.choice(opts); tf.append(f); R -= set(f)
        if len(R) <= 3:
            sc = (len(R), -len(octs))
            if best is None or sc < best[0]: best = (sc, octs, tf, sorted(R))
    if best is None: continue
    (nr, no), octs, tf, punT = best
    nfr = sum(3 for b in blocks) + len(frames) + 2 * len(octs) + len(tf)
    print('attempt', attempt, '| stars', len(blocks), '| partial star frames', len(frames), '| octets', len(octs), '| lone TTTT', len(tf),
          '| punctured P', punP, 'T', [g.supp[t] for t in punT], '| frames', nfr, flush=True)
    out = dict(stars=[(h, F4, fr) for _, h, F4, fr in blocks],
               pstar=[(h, e1, e2, (P(*e1), P(*e2), tri(h, *e1), tri(h, *e2))) for h, e1, e2 in frames],
               octets=octs, lone=tf, punct=[P(*e) for e in punP] + punT)
    allf = [f for _, _, fr in out['stars'] for f in fr] + [x[3] for x in out['pstar']] + [f for o in octs for f in o] + tf
    lines = [u for f in allf for u in f] + out['punct']
    assert sorted(lines) == list(range(V)), 'not a partition'
    pickle.dump(out, open('/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/blk/bp_s%d.pkl' % seed, 'wb'))
    if len(tf) <= 2: break

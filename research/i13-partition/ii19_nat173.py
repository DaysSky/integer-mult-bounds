"""nat173: THE TARGETS' B-CHAIN CENSUS + THE REFRAME-DUP TEST at the 121.
The un-measured item: the targets' B-chains (~480 rank-2 climbs, the 968-mass block).
(1) the per-target B-chain climb-hist;
(2) the reframe question: the targets' B-reads re-aimed at the dim-8 perp-frames
    -- the dup-law: the helpers read by 2+ targets at incomparable dim-8 frames
    need a dup per incomparable read (the r434's 471-dup law, never measured here).
"""
import json, gzip
from collections import Counter, defaultdict

w = json.load(gzip.open('/tmp/w4-tuned-gcheck.json.gz', 'rt'))
v = w['v']
LCDIM = {0: 0, 1: 1, 2: 2, 3: 3, 12: 4, 13: 5, 30: 6, 64: 8, 120: 8, 121: 9}
dims = [LCDIM[len(fr)] for fr in w['frames']]

# (1) the targets' B-chains
chains = defaultdict(list)
for F, d, ss in w['B']:
    if v <= d < 2 * v:
        chains[d - v].append(F)
print('the targets with B-gates: %d | the gates per target: %s' % (
    len(chains), dict(sorted(Counter(len(c) for c in chains.values()).items()))))

hist_t = Counter()
for t, Fs in chains.items():
    dd = sorted(set(dims[F] for F in Fs))
    for i in range(1, len(dd)):
        hist_t[dd[i] - dd[i - 1]] += 1
print('the targets\' distinct-frame dim-jumps: %s (the mass contribution: %d)' % (
    dict(sorted(hist_t.items())), sum(r * z for r, z in hist_t.items())))

# the helpers' reads in B (per helper: the reading targets)
hlp_users = defaultdict(set)
for F, d, ss in w['B']:
    if v <= d < 2 * v:
        for s in ss:
            if s >= 2 * v:
                hlp_users[s].add(d - v)
uses = Counter(len(u) for u in hlp_users.values())
print('the helpers in B: %d | the users-histogram: %s' % (len(hlp_users), dict(sorted(uses.items()))))

# (2) the dup-test: the reframe reads at the dim-8 perp-frames.
# each target's perp-frame: the dim-8 frame containing t's perp (the target's own final frame).
finals = w['final']
perp_frame = {}
for t in range(v):
    fr = finals[v + t]
    perp_frame[t] = fr

# the incomparability: two dim-8 frames are comparable iff one's line-set contains the other's.
def lineset(fr):
    return frozenset(tuple(int(c) for c in vec) for vec in w['frames'][fr])

ls = {perp_frame[t]: lineset(perp_frame[t]) for t in range(v)}

dups = 0
multi = 0
for s, us in hlp_users.items():
    if len(us) < 2:
        continue
    multi += 1
    us = sorted(us)
    # the reads at each user's perp-frame: count the incomparable pairs' extra visits
    # a wire visiting k incomparable frames needs (k-1) extra copies (the climb chain can't descend)
    frames = [perp_frame[t] for t in us]
    # cluster by comparability (greedy: new cluster if incomparable with all in it)
    clusters = []
    for f in frames:
        placed = False
        for cl in clusters:
            if ls[f] <= ls[cl[0]] or ls[cl[0]] <= ls[f]:
                cl.append(f)
                placed = True
                break
        if not placed:
            clusters.append([f])
    dups += len(clusters) - 1
print('the helpers with >=2 users: %d | THE DUP-COUNT (the reframe): %d extra copies' % (multi, dups))
print('the R-impact: %d + %d dups = %d vs the wall R<=591' % (w['R'], dups, w['R'] + dups))

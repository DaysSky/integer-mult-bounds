"""Shared-content demand decomposition for I_{13,1}: minimize total incidence.
The corrected frontier question: E8's words win via shared sub-sums (incidence 25/line over 190 demands;
9/line for partition demands).  Every I13 architecture examined is closed by its measured incidence
(PG top 28,808 = 79/line; maxpairs halves ~18,000 = 49/line).  Break-even at the best histogram shapes
needs incidence <= ~17,000 (47/line):  R ~ (I - 9,464 branch arrivals)/13 + 728 <= 1,312.
This script searches for the minimum-incidence decomposition of the 364 perp demands R(t):
  pieces = perp-sections S_ab = perp(a) & perp(b) for orthogonal pairs (a,b) [users = lines t with
  supp(t)-subset] + Q-parts of good frames; each target covered by disjoint pieces from its user list;
  sharing free (a piece's build cost |supp| paid once).  Greedy with reuse preference; report I.
Refinements not in v1: apex D10 parts (30-user), star rooms, GF(2) cancellation covers."""
import os, pickle, sys, time, collections, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(13); V = g.V; HYP = g.HYP; G = g.G; bits = g.bits
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

# demands: R(t) per target
R = {t: HYP[t] & ~(1 << t) for t in range(V)}
log('targets', len(R), 'mean |R(t)| %.1f' % (sum(bin(r).count('1') for r in R.values()) / V))

# piece vocabulary v1: sections of orthogonal pairs
pairs = [(a, b) for a in range(V) for b in range(a + 1, V) if G[a, b] == 0]
log('orthogonal pairs', len(pairs))
secs = {}
for a, b in pairs:
    s = HYP[a] & HYP[b]
    if bin(s).count('1') >= 20: secs[(a, b)] = s   # keep big sections
log('big sections', len(secs))
# users per section: t with supp <= HYP[t]
users = {}
for k, s in secs.items():
    us = [t for t in range(V) if s & ~HYP[t] == 0]
    if us: users[k] = us
log('sections with users', len(users), 'users hist', dict(sorted(collections.Counter(len(u) for u in users.values()).items())))
# per-target candidate lists
by_t = collections.defaultdict(list)
for k, us in users.items():
    for t in us: by_t[t].append(k)
log('candidates per target: mean %.1f' % (sum(len(v) for v in by_t.values()) / V))

# greedy: cover each R(t) by its sections, preferring widely-used and large ones; singles fill.
used = set()
incidence = 0
remaining = dict(R)
order = sorted(range(V), key=lambda t: -len(by_t.get(t, [])))
for t in order:
    need = remaining[t]
    cands = sorted(by_t.get(t, []), key=lambda k: (-len(users[k]), -bin(secs[k]).count('1')))
    for k in cands:
        s = secs[k]
        if s & ~need == 0 and s & need:
            if k not in used:
                used.add(k); incidence += bin(s).count('1')
            need &= ~s
            if not need: break
    # leftovers as single lines (branch reads, incidence already in branch budget? no: singles are
    # free branch arrivals — count them separately)
    singles = bin(need).count('1')
    remaining[t] = need
    if singles: incidence_share = None
# total: used sections + check uncovered mass
uncovered = sum(bin(remaining[t]).count('1') for t in remaining)
log('used sections', len(used), 'total section incidence', sum(bin(secs[k]).count('1') for k in used))
log('uncovered single lines (branch arrivals, free within 9,464):', uncovered)
I = sum(bin(secs[k]).count('1') for k in used)
# budget arithmetic
branch_arrivals = 2 * V * 13
print()
print('DECOMPOSITION INCIDENCE: sections %d + singles %d = %d (%.1f/line)' % (
    I, uncovered, I + uncovered, (I + uncovered) / V))
print('E8 reference: 3,000 (25/line); break-even threshold ~17,000 (47/line)')
print('branch arrivals cover singles up to 9,464; mid registers >= (I + uncovered - 9,464)/13')
mid = max(0, (I + uncovered - 9464 + 12) // 13)
print('=> R >= 728 + %d = %d = %.2fv (break-even needs <= 1,312)' % (mid, 728 + mid, (728 + mid) / V))
pickle.dump({'used_sections': list(used), 'incidence': I, 'uncovered': uncovered},
            open(os.path.join(HERE, 'shared Decomp.pkl' if False else 'shared_decomp.pkl'), 'wb'))

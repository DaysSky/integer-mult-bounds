"""THE DUTY/PIN STRUCTURE (ii19_nat27.py) — the honest concentration bound's ingredients.

The one-climax probe says the concentration lever is huge (+18.6% at R=472).  What's HONESTLY
permitted: every register's duty frames (the gates where it is an operand, in phase order) and
the pins that force multi-rung chains:
  (1) the B-phase target-gates: per target t, the helper srcs read at perp(t) — is each such
      helper read at exactly ONE perp (its chain can end there), or several (impossible walls)?
  (2) the helpers never B-read: are all their duties at FULL-able frames (one 0->9 climb)?
  (3) the sources: their duty frames across all phases (their pin spans).
"""
import json, os, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))

sys.argv = ['ii19_nat20.py']
exec(open('ii19_nat20.py').read().split('# (1) chain-shape census')[0])
PH = ('D', 'A', 'B')

# (1) the B target-gates and their helper srcs
bt = defaultdict(list)     # target -> [helper srcs]
bth = defaultdict(set)     # helper -> {targets reading it at perps}
for F, d, srcs in w['B']:
    if V <= d < 2 * V:
        for s in srcs:
            bt[d - V].append(s)
            if s >= 2 * V: bth[s].add(d - V)
sizes = Counter(len(v) for v in bt.values())
log('(1) B target-gates: %d targets | read-set size hist %s | helper-srcs %d' % (
    len(bt), dict(sorted(sizes.items())), len(bth)))
multi = Counter(len(v) for v in bth.values())
log('    per-helper reader counts (distinct perps): %s' % dict(sorted(multi.items())))

# (2) helpers never read by a target at a perp: their duty frames
bread = set(bth)
duty = defaultdict(list)
for ph in PH + ('C',):
    for gi, (F, d, srcs) in enumerate(w[ph]):
        for r in [d] + list(srcs):
            duty[r].append((ph, F))
n_full_only, n_other, other_frames = 0, 0, Counter()
for h in range(2 * V, nreg):
    if h in bread:
        continue
    frames = set(F for ph, F in duty[h])
    tops = set(dims[F] for F in frames)
    if tops <= {0, 9}:
        n_full_only += 1
    else:
        n_other += 1
        other_frames.update(tops - {0, 9})
log('(2) helpers never B-read: %d | all duties at {0,9}-dim frames (ONE 0->9 climb ok): %d | pinned lower: %d %s' % (
    len(bread) and (nreg - 2 * V - len(bread)), n_full_only, n_other, dict(sorted(other_frames.items()))))

# (3) the sources' duty frames (per phase)
spans = Counter()
sduty = defaultdict(set)
for ph in PH + ('C',):
    for F, d, srcs in w[ph]:
        for s in srcs:
            if s < V: sduty[s].add((ph, dims[F]))
for s in range(V):
    spans[tuple(sorted(sduty[s]))] += 1
log('(3) source duty (phase, dim) patterns: %s' % dict(sorted(spans.items(), key=lambda x: -x[1])[:14]))

# the B-read helpers' A-phase src composition: sources vs helpers (the nested-rung requirement)
tot_src_src, tot_helper_src = 0, 0
for h in bth:
    for F, d, srcs in w['A']:
        if d == h:
            for s in srcs:
                if s < V: tot_src_src += 1
                else: tot_helper_src += 1
log('(4) B-read helpers: A-gate src composition: source-reads %d | helper-reads %d' % (tot_src_src, tot_helper_src))

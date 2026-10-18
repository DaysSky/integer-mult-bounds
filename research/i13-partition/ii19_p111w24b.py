"""THE PASS-ANATOMY TRACE (ii19_p111w24b.py) — scratch diagnostic: WHY are the 706 legal joint
words hist-neutral (701/706 empty delta)?  Take the first depth-1 pass, dump the seed, the repair,
and the per-register climb-rank sequences (base vs modified)."""
import json, os, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
argv = sys.argv[1:]
sys.argv = ['ii19_p111w21.py']
exec(open('ii19_p111w21.py').read().split('# (1) the T155 helpers')[0])
sys.argv = ['ii19_p111w24.py']
src = open('ii19_p111w24.py').read()
exec(src.split("admitted, why, passes = ")[0])

def climbs_seq(re):
    """per-register list of (rank) over D/A/B/C/final on the reframed word."""
    G = dict(word_with(re)); G['C'] = w['C']
    cur = list(w['start']); seq = defaultdict(list)
    def go(gates):
        for F, d, srcs in gates:
            for r in [d] + srcs:
                if cur[r] != F:
                    seq[r].append(dims[F] - dims[cur[r]]); cur[r] = F
    for ph in ('D', 'A', 'B'): go(G[ph])
    for r in range(nreg):
        F = w['final'][r]
        if cur[r] != F: seq[r].append(dims[F] - dims[cur[r]])
    return seq

base = climbs_seq({})
for n, (r, Fb, Fc, gates) in enumerate(cands):
    re = {g: Fc for g in gates}
    e, hist, _ = replay_re(re)
    if e is None: continue
    mv = repair(re, e, levels(re))
    if mv is None: continue
    re2 = dict(re); re2.update(mv)
    e2, hist2, _ = replay_re(re2)
    if e2 is not None: continue
    log('FIRST DEPTH-1 PASS: seed reg %d %d(d%d) -> %d(d%d) over %d gates' % (r, Fb, dims[Fb], Fc, dims[Fc], len(gates)))
    log('  repair (blocking reg from failure %s): %s' % (e, {k: (v, dims[v]) for k, v in mv.items()}))
    mod = climbs_seq(re2)
    diff = [x for x in range(nreg) if base[x] != mod[x]]
    log('  per-register climb sequences changed: %d registers' % len(diff))
    for x in diff:
        log('    reg %d: base %s -> mod %s' % (x, base[x], mod[x]))
    log('  hist delta: %s' % {k: hist2[k] - hist0[k] for k in sorted(set(hist2) | set(hist0)) if hist2[k] != hist0[k]})
    break

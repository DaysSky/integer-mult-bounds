"""Exit-rank census on P111-tuned: for each helper, its frame at the end of B (last A/B frame), and the span of the
end-of-B frames of the helper and of every register it shares an A/B z-gate with.  A helper can end at a hyperplane G
(width-7 residual) only if that span has dim <= 7 (necessary condition for C at G)."""
import gzip, json
import numpy as np
from collections import Counter, defaultdict
w = json.load(gzip.open('/home/user/integer-mult-bounds/research/e8-bit-p111-tuned/tune/bitE8mut-p111-tuned.json.gz', 'rt'))
v = w['v']; R = w['R']; n = 2 * v + R
L = np.array(w['lines'], dtype=float)
FR = w['frames']
def rk(lines): return int(np.linalg.matrix_rank(L[sorted(lines)])) if lines else 0
cur = list(w['start'])
partners = defaultdict(set)
is_y = lambda r: v <= r < 2 * v
for sec in ('D', 'A', 'B'):
    for f, d, srcs in w[sec]:
        for r in [d] + srcs: cur[r] = f
        if sec != 'D' and not is_y(d):
            regs = [d] + srcs
            for a in regs:
                for b in regs:
                    if a != b: partners[a].add(b)
endB = cur[:]
dimh = Counter(); spand = Counter(); good = []
for h in range(2 * v, n):
    fh = set(FR[endB[h]])
    dimh[rk(fh)] += 1
    u = set(fh)
    for p in partners[h]: u |= set(FR[endB[p]])
    d = rk(u); spand[d] += 1
    if d <= 7: good.append(h)
print('helper end-of-B frame dims:', sorted(dimh.items()))
print('dim of span(helper + partners end-of-B frames):', sorted(spand.items()))
print('candidates (span <= 7):', len(good))
# sources: end-of-B frame dims
print('source end-of-B dims:', sorted(Counter(rk(set(FR[endB[s]])) for s in range(v)).items()))

"""Anatomy of an E8 bitE8/1+mut word: per-register piece lists (frame ranks), frontier cost per role."""
import gzip, json, sys, numpy as np
from collections import Counter, defaultdict
sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..'))
from qbudget import cost
path = sys.argv[1]
w = json.load(gzip.open(path, 'rt'))
v, R = w['v'], w['R']; n = 2 * v + R
L = np.array(w['lines'], dtype=float)
fdim = [int(np.linalg.matrix_rank(L[f])) if f else 0 for f in w['frames']]
cur = list(w['start']); path_ = [[fdim[c]] for c in cur]; frames_of = [[c] for c in cur]
phase_of_climb = [[] for _ in range(n)]
def run(name):
    for f, d, srcs in w[name]:
        for r in [d] + srcs:
            if cur[r] != f:
                cur[r] = f; path_[r].append(fdim[f]); frames_of[r].append(f); phase_of_climb[r].append(name)
for name in ('D', 'A'): run(name)
retf = [cur[q] for q in w['ret']]
for name in ('B', 'C'): run(name)
# final climbs
FULL = fdim.index(8)
for r in range(n):
    if r < v or r >= 2 * v:
        if fdim[cur[r]] != 8: path_[r].append(8); phase_of_climb[r].append('end')
    else:
        if fdim[cur[r]] != 7: path_[r].append(7); phase_of_climb[r].append('end')
m = 64
def pieces(p): return [b - a for a, b in zip(p, p[1:])]
role = {}
for r in range(n): role[r] = 'src' if r < v else ('tgt' if r < 2 * v else 'hlp')
agg = defaultdict(lambda: [0, 0.0, Counter()])
for r in range(n):
    pc = pieces(path_[r]); c = 9 * sum(cost(x, m) for x in pc)
    a = agg[role[r]]; a[0] += 1; a[1] += c; a[2][tuple(pc)] += 1
tot = 0
for k, (cnt, c, shapes) in agg.items():
    tot += c
    print('%s: n=%d  local cost %.2f (%.4f each)  #pieces avg %.2f' % (k, cnt, c, c / cnt, sum(len(s) * z for s, z in shapes.items()) / cnt))
    for s, z in shapes.most_common(8): print('    ', s, z, '%.4f' % (9 * sum(cost(x, m) for x in s)))
cst = sum(fdim[f] for f in retf)
print('cst', cst, 'retained ranks', [fdim[f] for f in retf], 'COPY cost', 9 * sum(cost(fdim[f], m) for f in retf))
print('local total', tot + 9 * sum(cost(fdim[f], m) for f in retf), 'budget', 8 * v - 9 * cst)
H = Counter()
for r in range(n):
    for x in pieces(path_[r]): H[x] += 1
for f in retf: H[fdim[f]] += 1
print('histogram', dict(sorted(H.items())))

"""All (sequence, split set) combos for K = 4 with total stretches <= 9 and positive price, grouped by sequence.
Constraints used (proven): strict F/R alternation does not restrict pairs; a pair active only at stage 0 or only at
stage 8 is impossible (rows freeze); 3-runs need a split at an inner junction of the run."""
import itertools, json, sys
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/sched')
from genprice import price
from splitp import slots
import mpmath as mp
ref = mp.mpf('0.001733427039589844')
tuned = {1: 1323, 2: 1342, 3: 79, 4: 44, 5: 102, 6: 11, 7: 19}
K = 4; s = 9
cache = {}
def pr(sl):
    if sl not in cache:
        c, d = price(tuned, 111, 8, 439, s, K, list(sl))
        cache[sl] = float((c / ref - 1) * 100) if c else -999
    return cache[sl]
out = {}
for sq in itertools.product(range(K), repeat=s):
    firsts = []
    for x in sq:
        if x not in firsts: firsts.append(x)
    if firsts != list(range(K)): continue
    act = {r: [j for j in range(s) if sq[j] == r] for r in range(K)}
    if any(act[r] == [0] or act[r] == [s - 1] for r in range(K)): continue
    def interior(r, b):
        last = max([j for j in act[r] if j < b], default=-1); nxt = min([j for j in act[r] if j >= b], default=s)
        return (last + 1) < b < nxt
    opts = [(r, b) for b in range(1, s) for r in range(K) if r not in (sq[b - 1], sq[b]) and interior(r, b)]
    base = len(slots(list(sq), ()))
    # 3-runs at b, b+1, b+2 need a split at time b+1 or b+2
    runs3 = [b for b in range(s - 2) if sq[b] == sq[b + 1] == sq[b + 2]]
    for k in range(0, 4):
        if base + k > 9: break
        for sp in itertools.combinations(opts, k):
            times = {b for (_, b) in sp}
            if len(times) < len(sp): continue                    # one split per time (search limit)
            if any(not ({b + 1, b + 2} & times) for b in runs3): continue
            if k == 0 and runs3: continue
            sl = slots(list(sq), sp)
            v = pr(sl)
            if v > 0: out.setdefault(tuple(sq), []).append((v, sp, sl))
rows = sorted(((max(x[0] for x in L), sq, sorted(L, reverse=True)) for sq, L in out.items()), reverse=True)
json.dump([(v, list(sq), [(a, [list(t) for t in b], list(c)) for a, b, c in L]) for v, sq, L in rows], open('splitlist_K4.json', 'w'))
print(len(rows), 'sequences with positive (seq, splits) options')
for v, sq, L in rows[:25]: print('%+.3f%%' % v, sq, 'options', len(L), 'best', L[0][1], L[0][2])

"""Price every canonical pair sequence of s = 2K + 1 stages (one pair per stage, junction-only bridges, so idle
stretches are unsplit gaps) with the unchanged P111-tuned local word.  Output: slot multisets sorted by price."""
import sys, itertools, json
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/sched')
from genprice import price
import mpmath as mp
K = int(sys.argv[1]); s = 2 * K + 1; a = 7
ref = mp.mpf('0.001733427039589844')
tuned = {1: 1323, 2: 1342, 3: 79, 4: 44, 5: 102, 6: 11, 7: 19}
def slots(sq):
    out = []
    for p in range(K):
        act = [j for j in range(s) if sq[j] == p]
        lv = 0
        for j in act:
            if j > lv: out.append((j - lv) * a)
            lv = j + 1
        if s > lv: out.append((s - lv) * a)
    return tuple(sorted(out, reverse=True))
bym = {}
for sq in itertools.product(range(K), repeat=s):
    firsts = []
    for p in sq:
        if p not in firsts: firsts.append(p)
    if firsts != list(range(K)): continue
    bym.setdefault(slots(sq), []).append(sq)
res = []
for sl, sqs in bym.items():
    c, d = price(tuned, 111, 8, 439, s, K, list(sl))
    res.append((float((c / ref - 1) * 100) if c else -999, sl, len(sqs), sqs[0]))
res.sort(reverse=True)
for r in res[:40]: print('%+.2f%%' % r[0], r[1], 'seqs', r[2], 'e.g.', r[3])
print('distinct multisets', len(res), 'positive', sum(1 for r in res if r[0] > 0))
json.dump([(r[0], r[1], [list(x) for x in bym[r[1]]]) for r in res], open('seqprice_K%d.json' % K, 'w'))

"""nat148: THE UN-OPTIMIZED PROCESSES - prune_dead + least_frames on the r434.

tune434.py only ran T/S/F; prune_dead (observable pruning, PR542/548) and
least_frames (PR542) were NEVER called on this word.
(1) prune_dead: count the dead A-summands; if any, apply + verify.
(2) least_frames: the least-span assignment; count the changed gates.
(3) Then: the adapter + gcheck + the price for each variant.
"""
import json, gzip, os, sys, copy

sys.path.insert(0, os.path.join('..', 'e8-bit-p111-tuned', 'tune'))
sys.path.insert(0, os.path.join('..', 'e8-bit-p111-tuned'))
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'tword'))

W = json.load(gzip.open('/tmp/r434-censusplan-tuned.json.gz', 'rt'))
print('the word: R=%d, gates D%d A%d B%d C%d' % (W['R'], len(W['D']), len(W['A']), len(W['B']), len(W['C'])))

import tune
import wlib

# (1) prune_dead
Tn = tune.Tuner(W, a=0.001733)
ndead = tune.prune_dead(Tn)
print('prune_dead: %d dead A-summands' % ndead)
if ndead:
    w1 = Tn.word()
    # the finals' integrity: the value replay
    ok = wlib.paid(w1)
    print('  after prune: the paid profile %s' % ok)
    json.dump(w1, gzip.open('/tmp/r434-pruned.json.gz', 'wt'))
    print('  SAVED /tmp/r434-pruned.json.gz')

# (2) least_frames
w2, moves = tune.least_frames(copy.deepcopy(W))
print('least_frames: %d gates changed' % len(moves))
if moves:
    print('  sample:', moves[:5])
    json.dump(w2, gzip.open('/tmp/r434-least.json.gz', 'wt'))
    print('  SAVED /tmp/r434-least.json.gz')

# (3) the hist comparison + the prices for the variants
import mpmath as mp
mp.mp.dps = 40
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
from pricer import idle_slots, host_greedy

P111 = mp.mpf('0.001733052823330162099157')
K, T = 4, 32
L = 2*K+1; a = 7; m_ = 1+L*a; w = 8


def hist_of(word):
    """the gcheck-style climb replay"""
    lines = word['lines']
    from fractions import Fraction

    def rref_int(rows):
        m = [list(map(Fraction, r)) for r in rows]
        r = 0
        for c in range(len(m[0]) if m else 0):
            p = None
            for i in range(r, len(m)):
                if m[i][c]:
                    p = i; break
            if p is None: continue
            m[r], m[p] = m[p], m[r]
            for i in range(len(m)):
                if i != r and m[i][c]:
                    f = m[i][c]/m[r][c]
                    m[i] = [(x - f*y) for x, y in zip(m[i], m[r])]
            r += 1
        return m[:r]

    dims = [len(rref_int([lines[i] for i in F])) for F in word['frames']]
    hist = {}
    cur = list(word['start'])
    nreg = 2*word['v'] + word['R']

    def climb(r, F):
        if cur[r] != F:
            hist[dims[F] - dims[cur[r]]] = hist.get(dims[F] - dims[cur[r]], 0) + 1
            cur[r] = F

    for F, d, ss in word['D']:
        climb(d, F)
        for s in ss: climb(s, F)
    for F, d, ss in word['A']:
        climb(d, F)
        for s in ss: climb(s, F)
    # the ret-frames (the replay positions at the A-end)
    curA = list(cur)
    for q in word['ret']:
        hist[dims[curA[q]]] = hist.get(dims[curA[q]], 0) + 1
    for F, d, ss in word['B']:
        climb(d, F)
        for s in ss: climb(s, F)
    for F, d, ss in word['C']:
        climb(d, F)
        for s in ss: climb(s, F)
    for r in range(nreg):
        climb(r, word['final'][r])
    return hist


def price_of(hist, v, R, cst):
    slots = {}
    for c in idle_slots(K, a):
        slots[c] = slots.get(c, 0) + 2*v
    WW = 2*K*v*T

    def F_of(q):
        nres = R*L
        rem = host_greedy(slots, nres, w, q, m_)
        prof = {}
        for r, z in hist.items(): prof[r] = prof.get(r, 0) + z*T*L
        for r, z in rem.items(): prof[r] = prof.get(r, 0) + z*T
        tot = sum(prof.values())
        s = sum(mp.mpf(r)*z/(m_*WW)*(mp.mpf(m_)/r)**q for r, z in prof.items() if r < m_)
        s += 32*m_*mp.mpf(tot)/(mp.mpf(10)**16 * WW)*mp.mpf(m_)**q
        return s - 1

    lo, hi = mp.mpf(0), mp.mpf('0.05')
    if F_of(lo) >= 0: return None
    for _ in range(60):
        mid = (lo+hi)/2
        if F_of(mid) >= 0: hi = mid
        else: lo = mid
    return (lo+hi)/2


variants = [('the published', W)]
if ndead:
    variants.append(('pruned', json.load(gzip.open('/tmp/r434-pruned.json.gz', 'rt'))))
if moves:
    variants.append(('least-frames', json.load(gzip.open('/tmp/r434-least.json.gz', 'rt'))))

for tag, wd in variants:
    H = hist_of(wd)
    mass = sum(r*c for r, c in H.items())
    ident = 8*wd['R'] + 63 + 2*wd['v']*7
    q = price_of(H, wd['v'], wd['R'], 63)
    qs = mp.nstr(q, 8) if q else 'NO-ROOT'
    pc = '%+.2f%%' % (float((q-P111)/P111)*100) if q else ''
    print('%-14s R=%d mass %d/%d hist=%s price %s %s' % (tag, wd['R'], mass, ident, dict(sorted(H.items())), qs, pc))

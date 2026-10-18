"""Entrance-conversion census on E1 (P111-tuned + 1 entrance helper): for each helper h, can it start at the frame of
its first write E (rank e) with D no longer reading it?  Rules (E1 mechanism generalised):
 - every reader r of h with an odd number of reads gets a pre-read r += h placed just before h's first write, at E;
   r must be able to stand at E then (frame nesting with its neighbours in time);
 - targets cannot pre-read in phase A, so h's first write must precede no target read unless the target can pre-read
   in B (first write in B);
 - exact single-column dirt simulation: after A, scatter, B no target may hold h's dirt."""
import gzip, json, sys, collections
import numpy as np
W = json.load(gzip.open(sys.argv[1] if len(sys.argv) > 1 else '/home/user/integer-mult-bounds/research/e8-bit-p111-e1/data/bitE8mut-p111-e1.json.gz', 'rt'))
v = W['v']; R = W['R']; nreg = 2 * v + R
fr = [frozenset(f) for f in W['frames']]
L = np.array(W['lines'], dtype=float)
rk = [int(np.linalg.matrix_rank(L[sorted(f)])) if f else 0 for f in fr]
istarget = lambda r: v <= r < 2 * v
gates = [('A', i, g) for i, g in enumerate(W['A'])] + [('S', 0, None)] + [('B', i, g) for i, g in enumerate(W['B'])]
ret = W['ret']; scat = W['scatter']
# register frame timeline: list of (time index, frame) at each gate it participates in
tl = collections.defaultdict(list)
for t, (ph, i, gt) in enumerate(gates):
    if gt is None: continue
    F, d, srcs = gt
    for r in [d] + srcs: tl[r].append((t, F))
def sub(a, b): return fr[a] <= fr[b]
ent = {int(k): v_ for k, v_ in W['stats'].get('entrance_helpers', {}).items()}
Dread = collections.Counter(s for _, d, srcs in W['D'] for s in srcs)
res = collections.Counter(); cands = []
for h in range(2 * v, nreg):
    if h in ret: res['ret'] += 1; continue
    if (h - 2 * v) in ent: res['already'] += 1; continue
    ev = [(t, gates[t][2]) for t, _ in tl[h]]
    fw = next(((t, gt) for t, gt in ev if gt[1] == h), None)
    if fw is None: res['never written'] += 1; continue
    t0, (E, _, _) = fw
    if gates[t0][0] == 'B': res['first write in B'] += 1
    # readers
    rd = collections.Counter(); treads = []
    for t, gt in ev:
        F, d, srcs = gt
        if h in srcs:
            if istarget(d): treads.append((t, d))
            else: rd[d] += 1
    if any(t < t0 for t, _ in treads): res['target reads before first write?'] += 1; continue
    pre = [r for r, c in rd.items() if c % 2]
    if treads and gates[t0][0] == 'A': res['target reader, first write in A'] += 1; continue
    ok = True
    for r in pre + [d for _, d in treads]:
        # r's frame just before t0 and its next frame after t0
        before = [F for t, F in tl[r] if t < t0]; after = [F for t, F in tl[r] if t > t0]
        fb = before[-1] if before else W['start'][r]
        if not sub(fb, E): ok = False; break
        if after and not sub(E, after[0]): ok = False; break
    if not ok: res['pre-read frame conflict'] += 1; continue
    # dirt simulation of h's column with pre-reads inserted just before t0
    b = [0] * nreg; b[h] = 1
    for t, (ph, i, gt) in enumerate(gates):
        if t == t0:
            for r in pre + [d for _, d in treads]: b[r] ^= 1
        if ph == 'S':
            for tt in range(v):
                for k in scat[tt]: b[v + tt] ^= b[ret[k]]
            continue
        F, d, srcs = gt
        x = 0
        for s in srcs: x ^= b[s]
        b[d] ^= x
    if any(b[v + tt] for tt in range(v)): res['dirt reaches a target'] += 1; continue
    res['CONVERTIBLE'] += 1; cands.append((h, rk[E], len(pre), Dread[h]))
print(dict(res))
print('entrance ranks of convertible helpers', collections.Counter(c[1] for c in cands))
print('examples', cands[:15])
json.dump(cands, open('entcands.json', 'w'))

"""Relaxed entrance census: pre-reads in any gap of the reader's timeline before h's first write (G = reader's frame
before or after the gap, G inside h's first-write frame), h's pre-read frames nested in time; exact dirt simulation."""
import gzip, json, sys, collections, itertools
import numpy as np
W = json.load(gzip.open(sys.argv[1], 'rt'))
v = W['v']; R = W['R']; nreg = 2 * v + R
fr = [frozenset(f) for f in W['frames']]
L = np.array(W['lines'], dtype=float)
rk = [int(np.linalg.matrix_rank(L[sorted(f)])) if f else 0 for f in fr]
istarget = lambda r: v <= r < 2 * v
gates = [('A', i, g) for i, g in enumerate(W['A'])] + [('S', 0, None)] + [('B', i, g) for i, g in enumerate(W['B'])]
tS = len(W['A'])
ret = W['ret']; scat = W['scatter']
tl = collections.defaultdict(list)
for t, (ph, i, gt) in enumerate(gates):
    if gt is None: continue
    F, d, srcs = gt
    for r in [d] + srcs: tl[r].append((t, F))
sub = lambda a, b: fr[a] <= fr[b]
ent = {int(k) for k in W['stats'].get('entrance_helpers', {})}
def simulate(h, pre):            # pre: list of (time, reader) inserted just before gate `time`
    at = collections.defaultdict(list)
    for t, r in pre: at[t].append(r)
    b = [0] * nreg; b[h] = 1
    for t, (ph, i, gt) in enumerate(gates):
        for r in at.get(t, ()): b[r] ^= 1
        if ph == 'S':
            for tt in range(v):
                for k in scat[tt]: b[v + tt] ^= b[ret[k]]
            continue
        F, d, srcs = gt
        x = 0
        for s in srcs: x ^= b[s]
        b[d] ^= x
    return not any(b[v + tt] for tt in range(v))
def try_h(h, tw, Fw):
    ev = [(t, gates[t][2]) for t, _ in tl[h]]
    rd = collections.Counter()
    for t, gt in ev:
        if h in gt[2]: rd[gt[1]] += 1
    need = [r for r, c in rd.items() if c % 2]
    opts = {}
    bad = None
    for r in need:
        o = []
        seq = [(-1, W['start'][r])] + [(t, F) for t, F in tl[r]]
        for (ta, Fa), (tb, Fb) in zip(seq, seq[1:] + [(10**9, None)]):
            lo = ta + 1; hi = min(tb, tw)          # insert just before gate time in [lo, hi]
            if lo > hi: continue
            if istarget(r) and hi <= tS: continue  # targets act only in B
            if istarget(r): lo = max(lo, tS + 1)
            if lo > hi: continue
            for G in ([Fa] + ([Fb] if Fb is not None else [])):
                if sub(G, Fw) and rk[G] > 0 and sub(Fa, G) and (Fb is None or sub(G, Fb)):
                    o.append((hi, G))
        if not o: bad = r; break
        opts[r] = sorted(set(o), key=lambda z: -z[0])
    if bad is not None:
        return None
    # choose latest slot per reader, then check nesting of G in time order
    choice = {r: opts[r][0] for r in need}
    seq = sorted((t, G) for t, G in choice.values())
    if not all(sub(a[1], b[1]) for a, b in zip(seq, seq[1:])):
        return None
    E = seq[0][1] if seq else Fw
    if not simulate(h, [(t, r) for r, (t, G) in choice.items()]):
        return None
    return (E, need)
res = collections.Counter(); cands = []
for h in range(2 * v, nreg):
    if h in ret or (h - 2 * v) in ent: continue
    ev = [(t, gates[t][2]) for t, _ in tl[h]]
    fw = next(((t, gt) for t, gt in ev if gt[1] == h), None)
    if fw is None: continue
    tw, (Fw0, dw, sw) = fw
    # candidate raised first-write frames G: every operand o of the first write can stand at G at time tw
    def window(o):
        before = [F for t, F in tl[o] if t < tw]; after = [F for t, F in tl[o] if t > tw]
        return (before[-1] if before else W['start'][o]), (after[0] if after else None)
    wins = [window(o) for o in [dw] + sw]
    Fws = [G for G in range(len(fr)) if sub(Fw0, G) and all(sub(a, G) and (b is None or sub(G, b)) for a, b in wins)]
    best = None
    for Fw in sorted(Fws, key=lambda G: -rk[G]):
        r_ = try_h(h, tw, Fw)
        if r_ is not None: best = (Fw, r_); break
    if best is None: res['no slot'] += 1; continue
    Fw, (E, need) = best
    res['CONVERTIBLE'] += 1; cands.append((h, rk[E], len(need), rk[Fw0], rk[Fw])); continue
print(dict(res)); print('entrance ranks', collections.Counter(c[1] for c in cands)); print(cands[:20])
json.dump(cands, open('entcands2.json', 'w'))

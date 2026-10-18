"""THE R434-MERGE-TRIAL-v2 (ii19_p111w17.py) — THE 3-RELAYS-THE-DELETE (THE R = 431!!!)

THE v16'-s-FINDINGS: (1) the relays-253/445'-s-srcs (409/369!!) STABLE (0-later-writes (the
A-tail-builds!!!)) -> THE INLINE-SAFE (the x-IDENTICAL!!!); (2) the 466 = THE PURE-SCRATCH
(the A+C-round-trip (the NET-0!!!)) -> THE EMPTY-SRC'-s-PURE-CLIMB (the §205!!); (3) THE D =
THE RE-COMPUTED (the v16'-s-remap-BUG (the old-D'-s-relay-srcs-the-CORRUPTED!!!) -> THE
EMPTY-D-first-pass -> the residues -> the exact-cancel (the w8'-s-(5)!!!)).

THE R = 434 - 3 = 431 (the ~the-+0.4%-expected (the ~the-c-0.001750?! (THE-ABOVE-THE-
FRONTIER (0.001744386!!!)!!!)))
"""
import json, time
from collections import Counter
from fractions import Fraction

w = json.load(open('ii19_pub2_p111-r434.json', 'rt'))
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

V, H = w['v'], w['h']
nreg0 = len(w['start'])
RELAYS = {253: ('inline', 409), 445: ('inline', 369), 466: ('empty', 575)}
DEL = sorted(RELAYS)
shift = {r: sum(1 for dh in DEL if dh < r) for r in range(nreg0 + 1)}
def remap(r):
    assert r not in RELAYS, r
    return r - shift[r]
log('(0) the relays: %s' % RELAYS)

A2 = []
for F, d, srcs in w['A']:
    if d in RELAYS:
        continue                                        # the build-OUT!!
    if d == 444 and 466 in srcs:
        A2.append([F, remap(d), []])                    # the EMPTY-SRC (the pure-climb!!)
        continue
    srcs2 = []
    for s in srcs:
        if s in RELAYS:
            srcs2.append(RELAYS[s][1])                  # the inline!!!
        else:
            srcs2.append(s)
    A2.append([F, remap(d), [remap(s) for s in srcs2]])
B2 = []
for F, d, srcs in w['B']:
    srcs2 = []
    for s in srcs:
        if s in RELAYS:
            srcs2.append(RELAYS[s][1])
        else:
            srcs2.append(s)
    B2.append([F, remap(d), [remap(s) for s in srcs2]])
ret2 = [remap(q) for q in w['ret']]
scat2 = [list(row) for row in w['scatter']]
start2 = [remap(r) for i, r in enumerate(w['start']) if i not in RELAYS]
final2 = [remap(r) for i, r in enumerate(w['final']) if i not in RELAYS]
rf2 = [f for f in w['ret_frames']]
nreg1 = nreg0 - len(DEL)
R2 = w['R'] - len(DEL)
log('(1) the edits: R %d -> %d (the nreg %d)' % (w['R'], R2, nreg1))

def replay(D, A, B, nreg):
    val = [1 << r for r in range(nreg)]
    for F, d, srcs in D:
        for s in srcs: val[d] ^= val[s]
    for F, d, srcs in A:
        x = 0
        for s in srcs: x ^= val[s]
        val[d] ^= x
    for t in range(V):
        for k in scat2[t]: val[V + t] ^= val[ret2[k]]
    for F, d, srcs in B:
        x = 0
        for s in srcs: x ^= val[s]
        val[d] ^= x
    return val

# (2) the SELF-CORRECTING-D (the EMPTY-first!!!)
val = replay([], A2, B2, nreg1)
D2 = []
nline = 0
for t in range(V):
    resid = val[V + t] ^ (1 << (V + t)) ^ (1 << t)
    lr = [b for b in range(V) if (resid >> b) & 1]
    if lr:
        nline += 1
        log('    !!! THE LINE-RESIDUE at t=%d: %s' % (t, lr[:8]))
    rr = [b for b in range(2 * V, nreg1) if (resid >> b) & 1]
    D2.append([0, V + t, rr])
log('(2) THE SELF-CORRECTING-D: the line-residues %d/%d' % (nline, V))
assert nline == 0, 'THE X-BALANCE (the deeper!!)'

# (3) the C (the regenerated (the H4!!))
zg = [[F, d, srcs] for F, d, srcs in A2 + B2 if not (V <= d < 2 * V)]
C2 = [[1, d, list(srcs)] for F, d, srcs in reversed(zg)]
log('(3) the C: %d (the z %d)' % (len(C2), len(zg)))

# (4) the full-replay + the climb-check
def rref(rows, n):
    m = [[Fraction(x) for x in r] for r in rows]; r = 0
    for c in range(n):
        p = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if p is None: continue
        m[r], m[p] = m[p], m[r]; iv = 1 / m[r][c]; m[r] = [x * iv for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]; m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
    return m[:r]
fr = [rref(F, H) for F in w['frames']]
dims = [len(F) for F in fr]
_sub = {}
def sub(a, b):
    if (a, b) not in _sub:
        _sub[(a, b)] = len(rref(list(fr[a]) + list(fr[b]), H)) == dims[b]
    return _sub[(a, b)]
cur = list(start2)
val = [1 << r for r in range(nreg1)]
bad_climbs = []
def climb(r, F, phase, gi):
    if cur[r] == F: return
    if not (sub(cur[r], F) and dims[F] > dims[cur[r]]):
        bad_climbs.append((phase, gi, r, cur[r], F, dims[cur[r]], dims[F]))
    cur[r] = F
def run(gates, phase):
    for gi, (F, d, srcs) in enumerate(gates):
        for r in [d] + srcs: climb(r, F, phase, gi)
        for s in srcs: val[d] ^= val[s]
run(D2, 'D')
run(A2, 'A')
for t in range(V):
    for k in scat2[t]: val[V + t] ^= val[ret2[k]]
run(B2, 'B')
run(C2, 'C')
for r in range(nreg1): climb(r, final2[r], 'FINAL', -1)
bad = [r for r in range(nreg1)
       if val[r] != ((1 << r) ^ (1 << (r - V)) if V <= r < 2 * V else 1 << r)]
log('(4) THE FULL-REPLAY: bad-vals %d/%d | illegal-climbs %d' % (len(bad), nreg1, len(bad_climbs)))
for b in bad[:5]: log('    !!! reg %d' % b)
for b in bad_climbs[:8]:
    log('    !!! [%s] gate %d reg %d: %d(d%d) -> %d(d%d)' % (b[0], b[1], b[2], b[3], b[5], b[4], b[6]))

# (5) the emission
word = dict(w)
word.update(R=R2, start=start2, final=final2, D=D2, A=A2, B=B2, C=C2,
            ret=ret2, ret_frames=rf2, scatter=scat2)
json.dump(word, open('ii19_r431.json', 'w'))
log('(5) EMITTED (ii19_r431.json): R = %d' % R2)
log('DONE')

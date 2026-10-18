"""THE R434-MERGE-TRIAL (ii19_p111w16.py) — THE RELAYS'-INLINE (THE R = 431?!)

THE FOUND-RELAYS (the w15-census!!!): the 253/445/466: the 1-build-1-read (the pure!!
(the ~the-2072-builds-ALL-single-src (§2057's-law!!!))) — THE INLINE: the reader'-s-srcs
[...h...] -> [...s...] (the h'-s-own-build'-s-src!!!) | the build-gate-OUT | the C'-s-the
reversal-OUT | the REGISTER-the-DELETE (the ~the-REMAP-the-the-the-ABOVE'-s-the-SHIFT!!!)

THE BIT-BALANCE (the self-correcting-D!!): the h'-s-SELF-BIT (the delivered-to-the-readers
(the ~the-the-OLD'-s-the-vals!!!)) -> the ~the-THE-MISSING-the-the-DETECTION (the ~the-the-
replay'-s-the-residues!!) -> the ~the-THE-COMPUTED-D (the ~the-the-the-D-gates'-the-srcs
(the ~the-the-the-w8'-s-(5) (the ~the-the-the-nat19'-s-the-LAW!!!))'-s-THE-the-RE-RUN!!!)

THE VERIFICATION-LADDER: (1) the algebra (the replay'-s-the-finals!!); (2) the climbs (the
gcheck-exact!!); (3) THE GCHECK (the real!!!); (4) THE PRICE (the ~the-+0.13%/reg (the ~the-
the-3-regs: the ~the-+0.4% (the ~the-the-the-c-0.001750?! (THE-ABOVE-THE-FRONTIER?!))))
"""
import json, time
from collections import Counter
from fractions import Fraction

w = json.load(open('ii19_pub2_p111-r434.json', 'rt'))
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

V, H = w['v'], w['h']
nreg0 = len(w['start'])
X = (1 << V) - 1

# ============ (0) THE RELAY-STRUCTURE (the find-the-s-the-reader-the-ALL!!!) ============
RELAYS = {}
for h in [253, 445, 466]:
    bg = [g for g in w['A'] if g[1] == h]
    assert len(bg) == 1, (h, len(bg))
    F, d, srcs = bg[0]
    assert len(srcs) == 1
    s = srcs[0]
    # the readers (the A + the B (the C = the-the-reversals!!!))
    readers = [(ph, gi, g) for ph in ['A', 'B'] for gi, g in enumerate(w[ph]) if h in g[2]]
    log('THE RELAY %d: built [%d, %d, [%d]] | the readers %s' % (
        h, F, d, s, [(ph, gi, g[1]) for ph, gi, g in readers]))
    RELAYS[h] = (s, readers)

# ============ (1) THE EDITS ============
DEL = sorted(RELV := set(RELAYS))
newidx = {r: r - sum(1 for dh in DEL if dh < r) for r in range(nreg0)}
def remap(r): return newidx.get(r, r - sum(1 for dh in DEL if dh < r))
A2 = []
for F, d, srcs in w['A']:
    if d in RELV:
        continue                       # the relay'-s-build: OUT!!
    srcs2 = []
    for s in srcs:
        if s in RELV:
            srcs2.append(RELAYS[s][0])  # the inline!!!
        else:
            srcs2.append(s)
    A2.append([F, remap(d), [remap(s) for s in srcs2]])
B2 = []
for F, d, srcs in w['B']:
    srcs2 = []
    for s in srcs:
        if s in RELV:
            srcs2.append(RELAYS[s][0])
        else:
            srcs2.append(s)
    B2.append([F, remap(d), [remap(s) for s in srcs2]])
ret2 = [remap(q) for q in w['ret'] if q not in RELV]
scat2 = [[k for k in row] for row in w['scatter']]
start2 = [remap(r) for i, r in enumerate(w['start']) if i not in RELV]
final2 = [remap(r) for i, r in enumerate(w['final']) if i not in RELV]
rf2 = [remap(f) for f in w['ret_frames']]
nreg1 = nreg0 - len(DEL)
R2 = w['R'] - len(DEL)
log('(1) THE EDITS: the %d-registers-deleted (the nreg %d -> %d (the R %d -> %d!!))' % (
    len(DEL), nreg0, nreg1, w['R'], R2))

# ============ (2) THE SELF-CORRECTING-D (the the-the-RESIDUE-the-DETECT-the-the-the-RE-COMPUTE!!!) ============
def replay_vals(D, A, B, scat, retl, nreg):
    val = [1 << r for r in range(nreg)]
    for F, d, srcs in D:
        for s in srcs: val[d] ^= val[s]
    for F, d, srcs in A:
        x = 0
        for s in srcs: x ^= val[s]
        val[d] ^= x
    for t in range(V):
        for k in scat[t]: val[V + t] ^= val[retl[k]]
    for F, d, srcs in B:
        x = 0
        for s in srcs: x ^= val[s]
        val[d] ^= x
    return val
# the FIRST-pass: the D-OLD (the ~the-the-residues-the-the-DETECTED!!!)
D0 = [[F, remap(d), [remap(s) for s in srcs]] for F, d, srcs in w['D']]
val = replay_vals(D0, A2, B2, scat2, ret2, nreg1)
resid_reg = 0
D2 = []
nline = 0
for t in range(V):
    resid = val[V + t] ^ (1 << (V + t)) ^ (1 << t)
    lr = [b for b in range(V) if (resid >> b) & 1]
    if lr:
        nline += 1
        log('    !!! THE LINE-RESIDUE at t=%d: %s (the x-balance (the deeper-check-the-NEEDED!!))' % (t, lr[:6]))
    rr = [b for b in range(2 * V, nreg1) if (resid >> b) & 1]
    resid_reg += len(rr)
    D2.append([0, V + t, rr])
log('(2) THE SELF-CORRECTING-D: the line-residues %d/%d | the register-residue-bits %d' % (
    nline, V, resid_reg))
assert nline == 0, 'THE X-BALANCE-BROKEN (the deeper-repair-the-NEEDED!!)'

# ============ (3) THE C (the H4 (the NEW-z'-s-the-REVERSAL!!!)) ============
zg = [[F, d, srcs] for F, d, srcs in A2 + B2 if not (V <= d < 2 * V)]
C2 = [[1, d, list(srcs)] for F, d, srcs in reversed(zg)]
log('(3) THE C: %d (the z-gates %d!!)' % (len(C2), len(zg)))

# ============ (4) THE FULL-REPLAY + THE CLIMB-CHECK (the gcheck-exact!!!) ============
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
log('(4) THE FULL-REPLAY: the bad-vals %d/%d | the illegal-climbs %d' % (len(bad), nreg1, len(bad_climbs)))
for b in bad[:5]: log('    !!! the reg %d' % b)
for b in bad_climbs[:8]:
    log('    !!! [%s] gate %d reg %d: %d(d%d) -> %d(d%d)' % (b[0], b[1], b[2], b[3], b[5], b[4], b[6]))

# ============ (5) THE EMISSION ============
word = dict(w)
word.update(R=R2, start=start2, final=final2, D=D2, A=A2, B=B2, C=C2,
            ret=ret2, ret_frames=rf2, scatter=scat2)
json.dump(word, open('ii19_r434_m.json', 'w'))
log('(5) THE WORD EMITTED (ii19_r434_m.json): R = %d' % R2)
log('    THE GCHECK: /Users/dayssky/.venv/bin/python '
    'research/lorentzian-frame-cell-handoff/code/tword/gcheck.py '
    'research/i13-partition/ii19_r434_m.json --price')
log('DONE — THE MERGE-TRIAL!!!')

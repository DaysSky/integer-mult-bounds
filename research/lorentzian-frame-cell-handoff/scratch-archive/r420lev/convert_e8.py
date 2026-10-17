"""Entrance-rank conversion analysis on a bitGen/1+mut word (I_{11,1} block word).
For each helper h (not read by targets, not retained), try entrance frame S = frame of h at its first WRITE (E_h).
Conditions (exact, timeline replay of D, A, scatter, B):
  - every helper reader q of h ends with even dirt(h) parity after adding at most one pure read;
  - the pure read is inserted at a time tau < t_h (h's first write) in q's timeline where q's frame f_q(tau) is a
    subframe of S and q's next frame (at its next gate after tau) contains S; h's frames before t_h all lie in S;
  - no register reads q between tau and q's first full read of h (no dirt leak).
Reports the number of convertible helpers and their entrance ranks."""
import gzip, json, sys
from fractions import Fraction as Fr
from collections import defaultdict, Counter
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/tword')
w = json.load(gzip.open(sys.argv[1], 'rt'))
h, v, R = w['h'], w['v'], w['R']
import numpy as np
LN = np.array(w['lines'], dtype=float)
FS = [frozenset(F) for F in w['frames']]
dims = [int(np.linalg.matrix_rank(LN[sorted(F)])) if F else 0 for F in FS]
def sub(a, b): return FS[a] <= FS[b]
nreg = 2*v + R
# timeline: list of (phase, idx, F, d, srcs)
TL = []
for ph in ('D', 'A'):
    for i, (F, d, s) in enumerate(w[ph]): TL.append((ph, i, F, d, s))
TL.append(('S', 0, None, None, None))
for i, (F, d, s) in enumerate(w['B']): TL.append(('B', i, F, d, s))
# per register: list of (time, frame after gate, role) ; frames start at start[]
start = w['start']
frames_at = defaultdict(list)     # reg -> [(time, frame)]
for r in range(nreg): frames_at[r].append((-1, start[r]))
reads_of = defaultdict(list)      # h -> [(time, reader)]
first_write = {}
reads_by = defaultdict(list)      # q -> times q is READ (as src) by anyone
for t, (ph, i, F, d, s) in enumerate(TL):
    if ph == 'S': continue
    for r in [d] + s:
        if frames_at[r][-1][1] != F: frames_at[r].append((t, F))
    if d not in first_write: first_write[d] = t
    for x in s:
        reads_of[x].append((t, d)); reads_by[x].append(t)
def frame_at(r, t):
    f = start[r]
    for tt, F in frames_at[r]:
        if tt <= t: f = F
        else: break
    return f
def next_frame_after(r, t):
    for tt, F in frames_at[r]:
        if tt > t: return tt, F
    return None, None
ret = set(w['ret'])
targets = set(range(v, 2*v))
conv = Counter(); fail = Counter(); total = 0
for hh in range(2*v, nreg):
    if hh in ret: fail['retained'] += 1; continue
    rd = reads_of[hh]
    if any(q in targets and TL[t][0] != 'D' for t, q in rd): fail['read by target'] += 1; continue
    if any(TL[t][0] == 'D' for t, q in rd): pass   # D reads are removed by the conversion
    th = first_write.get(hh)
    if th is None: fail['never written'] += 1; continue
    S = TL[th][2]                                   # entrance frame = frame of its first write gate
    if dims[S] == 0: fail['first write at frame 0'] += 1; continue
    # h's frames before t_h must lie in S (they are pushes by pure reads); S itself is its frame at t_h
    ok = all(sub(F, S) for tt, F in frames_at[hh] if 0 <= tt < th)
    if not ok: fail['pre-write frame outside S'] += 1; continue
    good = True
    for q in set(q for _, q in rd if TL[_][0] != 'D'):
        if q < v:  # source reader (mutable source): treat like helper reader
            pass
        qreads = [t for t, qq in rd if qq == q and TL[t][0] != 'D']
        pure = [t for t in qreads if t < th]; full = [t for t in qreads if t > th]
        if (len(pure) + len(full)) % 2 == 0: continue        # already even
        if not full: good = False; break
        tf = full[0]
        # find tau < th in q's timeline with frame_at(q, tau) subset S and next frame contains S, no reads of q in (tau, tf)
        cand = False
        times = sorted(set([-1] + [tt for tt, F in frames_at[q] if tt < th]))
        for tau in reversed(times):
            fq = frame_at(q, tau)
            if not sub(fq, S): continue
            nt, nf = next_frame_after(q, tau)
            if nf is not None and not sub(S, nf): continue
            if any(tau < x < tf for x in reads_by[q]): continue
            cand = True; break
        if not cand: good = False; break
    if good:
        conv[dims[S]] += 1
    else:
        fail['reader timing/frames'] += 1
print('helpers', R, 'convertible by entrance rank:', dict(sorted(conv.items())), 'total', sum(conv.values()))
print('failures:', dict(fail))

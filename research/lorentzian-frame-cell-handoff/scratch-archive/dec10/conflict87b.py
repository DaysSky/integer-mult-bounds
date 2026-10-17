"""Conflict anatomy for P110 (line 87 punctured, copy of total 66 read at <87> by its 62 readers right after the
scatter).  For every phase-B gate, decide its frame must contain 87 (forced) and find conflicts; for each conflict
(a target not orthogonal to 87 meeting a forced register r), test whether the read can be moved before r was forced:
no write to r (and to the other operands) between the forcing gate and the conflicting gate."""
import gzip, json, sys, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
w = json.load(gzip.open('/home/user/integer-mult-bounds/research/e8-bit-p111-tuned/tune/bitE8mut-p111-tuned.json.gz'))
v = w['v']; L = np.array(w['lines'], float); GI = np.array(e8.GI)
P = set(w['punctured']); live = [t for t in range(120) if t not in P]
x87 = np.linalg.lstsq(L, 2 * GI[87, live].astype(float), rcond=None)[0]; i87 = live.index(87)
frames = w['frames']; fc = {}
def has87(f):
    if f not in fc:
        lab = frames[f]
        fc[f] = bool(lab) and np.linalg.matrix_rank(np.vstack([L[lab], x87])) == np.linalg.matrix_rank(L[lab])
    return fc[f]
orth = set(i for i in range(v) if GI[87, live[i]] == 0 and i != i87)
B = [(g[0], g[1], g[2] if isinstance(g[2], list) else [g[2]]) for g in w['B']]
istarget = lambda r: v <= r < 2 * v
ok_t = lambda r: (not istarget(r)) or ((r - v) in orth)
forced_at = {v + t: -1 for t in orth}       # register -> index of gate at which it became forced (-1: at the cut)
conf = []
for k, (f, dst, srcs) in enumerate(B):
    regs = [dst] + srcs
    need = has87(f) or any(r in forced_at for r in regs)
    if need:
        bad = [r for r in regs if not ok_t(r)]
        if bad and not has87(f):
            conf.append((k, bad, [r for r in regs if r in forced_at]))
        for r in regs:
            if ok_t(r) and r not in forced_at: forced_at[r] = k
writes = {}
for k, (f, dst, srcs) in enumerate(B): writes.setdefault(dst, []).append(k)
movable = 0
for k, bad, fr in conf:
    # the conflicting gate reads/writes forced registers fr; can it move to just before the earliest forcing of fr?
    f, dst, srcs = B[k]
    earliest = min(forced_at[r] for r in fr)
    clean = all(not any(earliest < kk < k for kk in writes.get(r, [])) for r in [dst] + srcs)
    movable += clean
print('conflicts', len(conf), 'movable before forcing (no intervening writes):', movable)
# refined: r unchanged between earliest and k (only writes to r matter), and the target's own gates in between have
# frames containing the moved gate's frame (nesting preserved)
def lab(f): return frozenset(frames[f])
def sub(f, g):
    if not frames[f]: return True
    if not frames[g]: return False
    M = L[frames[g]]; return np.linalg.matrix_rank(np.vstack([M, L[frames[f]]])) == np.linalg.matrix_rank(M)
mv2 = 0; reasons = {'r written': 0, 'nesting': 0}
for k, bad, fr in conf:
    f, dst, srcs = B[k]
    earliest = min(forced_at[r] for r in fr if r != dst) if any(r != dst for r in fr) else -1
    if any(any(earliest < kk < k for kk in writes.get(r, [])) for r in srcs):
        reasons['r written'] += 1; continue
    tg = dst
    between = [kk for kk in range(max(earliest, 0), k) if B[kk][1] == tg or tg in B[kk][2]]
    if all(sub(f, B[kk][0]) for kk in between): mv2 += 1
    else: reasons['nesting'] += 1
print('refined movable', mv2, reasons)

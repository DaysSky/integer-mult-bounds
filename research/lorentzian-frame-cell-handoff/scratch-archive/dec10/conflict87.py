"""On the P111-tuned word with line 87 punctured: readers of total 66 (targets orthogonal to 87) read the copy at <87>
right after the scatter, so every later gate of theirs needs 87 in its frame.  Propagate the forced frame growth to
z registers and count conflicts (a forced register later meeting a target not orthogonal to 87)."""
import gzip, json, sys, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
w = json.load(gzip.open('/home/user/integer-mult-bounds/research/e8-bit-p111-tuned/tune/bitE8mut-p111-tuned.json.gz'))
v = w['v']; L = np.array(w['lines'], float); GI = np.array(e8.GI)
P = set(w['punctured']); live = [t for t in range(120) if t not in P]
g87 = GI[87, live].astype(float); x87 = np.linalg.lstsq(L, 2 * g87, rcond=None)[0]
i87 = live.index(87)
frames = w['frames']
fcache = {}
def has87(f):
    if f not in fcache:
        lab = frames[f]
        if not lab: fcache[f] = False
        else:
            M = L[lab]; fcache[f] = np.linalg.matrix_rank(np.vstack([M, x87])) == np.linalg.matrix_rank(M)
    return fcache[f]
orth87 = set(i for i in range(v) if GI[87, live[i]] == 0 and i != i87)   # readers (live, excluding 87 itself)
# phase B order; registers: sources 0..v-1, targets v..2v-1, helpers >= 2v ; gate = [frame, dst, srcs]
forced = set()          # registers whose frame now contains 87
conf_t = set(); conf_g = 0; enlarged = 0
for t in orth87: forced.add(v + t)
for g in w['B']:
    f, dst, srcs = g[0], g[1], g[2] if isinstance(g[2], list) else [g[2]]
    regs = [dst] + srcs
    tg = [r for r in regs if v <= r < 2 * v]
    need = has87(f) or any(r in forced for r in regs)
    if need and not has87(f):
        # gate frame must be enlarged by 87: every target operand must be orthogonal to 87 (and not 87 itself)
        bad = [r - v for r in tg if (r - v) not in orth87]
        if bad: conf_g += 1; conf_t.update(bad)
        enlarged += 1
        for r in regs:
            if not (v <= r < 2 * v and (r - v) not in orth87): forced.add(r)
    elif has87(f):
        for r in regs: forced.add(r) if not (v <= r < 2 * v and (r - v) not in orth87) else None
print('phase-B gates', len(w['B']), 'enlarged by 87:', enlarged, 'conflicting gates:', conf_g, 'targets hit:', len(conf_t))
print('z registers forced to contain 87:', len([r for r in forced if r < v or r >= 2 * v]))

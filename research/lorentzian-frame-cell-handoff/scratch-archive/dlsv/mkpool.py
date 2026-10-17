"""Pool of w-perp vectors of I_{n,1} (w = (1^n;3)) with |x_i| <= XM, |y| <= YM, norms in NORMS, written as text for dlsv."""
import itertools, sys, numpy as np
n, XM, YM = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); NORMS = set(int(a) for a in sys.argv[4].split(','))
out = sys.argv[5]
vals = list(range(-XM, XM + 1)); vecs = set()
def rec(i, rem, cur):
    if i == len(vals):
        if rem == 0: yield cur
        return
    for c in range(rem + 1): yield from rec(i + 1, rem - c, cur + [c])
for counts in rec(0, n, []):
    s = sum(c*v for c, v in zip(counts, vals)); q = sum(c*v*v for c, v in zip(counts, vals))
    if s % 3: continue
    y = s // 3
    if abs(y) > YM or (q - y*y) not in NORMS: continue
    base = []
    for c, v in zip(counts, vals): base += [v]*c
    for perm in set(itertools.permutations(base)):
        v_ = tuple(perm) + (y,); nv = tuple(-t for t in v_); vecs.add(max(v_, nv))
V = sorted(vecs)
with open(out, 'w') as f:
    f.write('%d %d\n' % (len(V), n + 1))
    for v in V: f.write(' '.join(map(str, v)) + '\n')
np.save(out + '.npy', np.array(V))
print(out, len(V))

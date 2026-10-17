"""K = 3: every canonical sequence, splits <= 3 (any per time), exhaustive over F_2; price every feasible layout
(with banks).  Reports the best."""
import itertools, subprocess, re, os, sys
sys.path.insert(0, '../k3'); sys.path.insert(0, '../sched2')
import k3slots as KS
from splitp import slots
K, s = 3, 7
best = []
env = dict(os.environ, PERTIME='2')
for sq in itertools.product(range(K), repeat=s):
    firsts = []
    for x in sq:
        if x not in firsts: firsts.append(x)
    if firsts != list(range(K)): continue
    out = subprocess.run(['./splitc5', str(K), str(s), '3'] + [str(x) for x in sq], capture_output=True, text=True, env=env).stdout.strip()
    if not out.startswith('FEASIBLE'): continue
    for s_ in re.findall(r'\[([^\]]*)\]', out):
        sp = tuple((int(a), int(b)) for a, b in re.findall(r'\((\d),(\d)\)', s_))
        sl = slots(list(sq), sp)
        best.append((len(sl), sl, sq, sp))
best.sort()
seen = {}
for n, sl, sq, sp in best:
    seen.setdefault(sl, (sq, sp))
rows = []
for sl, (sq, sp) in seen.items():
    c, over = KS.price_slots(KS.tuned, 111, 8, 439, s, K, list(sl))
    rows.append((float((c / KS.ref - 1) * 100) if c else -999, len(sl), sl, sq, sp))
rows.sort(reverse=True)
print('K=3 feasible layouts (distinct multisets):', len(rows), '; min stretches', min(r[1] for r in rows))
for r in rows[:10]: print('%+.3f%%' % r[0], 'stretches', r[1], r[2], r[3], r[4])

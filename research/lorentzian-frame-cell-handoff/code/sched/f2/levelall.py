import itertools, sys, json, time
from levelp import run
K = int(sys.argv[1]); L = int(sys.argv[2]); s = 2 * K + 1
def comps(total, parts, mx):
    if parts == 0:
        if total == 0: yield ()
        return
    for x in range(1, min(mx, total - (parts - 1)) + 1):
        for rest in comps(total - x, parts - 1, mx): yield (x,) + rest
found = []; n = 0; skipped = 0; t = time.time()
for sizes in comps(s, L, K):
    if sizes[0] != 1: continue
    choices = [list(itertools.combinations(range(K), k)) for k in sizes]
    for prog in itertools.product(*choices):
        flat = [p for lv in prog for p in lv]
        firsts = []
        for p in flat:
            if p not in firsts: firsts.append(p)
        if firsts != list(range(K)): continue
        # canonical within level: sorted already (combinations)
        n += 1
        r = run([list(x) for x in prog])
        if r == 'skip': skipped += 1; continue
        if r: found.append(prog); print('FEASIBLE', prog, flush=True)
print('K', K, 'L', L, 'programs', n, 'skipped(set>3)', skipped, 'feasible', len(found), '%.0fs' % (time.time() - t), flush=True)

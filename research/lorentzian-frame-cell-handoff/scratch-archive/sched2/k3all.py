import itertools, time
from feas import feasible
K = int(__import__('sys').argv[1]); s = 2 * K + 1
for sq in itertools.product(range(K), repeat=s):
    firsts = []
    for p in sq:
        if p not in firsts: firsts.append(p)
    if firsts != list(range(K)): continue
    t = time.time()
    f = feasible(list(sq), 1, limit_states=20000)
    runs = max(len(list(g)) for _, g in itertools.groupby(sq))
    print(sq, 'maxrun', runs, 'FEASIBLE ' + f[0][0] if f else 'none', '%.1fs' % (time.time() - t), flush=True)

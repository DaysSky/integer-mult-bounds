import pickle, sys, itertools, numpy as np
from symsat import solve, verify, cyclic, elems
classes = pickle.load(open('classes.pkl', 'rb'))
which = [int(x) for x in sys.argv[1].split(',')]   # class indices
budgets = [int(x) for x in sys.argv[2].split(',')]
tlim = float(sys.argv[3])
def multisets(o, T, qmax=6):
    out = []
    for q in range(max(1, -(-10 // o)), qmax + 1):
        for cs in itertools.combinations_with_replacement([1, 2, 3, 4], q):
            if o * sum(cs) <= T: out.append(list(cs))
    return out
for ci in which:
    o, size, rep, fixed = classes[ci]
    H = cyclic(elems[rep])
    found = None
    for T in budgets:
        cands = [cs for cs in multisets(o, T) if o * sum(cs) > T - (budgets[1] - budgets[0] if len(budgets) > 1 else T)] if found is None else []
        for cs in cands:
            ok, res, dt = solve(H, cs, tlim)
            tag = {True: 'SAT', False: 'UNSAT', None: 'TIMEOUT'}[ok]
            line = 'class %d (order %d, fixed %d) costs %s total<=%d -> %s %.1fs' % (ci, o, fixed, cs, o * sum(cs), tag, dt)
            if ok:
                okv, cost, nu = verify(H, *res)
                line += ' | verify %s true cost %d rects %d' % (okv, cost, nu)
                pickle.dump((ci, cs, [list(map(int, h)) for h in H], res), open('symdrive_c%d_%s.pkl' % (ci, '-'.join(map(str, cs))), 'wb'))
                found = (T, cost)
            print(line, flush=True)
            if found: break
        if found: break
    print('CLASS %d DONE best' % ci, found, flush=True)

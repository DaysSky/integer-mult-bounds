"""Driver for c/orbmeet: per-flat number of S11-orbit members of Y meeting the flat, and the orbit size."""
import sys, subprocess, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V
EXE = '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/declp/c/orbmeet'
def masks(cl):
    m = [0, 0, 0, 0]
    for i in cl: m[i >> 6] |= 1 << (i & 63)
    return m
def orbit_meet(Y, flatlist):
    lines = [sorted(g.supp[y]) for y in Y]
    inp = [str(len(Y))] + ['%d %s' % (len(l), ' '.join(map(str, l))) for l in lines]
    inp += ['%d %s' % (len(g.supp[x]), ' '.join(map(str, sorted(g.supp[x])))) for x in range(V)]
    inp += [str(len(flatlist))] + [' '.join(map(str, masks(cl))) for cl in flatlist]
    out = subprocess.run([EXE], input='\n'.join(inp) + '\n', capture_output=True, text=True, check=True).stdout.split()
    nperm, stab = int(out[0]), int(out[1]); cnts = [int(x) for x in out[2:]]
    assert nperm == 39916800 and all(c % stab == 0 for c in cnts)
    return nperm // stab, [c // stab for c in cnts]
if __name__ == '__main__':
    import pickle, flats
    D = '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/declp/'
    orb = pickle.load(open(D + 'corbits.pkl', 'rb'))
    test = [flats.closure([x for x in range(V) if (0 in g.supp[x]) == (g.kind[x] == 'T')])[0],
            flats.closure([s for s in range(V) if s != 55 and g.G[s, 55] == 0])[0],
            flats.closure([x for x in range(V) if set(g.supp[x]) <= set(range(8))])[0], (0,), (0, 55)]
    for k, v in orb.items():
        if len(v) not in (11, 495): continue
        size, cnts = orbit_meet(v[0], test)
        direct = [sum(1 for c in v if set(c) & set(cl)) for cl in test]
        print('orbit', len(v), 'C size', size, 'C counts', cnts, 'direct', direct, 'OK' if (size == len(v) and cnts == direct) else 'MISMATCH', flush=True)

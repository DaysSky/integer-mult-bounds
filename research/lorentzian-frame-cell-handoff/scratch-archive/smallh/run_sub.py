from subsat import run
from screen import dedupe_lines
import itertools, numpy as np, sys
h = int(sys.argv[1]); a = None if sys.argv[2] == 'none' else int(sys.argv[2]); sig = [int(x) for x in sys.argv[3].split(',')]
vals = tuple(int(x) for x in sys.argv[4].split(','))
F = np.diag(sig)
L = dedupe_lines(list(itertools.product(vals, repeat=h)), F)
print('candidates', len(L), flush=True)
for c in range(int(sys.argv[5]), int(sys.argv[6]) + 1):
    N = c * h + 1   # x_proxy < 1
    r = run(L, F, c, N, a=a, tlimit=int(sys.argv[7]))
    if r['res'] == 'SAT':
        print('  ports', r['ports'])

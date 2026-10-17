"""Single-BFS version of feasp.py: branch on F/R inside the search; state = matrix over F_p.  Exhaustive and rigorous
as a necessary test for integer schedules (reduction mod p), and exact for F_2 schedules."""
import sys, json
from feasp import make
def feasible_p2(seq, p, witness=False):
    K = max(seq) + 1; s = len(seq); n = 2 * K
    SL, pot, loc, junc = make(p, K)
    I = tuple(tuple(int(i == j) for j in range(n)) for i in range(n))
    layer = {loc(I, seq[0], False): None}            # first local F (R is the mirror image)
    hist = [layer]; P = 2 * K
    for b in range(1, s):
        nl = {}
        for M in layer:
            opts = [(M, None)] if seq[b] == seq[b - 1] else \
                   [(junc(M, seq[b - 1], seq[b], A, B), (A, B)) for A in SL for B in SL]
            for M1, j in opts:
                for rev in (False, True):
                    M2 = loc(M1, seq[b], rev)
                    if M2 in nl: continue
                    if pot(M2) != P - 1: continue
                    nl[M2] = (M, j, rev)
        P -= 1; layer = nl; hist.append(layer)
        if not layer: return None
    if not witness: return True
    M = next(iter(layer)); path = []
    for b in range(s - 1, 0, -1):
        prev, j, rev = hist[b][M]; path.append((j, 'R' if rev else 'F')); M = prev
    return list(reversed(path))
if __name__ == '__main__':
    p = int(sys.argv[1]); seq = json.loads(sys.argv[2])
    r = feasible_p2(seq, p, witness=True)
    print(seq, 'p', p, 'FEASIBLE' if r else 'INFEASIBLE', r if r else '')

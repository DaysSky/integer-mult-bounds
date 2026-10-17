# Small root systems: lines, Gram; exact minimum total row weight of a rank-k decoder (SAT, B = U W^T over F2,
# B_tt = 1, B_ts = 0 on non-orthogonal pairs), then the cheapest generating set of its row space (greedy over the
# code's codewords by frame rank = real rank of the codeword's lines).  Reports (k, load, cost, x, density).
import sys, itertools, numpy as np, time
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
def roots(name):
    R = []
    if name.startswith('A'):
        n = int(name[1:]); 
        for i, j in itertools.combinations(range(n + 1), 2):
            v = [0] * (n + 1); v[i] = 1; v[j] = -1; R.append(v)
    elif name.startswith('D'):
        n = int(name[1:])
        for i, j in itertools.combinations(range(n), 2):
            for s in (1, -1):
                v = [0] * n; v[i] = 1; v[j] = s; R.append(v)
    elif name == 'E6' or name == 'E7' or name == 'E8':
        # E8 roots, then E7 = roots orthogonal to a root, E6 = orthogonal to an A2
        E = []
        for i, j in itertools.combinations(range(8), 2):
            for s1 in (1, -1):
                for s2 in (1, -1):
                    v = [0] * 8; v[i] = s1; v[j] = s2; E.append(tuple(2 * x for x in v))
        for signs in itertools.product((1, -1), repeat=8):
            if signs.count(-1) % 2 == 0: E.append(tuple(signs))
        lines = []
        for v in E:
            if tuple(-x for x in v) not in lines: lines.append(v)
        ip = lambda a, b: sum(x * y for x, y in zip(a, b)) // 4
        if name == 'E8': R = lines
        elif name == 'E7':
            a = lines[0]; R = [l for l in lines if ip(l, a) == 0]
        else:
            a = lines[0]; b = next(l for l in lines if abs(ip(l, a)) == 1)
            R = [l for l in lines if ip(l, a) == 0 and ip(l, b) == 0]
        return [list(r) for r in R], 4
    return R, 1
def gram(R, sc):
    A = np.array(R); return (A @ A.T) // sc, A
def min_load(G, k, cap_total, timeout=120):
    v = len(G); pool = IDPool()
    U = [[pool.id(('u', t, j)) for j in range(k)] for t in range(v)]
    W = [[pool.id(('w', t, j)) for j in range(k)] for t in range(v)]
    cl = []
    def AND(a, b):
        x = pool.id(('and', a, b)); cl.extend([[-x, a], [-x, b], [x, -a, -b]]); return x
    def XOR(lits):
        acc = lits[0]
        for l in lits[1:]:
            x = pool.id(('xor', acc, l)); cl.extend([[-x, acc, l], [-x, -acc, -l], [x, -acc, l], [x, acc, -l]]); acc = x
        return acc
    Bv = {}
    for t in range(v):
        for s in range(v):
            if s != t and G[t, s] != 0: Bv[(t, s)] = None
    rowlits = []
    for t in range(v):
        for s in range(v):
            b = XOR([AND(U[t][j], W[s][j]) for j in range(k)])
            if s == t: cl.append([b])
            elif G[t, s] != 0: cl.append([-b])
            else: rowlits.append(b)
    if cap_total is not None:
        enc = CardEnc.atmost(lits=rowlits, bound=cap_total, vpool=pool, encoding=EncType.seqcounter)
        cl.extend(enc.clauses)
    s = Cadical153(bootstrap_with=cl)
    ok = s.solve()
    if not ok: return None
    m = set(l for l in s.get_model() if l > 0)
    Uv = np.array([[1 if U[t][j] in m else 0 for j in range(k)] for t in range(v)])
    Wv = np.array([[1 if W[t][j] in m else 0 for j in range(k)] for t in range(v)])
    return (Uv @ Wv.T) % 2
def code_cost(B, A):
    # cheapest generating set of the row space: greedy over all codewords (2^rank), weight = real rank of lines
    v = len(B); rows = [int(''.join(map(str, B[t][::-1])), 2) for t in range(v)]
    piv = {}; basis = []
    for r in rows:
        x = r
        while x:
            hb = x.bit_length() - 1
            if hb in piv: x ^= piv[hb]
            else: piv[hb] = x; basis.append(r); break
    k = len(basis); words = []; c = 0
    for i in range(1, 1 << k):
        c ^= basis[(i & -i).bit_length() - 1]
        idx = [s for s in range(v) if (c >> s) & 1]
        words.append((np.linalg.matrix_rank(A[idx].astype(float)), c))
    words.sort(); piv = {}; cost = 0; n = 0
    for r, c in words:
        x = c
        while x:
            hb = x.bit_length() - 1
            if hb in piv: x ^= piv[hb]
            else: piv[hb] = x; cost += r; n += 1; break
        if n == k: break
    return k, cost
if __name__ == '__main__':
    name = sys.argv[1]; R, sc = roots(name); G, A = gram(R, sc); v = len(R); h = np.linalg.matrix_rank(A.astype(float))
    deg = [int((G[t] == 0).sum()) for t in range(v)]
    print(name, 'v', v, 'h', h, '|R(t)|', sorted(set(deg)), flush=True)
    for k in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
        lo_cap = None; best = None
        B = min_load(G, k, None)
        if B is None: print('  k', k, 'no decoder'); continue
        load = int(B.sum()) - v
        # tighten total load by bisection
        hi = load; lo = 0
        while lo < hi:
            mid = (lo + hi) // 2
            Bm = min_load(G, k, mid)
            if Bm is not None: B, hi = Bm, int(Bm.sum()) - v
            else: lo = mid + 1
        kk, cost = code_cost(B, A)
        print('  k %d: min load %d (rows avg %.1f, density %.3f) | row-space rank %d cost %d x %.3f | x+density %.3f' % (
            k, hi, hi / v, hi / v / max(deg), kk, cost, cost / v, cost / v + hi / v / max(deg)), flush=True)

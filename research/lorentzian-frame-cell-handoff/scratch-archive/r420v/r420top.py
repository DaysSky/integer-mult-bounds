"""Faithful capacity model on R420's skeleton (geom.py) with an in-chain top.  No symmetry assumed.
Registers: each cell c (2 lines) emits 2 independent sums w[c,0], w[c,1] in F2^c, one to each of its 2 quads; optional
keeper kap[c] in F2^c (extra register, stays at the cell).  Quad U: 6 inputs (one sum from each of its cells), 6 outputs
(one to each owner D6), span(outputs) = span(inputs) (two-way coefficient encoding).  Block node of block b: span of the
keepers of b's cells (V_b); thirds for D6s whose owner lies in comp(b) are vectors of V_b, at most #keepers(b) of them.
D6 node (owner {t,e}): arrivals o1 (quad 1), o2 (quad 2), optional thirds (<= KX).  Delivered users' rows independent;
in-chain user (exactly one in-chain D6 per target) reads any combination.  In-chain node read (nested in the in-chain
D6): one of {a feeding quad of that D6: any combination of its 6 outputs; a keeper cell inside the D6; the block b ⊂ D6:
any vector of V_b}.  Targets: in-chain node + in-chain D6 + 2 delivered = R(t).  Objective: minimise #keepers (R = 240 +
#keepers + 0 fresh).  RELAXATIONS: phases/timing, decoder totals, block-node output count only bounded."""
import sys, os, itertools, collections, json
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
from geom import Geom
from ortools.sat.python import cp_model
tl = float(sys.argv[1]); KX = int(sys.argv[2]) if len(sys.argv) > 2 else 1
G = Geom(); V = e8.V; GI = e8.GI
pc = lambda m: bin(m).count('1')
M = cp_model.CpModel()
B = lambda: M.NewBoolVar('')
def xor_eq(target_bit, terms):
    # target_bit == XOR(terms)
    M.AddBoolXOr(list(terms) + [target_bit.Not()])
def prod(a, b):
    x = B(); M.AddBoolAnd([a, b]).OnlyEnforceIf(x); M.AddBoolOr([a.Not(), b.Not()]).OnlyEnforceIf(x.Not()); return x
cells = G.cells; quads = list(range(len(G.quads)))
# cell sums: w[c][k][line]
w = {c: [{s: B() for s in c} for k in range(2)] for c in cells}
for c in cells:
    v0, v1 = w[c]
    M.AddBoolOr([v0[s] for s in c]); M.AddBoolOr([v1[s] for s in c])
    eq = B()   # forbid v0 == v1
    M.AddBoolOr([prod(v0[c[0]], v1[c[0]].Not()), prod(v0[c[0]].Not(), v1[c[0]]), prod(v0[c[1]], v1[c[1]].Not()), prod(v0[c[1]].Not(), v1[c[1]])])
# which sum goes to which quad: cell c is in quads qa < qb: w[c][0] -> qa, w[c][1] -> qb
cq = collections.defaultdict(list)
for q in quads:
    for c in G.qcells[q]: cq[c].append(q)
inp = {q: [] for q in quads}
for c in cells:
    qa, qb = sorted(cq[c])
    inp[qa].append((c, w[c][0])); inp[qb].append((c, w[c][1]))
# keepers
kp = {c: B() for c in cells}
kap = {c: {s: B() for s in c} for c in cells}
for c in cells:
    for s in c: M.AddImplication(kap[c][s], kp[c])
    M.AddBoolOr([kap[c][s] for s in c] + [kp[c].Not()])
# quad outputs: out[q][owner][line in quad]
out = {}
for q in quads:
    U = G.quads[q]; lines = e8.bits(U)
    owners = G.qowners[q]
    ins = inp[q]
    mu = {(o, i): B() for o in owners for i in range(6)}
    nu = {(i, o): B() for o in owners for i in range(6)}
    out[q] = {}
    for o in owners:
        ob = {s: B() for s in lines}
        out[q][o] = ob
        for s in lines:
            terms = [prod(mu[(o, i)], ins[i][1][s]) for i in range(6) if s in ins[i][1]]
            xor_eq(ob[s], terms) if terms else M.Add(ob[s] == 0)
    for i in range(6):
        c, vec = ins[i]
        for s in lines:
            terms = [prod(nu[(i, o)], out[q][o][s]) for o in owners]
            if s in vec: xor_eq(vec[s], terms)
            else: M.AddBoolXOr(terms + [M.NewConstant(1)]) if False else M.AddBoolXOr(terms + [M.NewConstant(0)]) if False else xor_eq(M.NewConstant(0), terms)
print('quads built', flush=True)
# block spans: thirds and in-chain block reads are combinations of keepers of the block
blk_cells = collections.defaultdict(list)
for c in cells: blk_cells[G.cblk[c]].append(c)
def block_vector(b, tag):
    """a fresh vector in V_b = span of keepers of block b: coefficients rho_c (only if keeper), bits over block lines"""
    rho = {c: B() for c in blk_cells[b]}
    for c in blk_cells[b]: M.AddImplication(rho[c], kp[c])
    vec = {}
    for s in e8.bits(G.blocks[b]):
        vb = B(); vec[s] = vb
        terms = [prod(rho[c], kap[c][s]) for c in blk_cells[b] if s in c]
        xor_eq(vb, terms)
    return vec
# D6 nodes
arr = {}      # owner -> list of (vector dict, used flag)
thirds_by_block = collections.defaultdict(list)
for c2 in cells:
    q1, q2 = G.d6quads[c2]
    lst = [(out[q1][c2], None), (out[q2][c2], None)]
    b = G.comp[G.cblk[c2]]
    for k in range(KX):
        u = B(); vec = block_vector(b, 'third')
        for s, vb in vec.items(): M.AddImplication(vb, u)
        lst.append((vec, u)); thirds_by_block[b].append(u)
    arr[c2] = lst
for b, us in thirds_by_block.items():
    M.Add(sum(us) <= sum(kp[c] for c in blk_cells[b]))
print('D6 nodes built', flush=True)
lam = {}; zin = {}
for c2 in cells:
    n = len(arr[c2]); users = list(c2)
    for t in users:
        zin[(t, c2)] = B()
        for j in range(n): lam[(t, c2, j)] = B()
    for j in range(2, n):
        for t in users: M.AddImplication(lam[(t, c2, j)], arr[c2][j][1])
    allowed = []
    for combo in itertools.product(range(0, 2 ** n), repeat=2):
        for zs in itertools.product((0, 1), repeat=2):
            bb = []; ok = True
            for v, z in zip(combo, zs):
                if z: continue
                for x in bb:
                    if v ^ x < v: v ^= x
                if not v: ok = False; break
                bb.append(v); bb.sort(reverse=True)
            if ok: allowed.append([((combo[i] >> j) & 1) for i in range(2) for j in range(n)] + list(zs))
    M.AddAllowedAssignments([lam[(t, c2, j)] for t in users for j in range(n)] + [zin[(t, c2)] for t in users], allowed)
print('deliveries built', flush=True)
nprod = 0
for t in range(V):
    mine = [c for c in cells if t in c]
    assert len(mine) == 3
    M.Add(sum(zin[(t, c2)] for c2 in mine) == 1)
    # in-chain node options nested in the in-chain D6
    opts = []
    for c2 in mine:
        D6 = G.D6[c2]
        for q in G.d6quads[c2]:
            o = B(); M.AddImplication(o, zin[(t, c2)])
            rho = {oo: B() for oo in G.qowners[q]}
            vec = {}
            for s in e8.bits(G.quads[q]):
                vb = B(); vec[s] = vb
                xor_eq(vb, [prod(rho[oo], out[q][oo][s]) for oo in G.qowners[q]])
            opts.append((o, vec))
        for c in cells:
            if c != c2 and (G.cmask[c] & ~D6) == 0:
                o = B(); M.AddImplication(o, zin[(t, c2)]); M.AddImplication(o, kp[c])
                opts.append((o, kap[c]))
        b = G.comp[G.cblk[c2]]
        if (G.blocks[b] & ~D6) == 0:
            o = B(); M.AddImplication(o, zin[(t, c2)])
            opts.append((o, block_vector(b, 'inchain')))
    M.Add(sum(o for o, v in opts) <= 1)
    for s in e8.bits(e8.HYP[t]):
        terms = []
        for o, vec in opts:
            if s in vec: terms.append(prod(o, vec[s]))
        for c2 in mine:
            for j, (vec, u) in enumerate(arr[c2]):
                if s in vec: terms.append(prod(lam[(t, c2, j)], vec[s]))
        nprod += len(terms)
        M.AddBoolXOr(terms + [M.NewConstant(1)].__class__([]) ) if False else M.AddBoolXOr(terms)
print('targets built; products', nprod, flush=True)
M.Minimize(sum(kp.values()))
sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = tl; sol.parameters.num_workers = 4
r = sol.Solve(M)
print('status', sol.StatusName(r), flush=True)
if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    K = int(sol.ObjectiveValue())
    print('keepers', K, ' => R = 240 + keepers =', 240 + K, ' (R420: 420)  proven keepers >=', sol.BestObjectiveBound(), flush=True)
    third = sum(1 for c2 in cells for j, (vec, u) in enumerate(arr[c2]) if u is not None and sol.Value(u))
    print('thirds used', third, flush=True)

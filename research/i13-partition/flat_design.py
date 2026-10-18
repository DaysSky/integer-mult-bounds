"""Flat-total demand design test: can R(t) be XOR of <= k room-totals of D4-flats containing t?
Pieces: for each good frame F through t, flat M = perp(perp(F)) (12 lines), room = perp(M) (42-56).
Room(M) is readable by every line of M (t in M).  Test per target: parity of full family, then
CP-SAT odd-cover with <= k rooms."""
import os, pickle, sys, time, collections
from ortools.sat.python import cp_model
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(13); V = g.V; HYP = g.HYP; G = g.G
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time()-t0), *a, flush=True)
full = (1 << V) - 1
frames = pickle.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'goodframes13.pkl'), 'rb'))
log('good frames', len(frames))
# all D4 flats via perp(perp(F)); keep those with 12 lines
flat2room = {}
for F in frames:
    fl = full
    for s in [x for x in range(V) if F >> x & 1]: fl &= HYP[s]
    room = fl
    flat = full
    for r in [x for x in range(V) if room >> x & 1]: flat &= HYP[r]
    flat2room[flat] = room
log('distinct D4 flats', len(flat2room), 'line counts', dict(collections.Counter(bin(k).count('1') for k in flat2room)))
# per-target: flats containing t
by_t = collections.defaultdict(list)
for flat, room in flat2room.items():
    for s in range(V):
        if flat >> s & 1: by_t[s].append((flat, room))
log('flats per target: min %d max %d mean %.0f' % (min(len(v) for v in by_t.values()), max(len(v) for v in by_t.values()), sum(len(v) for v in by_t.values())/V))
# full-family parity for target t: XOR of rooms of flats containing t
for t in (g.P(0,1), g.T(0,1,2)):
    R_t = HYP[t] & ~(1 << t)
    X = 0
    for flat, room in by_t[t]: X ^= room
    log('t=%s: full-family XOR == R(t)? %s  (popcount %d vs |R| %d)' % (g.kind[t]+str(g.supp[t]), X == R_t, bin(X).count('1'), bin(R_t).count('1')))
    # parity per line: C(t,ell) = #(flats M in family with ell in room) mod 2
    cnt = collections.Counter()
    for flat, room in by_t[t]:
        for l in [x for x in range(V) if room >> x & 1]: cnt[l] += 1
    odd = {l for l, c in cnt.items() if c % 2}
    log('   odd-covered lines %d; R(t) %d; odd set == R(t)? %s' % (len(odd), bin(R_t).count('1'), odd == set(x for x in range(V) if R_t >> x & 1)))
    # CP-SAT sparse odd-cover: choose <= k rooms XORing to R(t)
    for KMAX in (4, 6, 8):
        m = cp_model.CpModel()
        cands = by_t[t]
        y = [m.NewBoolVar('') for _ in cands]
        m.Add(sum(y) <= KMAX)
        # per line: XOR parity constraint: sum of rooms containing line is odd for lines in R(t), even else
        for l in range(V):
            ids = [j for j, (flat, room) in enumerate(cands) if room >> l & 1]
            want = 1 if (R_t >> l & 1) else 0
            if not ids:
                if want: m.AddBoolOr([])  # infeasible
                continue
            # parity: sum(ids) % 2 == want -> use boolean sum with even/odd
            # parity: introduce XOR chain via add_modulo_equality on the sum is overkill; use
            # the standard linearization: s = sum(y[j]); s odd <=> exists z: s == 2z + want
            if ids:
                s = sum(y[j] for j in ids)
                z = m.NewIntVar(0, len(ids), '')
                m.Add(2 * z + want == s)
        sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = 60
        st = sol.Solve(m)
        log('   KMAX %d: %s (uses %d)' % (KMAX, sol.StatusName(st), sum(sol.Value(v) for v in y) if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else -1))

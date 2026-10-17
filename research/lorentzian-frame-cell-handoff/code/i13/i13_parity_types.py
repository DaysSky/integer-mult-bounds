"""Minimum parity covers of R(t) using only chosen frame TYPES (orbit types of (t,F) under Stab(t), named by a
representative's lines).  Exact CP-SAT (time-limited, reports bound).  usage: python3 i13_parity_types.py"""
import sys, pickle, collections
from lgeo13 import *
from ortools.sat.python import cp_model
def nm(s): return KIND[s] + ''.join('%x' % i for i in SUPP[s])
def run(kind, typenames, TL=300):
    t, FL, PL = pickle.load(open('i13_frames_%s.pkl' % kind, 'rb'))
    R = HYP[t]
    want = set()
    for tn in typenames:
        m = 0
        for w in tn.split():
            k, pts = w[0], tuple(int(c, 16) for c in w[1:])
            m |= 1 << IDX[(k, pts)]
        want.add(canon((1 << t, m))[0])
    idx = [i for i in range(len(FL)) if canon((1 << t, FL[i]))[0] in want]
    cov = collections.defaultdict(list)
    for i in idx:
        for s in bits(PL[i]): cov[s].append(i)
    M = cp_model.CpModel(); x = {i: M.NewBoolVar('') for i in idx}
    for s in bits(R):
        if not cov[s]: print(kind, typenames, 'line uncovered -> infeasible'); return
        M.AddBoolXOr([x[i] for i in cov[s]])
    M.Minimize(sum(x.values()))
    sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = 2
    st = sv.Solve(M)
    out = sv.ObjectiveValue() if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None
    print(kind, typenames, '| frames', len(idx), '|', sv.StatusName(st), 'min', out, 'bound', sv.BestObjectiveBound(), flush=True)
    if out:
        sel = [i for i in idx if sv.Value(x[i])]
        print('   ', ['%s' % ' '.join(nm(s) for s in bits(FL[i])) for i in sel], flush=True)
run('T', ['P34 P56 T012'])
run('T', ['T012 T034 T056'])
run('T', ['P34 P56 T012', 'T012 T034 T056'])
run('P', ['P01 P23 P45'])
run('P', ['P01 P23 P45', 'P01 P23 T456'])
run('P', ['P01 T234 T256'])
run('P', ['P01 P23 P45', 'P01 P23 T456', 'P01 T234 T256'])

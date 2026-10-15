"""Summarise the LP optimum: register mass by node (rank, lines, perp) and by section type; in-chain / delivery usage."""
import pickle, glob, collections
from lgeo import *
sol = pickle.load(open('lp_sol.pkl', 'rb')); x = sol['x']; VAR = sol['VAR']
planes = pickle.load(open('planes.pkl', 'rb')); side = pickle.load(open('side.pkl', 'rb'))
psize = side['psize']
secs = {}
for f in sorted(glob.glob('sec_*.pkl')):
    i = int(f.split('_')[1].split('.')[0]); secs[i] = pickle.load(open(f, 'rb'))
pname = {i: '%d|%d' % (pc(p), pc(pm(p))) for i, p in enumerate(planes)}
bynode = collections.Counter(); bysec = collections.Counter()
for i, s in secs.items():
    for yk, r in s['reps'].items():
        v = x[VAR[('Y', yk)]] * psize[i] * r['count']
        if v > 1e-6:
            bynode[(r['rank'], r['size'], r['perp'], r['lam'])] += v
            bysec[pname[i]] += v
print('LP registers', sol['fun'])
print('register mass by node (rank, lines, perp, lam):')
for k, v in sorted(bynode.items(), key=lambda kv: -kv[1])[:25]: print('  ', k, round(v, 2))
print('register mass by section type (plane lines | section lines):')
for k, v in sorted(bysec.items(), key=lambda kv: -kv[1]): print('  ', k, round(v, 2))
for t0, d in side['tgt'].items():
    ins = collections.Counter(); dels = collections.Counter()
    for p in d['planes']:
        ins[pname[p['sec']]] += x[VAR[('IN', p['inkey'])]] if ('IN', p['inkey']) in VAR else 0
        dels[pname[p['sec']]] += x[VAR[('DEL', p['inkey'])]] if ('DEL', p['inkey']) in VAR else 0
    print('target', 'P' if t0 < 55 else 'T', 'in-chain by section type', {k: round(v, 3) for k, v in ins.items() if v > 1e-6})
    print('       deliveries by section type', {k: round(v, 3) for k, v in dels.items() if v > 1e-6})
    print('       private regs', round(x[VAR[('PRIV', t0)]], 3), 'rank<=2 reads', round(sum(x[VAR[('C', ck)]] for ck in d['ckeys'].values()), 3))

"""THE PRECEDENT'S OWN GRAMMAR CENSUS (ii19_nat87.py) — the r434's cst=63 structure!!

THE nat86's verdict: F(0) < 0 ⟺ cst ≤ 106 (R-exactly-neutral!!); the pure-scatter grammar
is cst ≥ 120 (the GF(2)-rank bound — DEAD); the r434's OWN cst = 63 (its mass 5,129 =
8·439 + 63 + 2·111·7!!!) — THE PUBLISHED FRONTIER WORD ITSELF IS THE GATHER-GRAMMAR!!
THIS CENSUS: the r434's exact delivery structure (the ret/ret_frames (the gathers!!),
the scatter lists, the B-phase (the targets' reads), the D, the A/C shape) — THE TEMPLATE
FOR THE ext120 PORT (the last mile's ground truth!!!).
"""
import os, sys, json
from collections import Counter
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'tword'))
from gcheck import main
log = lambda *a: print(*a, file=sys.stderr, flush=True)

path = 'ii19_pub2_p111-r434.json'
w = json.load(open(path, 'rt'))
v, h, R = w['v'], w['h'], w['R']
nreg = 2 * v + R
log('v=%d h=%d R=%d nreg=%d frames=%d' % (v, h, R, nreg, len(w['frames'])))
out = main(path, do_price=True)
log('THE CONTROL REPLAY: %s' % json.dumps({k: out[k] for k in
    ('status', 'R', 'rho', 'totals', 'cst', 'x', 'local_histogram', 'rank_mass', 'gates')}))
log('price: %s (%s%%)' % (out.get('bit_c_nine_stage'), out.get('vs_P111_percent')))

dims = [len(json.loads('[' + ','.join('0') + ']')) for _ in ()]  # placeholder
# the frames' dims via gcheck's rref (exact fractions as strings!!)
from fractions import Fraction as Fr
def rref_dim(F):
    rows = [[Fr(x) for x in row] for row in F]
    m = [row[:] for row in rows]; r = 0
    for c in range(h):
        p = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if p is None: continue
        m[r], m[p] = m[p], m[r]; iv = 1 / m[r][c]; m[r] = [x * iv for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]; m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
    return r
fdim = [rref_dim(F) for F in w['frames']]
log('frame dims census: %s' % dict(sorted(Counter(fdim).items())))

ret, rf = w['ret'], w['ret_frames']
log('\nTHE RETAINED (%d!!):' % len(ret))
kinds = Counter()
for k, q in enumerate(ret):
    kind = 'SRC' if q < v else ('TGT' if q < 2 * v else 'HLP')
    kinds[kind] += 1
    log('  k=%3d q=%4d (%s) ret_frame=%4d dim=%d' % (k, q, kind, rf[k], fdim[rf[k]]))
log('the kinds: %s | THE CST = %d (the copy-ranks %s)'
    % (dict(kinds), sum(fdim[f] for f in rf), dict(sorted(Counter(fdim[f] for f in rf).items()))))

log('\nTHE SCATTER (per-target ret-subsets):')
cnt = Counter(len(s) for s in w['scatter'])
log('  the scatter-list sizes: %s' % dict(sorted(cnt.items())))
use = Counter()
for s in w['scatter']:
    for k in s: use[k] += 1
log('  the ret usage census: %s' % dict(sorted(Counter(use.values()).items())))
log('  each ret k used by: %s' % {k: use.get(k, 0) for k in range(len(ret))})

log('\nTHE GATES:')
for ph in ('D', 'A', 'B', 'C'):
    G = w[ph]
    nd = Counter('TGT' if v <= d < 2 * v else ('SRC' if d < v else 'HLP') for _, d, _ in G)
    ns = Counter()
    for _, _, srcs in G:
        for s in srcs: ns['TGT' if v <= s < 2 * v else ('SRC' if s < v else 'HLP')] += 1
    sizes = Counter(len(s) for _, _, s in G)
    log('  %s: %d gates | dests %s | srcs %s | src-counts %s'
        % (ph, len(G), dict(nd), dict(ns), dict(sorted(sizes.items()))))

log('\nTHE B-PHASE (the targets reads (the perp-delivery!!)):')
BG = [g for g in w['B'] if v <= g[1] < 2 * v]
tf = Counter()
for F, d, srcs in BG:
    tf[(fdim[F], len(srcs))] += 1
log('  the target-dest B-gates: %d | (frame-dim, nsrcs) census: %s' % (len(BG), dict(sorted(tf.items()))))
# the per-target read census
per_t = Counter()
for F, d, srcs in BG: per_t[d - v] += len(srcs)
log('  per-target B-srcs: %s' % dict(sorted(Counter(per_t.values()).items())))
# the B-src registers' kinds
bsrc = Counter()
for F, d, srcs in BG:
    for s in srcs: bsrc['SRC' if s < v else 'HLP'] += 1
log('  the B-src kinds: %s' % dict(bsrc))
zG = [g for g in w['B'] if not (v <= g[1] < 2 * v)]
log('  the z-B-gates (helper-dests!!): %d' % len(zG))

log('\nTHE D-PHASE:')
nd = Counter(); sz = Counter()
for F, d, srcs in w['D']:
    nd[d - v] += 1; sz[len(srcs)] += 1
log('  D: %d gates | per-target %s | src-counts %s' % (len(w['D']), dict(sorted(nd.items())), dict(sorted(sz.items()))))

log('\nTHE A-PHASE (the helper builds shapes):')
adest = Counter(); asrc = Counter(); asz = Counter(); afdim = Counter()
for F, d, srcs in w['A']:
    adest['HLP' if d >= 2 * v else 'SRC'] += 1
    for s in srcs: asrc['SRC' if s < v else 'HLP'] += 1
    asz[len(srcs)] += 1
    afdim[fdim[F]] += 1
log('  A: %d | dests %s | srcs %s | src-counts %s | frame-dims %s'
    % (len(w['A']), dict(adest), dict(asrc), dict(sorted(asz.items())), dict(sorted(afdim.items()))))

log('\nTHE GATHERS OWN BUILDS (the deep-DAG!!):')
retset = set(ret)
for k, q in enumerate(ret):
    if q < 2 * v: continue
    gates_in = [(ph, F, d, srcs) for ph in ('D', 'A', 'B') for F, d, srcs in w[ph] if d == q]
    allsrcs = [s for _, _, _, srcs in gates_in for s in srcs]
    log('  gather q=%d (ret_frame dim %d): %d dest-gates %s | total srcs %d (%s)'
        % (q, fdim[rf[k]], len(gates_in), [(ph, fdim[F], len(srcs)) for ph, F, d, srcs in gates_in],
           len(allsrcs), 'SRC' if all(s < v for s in allsrcs) else 'mixed'))

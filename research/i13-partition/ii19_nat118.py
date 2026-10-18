"""nat118: end-to-end pipeline for a keeper plan -> tuned word -> gcheck -> priced root.
usage: python ii19_nat118.py PARAMS.json OUT.json.gz [TAG]
Steps: gen_p4 make -> tune434 fixed point -> gcheck (exact replay) -> price at the landed R.
"""
import json, os, subprocess, sys

log = print
PRM = os.path.abspath(sys.argv[1])
OUT = os.path.abspath(sys.argv[2])
TAG = sys.argv[3] if len(sys.argv) > 3 else os.path.basename(PRM)
HUB = os.path.abspath(os.path.join('..', 'e8-bit-p111-r434', 'code'))
PLAN = os.path.abspath(os.path.join('..', 'e8-bit-p111', 'data', 'plan-l3.json'))
PY = sys.executable

# (1) build
base = OUT.replace('.json.gz', '-base.json.gz')
r = subprocess.run([PY, '-I', 'gen_p4.py', PLAN, PRM, base], capture_output=True, text=True, cwd=HUB)
line = [l for l in r.stdout.splitlines() if l.startswith('R ')]
if not line:
    log('BUILD FAILED:\n' + r.stdout[-2000:] + r.stderr[-2000:]); sys.exit(1)
log('[%s] base: %s' % (TAG, line[0]))

# (2) tune
tuned = OUT.replace('.json.gz', '-tuned.json.gz')
r = subprocess.run([PY, '-I', 'tune434.py', base, tuned], capture_output=True, text=True, cwd=HUB)
log('[%s] tune: %s' % (TAG, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-500:]))

# (3) format adapter: form {num, den} + ret_frames (lightweight replay to the scatter!!)
import gzip
wd = json.load(gzip.open(tuned, 'rt'))
wd['form'] = {'num': [[1 if i == j else 0 for j in range(8)] for i in range(8)], 'den': 2}
dims = [len(f) if not isinstance(f, int) else f for f in wd['frames']]
# the frames are lists of vectors; dims via rref would be exact but the hub writes basis lists already.
cur = list(wd['start'])
for F, d, ss in wd['D'] + wd['A']:
    cur[d] = F
    for s in ss: cur[s] = F
wd['ret_frames'] = [cur[q] for q in wd['ret']]
# frames: line-index lists -> vector lists (gcheck's convention!!)
wd['frames'] = [[list(wd['lines'][i]) for i in F] for F in wd['frames']]
tmp = tuned.replace('.json.gz', '-gcheckfmt.json')
json.dump(wd, open(tmp, 'wt'))
log('[%s] adapter: form + ret_frames %s written' % (TAG, wd['ret_frames']))

# (4) gcheck + price (our judge, on the adapted word)
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'tword'))
import gcheck
out = gcheck.main(tmp, do_price=True)
for k in ('status', 'R', 'rho', 'cst', 'totals', 'rank_mass', 'local_histogram'):
    log('[%s] %-18s %s' % (TAG, k, out.get(k)))
log('[%s] bit_c_nine_stage   %s' % (TAG, out.get('bit_c_nine_stage')))
log('[%s] vs_P111_percent    %s' % (TAG, out.get('vs_P111_percent')))
json.dump({'tag': TAG, 'params': PRM, 'tuned': tuned, 'gcheck': {k: (str(v) if isinstance(v, (list, dict)) else v) for k, v in out.items()}},
          open('ii19_nat118_%s.json' % os.path.splitext(TAG)[0].replace('.json', ''), 'wt'), indent=1, default=str)

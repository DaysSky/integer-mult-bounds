"""The record word ii19_fullraise_tuned (W4 tuned, c = 0.0013435, -22.98% vs r434) uses form diag(1^8, 2):
positive-definite.  Flip the special line's norm to -2 (signature (8,1), i.e. E8(2) + <-2>, the E8 + <e - f>
section of II_{1,9}) and re-run the unmodified gcheck on both.  Expected: identical PASS, hist and price."""
import gzip, json, os, subprocess, sys, tempfile
from _common import I13, GCHECK
src = os.path.join(I13, 'ii19_fullraise_tuned.json.gz')
w = json.load(gzip.open(src, 'rt'))
assert w['form']['num'][8][8] == 2 and all(w['form']['num'][i][i] == 1 for i in range(8))
w['form']['num'][8][8] = -2
tmp = os.path.join(tempfile.mkdtemp(), 'w4_tuned_signature_8_1.json')
json.dump(w, open(tmp, 'w'))
outs = []
for path in (src, tmp):
    r = subprocess.run([sys.executable, GCHECK, path, '--price'], capture_output=True, text=True)
    out = json.loads(r.stdout); outs.append(out)
    print('%-28s status %s  hist %s  c %s' % (os.path.basename(path), out['status'], out['local_histogram'],
                                              out.get('bit_c_nine_stage')))
print('identical gcheck verdicts:', outs[0] == outs[1])

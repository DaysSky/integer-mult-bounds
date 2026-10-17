# For a block partition: fraction of (frame, block) pairs with pi_frame n W_block^perp != 0, i.e. lines of the frame
# have an aligned cell partner inside the block's layers.  Compare E8 (#493 partition).
import sys, pickle, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, bits, V
exec(open('/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/blk/f2lib.py').read())
blocks, pun = pickle.load(open(sys.argv[1], 'rb'))
frames = [tuple(f) for b in blocks for f in b]
Ws = [span([vv[x] for q in b for x in q]) for b in blocks]
cnt = collections.Counter(); tot = 0
for f in frames:
    pi = [vv[f[0]] ^ vv[x] for x in f[1:]]
    for bi, W in enumerate(Ws):
        if any(x in W for x in [vv[u] for u in f]): continue          # frame inside the block
        k = sum(1 for s in pi if all(dot(s, w) == 0 for w in W))
        cnt[k] += 1; tot += 1
print('I11 (frame, other block) pairs:', tot, '| #pi vectors orthogonal to W_B:', dict(cnt), '| aligned fraction %.3f' % (1 - cnt[0] / tot))

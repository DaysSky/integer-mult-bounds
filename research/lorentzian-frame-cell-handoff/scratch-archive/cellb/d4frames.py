import sys, pickle, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
V = e8.V
D4 = pickle.load(open('../sec4/d4.pkl', 'rb'))
frames = set()
for W in D4:
    ls = list(e8.bits(W))
    for a in ls:
        f = [a] + [b for b in ls if e8.GI[a, b] == 0]
        assert len(f) == 4
        frames.add(sum(1 << x for x in f))
frames = sorted(frames)
print('D4s', len(D4), 'D4 frames', len(frames), 'per line', collections.Counter(sum(1 for F in frames if F >> s & 1) for s in range(V)))
pickle.dump(frames, open('d4frames.pkl', 'wb'))

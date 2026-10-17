import sys, os, pickle, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lbuild')
from lw import g, bits, V
from fastcl import fclosure
pc = lambda m: bin(m).count('1')
choice = pickle.load(open('a3_choice_pack.pkl','rb'))
def nm(s): return g.kind[s] + ''.join('0123456789X'[i] for i in g.supp[s])
blocks = collections.defaultdict(list)
for t,(a,b,c,d) in choice.items():
    tris=[Q for Q in (a,b,c) if pc(Q)==3]
    if len(tris)==2:
        A3=fclosure(tris[0]|tris[1])
        if pc(A3)==6: blocks[A3].append(t)
typ = collections.Counter()
for A3, ts in blocks.items():
    if len(ts)!=6: continue
    k = ''.join(sorted(g.kind[s] for s in bits(A3)))
    typ[k]+=1
print(typ)
for A3, ts in list(blocks.items())[:8]:
    print([nm(s) for s in bits(A3)], len(ts))
left=[t for t in range(V) if not any(t in ts for ts in blocks.values() if len(ts)==6)]
print('left', len(left), collections.Counter(g.kind[t] for t in left))
print('block lines kinds', collections.Counter(g.kind[t] for ts in blocks.values() if len(ts)==6 for t in ts))

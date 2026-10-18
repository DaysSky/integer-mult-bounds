import sys,pickle,json,random
sys.path.insert(0,'.')
from bld import *
from mpmath import mp
P=[10,15,51,53,56,66,72,89,111]
prm=json.load(open(R+'/data/punct.json'))
sel0={int(k):v for k,v in prm['receivers'].items()}
opt=pickle.load(open('opt_ship.pkl','rb'))
E1=mp.mpf('0.001734473240795253742474')
rng=random.Random(int(sys.argv[1]))
res=[]
for trial in range(int(sys.argv[2])):
    choice={}
    for B in (0,1,3,5):
        flb,perm,rs,c=opt[B][1][rng.randrange(len(opt[B][1]))]
        choice[B]=(flb,perm,rs)
    fl,assign,sel=make_params(P,choice,rcvbase=sel0)
    word,extras=build(P,fl,assign,sel,nodeopt=1)
    H,c=evalw(word)
    res.append((float(c),word['R'],dict(H),choice))
res.sort(key=lambda r:-r[0])
pickle.dump(res,open('samp437_%s.pkl'%sys.argv[1],'wb'))
import collections
print(collections.Counter(round((r[0]/float(E1)-1)*100,4) for r in res).most_common(12))
print('best',res[0][:3],'%+.4f%%'%((res[0][0]/float(E1)-1)*100))

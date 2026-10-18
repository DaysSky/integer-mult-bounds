import sys,pickle,json,random,collections
sys.path.insert(0,'.')
sys.path.insert(0,'/tmp/claude-0/-home-user-integer-mult-bounds/45552e66-7196-5fbb-857a-ded5e6dbacae/scratchpad/pkg/code')
from bld import *
import gen_p4
from mpmath import mp
E1=mp.mpf('0.001734473240795253742474')
P=[10,15,51,53,56,66,72,89,111]
prm=json.load(open(R+'/data/punct.json')); sel0={int(k):v for k,v in prm['receivers'].items()}
gopt=pickle.load(open(sys.argv[1],'rb'))
rng=random.Random(int(sys.argv[2])); N=int(sys.argv[3])
gen_p4.NODEOPT[0]=1
res=[]
for trial in range(N):
    choice={}; extras={}
    for B in (0,1,3,5):
        flb,perm,rs,E,nj=gopt[B][1][rng.randrange(len(gopt[B][1]))]
        choice[B]=(flb,perm,rs); extras[B]=[x[0] if len(x)==1 else list(x) for x in E]
    fl,assign,sel=make_params(P,choice,rcvbase=sel0)
    r=gen_p4.build(G,sol,P,fl,assign,extras=extras,verbose=False,rcvsel=sel)
    if r[0]=='missing': print('MISSING',r[1]); continue
    word=r[1]; H,c=evalw(word)
    res.append((float(c),word['R'],dict(H),choice,extras,word['stats']))
res.sort(key=lambda r:-r[0])
pickle.dump(res,open('sampg_%s.pkl'%sys.argv[2],'wb'))
print('R',collections.Counter(r[1] for r in res))
print(collections.Counter(round((r[0]/float(E1)-1)*100,3) for r in res).most_common(10))
print('best',res[0][1],res[0][2],res[0][5],'%+.4f%%'%((res[0][0]/float(E1)-1)*100))

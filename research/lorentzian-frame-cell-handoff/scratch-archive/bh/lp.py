import numpy as np, pickle, scipy.sparse as sp, time
from scipy.optimize import linprog
g=pickle.load(open('bh.pkl','rb')); E=g['phys']; S=g['sessions']; V=182; nE=len(E); nS=len(S)
# vars: l_e (nE), pi[q,v] (nS*V). minimize sum l. constraints: pi[q,u]-pi[q,v]-l_e<=0 both dirs; pi[q,s]-pi[q,t]<=-2
rows=[];cols=[];vals=[];b=[];r=0
def pv(q,v): return nE+q*V+v
for q in range(nS):
    for k,(u,v) in enumerate(E):
        for a,c in ((u,v),(v,u)):
            rows+= [r,r,r]; cols+=[pv(q,a),pv(q,c),k]; vals+=[1,-1,-1]; b.append(0); r+=1
    s,t=S[q]; rows+=[r,r]; cols+=[pv(q,s),pv(q,t)]; vals+=[1,-1]; b.append(-2); r+=1
A=sp.csr_matrix((vals,(rows,cols)),shape=(r,nE+nS*V))
c=np.zeros(nE+nS*V); c[:nE]=1
bounds=[(0,None)]*nE+[(None,None)]*(nS*V)
for q in range(nS): bounds[pv(q,S[q][0])]=(0,0)
t0=time.time()
res=linprog(c,A_ub=A,b_ub=np.array(b,float),bounds=bounds,method='highs-ipm')
print(res.status,res.message[:60],'LP min total length =',res.fun,'(W*m = 314)',round(time.time()-t0,1))
l=res.x[:nE]; print('length histogram',np.unique(np.round(l,3),return_counts=True))

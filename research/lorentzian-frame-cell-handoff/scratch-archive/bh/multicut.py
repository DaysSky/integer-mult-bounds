import numpy as np, pickle, scipy.sparse as sp, time
from scipy.optimize import milp, LinearConstraint, Bounds
g=pickle.load(open('bh.pkl','rb')); E=g['phys']; S=g['sessions']; V=182; nE=len(E); nS=len(S)
rows=[];cols=[];vals=[];ub=[];r=0
def pv(q,v): return nE+q*V+v
for q in range(nS):
    for k,(u,v) in enumerate(E):
        for a,c in ((u,v),(v,u)):
            rows+=[r,r,r]; cols+=[pv(q,a),pv(q,c),k]; vals+=[1,-1,-1]; ub.append(0); r+=1
    s,t=S[q]; rows+=[r,r]; cols+=[pv(q,s),pv(q,t)]; vals+=[1,-1]; ub.append(-1); r+=1
A=sp.csr_matrix((vals,(rows,cols)),shape=(r,nE+nS*V))
c=np.zeros(nE+nS*V); c[:nE]=1
lb=np.full(nE+nS*V,-np.inf); ubv=np.full(nE+nS*V,np.inf); lb[:nE]=0; ubv[:nE]=1
for q in range(nS): lb[pv(q,S[q][0])]=0; ubv[pv(q,S[q][0])]=0
integ=np.zeros(nE+nS*V); integ[:nE]=1
t0=time.time()
res=milp(c,constraints=LinearConstraint(A,-np.inf,np.array(ub,float)),bounds=Bounds(lb,ubv),integrality=integ,options={'time_limit':1500,'disp':False})
print(res.status,res.message,'obj',res.fun,'bound', getattr(res,'mip_dual_bound',None),round(time.time()-t0,1))

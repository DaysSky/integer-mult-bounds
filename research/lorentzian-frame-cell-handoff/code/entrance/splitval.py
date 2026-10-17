import sys
exec(open('pricew.py').read().replace("if __name__=='__main__':","if False:"))
ref=mpf('0.001733427039589844')
base={1:1323,2:1342,3:79,4:44,5:102,6:11,7:19}
for s in [0,10,50,74,100,150,200,300,439]:
    wc={}
    if 439-s: wc[8]=439-s
    if s: wc[7]=s; wc[1]=2*s
    loc=dict(base); loc[1]+=s
    out=price(loc,wc)
    if out is None: print(s,'infeasible',flush=True); continue
    c,rem,o=out
    print('splits/call %3d (7+1+1 cells, +1 rank-1 child): c %.12f %+.3f%% opt %s rem %s'%(s,float(c),float((c/ref-1)*100),o,rem),flush=True)

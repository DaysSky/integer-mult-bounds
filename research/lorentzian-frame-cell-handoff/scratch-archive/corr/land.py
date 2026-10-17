from ceil_a import X
def best(w,xr):  # k=1 scaling: h=w, a=w-1, x=xr
    return max((X(s,w,1,xr,w-1) or 0) for s in range(3,61,2))
print('E8 ref', best(8,63/111))
ws=[2,3,4,5,6,8]; xs=[0.3,0.5,0.7,0.8,0.9]
print('w\\x/k',xs)
for w in ws: print(w,['%.2e'%best(w,x) for x in xs])

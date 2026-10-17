import sys, json
sys.path.insert(0,'/home/user/integer-mult-bounds/research/e8-bit-p111-tuned/tune')
import wlib, tune
w=wlib.load('/home/user/integer-mult-bounds/research/e8-bit-p111-e1/data/bitE8mut-p111-e1.json.gz')
print('E1 profile', wlib.paid(w))
Tn=tune.Tuner(w,a=0.0017343)
total=0
for rnd in range(6):
    n=0
    for ch in "TSF":
        for sec in "AB":
            V=Tn.view(sec)
            ap=(tune.transport_sweep(V,verbose=False) if ch=="T" else tune.steinberg_sweep(V,verbose=False) if ch=="S" else tune.transport_sweep(V,verbose=False,allow_move=False))
            if ap: print('round',rnd,ch,sec,'applied',len(ap),ap[:3],flush=True)
            n+=len(ap)
    total+=n
    if not n: break
print('total moves',total)
pw,found=Tn.paid()
print('profile after', pw)
wlib.save(found,'tuned_e1.json.gz')

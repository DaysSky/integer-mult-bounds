import gzip, json, sys, hashlib
sys.path.insert(0,'/home/user/integer-mult-bounds/research/e8-bit-p111-tuned/tune')
import wlib
w=json.load(gzip.open('/home/user/integer-mult-bounds/research/e8-bit-p111-e1/data/bitE8mut-p111-e1.json.gz','rt'))
P=186
assert w['A'][230]==[79,444,[470]] and w['A'][231]==[79,470,[77]] and w['A'][1994]==[79,444,[470]]
for i in (230,231,1994): w['A'][i][0]=P
w['start'][470]=P
w['C']=wlib.rebuild_C(w)
w['stats']=dict(w['stats'],entrance_rank2_helpers=[470-222])
print('profile', wlib.paid(w))
sha=wlib.save(w,sys.argv[1]); print('written',sys.argv[1],sha[:16])

#!/usr/bin/env bash
# One-command verification of research/e8-bit-p111-r434: PR #555's punctured L3 word family (P111) with an exhaustively
# chosen keeper plan and cell-sum extra helpers, R = 434 instead of 439.  The base word is rebuilt from #543's frozen
# L3 plan and this package's explicit parameters by code/gen_p4.py (PR #555's gen_p3.py with two listed edits), the
# shipped word from it by PR #589's tuner run to its fixed point (code/tune434.py); the shipped word is replayed exactly
# by P111's independent checker (unchanged), passed through the official cohort checkers at (v, R) = (111, 434), and
# priced by the same two hub pipelines as P111-tuned: PR #510's nine-stage chain parameterised by P111's adapt9p.py,
# and PR #493's eleven-stage chain as parameterised by PR #545's adapt.py, with hosting selections that the hosting
# programmes rediscover.  Control: gen_p4.py with P111's own keeper plan (data/params-p111.json) rebuilds P111's shipped
# word exactly (decompressed payloads are compared).
#   usage: bash research/e8-bit-p111-r434/verify.sh /fresh/output/dir
#   needs python3 >= 3.11 with numpy, sympy and scipy, a C++17 compiler (CXX, default c++) and Boost headers
#   (BOOST_INCLUDE, default /usr/include).
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd); WD=$(mkdir -p "$1" && cd "$1" && pwd)
TP=$(cd "$HERE/../e8-bit-p111-tuned" && pwd); P111=$(cd "$HERE/../e8-bit-p111" && pwd); P=$(cd "$HERE/../e8-bit-carrier-skeleton" && pwd)
case "$WD/" in "$HERE"/*|"$TP"/*|"$P111"/*|"$P"/*) echo "output dir must be outside the packages"; exit 2;; esac
export PYTHONDONTWRITEBYTECODE=1
PY="${PYTHON:-python3} -I -B"
PYS="${PYTHON:-python3} -E -s -B"     # scripts that import siblings from their own directory
CXX=${CXX:-c++}; BI=${BOOST_INCLUDE:-/usr/include}
E=$HERE/code; C=$TP/code; D=$TP/data; WORD=$HERE/data/bitE8mut-p111-r434.json.gz; BASE=$HERE/data/bitE8mut-p111-r434-base.json.gz
PC=$P/code; B=$PC/bit; CK=$B/checkers; INC="-I$P/portable-include -I$CK -I$BI"
V510=$TP/vendor/pr510/e8-r480-nine-stage; VK=$V510/vendor/e8-r715-eleven-stage-whole/code
A545=$TP/vendor/pr545/code
ISO=$P/data/eleven/residual-isometries.json; BIN=$WD/bin; mkdir -p "$BIN"
V=$($PY -c "import json,gzip;print(json.load(gzip.open('$WORD','rt'))['v'])")
R=$($PY -c "import json,gzip;print(json.load(gzip.open('$WORD','rt'))['R'])")
T0=$SECONDS
same() {   # decompressed payloads equal (gzip container bytes may differ across zlib versions; CONTRIBUTING.md)
  $PY -c "import gzip,sys;sys.exit(0 if gzip.open('$1').read()==gzip.open('$2').read() else 1)" || { echo "payload differs: $1 $2"; exit 1; }
}
step() { echo "== $1  [$((SECONDS - T0))s]"; }

step "0. manifest"
(cd "$HERE" && $PY -c "
import hashlib,os,sys
bad=0;listed=set()
for line in open('MANIFEST.sha256'):
    h,p=line.rstrip('\n').split('  ',1);listed.add(p)
    if hashlib.sha256(open(p,'rb').read()).hexdigest()!=h: print('MISMATCH',p);bad+=1
files={os.path.relpath(os.path.join(r,f)) for r,_,fs in os.walk('.') for f in fs if '__pycache__' not in r}-{'MANIFEST.sha256'}
if files-listed: print('UNLISTED',sorted(files-listed));bad+=1
sys.exit(1 if bad else 0)") && echo "   all files match MANIFEST.sha256"
mkdir -p $WD/root/data && ln -sfn $PC $WD/root/code && cp $D/complex-b.json $WD/root/data/   # assembly root

step "1. the base word from #543's frozen L3 plan and data/params.json, the shipped word by PR #589's tuner; control: P111's keeper plan rebuilds P111's word"
$PY $E/gen_p4.py $D/plan-l3.json $HERE/data/params.json $WD/base.json.gz | sed 's/^/   /'
same $WD/base.json.gz $BASE
$PY $E/tune434.py $BASE $WD/word.json.gz | sed 's/^/   /'
same $WD/word.json.gz $WORD
$PY $E/gen_p4.py $D/plan-l3.json $HERE/data/params-p111.json $WD/p111.json.gz > /dev/null
same $WD/p111.json.gz $D/bitE8mut-p111.json.gz
echo "   control: gen_p4.py with P111's keeper plan (plan_thirds seed 552, written out explicitly) rebuilds P111's shipped word (same decompressed payload)"
$PY -c "
import json,gzip,hashlib
w=json.load(gzip.open('$WORD','rt'));e=json.load(open('$HERE/EXPECTED.json'))['word']
h=hashlib.sha256(json.dumps(w,sort_keys=True,separators=(',',':')).encode()).hexdigest()
assert h==e['content_sha256'] and (w['v'],w['R'])==(e['v'],e['R']) and len(w['ret'])==9
assert {k:len(w[k]) for k in 'DABC'}==e['gates'] and w['stats']==e['stats']
assert all(w['frames'][f]==[] for f in w['start'][w['v']:]), 'every target and helper starts at frame 0'
b=json.load(gzip.open('$BASE','rt'))
assert hashlib.sha256(open('$BASE','rb').read()).hexdigest()==e['base_file_sha256']
assert {k:w[k] for k in w if k not in ('A','B','C')}=={k:b[k] for k in b if k not in ('A','B','C')}
print('   rebuilt base and tuned words equal the shipped files (decompressed payloads) (content sha256',h[:16]+'...); v',w['v'],'R',w['R'],'stats',w['stats'])
print('   the tuned word differs from the base word only in A, B and C (same registers, frames, D, scatter, start, final)')"

step "2. independent exact replay, totals, the interleaved interface lemma, mutation controls (P111's checker, unchanged)"
$PY $C/xcheck_p.py $WORD --json $WD/xcheck.json | sed 's/^/   /'
$PY $C/mutants.py $C/xcheck_p.py $WORD --json $WD/mutants.json | sed 's/^/   /'
$PY $C/mutants_p.py $C/xcheck_p.py $WORD --json $WD/mutants_p.json | sed 's/^/   /'

step "3. hub checkers: PR #545's v <= 120 form of PR #370's checker refuses (source writes) and its relaxed copy passes; PR #493's interface.py refuses"
$PY $A545/adapt.py $P $WORD $WD/ad545 | sed 's/^/   /'
if $PY $WD/ad545/chk/checkword.py $WORD $PC/pricing > $WD/stock.out 2> $WD/stock.err; then echo "stock-form checker accepted"; exit 1; fi
grep -q "x register written" $WD/stock.err && echo "   stock-form checker refuses, as expected: $(tail -1 $WD/stock.err)"
$PY $WD/ad545/chk/relax.py $WD/rchk > /dev/null
$PY $WD/rchk/checkword_mut.py $WORD $PC/pricing | tee $WD/checkword_mut.txt | sed 's/^/   /'
if $PY $B/independent/interface.py $WORD > $WD/iface493.out 2> $WD/iface493.err; then echo "PR #493 interface.py accepted"; exit 1; fi
grep -q "phase B writes a z register" $WD/iface493.err && echo "   PR #493 interface.py refuses, as expected: its check (4) requires phase B to write only targets"

step "4. official cohort checkers at (v, R): legality (NCOPY = 9), formal columns at five, nine and eleven stages, Gram witnesses"
$PY $B/export_records.py $WORD $WD/records | sed 's/^/   /'
$PY $B/regression/stage_cohort.py $WD/records $WD/records $WD/cin $WD/cout
$CXX -O2 -std=c++17 -DHDIM=8 -DNCOPY=9 $INC -o $BIN/legality $CK/legality_h.cpp &
$CXX -O2 -std=c++17 -DHDIM=8 $INC -o $BIN/legality_ncopy_h $CK/legality_h.cpp &
$CXX -O2 -std=c++17 -DHDIM=8 -DNCOPY=9 -DVPORTS=$V -DRHELP=$R $INC -o $BIN/columns_h_${V}_${R} $CK/columns_h.cpp &
wait
for K in 2 4 5; do $CXX -O2 -std=c++17 -DHDIM=8 -DNCOPY=9 -DVPORTS=$V -DRHELP=$R -DKPAIRS=$K $INC -o $BIN/columns_k$K $CK/columns_k.cpp & done
wait
$BIN/legality $WD/cin $WD/cout $WD/cout/legality.json > /dev/null
$BIN/columns_h_${V}_${R} $WD/cout/COHORT249-RECORDS.bin $WD/cout/columns.json > /dev/null 2> $WD/cout/columns.log
for K in 2 4 5; do $BIN/columns_k$K $WD/cout/COHORT249-RECORDS.bin $WD/cout/columns_k$K.json > /dev/null 2> $WD/cout/columns_k$K.log; done
$PY -c "
import json
V,R=$V,$R
l=json.load(open('$WD/cout/legality.json'));c=json.load(open('$WD/cout/columns.json'))
k4=json.load(open('$WD/cout/columns_k4.json'));k5=json.load(open('$WD/cout/columns_k5.json'));k2=json.load(open('$WD/cout/columns_k2.json'))
assert l['status']=='PASS_INDEPENDENT_COHORT_LEGALITY_SOURCE_OWNERS_AND_LIFECYCLE' and l['copies']==l['erasures']==9
assert l['rank_mass']==8*R+63+14*V
print('   legality PASS:',l['records'],'records,',l['common_frame_ADDs'],'common-frame ADDs, rank mass',l['rank_mass'],'= 8R + 63 + 14v; 9 COPY/ERASE')
assert c['status']=='PASS_NEW_COHORT249_ALL_FIVE_STAGE_FORMAL_COLUMNS_AND_PREFIX_BILL' and c['formal_columns_checked']==4*V+R
print('   five-stage formal columns PASS:',c['formal_columns_checked'],'physical columns over F2; prefix payload',c['payload_prefix_bits'],'bits < 104')
for k,S,nb in ((k4,9,18),(k5,11,24)):
    assert k['status']=='PASS_NEW_COHORT249_ALL_BRIDGED_STAGE_FORMAL_COLUMNS_AND_PREFIX_BILL'
    assert k['formal_columns_checked']==(S-1)*V+R and len(k['stages'])==S and k['bridge_additions']==nb*V
    assert len(k['negative_controls'])==nb and all(x['rejected'] for x in k['negative_controls'])
    assert dict(map(tuple,k['local_raw_H']))==dict(map(tuple,c['local_raw_H']))
    print('   %s-stage formal columns PASS (columns_k, KPAIRS = %d): %d columns, %d bridge additions, %d/%d omitted-bridge controls rejected, payload %d bits'%(['nine','eleven'][S==11],(S-1)//2,k['formal_columns_checked'],k['bridge_additions'],nb,nb,k['payload_prefix_bits']))
for d in (c,k2): d.pop('seconds')
assert c==k2;print('   regression: columns_k at KPAIRS = 2 reproduces the five-stage receipt field for field')"
$PY $WD/ad545/mutate_records.py $WD/records $WD/cin $WD/cout $BIN/legality $BIN/columns_k5 $BIN/legality_ncopy_h | tail -1 | sed 's/^/   /'
$PY $C/mutrec_b.py $WORD $WD/records $WD/cin $WD/cout $BIN/legality $BIN/columns_h_${V}_${R} $BIN/columns_k4 $BIN/columns_k5 | tail -1 | sed 's/^/   /'
$PY $CK/gram_frames.py $WD/records --gram e8ham --h 8 --positive | sed 's/^/   /'

step "5. geometry (live labels: PR #545's parameterised PR #386 / PR #445 files), nine-stage files parameterised"
mkdir -p $WD/nine $WD/bit
$PY $WD/ad545/nine_geometry.py --source $P --out $WD/nine --word $WORD > /dev/null
$PY $WD/ad545/eleven_geometry.py --source $P --out $WD/bit --word $WORD > /dev/null
$PYS $V510/code/adapt.py $VK $WD/adapted9 | sed 's/^/   /'
$PY $C/adapt9p.py $VK $V510/code $WD/adapted9/audit_parent_k.py $WD/a9p | sed 's/^/   /'

step "6. nine-stage whole-residual hosting and price (PR #510's chain, parameterised: PR #463 template and audits, 32 replicas; discovered hosting)"
o=$WD; mkdir -p $o/v9/nine; cp $WD/nine/GEOMETRY.json $o/v9/nine/GEOMETRY.json; ln -sfn $WD/records $o/v9/records
$PYS $WD/a9p/global_k.py --word $WORD --local-check $WD --out $o/v9/nine --isometries $ISO > $o/v9/global.log
$PYS $WD/a9p/audit_parent_k.py --local-check $WD --out $o/v9/nine --word $WORD > $o/v9/audit_parent.log
$PYS $WD/a9p/emit_k.py $o/v9/nine $WD $o/v9/hosted --selection $o/selection9.json --key bit --discover > $o/v9/emit.log
$PY -c "
import json,sys
a=json.load(open('$o/selection9.json'))['bit'];b=json.load(open('$HERE/data/selection9-r434.json'))['bit']
same=a['patterns']==b['patterns'] and a['stages']==b['stages']
print('   the hosting programme', 'rediscovers the shipped selection (data/selection9-r434.json) exactly' if same else 'returns another selection than data/selection9-r434.json')
sys.exit(0 if same else 1)"
$PYS $WD/a9p/audit_hosted_k.py $o/v9 $o/v9/hosted $o/v9/hosted/AUDIT.json > $o/v9/audit_hosted.log
$PYS $WD/a9p/assemble9.py $o/v9 $o/v9/hosted $o/v9/hosted/AUDIT.json $WD/root $o/RESULT9.json pr548,pr544,pr535,pr531
$PY -c "
import json
g=json.load(open('$o/v9/nine/GLOBAL.json'));ap=json.load(open('$o/v9/nine/AUDIT.json'));au=json.load(open('$o/v9/hosted/AUDIT.json'))
assert g['R']==$R and g['replicas']==32 and g['m']==64 and g['local_invocations']==9*32
assert ap['status']=='PASS_INDEPENDENT_COMPRESSED_BIT_TEMPLATE_AUDIT' and au['status']=='PASS_INDEPENDENT_REPLICATED_HOSTING_AUDIT'
assert au['hosted_residuals']==9*32*$R
print('   template %s (v %d): %d unbanked scalar columns, %d omitted bridge shears rejected; parent audit: %d template mutations rejected'%(g['status'],g['v'],g['independent_unbanked_scalar_columns'],len(g['omitted_bridge_shears_rejected']),len(ap['mutations_rejected'])))
print('   hosted audit PASS: %d of %d helper residuals hosted whole, %d banks, %d renamed instructions, %d mutations rejected, deficit %d'%(au['hosted_residuals'],9*32*$R,au['bank_assignments'],au['emitted_events'],len(au['mutations_rejected']),au['deficit']))"

step "7. eleven-stage whole-residual hosting and price (PR #493's chain as parameterised by PR #545's adapt.py; discovered hosting)"
$PY $WD/ad545/host_select.py $WORD $WD/hosting11.json > /dev/null
$PY -c "
import json,sys
a=json.load(open('$WD/hosting11.json'))['bit'];b=json.load(open('$HERE/data/hosting11-r434.json'))['bit']
same=a['patterns']==b['patterns'] and a['stages']==b['stages']
print('   PR #442 hosting programme (PR #545 host_select.py)',('rediscovers the shipped eleven-stage selection (data/hosting11-r434.json) exactly' if same else 'returns another selection'))
sys.exit(0 if same else 1)"
$PYS $WD/ad545/emit.py --word $WORD --local-check $WD --out $WD/bit --isometries $ISO --hosting $HERE/data/hosting11-r434.json > $WD/bit/emit.log
$PYS $WD/ad545/audit.py $WD $WD/nine $WD/bit > $WD/bit/audit.log
$PY $WD/ad545/assemble.py $WD/bit $R $P $WD/RESULT11.json pr548,pr544,pr535,pr531 $WD/root/data/complex-b.json
$PY -c "
import json;g=json.load(open('$WD/bit/GLOBAL.json'));a=json.load(open('$WD/bit/AUDIT.json'))
assert a['status']=='PASS_INDEPENDENT_ELEVEN_STAGE_HOSTING_AUDIT'
print('   template: 88 calls,',g['hosted_residuals'],'whole helper residuals hosted on idle data families (no banks),',g['independent_unbanked_scalar_columns'],'unbanked scalar columns restored, deficit',g['deficit'])
print('   independent audit PASS:',a['emitted_events'],'renamed instructions,',len(a['mutations_rejected']),'template mutations rejected, physical prefix',a['physical_prefix_bits'],'bits')"

step "8. summary against EXPECTED.json, E1's and P111-tuned's"
$PY $E/summary.py $HERE $WD
echo "== done  [$((SECONDS - T0))s]"

#!/usr/bin/env bash
# One-command verification of research/e8-bit-p111-e1: P111-tuned (PR #589) with one entrance-rank-1 helper.
# The E1 word is rebuilt from P111-tuned's shipped word (code/build_e1.py, byte for byte), replayed exactly by the
# E1 variant of P111's independent checker (code/xcheck_e1.py), passed through the same official cohort checkers, and
# priced by PR #510's nine-stage chain as parameterised by P111's code/adapt9p.py, with E1's residual isometries
# (code/make_iso_e1.py, code/isometry_e1.py, code/adapt_e1.py) and the hosting selection the chain's own programme
# discovers.  P111-tuned's verify.sh is unchanged and still checks the tuned word.
#   usage: bash research/e8-bit-p111-e1/verify.sh /fresh/output/dir
#   needs python3 >= 3.11 with numpy, sympy and scipy, a C++17 compiler (CXX, default c++) and Boost headers
#   (BOOST_INCLUDE, default /usr/include).
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd); WD=$(mkdir -p "$1" && cd "$1" && pwd)
TP=$(cd "$HERE/../e8-bit-p111-tuned" && pwd); P=$(cd "$HERE/../e8-bit-carrier-skeleton" && pwd)
case "$WD/" in "$HERE"/*|"$TP"/*|"$P"/*) echo "output dir must be outside the packages"; exit 2;; esac
export PYTHONDONTWRITEBYTECODE=1
PY="${PYTHON:-python3} -I -B"
PYS="${PYTHON:-python3} -E -s -B"     # scripts that import siblings from their own directory
CXX=${CXX:-c++}; BI=${BOOST_INCLUDE:-/usr/include}
E=$HERE/code; C=$TP/code; D=$TP/data; WORD=$HERE/data/bitE8mut-p111-e1.json.gz; TUNED=$TP/tune/bitE8mut-p111-tuned.json.gz
PC=$P/code; B=$PC/bit; CK=$B/checkers; INC="-I$P/portable-include -I$CK -I$BI"
V510=$TP/vendor/pr510/e8-r480-nine-stage; VK=$V510/vendor/e8-r715-eleven-stage-whole/code
A545=$TP/vendor/pr545/code
ISO=$HERE/data/residual-isometries-e1.json; BIN=$WD/bin; mkdir -p "$BIN"
V=$($PY -c "import json,gzip;print(json.load(gzip.open('$WORD','rt'))['v'])")
R=$($PY -c "import json,gzip;print(json.load(gzip.open('$WORD','rt'))['R'])")
T0=$SECONDS
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

step "1. the E1 word rebuilt from P111-tuned's shipped word; residual isometries rebuilt"
$PY $E/build_e1.py $WD/e1.json.gz | sed 's/^/   /'
cmp $WD/e1.json.gz $WORD
$PY $E/make_iso_e1.py $WORD $P/data/eleven/residual-isometries.json $WD/iso.json | sed 's/^/   /'
cmp $WD/iso.json $ISO
$PY -c "
import json,gzip
w=json.load(gzip.open('$WORD','rt'));t=json.load(gzip.open('$TUNED','rt'))
n=2*w['v']+w['R'];diff=[k for k in w if k not in ('A','C','D','start','stats') and w[k]!=t[k]]
assert not diff,diff
assert [r for r in range(n) if w['start'][r]!=t['start'][r]]==[470] and w['start'][470]==186 and t['start'][470]==0
assert t['A'][230]==[79,470,[77]] and t['A'][1993]==[79,444,[470]] and sorted(w['frames'][186])==[33,77]
assert w['A']==t['A'][:230]+[[186,444,[470]],[186,470,[77]]]+t['A'][231:1993]+[[186,444,[470]]]+t['A'][1994:]
print('   E1 = P111-tuned + {helper 248 (register 470) starts at frame 186 = span(root 33, root 77); one inserted A gate'
      ' [186, 444, [470]] before A[230]; A[230] and A[1993] moved from frame 79 to 186}; D recomputed, C = literal reverse;'
      ' everything else identical')"

step "2. independent exact replay (E1 variant of P111's xcheck_p.py), the interleaved interface lemma, mutation controls"
$PY $E/xcheck_e1.py $WORD --json $WD/xcheck.json | sed 's/^/   /'
$PY $C/mutants.py $E/xcheck_e1.py $WORD --json $WD/mutants.json | sed 's/^/   /'
$PY $C/mutants_p.py $E/xcheck_e1.py $WORD --json $WD/mutants_p.json | sed 's/^/   /'
if $PY $C/xcheck_p.py $WORD > $WD/xcheck_p.out 2>&1; then echo "   unmodified xcheck_p.py accepts the E1 word"
else echo "   unmodified xcheck_p.py refuses, as expected (helper 470 does not start at frame 0): $(tail -1 $WD/xcheck_p.out)"; fi

step "3. hub checker: PR #545's relaxed copy of PR #370's checker refuses (all-zero start)"
$PY $A545/adapt.py $P $WORD $WD/ad545 | sed 's/^/   /'
$PY $WD/ad545/chk/relax.py $WD/rchk > /dev/null
if $PY $WD/rchk/checkword_mut.py $WORD $PC/pricing > $WD/checkword_mut.txt 2> $WD/checkword_mut.err; then echo "relaxed checker accepted"; exit 1; fi
grep -q "for r in range(v,nreg): assert fdim\[cur\[r\]\]==0" $WD/checkword_mut.err && echo "   PR #545's relaxed checker refuses, as expected: it requires every target and helper to start at frame 0 (the all-zero start that E1 relaxes for helper 470; see README)"

step "4. official cohort checkers at (v, R): legality (NCOPY = 9), formal columns at five, nine and eleven stages, Gram witnesses"
$PY $B/export_records.py $WORD $WD/records | sed 's/^/   /'
$PY $B/regression/stage_cohort.py $WD/records $WD/records $WD/cin $WD/cout
$CXX -O2 -std=c++17 -DHDIM=8 -DNCOPY=9 $INC -o $BIN/legality $CK/legality_h.cpp &
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
assert l['rank_mass']==8*R+63+14*V-2
print('   legality PASS:',l['records'],'records,',l['common_frame_ADDs'],'common-frame ADDs, rank mass',l['rank_mass'],'= 8R + 63 + 14v - 2 (entrance rank 2); 9 COPY/ERASE')
assert c['status']=='PASS_NEW_COHORT249_ALL_FIVE_STAGE_FORMAL_COLUMNS_AND_PREFIX_BILL' and c['formal_columns_checked']==4*V+R
print('   five-stage formal columns PASS:',c['formal_columns_checked'],'physical columns over F2; prefix payload',c['payload_prefix_bits'],'bits')
for k,S,nb in ((k4,9,18),(k5,11,24)):
    assert k['status']=='PASS_NEW_COHORT249_ALL_BRIDGED_STAGE_FORMAL_COLUMNS_AND_PREFIX_BILL'
    assert k['formal_columns_checked']==(S-1)*V+R and len(k['stages'])==S and k['bridge_additions']==nb*V
    assert len(k['negative_controls'])==nb and all(x['rejected'] for x in k['negative_controls'])
    assert dict(map(tuple,k['local_raw_H']))==dict(map(tuple,c['local_raw_H']))
    print('   %s-stage formal columns PASS (columns_k, KPAIRS = %d): %d columns, %d bridge additions, %d/%d omitted-bridge controls rejected, payload %d bits'%(['nine','eleven'][S==11],(S-1)//2,k['formal_columns_checked'],k['bridge_additions'],nb,nb,k['payload_prefix_bits']))
for d in (c,k2): d.pop('seconds')
assert c==k2;print('   regression: columns_k at KPAIRS = 2 reproduces the five-stage receipt field for field')"
$PY $CK/gram_frames.py $WD/records --gram e8ham --h 8 --positive | sed 's/^/   /'

step "5. geometry (PR #545's parameterised PR #386 / PR #445 files), nine-stage files parameterised, E1 isometry validator"
mkdir -p $WD/nine
$PY $WD/ad545/nine_geometry.py --source $P --out $WD/nine --word $WORD > /dev/null
mkdir -p $WD/bit; $PY $WD/ad545/eleven_geometry.py --source $P --out $WD/bit --word $WORD > /dev/null
$PYS $V510/code/adapt.py $VK $WD/adapted9 | sed 's/^/   /'
$PY $C/adapt9p.py $VK $V510/code $WD/adapted9/audit_parent_k.py $WD/a9p | sed 's/^/   /'
$PY $E/adapt_e1.py $WD/a9p $WD/ad545 $ISO | sed 's/^/   /'

step "6. nine-stage whole-residual hosting and price (PR #510's chain, parameterised; 32 replicas; --no-banks and --host-all: every residual hosted; discovered selection)"
o=$WD; mkdir -p $o/v9/nine; cp $WD/nine/GEOMETRY.json $o/v9/nine/GEOMETRY.json; ln -sfn $WD/records $o/v9/records
$PYS $WD/a9p/global_k.py --word $WORD --local-check $WD --out $o/v9/nine --isometries $ISO --no-banks > $o/v9/global.log
$PYS $WD/a9p/audit_parent_k.py --local-check $WD --out $o/v9/nine --word $WORD > $o/v9/audit_parent.log
$PYS $WD/a9p/emit_k.py $o/v9/nine $WD $o/v9/hosted --selection $o/selection9.json --key bit --discover --host-all > $o/v9/emit.log
if [ -f $HERE/data/selection9-e1.json ]; then $PY -c "
import json,sys
a=json.load(open('$o/selection9.json'))['bit'];b=json.load(open('$HERE/data/selection9-e1.json'))['bit']
same=a['patterns']==b['patterns'] and a['stages']==b['stages']
print('   the hosting programme', 'rediscovers the shipped selection (data/selection9-e1.json) exactly' if same else 'returns another selection than data/selection9-e1.json')
sys.exit(0 if same else 1)"; fi
$PYS $WD/a9p/audit_hosted_k.py $o/v9 $o/v9/hosted $o/v9/hosted/AUDIT.json > $o/v9/audit_hosted.log
$PYS $WD/a9p/assemble9.py $o/v9 $o/v9/hosted $o/v9/hosted/AUDIT.json $WD/root $o/RESULT9.json pr548,pr544,pr535,pr531
$PY -c "
import json
from fractions import Fraction as F
g=json.load(open('$o/v9/nine/GLOBAL.json'));ap=json.load(open('$o/v9/nine/AUDIT.json'));au=json.load(open('$o/v9/hosted/AUDIT.json'))
assert g['R']==$R and g['replicas']==32 and g['m']==64 and g['local_invocations']==9*32 and g['entrance_rank_total']==2 and g['banks_per_stage'] is None
assert ap['status']=='PASS_INDEPENDENT_COMPRESSED_BIT_TEMPLATE_AUDIT' and au['status']=='PASS_INDEPENDENT_REPLICATED_HOSTING_AUDIT'
assert 'omit a residual route factor' in ap['mutations_rejected'] and au['bank_assignments']==0 and au['hosted_residuals']==9*32*$R
print('   template %s (v %d): entrance rank total %d, %d unbanked scalar columns; parent audit: %d template mutations rejected'%(g['status'],g['v'],g['entrance_rank_total'],g['independent_unbanked_scalar_columns'],len(ap['mutations_rejected'])))
print('   hosted audit PASS: %d of %d helper residuals hosted whole, %d banks, %d renamed instructions, %d mutations rejected, deficit %d'%(au['hosted_residuals'],9*32*$R,au['bank_assignments'],au['emitted_events'],len(au['mutations_rejected']),au['deficit']))"

step "7. eleven-stage whole-residual hosting and price (PR #493's chain as parameterised by PR #545's adapt.py; mixed-width nominator)"
$PY $E/host11_e1.py $WD/ad545 $WORD $WD/hosting11.json > /dev/null
$PY -c "
import json
a=json.load(open('$WD/hosting11.json'))['bit'];b=json.load(open('$HERE/data/hosting11-e1.json'))['bit']
same=a['patterns']==b['patterns'] and a['stages']==b['stages']
print('   the mixed-width nominator (code/host11_e1.py)',('rediscovers the shipped selection (data/hosting11-e1.json) exactly' if same else 'returns another selection; the shipped one is priced'))"
$PYS $WD/ad545/emit.py --word $WORD --local-check $WD --out $WD/bit --isometries $ISO --hosting $HERE/data/hosting11-e1.json > $WD/bit/emit.log
$PYS $WD/ad545/audit.py $WD $WD/nine $WD/bit > $WD/bit/audit.log
$PY $WD/ad545/assemble.py $WD/bit $R $P $WD/RESULT11.json pr548,pr544,pr535,pr531 $WD/root/data/complex-b.json
$PY -c "
import json;g=json.load(open('$WD/bit/GLOBAL.json'));a=json.load(open('$WD/bit/AUDIT.json'))
assert a['status']=='PASS_INDEPENDENT_ELEVEN_STAGE_HOSTING_AUDIT' and g['entrance_rank_total']==2
print('   template: 88 calls,',g['hosted_residuals'],'whole helper residuals hosted on idle data families (no banks), entrance rank total',g['entrance_rank_total'],', deficit',g['deficit'])
print('   independent audit PASS:',a['emitted_events'],'renamed instructions,',len(a['mutations_rejected']),'template mutations rejected, physical prefix',a['physical_prefix_bits'],'bits')"

step "8. summary against EXPECTED.json and P111-tuned's"
$PY -c "
import json,gzip,hashlib
from fractions import Fraction as F
e=json.load(open('$HERE/EXPECTED.json'));t=json.load(open('$TP/tune/EXPECTED.json'))
w=json.load(gzip.open('$WORD','rt'))
assert hashlib.sha256(open('$WORD','rb').read()).hexdigest()==e['word']['file_sha256']
assert hashlib.sha256(json.dumps(w,sort_keys=True,separators=(',',':')).encode()).hexdigest()==e['word']['content_sha256']
r=json.load(open('$WD/RESULT9.json'))
assert r['status']=='PASS_NINE_STAGE_WHOLE_HOSTED_BIT_PRICE_AND_CITED_ASSEMBLY'
assert r['bit_lower']==e['nine']['bit_lower'] and r['bit_profile']==e['nine']['bit_profile']
c=F(r['bit_lower']);c0=F(t['nine']['bit_lower'])
print('PASS bit c, nine stages (PR #510 chain, discovered hosting, all residuals hosted whole, 0 banks) =',r['bit_lower'],'=',r['bit_lower_decimal'])
print('     P111-tuned (PR #589):',t['nine']['bit_lower_decimal'],'; E1 %+.4f%%'%(float(c/c0-1)*100),'; c > P111-tuned:',c>c0)
assert c>c0
for k,x in r['kappa'].items():
    assert x['kappa']==e['nine']['kappa'][k]
    print('PASS kappa with %s complex b: %s = %s (%s-bound, %d/47 strict)'%(k,x['kappa'],x['kappa_decimal'],x['binding_component'],x['strict_outer_constraints']))
r11=json.load(open('$WD/RESULT11.json'))
assert r11['bit_lower']==e['eleven']['bit_lower']
c11=F(r11['bit_lower']);c110=F(t['eleven']['bit_lower'])
print('PASS bit c, eleven stages (PR #493 chain via PR #545, mixed-width hosting, no banks) =',r11['bit_lower'],'=',r11['bit_lower_decimal'])
print('     P111-tuned (PR #589) eleven stages:',t['eleven']['bit_lower_decimal'],'; E1 %+.4f%%'%(float(c11/c110-1)*100))
assert c11>c110"
echo "== done  [$((SECONDS - T0))s]"

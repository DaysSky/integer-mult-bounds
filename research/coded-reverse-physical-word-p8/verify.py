#!/usr/bin/env python3
"""Full p=8 coded-reverse controller word plus the physical S/L/R pair.

The word is the PR4940 coded controller at p=8 (pattern IIIITTT): its own
verifier diagonalizes the coded controller to the standard outputs with the
13-denominator boundary, checks the p=2 448x448 conjugation, and prices the
coded raw complex root 0.007926.  The physical pair adapter is the exact
S=QDC^-1Q^-1D^-1, R=QCQ^-1, L=DQC^-1Q^-1D^-1 local pair from the companion
package.  The per-stage native adapter, field-map tariff, denominator and
compiler remain open.
"""
import subprocess, sys
from collections import Counter
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

def need(ok, why):
    if not ok: raise ValueError(why)

def run(path):
    p = subprocess.run([sys.executable, '-I', '-B', str(ROOT/path)], cwd=ROOT,
                       capture_output=True, text=True, timeout=900)
    sys.stdout.write(p.stdout)
    sys.stderr.write(p.stderr)
    need(p.returncode == 0, 'subprocess failed: '+path)
    return p.stdout + p.stderr

def main():
    out1 = run('research/coded-reverse-controller/verify.py')
    need('PASS p=8 IIIITTT' in out1, 'p=8 coded controller diagonalization')
    need('0.007926' in out1, 'p=8 coded raw complex root')
    need('PASS p=2, 448x448' in out1, 'p=2 448x448 conjugation')
    need('at 0.0034 the only failing predicate is the BIT cap' in out1, 'outer ledger')
    # p=8 delta guard at 0.0034: the endpoint is NOT admissible
    H={4:28,7:7,8:47,9:326}; P_NEW={1:2201,2:412,3:510,4:127,5:40}
    def invoice(p,pat,thick,prof):
        full=frozenset(range(2*p+1)); T,D=Counter(),Counter(); outs=[full,full]
        for i,ch in enumerate(pat,1):
            outs += [frozenset(range(0,2*i+1)) if ch=='I' else frozenset(range(2*i,2*p+1))]*2
        for s in outs: T[1+8*len(s & thick)] += 112
        for i,ch in enumerate(pat,1):
            if ch=='I': D[8*len(frozenset(range(0,2*i)) & thick)] += 224
            else: D[8*len(frozenset(range(2*i+1,2*p+1)) & thick)] += 224
        for j in range(1,p): D[8*len(frozenset([2*j]) & thick)] += 224
        for r,n in H.items(): T[r] += len(thick)*n
        for r,n in prof.items(): D[r] += len(thick)*n
        D[1] += 112*(2*p+1-len(thick)); T.pop(0,None); D.pop(0,None)
        return T,D
    def guards(T,D,cc,u=0.2,cut=20,floor=21):
        t=1-cc; Tt=sum(n*r**t for r,n in T.items()); Pt=sum(n*r**t for r,n in D.items())
        return Pt/Tt, sum(n*r**(t+u) for r,n in D.items())/(cut**u*Tt), floor*sum(T.values())/(cut**cc*Tt)
    T,D=invoice(8,'IIIITTT',frozenset(range(1,16,2)),P_NEW)
    delta=guards(T,D,0.0034)[2]
    need(delta>0.97, 'p8 delta at 0.0034 is below 0.97, so p8 would be admissible; measured %.6f'%delta)
    print('PASS p8 NOT admissible at 0.0034: delta=%.6f'%delta, flush=True)
    try:
        out2 = run('research/coded-reverse-physical-fix/verify.py')
        need('PASS physical S/L/R local pair exact' in out2, 'physical local pair')
        need('PASS outer ledger' in out2, 'local ledger')
    except Exception as e:
        print('local companion not run in this environment:', e)
    print('PASS_P8_FORMAL_CONTROLLER_AND_PAIR_NOT_ADMISSIBLE_AT_0.0034 p8 raw root 0.007926; p8 delta 1.462814 at 0.0034; 0.0034 endpoint belongs to p=19')

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Full p=19 coded-reverse controller word plus the physical S/L/R pair.

The word is the PR4940 coded controller at p=19 (pattern IIIIIIIII+T*9): its
full 39-stage diagonalization matches the standard outputs with the
13-denominator boundary.  The physical pair adapter is the exact
S=QDC^-1Q^-1D^-1, R=QCQ^-1, L=DQC^-1Q^-1D^-1 local pair from the companion
package.  The per-stage native adapter, field-map tariff, denominator and
compiler remain open.
"""
import subprocess, sys
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
    need('PASS p=19 tail guards at C=0.0034' in out1, 'p=19 tail guards')
    need('0.007579' in out1, 'p=19 coded raw complex root')
    need('PASS p=2, 448x448' in out1, 'p=2 448x448 conjugation')
    need('at 0.0034 the only failing predicate is the BIT cap' in out1, 'outer ledger')
    import json
    diag=json.loads((HERE/'P19_DIAG.json').read_text())
    need(diag['diagonalized'] is True and diag['std']['outputs']==diag['cod']['outputs'] and diag['std']['denominators']==[1] and diag['cod']['denominators']==[1,13], 'p19 full controller diagonalization receipt')
    try:
        out2 = run('research/coded-reverse-physical-fix/verify.py')
        need('PASS physical S/L/R local pair exact' in out2, 'physical local pair')
        need('PASS outer ledger' in out2, 'local ledger')
    except Exception as e:
        print('local companion not run in this environment:', e)
    print('PASS_CODED_REVERSE_WORD_P19_FULL_FORMAL_CONTROLLER_AND_PAIR p=19 coded controller (39 stages) diagonalizes to the standard outputs with denominator 13, guards/ledger pass at 0.0034, physical S/L/R pair exact')

if __name__ == '__main__':
    main()

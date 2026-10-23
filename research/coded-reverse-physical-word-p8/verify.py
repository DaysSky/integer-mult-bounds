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
    out2 = run('research/coded-reverse-physical-fix/verify.py')
    need('PASS physical S/L/R local pair exact' in out2, 'physical local pair')
    need('PASS outer ledger' in out2, 'local ledger')
    print('PASS_CODED_REVERSE_PHYSICAL_WORD_P8 full p=8 coded controller + physical S/L/R pair; '
          'raw complex root 0.007926; outer BIT cap 0.0034')

if __name__ == '__main__':
    main()

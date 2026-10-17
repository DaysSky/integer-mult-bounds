#!/bin/bash
# exact S_n- and S_{n-1}xS_1-invariant max odd-or-zero systems in w^perp, w = (1^n; t), t != 3
O=../lor3/orbits2.py
for t in 0 1 2 4; do
  for n in 5 6 7 8 9 10 11 12 13 14 17 18; do
    w2=$((n - t*t)); [ $w2 -le 0 ] && continue
    [ $t -eq 4 ] && [ $n -lt 17 ] && continue
    for blocks in "$n" "$((n-1)),1"; do
      echo "== t=$t n=$n blocks=$blocks (w^2=$w2)"
      timeout 900 python3 -u $O $n $t 2 3 2,-2,4,-4,6,-6 $blocks 2>&1 | grep -E "MAX|orbits|edges|Error|error" 
    done
  done
done

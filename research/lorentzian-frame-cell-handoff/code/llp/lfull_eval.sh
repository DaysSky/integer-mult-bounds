#!/bin/bash
# usage: lfull_eval.sh system.json tag  -- top-level sharing/kappa (lmatch3), first-frame layer (lframe1), middle
# capacity screen (lmidcap) for a union in-chain frame design.
set -e
S=$1; T=$2
python3 lmatch3.py "$S" "parts_$T.json"
python3 lmidcap.py "$S" "parts_$T.json"
python3 lframe1.py "$S" "parts_$T.json" 240

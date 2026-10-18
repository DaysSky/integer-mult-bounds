# Notice

Apache-2.0 (`LICENSE`, copied from E1's package, itself #493's). Prepared by DaysSky with assistance from Claude.

## New in this package

- `code/gen_p4.py`: a modified copy of P111's `code/gen_p3.py` (PR #555, eumemic), with two listed edits. The first adds
  cell-sum helpers as a second kind of extra. The second makes `make()`/main read an explicit keeper plan (freeline,
  thirds, receivers, extras) from the parameter file instead of `plan_thirds`' random draw. The file keeps gen_p3's
  attribution line; everything else is gen_p3's.
- `code/census.py`: the exhaustive block-local keeper-plan census, its two calibrations against full builds, and the
  all-puncture-set combination. It imports only the geometry, the plan and `derive`/`ex_part`/`eligible` from gen_p3.
- `code/summary.py`: adapted from P111-tuned's `tune/summary.py` (PR #589).
- `data/params.json`: the keeper plan of the R = 434 word.
- `data/params-p111.json`: P111's own keeper plan written out explicitly (the byte-for-byte control).
- `data/bitE8mut-p111-r434.json.gz`: the word.
- `data/selection9-r434.json` and `data/hosting11-r434.json`: the hosting programmes' selections, rediscovered by
  `verify.sh`.
- `verify.sh`, `EXPECTED.json`, `README.md`, `MANIFEST.sha256`.

## Used from the repository, unchanged

- `research/e8-bit-p111` (PR #555, eumemic): `code/gen_p3.py` is imported by `census.py`. `planio.py`, `nodeopt.py`
  and `pwordl.py` are imported by `gen_p4.py`. Its shipped word is the byte-for-byte control.
- `research/e8-bit-p111-tuned` (PR #589, DreamingOfClouds):
  - P111's code: `xcheck_p.py`, `mutants*.py`, `mutrec_b.py` and `adapt9p.py`;
  - its data: #543's `plan-l3.json` and `complex-b.json`;
  - its vendored PR #510 and PR #545 files;
  - its `tune/EXPECTED.json`, used as a baseline only.
- `research/e8-bit-p111-e1`: its `EXPECTED.json`, used as a baseline only.
- `research/e8-bit-carrier-skeleton` (PR #493, eumemic): the skeleton modules, official cohort checkers, record
  exporter, geometries, eleven-stage chain, hosting programme and engines.

## Ideas used

- PR #555 (eumemic) and PR #545 (DreamingOfClouds): the punctured-star unit. This covers the pseudo-target totals, the
  phase-A mini-nodes at the block frames, extra carriers and junk wires.
- PR #543 (eumemic): the R420 L3 skeleton and its CP-SAT plan.
- PR #589 (DreamingOfClouds): P111-tuned and its package structure.
- E1: the entrance-rank-2 helper; this package does not use it.
- The hub pipelines and checkers listed in P111's NOTICE.

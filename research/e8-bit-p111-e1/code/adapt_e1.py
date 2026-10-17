"""Point the parameterised nine-stage chain (P111's code/adapt9p.py output) at E1's residual-isometry validator.
Two exact string edits (each anchor must occur exactly once), and code/isometry_e1.py is copied next to the scripts:
  global_k.py        from bank_routes_k import placement, validate_isometries
                  -> from bank_routes_k import placement; from isometry_e1 import validate_isometries
  audit_parent_k.py  from bank_routes import validate_isometries
                  -> from isometry_e1 import validate_isometries
With a second argument (PR #545's adapted eleven-stage directory) and the E1 isometry file, the eleven-stage chain is
pointed at the same validator and file:
  emit.py            from bank_routes import validate_isometries -> from isometry_e1 import validate_isometries
  local_audit.py     the same import edit; the frozen frame-zero isometry file -> the E1 file; the two assertions that
                     encode "all helpers enter at frame zero" (exactly one isometry record, entrance rank 0) are
                     dropped -- the audit still compares the template's residual_isometries and entrance_rank_total
                     with the values it recomputes, so they must equal the E1 file and the replayed rank (2).
Nothing else changes; isometry_e1.py's docstring lists its one change against the vendored function.
usage: adapt_e1.py A9P_DIR [AD545_DIR ISOMETRIES_JSON]"""
import shutil, sys
from pathlib import Path

d = Path(sys.argv[1]).resolve()
EDITS = {
    'global_k.py': [("from bank_routes_k import placement, validate_isometries\n",
                     "from bank_routes_k import placement; from isometry_e1 import validate_isometries   # E1 (adapt_e1.py)\n")],
    'audit_parent_k.py': [("from bank_routes import validate_isometries\n",
                           "from isometry_e1 import validate_isometries   # E1 (adapt_e1.py)\n")],
}
def apply(d, edits_by_file):
    for name, edits in edits_by_file.items():
        p = d / name; s = p.read_text()
        for a, b in edits:
            assert s.count(a) == 1, (name, a)
            s = s.replace(a, b)
        p.write_text(s)
    shutil.copy(Path(__file__).resolve().parent / 'isometry_e1.py', d / 'isometry_e1.py')
apply(d, EDITS)
print('E1 isometry validator wired into %s (2 edits)' % d.name)
if len(sys.argv) > 2:
    d2 = Path(sys.argv[2]).resolve()
    iso = str(Path(sys.argv[3]).resolve())
    imp = ("from bank_routes import validate_isometries\n", "from isometry_e1 import validate_isometries   # E1 (adapt_e1.py)\n")
    apply(d2, {'emit.py': [imp],
               'local_audit.py': [imp,
                                  ("iso=read(ROOT/'data/eleven/residual-isometries.json')", "iso=read(Path(%r))" % iso),
                                  (" and len(iso)==1\n", "\n"),
                                  ("rank=sum(dims[f] for f in initial[2*state['v']:]);assert rank==0",
                                   "rank=sum(dims[f] for f in initial[2*state['v']:])")]})
    print('E1 isometry validator and file wired into %s (emit.py 1 edit, local_audit.py 4 edits)' % d2.name)

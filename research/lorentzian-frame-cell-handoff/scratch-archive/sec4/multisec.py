"""All candidate flats (rank 3..5) feeding >= 2 design sections: stats of (rank, lines, #cells, #sections)."""
import pickle
from common import *
out = pickle.load(open('flats.pkl', 'rb'))
st = collections.Counter((r, pc(F), len(c), len(s)) for F, r, c, s in out if len(s) >= 2 and len(c) >= 2)
for k, n in sorted(st.items(), key=lambda kv: -kv[0][2] * kv[0][3]): print(k, n)

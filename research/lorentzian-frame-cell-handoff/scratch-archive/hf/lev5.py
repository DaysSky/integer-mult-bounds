# enumerate port-spanned subspaces of dim k (as frozenset of member ports + basis)
from e8 import *
import itertools, pickle, sys
def port_spans(k):
    seen={}
    # grow from (k-1)-spans by adding a port outside
    if k==1:
        for i in range(V): seen[basis([P[i]])]=None
        return list(seen)
    prev=port_spans_cache[k-1]
    for B in prev:
        Sp=span(B)
        for i in range(V):
            if P[i] not in Sp:
                nb=basis(list(B)+[P[i]])
                if nb not in seen: seen[nb]=None
    return list(seen)
port_spans_cache={}
for k in range(1,6):
    port_spans_cache[k]=port_spans(k)
    print(k, len(port_spans_cache[k]), flush=True)
pickle.dump(port_spans_cache, open('portspans.pkl','wb'))

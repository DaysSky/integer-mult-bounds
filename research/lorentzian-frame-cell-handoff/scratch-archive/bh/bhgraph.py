import json, pickle, collections, sys
d=json.load(open(sys.argv[1]))
order=[int(x) for x in d['order']]; R=set(int(x) for x in d['backward'])
C=set(int(x) for x in d['C']); J=set(int(x) for x in d['J'])
def mul(a,b): return ((a[0]*b[0]-a[1]*b[1])%3,(a[0]*b[1]+a[1]*b[0])%3)
def add(a,b): return ((a[0]+b[0])%3,(a[1]+b[1])%3)
E=[(r%3,r//3) for r in range(9)]; Z=(0,0); O=(1,0)
T=[(Z,Z,O)]+[(Z,O,E[r]) for r in range(9)]+[(O,E[r],E[s]) for r in range(9) for s in range(9)]
def dot(x,y):
    s=Z
    for a,b in zip(x,y): s=add(s,mul(a,b))
    return s
edges=[]
for i in range(91):
    js=sorted(j for j in range(91) if dot(T[i],T[j])==Z); assert len(js)==10
    edges+=[(i,91+j) for j in js]
pos={v:k for k,v in enumerate(order)}
phys=[e for q,e in enumerate(edges) if q not in R]
sessions=[]
for q in sorted(R-C-J):
    u,v=edges[q]; sessions.append((u,v) if pos[u]<pos[v] else (v,u))
adj=collections.defaultdict(list)
for u,v in phys: adj[u].append(v); adj[v].append(u)
def bfs(s):
    dist={s:0}; dq=collections.deque([s])
    while dq:
        x=dq.popleft()
        for y in adj[x]:
            if y not in dist: dist[y]=dist[x]+1; dq.append(y)
    return dist
print('edges',len(phys),'sessions',len(sessions),'dist',collections.Counter(bfs(s)[t] for s,t in sessions))
pickle.dump(dict(phys=phys,sessions=sessions),open('bh.pkl','wb'))

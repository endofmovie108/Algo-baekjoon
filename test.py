
N = 10

dr = [-1, -1, 0, 1, 1, 1, 0, -1]
dc = [0, 1, 1, 1, 0, -1, -1, -1]

def moveBall(r, c, s, d):
    #s%=N
    rt, ct = r + s*dr[d], c + s*dc[d]
    if rt < 0: rt = (N - abs(rt)%N)
    if ct < 0: ct = (N - abs(ct)%N)
    rt = rt % N
    ct = ct % N
    return rt, ct

maps = [[0]*N for _ in range(N)]

def printMaps(maps):
    for m in maps:
        print(m)
    print()

for d in range(8):
    r, c = 4, 4
    print(d)
    for i in range(20):
        maps[r][c] = 0
        r, c = moveBall(r, c, 100001, d)
        maps[r][c] = 1
        printMaps(maps)
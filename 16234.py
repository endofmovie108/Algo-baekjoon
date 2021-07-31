import sys
sys.setrecursionlimit(10000)
sys.stdin = open('input.txt', 'rt')
N, L, R = map(int, input().split())
maps = [list(map(int, input().split())) for _ in range(N)]

def inMaps(r, c):
    global N
    return 0<=r<N and 0<=c<N

def finderDFS(maps, visits, val_cur, r, c, nBor):
    dr = [0, 1, 0, -1]
    dc = [1, 0, -1, 0]
    if not inMaps(r, c):
        return
    if visits[r][c] == 1:
        return

    visits[r][c] = 1
    if L <= abs(val_cur-maps[r][c]) <= R:
        nBor.append([r, c])

    for i in range(4):
        rt, ct = r+dr[i], c+dc[i]
        finderDFS(maps, visits, val_cur, rt, ct, nBor)

def findNbor(maps):
    global N
    visits = [[0]*N for _ in range(N)]
    nBors = []
    for r in range(N):
        for c in range(N):
            val_cur = maps[r][c]
            nBor = []
            nBor.append([r, c])
            finderDFS(maps, visits, val_cur, r, c, nBor)
            if not len(nBor) > 1:
                nBor = []
            visits[r][c] = 1
            if len(nBor) > 0:
                nBors.append(nBor)
    return nBors

def doAvg(maps, nBors):
    for nBor in nBors:
        if len(nBor) == 0: continue
        nBor_avgval=0
        for [r, c] in nBor:
            nBor_avgval += maps[r][c]
        nBor_avgval/=len(nBor)
        for [r, c] in nBor:
            maps[r][c] = int(nBor_avgval)

cnt = 0
while True:
    # find neighbors
    nBors = findNbor(maps)

    if len(nBors) == 0:
        break

    # do averaging
    doAvg(maps, nBors)
    cnt += 1

print(cnt)
print(maps)

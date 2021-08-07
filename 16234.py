import sys
sys.setrecursionlimit(10000) # 재귀 깊이 한도 올리기!
#sys.stdin = open('input.txt', 'rt')
N, L, R = map(int, input().split())
maps = [list(map(int, input().split())) for _ in range(N)]
dr = [0, 1, 0, -1]
dc = [1, 0, -1, 0]

def notInMaps(r, c):
    if 0<=r<N and 0<=c<N: return False
    else: return True

def findNbor(maps, visits, curr_val, rt, ct, Nbor, lv):
    global N, L, R, dr, dc
    if notInMaps(rt, ct): return
    if visits[rt][ct] == 1: return
    visits[rt][ct] = 1
    if lv == 0:
        Nbor.append([rt, ct])
    else:
        if L <= abs(curr_val-maps[rt][ct]) <= R:
            # if connected
            Nbor.append([rt, ct])
        else:
            return

    for i in range(4):
        findNbor(maps, visits, maps[rt][ct], rt+dr[i], ct+dc[i], Nbor, lv+1)

def findNbors(maps):
    global N, L, R
    Nbors = []
    for r in range(N):
        for c in range(N):
            Nbor = []
            visits = [[0] * N for _ in range(N)]
            findNbor(maps, visits, maps[r][c], r, c, Nbor, 0)
            if len(Nbor) > 1: Nbors.append(Nbor)
    return Nbors

def update(maps, Nbors):
    for Nbor in Nbors:
        avg_val = 0
        for [r, c] in Nbor:
            avg_val += maps[r][c]
        avg_val /= len(Nbor)
        avg_val = int(avg_val)
        for [r, c] in Nbor:
            maps[r][c] = avg_val

cnt = 0
while True:
    Nbors = findNbors(maps)
    if len(Nbors) == 0: break
    update(maps, Nbors)
    cnt += 1
    #printMaps(maps)
print(cnt)
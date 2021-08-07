import sys
sys.setrecursionlimit(10000) # 재귀 깊이 한도 올리기!
sys.stdin = open('input.txt', 'rt')
N, L, R = map(int, input().split())
maps = [list(map(int, input().split())) for _ in range(N)]
dr = [-1, 0, 1, 0] # up, right, down, left
dc = [0, 1, 0, -1]

def notInMaps(r, c):
    if 0<=r<N and 0<=c<N: return False
    else: return True

def meetCond(v1, v2):
    global L, R
    if L<= abs(v1 - v2) <=R: return True
    else: return False

def findNbor(maps, visits, curr_val, rt, ct, rt_prev, ct_prev, Nbor, cond_prev):
    global N, L, R, dr, dc
    if notInMaps(rt, ct): return
    if visits[rt][ct] == 1: return
    cond = meetCond(curr_val, maps[rt][ct])

    if len(Nbor) == 0 or cond:
        visits[rt][ct] = 1
        Nbor.append([rt, ct])
    else:
        return

    for i in range(4):
        findNbor(maps, visits, maps[rt][ct], rt+dr[i], ct+dc[i], rt, ct, Nbor, cond)

def findNbors(maps):
    global N, L, R
    Nbors = []
    visits = [[0] * N for _ in range(N)]
    for r in range(N):
        for c in range(N):
            Nbor = []
            findNbor(maps, visits, maps[r][c], r, c, r, c, Nbor, True)
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

def printMaps(maps):
    global N
    for r in range(N):
        for c in range(N):
            print(maps[r][c], end = ' ')
        print()

cnt = 0
while True:
    Nbors = findNbors(maps)
    if len(Nbors) == 0: break
    update(maps, Nbors)
    cnt += 1
    printMaps(maps)
print(cnt)
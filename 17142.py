import sys
from copy import deepcopy
from collections import deque as dq
sys.stdin = open('input.txt', 'rt')
N, M = map(int, input().split())
virusMaps = [list(map(int, input().split())) for _ in range(N)]

WALL = 1
EMPTY = 0
VIR_NONACT = 2
VIR_ACT = 3

NO_GO = -1
GO_EMPTY = 0
GO_NONACT = 1

dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1] # up, right, down, left

# functions
def printMaps(maps, lv):
    for m in maps:
        print(m)
    print(lv)
    print()

def virusMselDFS(virusSel, lv):
    global viursAll, virusMsels, V
    if lv >= V:
        return
    if len(virusSel) == 3:
        virusMsels.append(virusSel)
        return
    virusMselDFS(virusSel + [virusAll[lv]], lv + 1)
    virusMselDFS(virusSel, lv + 1)

def isVirusCanSpread(maps, r, c, chkMaps):
    if 0<=r<N and 0<=c<N and chkMaps[r][c] != 1:
        chkMaps[r][c] = 1
        if maps[r][c] == EMPTY:
            return GO_EMPTY
        elif maps[r][c] == VIR_NONACT:
            return GO_NONACT
        else:
            return NO_GO
    else:
        return NO_GO

def isAllVirusSpread(maps):
    for r in range(N):
        for c in range(N):
            if maps[r][c] == 0:
                return False
    else:
        return True

virusAll = []
V = 0
for r in range(N):
    for c in range(N):
        if virusMaps[r][c] == VIR_NONACT:
            virusAll.append([r, c])
            V += 1
virusMsels = []
virusMselDFS([], 0)
#print(virusMsels)

# make deque for BFS
virDq = dq()
for virusMsel in virusMsels:
    virusMaps_cpy = [[0]*N for _ in range(N)]
    for r in range(N):
        for c in range(N):
            if virusMaps[r][c] == 1:
                virusMaps_cpy[r][c] = WALL
            elif virusMaps[r][c] == 0:
                virusMaps_cpy[r][c] = EMPTY
            elif virusMaps[r][c] == 2:
                virusMaps_cpy[r][c] = VIR_NONACT

    # activate virus
    chkMaps = [[0]*N for _ in range(N)]
    vDq = dq()
    for virusSel in virusMsel:
        vDq.append([virusSel, 0])
        [r, c] = virusSel
        virusMaps_cpy[r][c] = VIR_ACT
        chkMaps[r][c] = 1

    virDq.append([virusMaps_cpy, vDq, 0, chkMaps])

# main, BFS 1
while virDq:
    vir = virDq.popleft()
    [virusMaps, vDq, lv, chkMaps] = vir

    # BFS 2
    atLeastOneSpread = False
    v_lv_prev = -1
    while vDq:
        [[v_r, v_c], v_lv] = vDq.popleft()
        if v_lv_prev > -1 and v_lv != v_lv_prev:
            vDq.append([[v_r, v_c], v_lv])
            break
        else:
            for dir in range(4):
                v_rt = v_r + dr[dir]
                v_ct = v_c + dc[dir]
                spreadCode = isVirusCanSpread(virusMaps, v_rt, v_ct, chkMaps)
                if spreadCode == NO_GO:
                    atLeastOneSpread = False

                elif spreadCode == GO_EMPTY:
                    atLeastOneSpread = True
                    vDq.append([[v_rt, v_ct], v_lv + 1])
                    virusMaps[v_rt][v_ct] = VIR_ACT

                elif spreadCode == GO_NONACT:
                    atLeastOneSpread = True
                    vDq.insert(1, [[v_rt, v_ct], v_lv])
                    virusMaps[v_rt][v_ct] = VIR_ACT
        v_lv_prev = v_lv

    printMaps(virusMaps, lv)
    if atLeastOneSpread:
        virDq.append([virusMaps, vDq, lv+1, chkMaps])
    else:
        isSuccess = isAllVirusSpread(virusMaps)
        if isSuccess:
            print("success!", lv)
            break


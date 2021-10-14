import sys
from collections import deque as dq
from copy import deepcopy
sys.stdin = open('input.txt', 'rt')
N, M = map(int, input().split())
virusMaps = [list(map(int, input().split())) for _ in range(N)]

dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]
ACT_VIRUS = -1
WALL = 1
EMPTY = 0
NONACT_VIRUS = 2

# functions
def printMaps(maps):
    for m in maps:
        print(m)
    print()

def virusMselDFS(virusAll_list, lv, Msel_list, MselAll_list):
    if len(Msel_list) >= M:
        MselAll_list.append(Msel_list)
        return
    if lv >= len(virusAll_list):
        return
    virusMselDFS(virusAll_list, lv + 1, Msel_list + [virusAll_list[lv]], MselAll_list)
    virusMselDFS(virusAll_list, lv + 1, Msel_list, MselAll_list)

def isVirusCanSpread(maps, r, c):
    if 0<=r<N and 0<=c<N and maps[r][c] != WALL and maps[r][c] != ACT_VIRUS:
        if maps[r][c] == NONACT_VIRUS:
            spreadCode = NONACT_VIRUS
        else:
            spreadCode = EMPTY
    else:
        spreadCode = WALL
    return spreadCode

def isVirusSpreadSuccess(maps):
    for r in range(N):
        for c in range(N):
            if maps[r][c] == EMPTY:
                return False
    return True

# Main
virusAll_list = []
for r in range(N):
    for c in range(N):
        if virusMaps[r][c] == 2:
            virusAll_list.append([r, c])

print(len(virusAll_list), virusAll_list)
MselAll_list = []
virusMselDFS(virusAll_list, 0, [], MselAll_list)
print(len(MselAll_list), MselAll_list)

# create BFS
statsAll_BFS_dq = dq()
for Msel_list in MselAll_list:
    virusMaps_cpy = deepcopy(virusMaps)
    for [r, c] in Msel_list:
        virusMaps_cpy[r][c] = ACT_VIRUS
    isAllNONACT = False
    statsAll_BFS_dq.append([virusMaps_cpy, deepcopy(Msel_list), 0, isAllNONACT])

lv_tmp_prev = -1
while statsAll_BFS_dq:
    statsAll = statsAll_BFS_dq.popleft()
    [virusMaps_tmp, Msel_list_tmp, lv_tmp, isAllNONACT_tmp] = statsAll

    if lv_tmp != lv_tmp_prev:
        print(lv_tmp, isAllNONACT_tmp)
        printMaps(virusMaps_tmp)
    lv_tmp_prev = lv_tmp

    Msel_list_next = []
    atLeastOneSpread = False
    isAllNONACT = True
    for [r, c] in Msel_list_tmp:
        for d in range(4):
            rt, ct = r + dr[d], c + dc[d]
            spreadCode = isVirusCanSpread(virusMaps_tmp, rt, ct)
            if spreadCode != WALL:
                isAllNONACT &= (spreadCode == NONACT_VIRUS)
                virusMaps_tmp[rt][ct] = ACT_VIRUS
                Msel_list_next.append([rt, ct])
                atLeastOneSpread = True

    if not atLeastOneSpread:
        if isVirusSpreadSuccess(virusMaps_tmp):
            if isAllNONACT_tmp:
                print(lv_tmp - 1)
            else:
                print(lv_tmp)
            break
    else:
        statsAll_BFS_dq.append([virusMaps_tmp, Msel_list_next, lv_tmp+1, isAllNONACT])



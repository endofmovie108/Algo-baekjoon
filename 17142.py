import sys
from pytictoc import TicToc
from collections import deque as dq
from copy import copy
sys.stdin = open('input.txt', 'rt')
N, M = map(int, input().split())
virusMaps = [list(map(int, input().split())) for _ in range(N)]

dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]
t = TicToc()

EMPTY = 0
WALL = 1
NONACT_VIRUS = 2
ACT_VIRUS = 3

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

def isInMaps(rt, ct):
    return 0<=rt<N and 0<=ct<N

def isEmptyOrNonactThenSpread(virusMaps_curr, rt, ct, virus_dq_next, EmptyCNT_curr):
    spreadCode = virusMaps_curr[rt][ct]
    if spreadCode == EMPTY or spreadCode == NONACT_VIRUS:
        if spreadCode == EMPTY:
            EmptyCNT_curr -= 1
        virusMaps_curr[rt][ct] = ACT_VIRUS
        virus_dq_next.append([rt, ct])
        return True, EmptyCNT_curr
    else:
        return False, EmptyCNT_curr

def isAllVirusSpread(virusMaps_curr):
    for r in range(N):
        for c in range(N):
            if virusMaps_curr[r][c] == EMPTY:
                return False
    return True

def copyJY(outList, inList):
    for idx, inList_sub in enumerate(inList):
        outList[idx][:] = inList_sub[:]

t.tic()
# Main
# 0. select M virus
virusAll_list = []
EmptyCNT = 0
for r in range(N):
    for c in range(N):
        if virusMaps[r][c] == NONACT_VIRUS:
            virusAll_list.append([r, c])
        elif virusMaps[r][c] == EMPTY:
            EmptyCNT += 1
virusM_list = []
virusMselDFS(virusAll_list, 0, [], virusM_list)

# 1. create BFS deque
virCaseDq = dq()
for idx, virus_list in enumerate(virusM_list):
    # create maps
    virusMaps_cpy = [[0]*N for _ in range(N)]
    copyJY(virusMaps_cpy, virusMaps)
    # virusMaps_cpy = copy(virusMaps)
    for [r, c] in virus_list:
        virusMaps_cpy[r][c] = ACT_VIRUS
    lv = 0
    virCaseDq.append([virusMaps_cpy, dq(virus_list), lv, idx, EmptyCNT])

# 3. Main, BFS
while virCaseDq:
    [virusMaps_curr, virus_dq_curr, lv_curr, idx, EmptyCNT_curr] = virCaseDq.popleft()

    if EmptyCNT_curr == 0:
        print(lv_curr)
        break

    virus_dq_next = dq()
    atLeastOneSpread = False
    while virus_dq_curr:
        [r, c] = virus_dq_curr.popleft()
        for d in range(4):
            rt, ct = r + dr[d], c + dc[d]
            if isInMaps(rt, ct):
                flag, EmptyCNT_curr = isEmptyOrNonactThenSpread(virusMaps_curr, rt, ct, virus_dq_next, EmptyCNT_curr)
                if flag:
                    atLeastOneSpread = True

    if atLeastOneSpread:
        # continue BFS
        lv_next = lv_curr + 1
        virCaseDq.append([virusMaps_curr, virus_dq_next, lv_next, idx, EmptyCNT_curr])
else:
    print(-1)
t.toc()
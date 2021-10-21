import sys
from collections import deque as dq
sys.stdin = open('input.txt', 'rt')

N, M = map(int, input().split())
maps = [list(map(int, input().split())) for _ in range(N)]

EMPTY = -2
BLACK = -1
RNBW = 0
dr = [-1, 0, 1, 0]
dc = [0, -1, 0, 1]
group_list = [] # block_num, rnbw_num, row_rep, col_rep

# functions
def isInMaps(r, c): return -1<r<N and -1<c<N

def isNormalBlock(r, c):
    global maps
    return 0 < maps[r][c] < M+1

def isNotVisited(r, c, maps_chk):
    return maps_chk[r][c] == False

def groupFindBFS(r, c, maps_chk, maps_rnbw_chk):
    global maps, group_list
    block = maps[r][c]
    findDq = dq()
    findDq.append([r, c, block, 0])
    rep_r, rep_c = 1000, 1000
    block_num = 0
    rnbw_num = 0
    all_locs_list = []
    while findDq:
        [rf, cf, block, is_rnbw] = findDq.popleft()
        all_locs_list.append([rf, cf])
        block_num += 1
        if is_rnbw:
            maps_rnbw_chk[rf][cf] = True
            rnbw_num += 1
        else:
            if rf <= rep_r:
                rep_r = rf
                if cf <= rep_c:
                    rep_c = cf
            maps_chk[rf][cf] = True
        for d in range(4):
            rt, ct = rf + dr[d], cf + dc[d]
            if isInMaps(rt, ct):
                if maps[rt][ct] == block and isNotVisited(rt, ct, maps_chk):
                    maps_chk[rt][ct] = True
                    findDq.append([rt, ct, block, False])
                elif maps[rt][ct] == RNBW and isNotVisited(rt, ct, maps_rnbw_chk):
                    maps_rnbw_chk[rt][ct] = True
                    findDq.append([rt, ct, block, True])
    if block_num > 1:
        group_list.append([block_num, rnbw_num, rep_r, rep_c, all_locs_list])

def deleteGroup():
    global group_list, maps
    group_list.sort(key = lambda x:(x[0], x[1], x[2], x[3]), reverse = True)
    all_locs_list = group_list[0][4]
    for [r, c] in all_locs_list:
        maps[r][c] = EMPTY
    return group_list[0][0]

def printMaps():
    global maps
    for m in maps:
        print(m)
    print()

def gravity():
    global maps
    for c in range(N):
        for r in range(N-1, -1, -1):
            if isNormalBlock(r, c) or maps[r][c] == RNBW:
                empty_cnt = 0
                for rt in range(r+1, N):
                    if not isInMaps(rt, c) or maps[rt][c] == BLACK: break
                    if maps[rt][c] == EMPTY:
                        empty_cnt += 1
                tmp = maps[r+empty_cnt][c]
                maps[r+empty_cnt][c] = maps[r][c]
                maps[r][c] = tmp

def rotate():
    global maps
    maps_res = [[0]*N for _ in range(N)]
    for r in range(N):
        for c in range(N):
            maps_res[N-1-c][r] = maps[r][c]
    maps = maps_res.copy()

# main
total_score = 0
while True:
    maps_chk = [[False]*N for _ in range(N)]
    group_list = []
    for r in range(N):
        for c in range(N):
            if isNotVisited(r, c, maps_chk) and isNormalBlock(r, c):
                maps_rnbw_chk = [[False] * N for _ in range(N)]
                groupFindBFS(r, c, maps_chk, maps_rnbw_chk)

    if len(group_list) < 1: break
    B = deleteGroup()
    total_score += (B*B)
    gravity()
    rotate()
    gravity()
print(total_score)


from collections import deque as dq
import sys
sys.stdin = open('input.txt', 'rt')
N = int(input())
maps = [list(map(int, input().split())) for _ in range(N)]
lv = 0
DIR_UP = 0
DIR_RT = 1
DIR_DN = 2
DIR_LT = 3

maps_all = dq([[maps, lv]])

def DIR2RC(d_idx, i, j):
    global N, DIR_UP, DIR_RT, DIR_DN, DIR_LT
    if      d_idx == DIR_UP: r, c = j, i
    elif    d_idx == DIR_RT: r, c = i, (N-1)-j
    elif    d_idx == DIR_DN: r, c = (N-1)-j, i
    elif    d_idx == DIR_LT: r, c = i, j
    return r, c

# doMove
def doMove(mp, d_idx):
    global N
    mp_new = [[0]*N for _ in range(N)]
    mp_cands = [dq([]) for _ in range(N)]

    for i in range(N):
        for j in range(N):
            r, c = DIR2RC(d_idx, i, j)
            if mp[r][c] != 0: mp_cands[i].append(mp[r][c])

    for i in range(N):
        mp_cand = mp_cands[i]
        j_cnt = 0
        while mp_cand:
            mp = mp_cand.popleft()
            r, c = DIR2RC(d_idx, i, j_cnt)
            mp_new[r][c] = mp
            j_cnt += 1
    return mp_new

# doHap
def doHap(mp, d_idx):
    global N
    for i in range(N):
        for j in range(1, N):
            r, c = DIR2RC(d_idx, i, j)
            r_prev, c_prev = DIR2RC(d_idx, i, j-1)
            if mp[r][c] == mp[r_prev][c_prev]:
                mp[r_prev][c_prev] *= 2
                mp[r][c] = 0
    return mp

def findMaxBlock(mp):
    max_block = 0
    for i in range(N):
        for j in range(N):
            if mp[i][j] > max_block: max_block = mp[i][j]
    return max_block

# 0. BFS main
max_block_global = 0
while maps_all:
    mp, lv_c = maps_all.popleft()

    max_block_local = findMaxBlock(mp)
    if max_block_local > max_block_global:
        max_block_global = max_block_local

    for d_idx in range(4):
        mp_new = doMove(mp, d_idx)
        mp_new = doHap(mp_new, d_idx)
        mp_new = doMove(mp_new, d_idx)

        if lv_c < 5:
            maps_all.append([mp_new, lv_c+1])
print(max_block_global)

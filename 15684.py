# 사다리 연결이 가능한 모든 case를 탐색
# 모든 세로선 출발지 i에서 모든 세로선 종착지 i로 도착해야함

import sys
sys.stdin = open('input.txt', 'rt')
N, M, H = map(int, input().split()) # N: row size, H: col size
lad_stats = [list(map(int, input().split())) for _ in range(M)]

# 0, 1, 2 : left, down, right
dr = [0, 1, 0]
dc = [-1, 0, 1]
lad_dats = [[1]*N for _ in range(H)]

# update lad_stats
for lad_stat in lad_stats:
    a, b = lad_stat
    lad_dats[a-1][b-1] = 2
    lad_dats[a-1][b] = 0

# check all downs
all_downs = []
all_downs_cnt = 0
for r_idx in range(N):
    for c_idx in range(H):
        if lad_dats[r_idx][c_idx] == 1:
            all_downs.append([r_idx, c_idx])
            all_downs_cnt += 1

def lad_checker(lad_dats):
    for c_idx in range(H):
        loc_r, loc_c = 0, c_idx
        curr_stat = lad_dats[loc_r][loc_c]
        while True:
            loc_r += dr[curr_stat]
            loc_c += dc[curr_stat]
            if loc_r == H:
                if loc_c == c_idx:
                    out_flag = False
                    # good condition
                else:
                    out_flag = True
                    # bad condition
                break
        if out_flag:
            break
    else:
        return True
    return False

def DFS(l, change_cnt):
    global min_change_cnt
    if l >= all_downs_cnt:
        success_flag = lad_checker(lad_dats)
        if success_flag:
            if min_change_cnt < change_cnt:
                min_change_cnt = change_cnt
            return
        else:
            return

    r_idx_d, c_idx_d = all_downs[l]
    if c_idx_d < H-1 and :



min_change_cnt = 1e+10
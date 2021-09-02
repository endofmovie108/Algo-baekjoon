from collections import deque as dq
import sys
sys.stdin = open('input.txt', 'rt')

N, M, K = map(int, input().split())
shark_maps = [list(map(int, input().split())) for _ in range(N)]
shark_dirs = list(map(int, input().split()))
shark_dir_priors = [list(map(int, input().split())) for _ in range(4*M)]

dr = [-1, 1, 0, 0]
dc = [0, 0, -1, 1]

# smell maps
# [[ori_idx, time], [], [], ...]
# []
# []
smell_maps = []
for r in range(N):
    smell_maps_sub = []
    for c in range(N):
        smell_maps_sub.append([])
    smell_maps.append(smell_maps_sub)

# smell stats deque
# [[ori_idx, r, c, time], [], ...]
smell_stats_dq = dq([])

# find shark, save to status deque
# [
#  [ori_idx, row, col, dir],
#  [],
#  []
# ]
shark_stats_dq = dq([list() for _ in range(M)])
for r in range(N):
    for c in range(N):
        shark_idx_ori = shark_maps[r][c]
        if shark_idx_ori != 0:
            shark_stats_dq[shark_idx_ori - 1].append(shark_idx_ori)
            shark_stats_dq[shark_idx_ori - 1].append(r)
            shark_stats_dq[shark_idx_ori - 1].append(c)
            shark_stats_dq[shark_idx_ori - 1].append(shark_dirs[shark_idx_ori - 1])

def isInMaps(r, c):
    return 0<=r<N and 0<=c<N

def isNoSmell(r, c):
    return len(smell_maps[r][c]) == 0

def retDir(shark_idx_ori, dir):
    return shark_dir_priors[4*(shark_idx_ori-1)+dir-1]

# Main loop
while True:
    # 0. spread smell
    for i in range(len(shark_stats_dq)):
        shark_stat = shark_stats_dq.popleft()
        [shark_idx_ori, row, col, dir] = shark_stat
        # 0-1. mark to smell_maps
        smell_maps[row][col] = [shark_idx_ori, K]
        # 0-2. update stats
        smell_stats_dq.append([shark_idx_ori, row, col, K])
        shark_stats_dq.append(shark_stat)

    # 1. move shark
    for i in range(len(shark_stats_dq)):
        shark_stat = shark_stats_dq.popleft()
        [shark_idx_ori, row, col, dir] = shark_stat

        # 1-1. find non smell area
        cnt = 0
        for j in range(4):
            dir_s = retDir(shark_idx_ori, dir)
            ddir = dir_s[j]
            row_t, col_t = row + dr[ddir-1], col + dc[ddir-1]
            if isInMaps(row_t, col_t) and isNoSmell(row_t, col_t):
                row_r, col_r = row_t, col_t
                break
        else:
            # 1-2. go back to



        shark_stats_dq.append(shark_stat)


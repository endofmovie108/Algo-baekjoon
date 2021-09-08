from collections import deque as dq
import sys
sys.stdin = open('input.txt', 'rt')

N, M, K = map(int, input().split())
shark_maps = [list(map(int, input().split())) for _ in range(N)]
shark_dirs = list(map(int, input().split()))
shark_dir_priors = [list(map(int, input().split())) for _ in range(4*M)]

# up, down, left, right
dr = [-1, 1, 0, 0]
dc = [0, 0, -1, 1]

# shark maps
# [[shark_idx, 0, 0, 0, ...]]
# [[0, 0, 0, ...]]

# shark stats
# [[shark_idx, r, c, d], ...]
shark_stats = [[0, 0, 0, 0]]*M
for r in range(N):
    for c in range(N):
        shark_idx = shark_maps[r][c]
        if shark_idx != 0:
            shark_stats[shark_idx-1] = [shark_idx, r, c, shark_dirs[shark_idx-1]]

# smell_maps
# [[shark_idx, time], [0, 0], [0, 0], ...]
# [[0, 0], [0, 0], ...]
# [[0, 0], [0, 0], ...]
smell_maps = [[[0, 0]]*N for _ in range(N)]

# smell_stats
# [[[shark_idx, r, c, time]],
#  [[0, 0, 0, 0]],
#  [[0, 0, 0, 0]], ...]
smell_stats = [[] for _ in range(M)]

# def spreadSmells(shark_stats, smell_maps, smell_stats):
#     # Old smell
#     # deque를 copy로 삭제해야할 값을 찾고,
#     # time 이 0이 되거나 음수인 경우 해당 index의 deque를 del()로 삭제
#     for smell_stat in smell_stats:
#         del_cnt = 0
#         for sub_idx, smell_stat_sub in enumerate(smell_stat[0].copy()):
#             sub_idx -= del_cnt
#             [shark_idx, r, c, time] = smell_stat_sub
#             time -= 1
#             smell_stat_sub = [shark_idx, r, c, time]
#             if time < 1:
#                 del(smell_stat[0][sub_idx])
#                 smell_maps[r][c] = [0, 0]
#                 del_cnt += 1
#             else:
#                 smell_stat[0][sub_idx] = smell_stat_sub
#                 smell_maps[r][c] = [shark_idx, time]
#
#     # New smell
#     for shark_idx in range(1, M+1):
#         shark_stat = shark_stats[shark_idx-1]
#         [_, r, c, _] = shark_stat
#
#         # update smell_maps
#         smell_maps[r][c] = [shark_idx, K]
#
#         # update smell_stats
#         if len(smell_stats[shark_idx-1]) == 0:
#             smell_stats[shark_idx-1] = [[shark_idx, r, c, K]]
#         else:
#             smell_stats[shark_idx-1][0].append([shark_idx, r, c, K])

def spreadSmells(shark_stats, smell_maps, smell_stats):
    for shark_idx_pre, smell_stat in enumerate(smell_stats.copy()):
        del_cnt = 0
        for smell_idx_pre, smell_sta in enumerate(smell_stat.copy()):
            [shark_idx, r, c, t] = smell_sta
            smell_idx = smell_idx_pre - del_cnt
            if t <= 1:
                # 1. smell_stats 에서 삭제되어야
                del(smell_stats[shark_idx_pre][smell_idx])
                del_cnt += 1
                # 2. smell_maps 에서 삭제되어야
                smell_maps[r][c] = [0, 0]
            else:
                # 1. smell_stats 업데이트
                smell_stats[shark_idx_pre][smell_idx] = [shark_idx, r, c, t-1]
                # 2. smell_maps 를 업데이트
                smell_maps[r][c][1] = t-1
    # shark_stats에 대해 smell_stats, smell_maps 업데이트
    for shark_stat in shark_stats:
        [shark_idx, r, c, d] = shark_stat
        # 1. smell_stats 에 집어넣기
        smell_stats[shark_idx-1].append([shark_idx, r, c, K])
        # 2. smell_maps 업데이트
        smell_maps[r][c] = [shark_idx, K]

def returnDir(shark_dir_priors, shark_idx, dir, i):
    return shark_dir_priors[4*(shark_idx-1) + (dir-1)][i]-1

def isNoSmell(r, c, smell_maps):
    return 0<=r<N and 0<=c<N and smell_maps[r][c][0] == 0

def isMySmell(r, c, shark_idx, smell_maps):
    return 0<=r<N and 0<=c<N and smell_maps[r][c][0] == shark_idx

def moveShark(r, c, rt, ct, shark_idx, shark_maps, shark_stats, ii):
    # update shark_stats
    shark_stats[shark_idx-1] = [shark_idx, rt, ct, ii+1]
    # update shark_maps
    shark_maps[r][c] = 0
    shark_maps[rt][ct] = shark_idx

def moveSharks(shark_stats, shark_maps, smell_maps):
    for shark_stat in shark_stats:
        # cond 1: 아무 냄새가 안나는 곳
        [shark_idx, r, c, dir] = shark_stat
        for i in range(4):
            ii = returnDir(shark_dir_priors, shark_idx, dir, i)
            rt, ct = r+dr[ii], c+dc[ii]
            if isNoSmell(rt, ct, smell_maps):
                moveShark(r, c, rt, ct, shark_idx, shark_maps, shark_stats, ii)
                break
        else:
            # cond 2: 자신의 냄새로 back
            for i in range(4):
                ii = returnDir(shark_dir_priors, shark_idx, dir, i)
                rt, ct = r+dr[ii], c+dc[ii]
                if isMySmell(rt, ct, shark_idx, smell_maps):
                    moveShark(r, c, rt, ct, shark_idx, shark_maps, shark_stats, ii)
                    break
    shark_num = len(shark_stats)
    shark_num1 = shark_num-1
    shark_num2 = shark_num
    shark_idx_pre1 = 0
    while shark_idx_pre1 < shark_num1:
        shark_stat1 = shark_stats[shark_idx_pre1]
        [_, r1, c1, _] = shark_stat1
        shark_idx_pre2 = shark_idx_pre1 + 1
        while shark_idx_pre2 < shark_num2:
            shark_stat2 = shark_stats[shark_idx_pre2]
            [_, r2, c2, _] = shark_stat2
            if r1 == r2 and c1 == c2:
                del(shark_stats[shark_idx_pre2])
                shark_num1 -= 1
                shark_num2 -= 1
                shark_idx_pre2 -= 1
                if len(shark_stats) == 1: return True
            shark_idx_pre2 += 1
        shark_idx_pre1 += 1
    return False

def print_sharkMaps(cnt):
    print(cnt)
    for r in range(N):
        print(shark_maps[r])
    print()

    for r in range(N):
        print(smell_maps[r])
    print()
    print()

cnt = 0
spreadSmells(shark_stats, smell_maps, smell_stats)
#print_sharkMaps(cnt)
while True:
    cnt += 1

    # 1. Move sharks
    if moveSharks(shark_stats, shark_maps, smell_maps):
        print(cnt)
        break
    if cnt == 1000:
        print(-1)
        break
    # 0. Spread smells
    spreadSmells(shark_stats, smell_maps, smell_stats)

    #print_sharkMaps(cnt)


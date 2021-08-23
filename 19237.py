from collections import deque as dq
import sys
sys.stdin = open('input.txt', 'rt')


N, M, K = map(int, input().split())
maps = [list(map(int, input().split())) for _ in range(N)]
d_curr = list(map(int, input().split()))
d_priority = [list(map(int, input().split())) for _ in range(4*M)]
# 1, 2, 3, 4
# up, down, left, right
dr = [-1, 1, 0, 0]
dc = [0, 0, -1, 1]

# row, col, dir
shark_sta = [[0, 0, 0] for _ in range(N)]
shark_sta = dq(shark_sta)

# shark_idx, rest time
smell_maps = [[0, 0]*N for _ in range(N)]

# check
def isInArea(r, c):
    return 0<=r<N and 0<=c<N

def isNonSmell(r, c):
    return smell_maps[r][c] == 0

def moveShark(r, c, d, shark_idx):
    global maps, smell_maps, smell_sta
    # update maps
    maps[r][c] = shark_idx + 1
    # update smell_maps

    # append smell_sta

def isSharkCanMove(shark_sta, shark_idx):
    [r, c, d] = shark_sta[shark_idx]
    # (1) first, check initial direction area
    rt, ct = r + dr[d-1], c + dc[d-1]
    if isInArea(rt, ct):
        if isNonSmell(rt, ct):
            moveShark()

    smell_maps[r][c]
    if 0<=r<N and 0<=c<N and smell_maps[r][c] == 0:
        return True


# 0. find sharks
for r in range(N):
    for c in range(N):
        if maps[r][c] != 0:
            shark_sta[maps[r][c]-1][0] = r
            shark_sta[maps[r][c]-1][1] = c
            shark_sta[maps[r][c]-1][2] = d_curr[maps[r][c]-1]

# 1. set shark smell deque
shark_smell = dq([])

# 2. while True
while True:
    for shark_idx in range(M):
        isSharkCanMove(shark_sta, shark_idx)




import sys
from collections import deque as dq
sys.stdin = open('input.txt', 'rt')
N, M = map(int, input().split())
maps = [list(map(int, input())) for _ in range(N)]

ROAD = 1
WALL = 0
NOT_VISIT = 0
VISIT = 1

chk = [[NOT_VISIT]*M for _ in range(N)]
dr = [0, 1, 0, -1]
dc = [1, 0, -1, 0]

# functions
def isInMaps(r, c): return -1<r<N and -1<c<M

def minWayFinderBFS(N, M):
    global maps, chk
    N, M = N-1, M-1
    findDq = dq()
    findDq.append([0, 0, 1])

    while findDq:
        [r, c, l] = findDq.popleft()
        if not isInMaps(r, c) or chk[r][c] == VISIT or maps[r][c] == WALL:
            continue
        chk[r][c] = VISIT

        if r == N and c == M:
            print(l)
            break
        for d in range(4):
            rt = r + dr[d]
            ct = c + dc[d]
            findDq.append([rt, ct, l + 1])

# main
minWayFinderBFS(N, M)
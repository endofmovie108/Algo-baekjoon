import sys
from collections import deque as dq
from copy import deepcopy

# functions
def printMaps(maps):
    for r in range(H):
        print(maps[r])
    print()

def goLeft(c):
    if c == 0: return N-1
    else: return c-1

def goRight(c):
    if c == N-1: return 0
    else: return c+1

def isLeftCenterRightOK(ladMaps, r, c):
    return ladMaps[r][c] == 0 and ladMaps[r][goLeft(c)] == 0 and ladMaps[r][goRight(c)] == 0

def isCanConnect(ladMaps, r, c):
    canConnect = isLeftCenterRightOK(ladMaps, r, c)
    return canConnect

def playLadGame(ladMapsCur, lv):
    for c in range(N):
        ct = c
        for r in range(H):
            if ladMapsCur[r][ct] == 1:
                # 만약 가로선이 우측에 있다면
                ct = goRight(ct)
            elif ladMapsCur[r][goLeft(ct)] == 1:
                # 만약 가로선이 좌측에 있다면
                ct = goLeft(ct)
        if not ct == c:
            return False
    else:
        return True

sys.stdin = open('input.txt', 'rt')
N, M, H = map(int, input().split()) # N: COL, H: ROW, M: 이미 놓여있는 가로선의 수
conInfo = [list(map(int, input().split())) for _ in range(M)] # [a(row), b(col)]: b번 세로선과 b+1번 세로선을 a번 가로선 위치에서 연결함
ladMaps = [[0]*N for _ in range(H)]
for [a, b] in conInfo:
    ladMaps[a-1][b-1] = 1

ladMapsDq = dq()
lv = 0
ladMapsDq.append([ladMaps, lv])

while ladMapsDq:
    [ladMapsCur, lv] = ladMapsDq.popleft()
    printMaps(ladMapsCur)

    # level condition
    if lv > 3:
        print(-1)
        break

    # play ladder game
    gameEnd = playLadGame(ladMapsCur, lv)
    if gameEnd:
        print(lv)
        break

    for r in range(H):
        for c in range(N):
            if isCanConnect(ladMapsCur, r, c):
                ladMapsCur_cpy = deepcopy(ladMapsCur)
                ladMapsCur_cpy[r][c] = 1
                ladMapsDq.append([ladMapsCur_cpy, lv+1])
else:
    print(-1)






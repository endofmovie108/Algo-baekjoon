import sys
sys.stdin = open('input.txt', 'rt')
N = int(input())
maps = [list(map(int, input().split())) for _ in range(N)]
dr = [-1, 0, 0, 1] # up, left, right, down
dc = [0, -1, 1, 0]

def isSharkCanGo(r, c, s, chk):
    global N, maps
    if 0<=r<N and 0<=c<N and chk[r][c] == 0 and maps[r][c] <= s:
        chk[r][c] = 1
        return True
    else:
        return False

def isSharkCanEat(r, c, s):
    global maps
    if 0 < maps[r][c] < s:
        return True
    else:
        return False

d

def DFS(r, c, s, rc_new, chk, lv):
    if not isSharkCanGo(r, c, s, chk):
        return

    if isSharkCanEat(r, c, s):
        rc_new.append([r, c, lv, 0])

    for i in range(4):
        DFS(r+dr[i], c+dc[i], s, rc_new, chk, lv+1)

def decideWhatFish(rc_new, shark_r, shark_c, shark_s, shark_e):
    global maps
    for i in range(len(rc_new)):
        rc_new[i][3] = abs(shark_r - rc_new[i][0]) + abs(shark_c - rc_new[i][1])

    rc_new.sort(key=lambda x: (x[3], x[0], x[1]))
    shark_r, shark_c = rc_new[0][0], rc_new[0][1]
    maps[shark_r][shark_c] = 0
    shark_e += 1
    if shark_e >= shark_s:
        shark_s += 1
        shark_e = 0
    return shark_r, shark_c, shark_s, shark_e

# Main
# 1. find shark
for r in range(N):
    for c in range(N):
        if maps[r][c] == 9:
            maps[r][c] = 0
            shark_r, shark_c, shark_s, shark_e = \
                r, c, 2, 0

# 2. infinite loop
cnt = 0
while True:
    shark_r_prev, shark_c_prev = shark_r, shark_c
    chk = [[0]*N for _ in range(N)]
    rc_new = [] # row, col, level
    DFS(shark_r, shark_c, shark_s, rc_new, chk, 0)
    cnt += 1

    if not len(rc_new) > 0:
        print(cnt)
        break
    else:
        shark_r, shark_c, shark_s, shark_e = decideWhatFish(rc_new, shark_r, shark_c, shark_s, shark_e)



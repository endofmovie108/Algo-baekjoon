from collections import deque as dq
import sys
sys.stdin = open('input.txt', 'rt')
N, M = map(int, input().split())
maps = [list(input()) for _ in range(N)]

allHole = 0
redHole = 1
blueHole = 2
noHole = 3

# 0. find red, blue balls and hole
dr = [-1, 0, 1, 0] # up, right, down, left
dc = [0, 1, 0, -1]
R_r, R_c, B_r, B_c, H_r, H_c = 0, 0, 0, 0, 0, 0
for r in range(1, N-1):
    for c in range(1, M-1):
        if maps[r][c] == 'R': R_r, R_c = r, c
        if maps[r][c] == 'B': B_r, B_c = r, c
        if maps[r][c] == 'O': H_r, H_c = r, c

# 1. create deque for BFS (Red row, Red col, dist, Blue row, Blue col, dist)
RB = dq([[[R_r, R_c, 0, B_r, B_c, 0, 0], 0]])

def rev(i):
    return (i+2)%4

def moveOne(r, c, i):
    global dr, dc
    return r+dr[i], c+dc[i]

def moveTest(r, c, d, i):
    global dr, dc, maps
    d = 0
    flag = 0
    while True:
        rr, cc = r+dr[i], c+dc[i]
        if maps[rr][cc] != '#' and maps[rr][cc] != 'O':
            d += 1
            r, c = rr, cc
        elif maps[rr][cc] == 'O':
            d += 1
            r, c = rr, cc
            flag = 1
            break
        else:
            break
    return r, c, d, flag

def moveBalls(ballSta, i):
    global dr, dc, H_r, H_c, maps
    [R_r, R_c, R_d, B_r, B_c, B_d, ff] = ballSta
    R_rt, R_ct, R_dt, R_flag = moveTest(R_r, R_c, R_d, i)
    B_rt, B_ct, B_dt, B_flag = moveTest(B_r, B_c, B_d, i)

    if R_flag and not B_flag:
        return R_rt, R_ct, R_dt, B_rt, B_ct, B_dt, redHole
    elif B_flag and not R_flag:
        return R_rt, R_ct, R_dt, B_rt, B_ct, B_dt, blueHole

    # 만약 같은 위치라면 같은 방향으로 움직인 경우
    if R_rt == B_rt and R_ct == B_ct:
        # 조건 1, 두 공 모두 hole 이라면
        if R_rt == H_r and R_ct == H_c:
            return R_rt, R_ct, R_dt, B_rt, B_ct, B_dt, allHole

        # 조건 2, 벽에 멈춘것 이라면 짧은 움직임 거리를 갖는 ball이 우선권을 갖음.
        # Red가 우선권을 갖는 경우.
        if R_dt < B_dt:
            B_rt, B_ct = moveOne(B_rt, B_ct, rev(i))
            return R_rt, R_ct, R_dt, B_rt, B_ct, B_dt, noHole
        else:
            R_rt, R_ct = moveOne(R_rt, R_ct, rev(i))
            return R_rt, R_ct, R_dt, B_rt, B_ct, B_dt, noHole

    # 두 공 모두 벽에 의해 멈춘 경우
    return R_rt, R_ct, R_dt, B_rt, B_ct, B_dt, noHole

# 2. BFS
while RB:
    [ballSta, cnt] = RB.popleft()
    if ballSta[6] == redHole:
        print(cnt)
        break
    for i in range(4):
        R_rt, R_ct, R_dt, B_rt, B_ct, B_dt, flag = moveBalls(ballSta, i)
        ballSta_new = [R_rt, R_ct, R_dt, B_rt, B_ct, B_dt, flag]
        if (R_dt == 0 and B_dt == 0) or flag == blueHole or flag == allHole:
            continue
        else:
            #updateMaps(ballSta_new, ballSta, flag)
            if cnt < 10:
                RB.append([ballSta_new, cnt+1])
else:
    print(-1)
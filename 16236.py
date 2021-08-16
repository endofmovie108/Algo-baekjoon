import sys
from collections import deque as dq
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

def BFS(shark_r, shark_c, shark_s, chk):
    step = 0
    find_step = 0
    shark_dq = dq([[shark_r, shark_c, step]])
    chk[shark_r][shark_c] = 1
    find_flag = False
    res_list = []
    while shark_dq:
        [r, c, step] = shark_dq.popleft()

        if isSharkCanEat(r, c, shark_s):
            find_flag = True
            find_step = step
            res_list.append([r, c, step])

        # find_step < step 조건:
        # BFS 특성상, 해당 조건으로 다음 계층의 노드를 탐색중임을 알 수 있음
        # 다음 계층의 노드를 탐색중인것은 거리가 더 물고기들을 탐색중인 것 이므로
        # return 해야할 필요가 있다.
        if find_flag and find_step < step:
            return res_list

        for i in range(4):
            rt, ct = r+dr[i], c+dc[i]
            if isSharkCanGo(rt, ct, shark_s, chk):
                shark_dq.append([rt, ct, step+1])
    return res_list

def decideWhatFish(res_list, shark_s, shark_e):
    res_list.sort(key=lambda x:(x[2], x[0], x[1]))
    shark_r, shark_c, shark_step = res_list[0][0], res_list[0][1], res_list[0][2]
    shark_e += 1
    if shark_e >= shark_s:
        shark_s += 1
        shark_e = 0
    maps[shark_r][shark_c] = 0
    return shark_r, shark_c, shark_step, shark_s, shark_e

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

    res_list = BFS(shark_r, shark_c, shark_s, chk)

    if len(res_list) == 0:
        print(cnt)
        break
    else:
        shark_r, shark_c, step, shark_s, shark_e = decideWhatFish(res_list, shark_s, shark_e)
        cnt += step


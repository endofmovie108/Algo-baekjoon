import sys
sys.setrecursionlimit(10000) # 재귀 깊이 한도 올리기!
sys.stdin = open('input.txt', 'rt')

from collections import deque as dq

def dqRotRight(d):
    d.appendleft(d.pop())
    return d

def dqRotLeft(d):
    d.append(d.popleft())
    return d

def isNumExist(won_pan):
    res = False
    for r in range(N):
        for c in range(M):
            if won_pan[r][c] != 'x':
                return True

    return False # 하나라도 숫자가 없으면



def DFS_sameNumFinder(level, r, c, r_prev, c_prev, num_prev):
    global visitChk, won_pan, VISIT_NO, VISIT_YES, M, N

    visitChk[r][c] = VISIT_YES
    if level >= 1:
        atLeastOne = True
        if level == 1: # 인접이 두 개 일때
            won_pan[r][c] = 'x'
            won_pan[r_prev][c_prev] = 'x'
        else: # 인접이 세개 이상일 때
            won_pan[r][c] = 'x'
    else:
        atLeastOne = False

    dr = [0, 1, 0, -1]
    dc = [1, 0, -1, 0]
    for i in range(4):
        rr = r + dr[i]
        cc = c + dc[i]

        # 조건 1, row 조건이 0보다 작아지거나, N보다 같거나 커지면 안된다.
        if rr < 0 or rr > N-1: continue

        # 조건 2, col 조건이 0보다 작아지면 M-1이 되며, M-1보다 커지면 0이 된다.
        if cc < 0: cc = M-1
        if cc > M-1: cc = 0

        if visitChk[rr][cc] == VISIT_NO and won_pan[rr][cc] == num_prev:
            atLeastOne += DFS_sameNumFinder(level+1, rr, cc, r, c, won_pan[rr][cc])
    return atLeastOne

def print_res(won_pan, N, M):
    sum_val= 0
    for r in range(N):
        for c in range(M):
            if won_pan[r][c] != 'x': sum_val += won_pan[r][c]
    print(sum_val)

def rotation(xi, di, ki):
    global N, M, T, won_pan, visitChk, VISIT_NO, VISIT_YES, DIR_LEFT, DIR_RIGHT

    # 1. xi의 배수인 원판을 di 방향으로 ki 칸 회전
    for idx_won in range(N):
        # 1-1. xi의 배수인 원판
        if (idx_won + 1) % xi == 0:
            won_pan_sub = won_pan[idx_won]
            visitChk_sub = visitChk[idx_won]
            for idx_rot in range(ki):
                if di == DIR_LEFT:
                    visitChk_sub = dqRotLeft(visitChk_sub)
                    won_pan_sub = dqRotLeft(won_pan_sub)
                if di == DIR_RIGHT:
                    visitChk_sub = dqRotRight(visitChk_sub)
                    won_pan_sub = dqRotRight(won_pan_sub)
            won_pan[idx_won] = won_pan_sub
            visitChk[idx_won] = visitChk_sub
        # 1-2. xi의 배수가 아닌 원판은 skip
        else:
            continue

    # 2. 원판에 수가 남아있으면, 인접하면서 수가 같은 것을 모두 찾음
    # 2-1. 원판에 수가 남아있으면 진행
    numExist = isNumExist(won_pan)
    atLeast = 0
    if numExist:
        # 2-2. 인접하면서 수가 같은것을 찾아 'x'로 변경
        cnt = 0
        avg_val = 0
        for r in range(N):
            for c in range(M):
                if won_pan[r][c] != 'x':
                    avg_val += won_pan[r][c]
                    cnt += 1
                if won_pan[r][c] != 'x' and visitChk[r][c] == VISIT_NO:
                    atLeast += DFS_sameNumFinder(0, r, c, r, c, won_pan[r][c])
        if not atLeast:
            avg_val /= cnt
            for r in range(N):
                for c in range(M):
                    if won_pan[r][c] != 'x':
                        if won_pan[r][c] > avg_val:
                            won_pan[r][c] -= 1
                        elif won_pan[r][c] < avg_val:
                            won_pan[r][c] += 1

N, M, T = map(int, input().split())
won_pan = [dq(list(map(int, input().split()))) for _ in range(N)]
rot_seq = [list(map(int, input().split())) for _ in range(T)]

VISIT_YES = 1
VISIT_NO = 0
DIR_LEFT = 1  # 반시계
DIR_RIGHT = 0  # 시계

for idx, rot in enumerate(rot_seq):
    # visit check는 매 회전 seq 마다 초기화 해줘야!
    # 알고리즘과는 상관이 없다. DFS를 돌리기 위해 선언했기 때문
    visitChk = [dq([0] * M) for _ in range(N)] 
    rotation(rot[0], rot[1], rot[2])
print_res(won_pan, N, M)

#print(won_pan)
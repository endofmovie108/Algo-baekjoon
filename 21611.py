import sys
sys.stdin = open('input.txt', 'rt')

N, M = map(int, input().split())
maps = [list(map(int, input().split())) for _ in range(N)]
DS = [list(map(int, input().split()))for _ in range(M)]

def stepCalculator(N):
    n_step = (N*N-1)-1
    return n_step

# tornado step template
def stepTemplate(n_step):
    cnt = 0
    step = 2
    booHo = 1
    list_booHo = [1]
    list_res = [1]
    GO = True
    while GO:
        cnt += 1
        tmp = list_res[-1]+step
        if tmp > n_step:
            tmp -= 1
            GO = False
        list_res.append(tmp)
        list_booHo.append(booHo)
        if cnt % 2 == 1:
            booHo = booHo*-1
        if cnt % 2 == 0:
            step += 1
    return list_booHo, list_res

n_step = stepCalculator(N)
list_step = stepTemplate(n_step)

print(n_step)
print(list_step)

DIR_UP = 1
DIR_DN = 2
DIR_LT = 3
DIR_RT = 4

shark_row = (N+1)/2
shark_col = (N+1)/2

dr = [0, -1, 1, 0, 0]
dc = [0, 0, 0, -1, 1]

for i in range(M):
    d = DS[i][0]
    s = DS[i][1]

    # 0. 구슬 파괴
    for j in range(s):
        rt = shark_row + dr[d]
        ct = shark_col + dc[d]
        maps[rt][ct] = -1

    # 1. 토네이도 회전하며 빈칸으로 당겨오기



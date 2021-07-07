import sys
sys.stdin = open('input.txt', 'rt')
N = int(input())
dats = [list(map(int, input().split())) for _ in range(N*N)]
seats = [[0]*N for _ in range(N)]
dr = [0, 1, 0, -1]
dc = [1, 0, -1, 0]

def isIn(r, c):
    if 0 <= r < N and 0 <= c < N: return True
    else: return False

def isEmpty(r, c):
    global seats
    if seats[r][c] == 0: return True
    else: return False

def condition_check(stdt_idx):
    global dats, seats

    max_joha_cnt = 0
    max_empty_cnt = 0
    rr_sub_max = 0
    cc_sub_max = 0
    for rr in range(N-1, -1, -1):
        for cc in range(N-1, -1, -1):
            if not isEmpty(rr, cc): continue
            joha_cnt = 0
            empty_cnt = 0
            # 인접한 네 방향에
            for i in range(4):
                rr_sub = rr + dr[i]
                cc_sub = cc + dc[i]
                if not isIn(rr_sub, cc_sub): continue

                # 좋아하는 학생이 있으면 cnt
                if seats[rr_sub][cc_sub] in dats[stdt_idx][1:5]:
                    joha_cnt += 1
                # 빈자리 이면
                elif seats[rr_sub][cc_sub] == 0:
                    empty_cnt += 1

            # 조건 1. 좋아하는 학생이 가장 많은 자리라면
            if joha_cnt >= max_joha_cnt:

                # 조건 2. 조건 1을 만족하는 칸이 여러개 일때,
                if joha_cnt == max_joha_cnt:

                    if empty_cnt >= max_empty_cnt:

                        # 조건 3. 조건 2를 만족하는 칸이 여러개 일때
                        if empty_cnt == max_empty_cnt:
                            rr_sub_max = rr
                            cc_sub_max = cc

                        # 조건 2만 만족할 때
                        else:
                            rr_sub_max = rr
                            cc_sub_max = cc
                            max_empty_cnt = empty_cnt

                # 조건 1만 만족할 때
                else:
                    rr_sub_max = rr
                    cc_sub_max = cc

                    max_empty_cnt = empty_cnt
                    max_joha_cnt = joha_cnt
    return rr_sub_max, cc_sub_max

def areYouHappy():
    global seats, dats, N, dr, dc
    manjok = 0
    dats.sort(key=lambda x:x[0])
    print(dats)

    for rr in range(N):
        for cc in range(N):

            joha_cnt = 0
            for i in range(4):
                rr_sub = rr + dr[i]
                cc_sub = cc + dc[i]

                if not isIn(rr_sub, cc_sub): continue
                # 좋아하는 학생이 있으면 cnt
                if seats[rr_sub][cc_sub] in dats[seats[rr][cc]-1][1:5]:
                    joha_cnt += 1
            if joha_cnt == 1:
                manjok += 1
            elif joha_cnt == 2:
                manjok += 10
            elif joha_cnt == 3:
                manjok += 100
            elif joha_cnt == 4:
                manjok += 1000
    return manjok


for stdt_idx in range(0, N*N):
    if stdt_idx == 1:
        print()
    r, c = condition_check(stdt_idx)
    seats[r][c] = dats[stdt_idx][0]

print(seats)
print(areYouHappy())
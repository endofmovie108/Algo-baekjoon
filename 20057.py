def rot_90(m):
    sz=len(m)
    t=[[0]*sz for _ in range(sz)]
    for i in range(sz):
        for j in range(sz):
            t[sz-1-j][i] = m[i][j]
    return t


def Mover(rr, cc, dd, mm, ll):
    tmp1=(2*ll+1)
    tmp2=(2*ll+2)
    if 0<=mm<1:
        # left 1
        return rr, cc-1, 0
    elif 1<=mm<1+tmp1:
        # down 1
        return rr+1, cc, 1
    elif 1+tmp1<=mm<1+tmp1+tmp2:
        # right
        return rr, cc+1, 2
    elif 1+tmp1+tmp2<=mm<1+tmp1+tmp2+tmp2:
        # up
        return rr-1, cc, 3
    else:
        # left
        return rr, cc-1, 0

left_m=[
    [0.0, 0.0, 0.02, 0.0, 0.0],
    [0.0, 0.1, 0.07, 0.01, 0.0],
    [0.05, 0, 0, 0, 0],
    [0.0, 0.1, 0.07, 0.01, 0.0],
    [0.0, 0.0, 0.02, 0.0, 0.0]
]
down_m=rot_90(left_m)
right_m=rot_90(down_m)
up_m=rot_90(right_m)


def Dust_spreader(rr, cc, dd, mat):
    global FALL_DUST
    if dd==0: # left spread
        mm=left_m
    elif dd==1: # down spread
        mm=down_m
    elif dd==2: # right spread
        mm=right_m
    elif dd==3: # up spread
        mm=up_m
    sz=len(mm)
    sz_half=sz//2
    curr_dust=mat[rr][cc]
    rest_dust=curr_dust

    for r in range(sz):
        for c in range(sz):
            if mm[r][c] != 0:
                rt, ct=rr+(r-sz_half), cc+(c-sz_half)
                if 0<=rt<=N-1 and 0<=ct<=N-1:
                    # 내부에 있을때, 모래를 쌓음
                    mat[rt][ct]+=int(curr_dust*mm[r][c])
                else:
                    # 내부에 없을때, 모래는 밖으로 흘러내림
                    FALL_DUST+=int(curr_dust*mm[r][c])
                # 내부에 있건 없건, 상관없이 나머지 rest_dust 갱신
                rest_dust-=int(curr_dust*mm[r][c])

    # mm 전부 탐색하며, 나머지 rest_dust 구해짐
    # 나머지 alpha에 해당하는 모래도 내부에 있는지 없는지.
    if dd==0: rt, ct=rr, cc-1 # left
    elif dd==1: rt, ct=rr+1, cc # down
    elif dd==2: rt, ct=rr, cc+1 # right
    elif dd==3: rt, ct=rr-1, cc # up
    if 0<=rt<=N-1 and 0<=ct<=N-1:
        # 내부에 있을때, 모래를 쌓음
        mat[rt][ct]+=rest_dust
    else:
        # 내부에 없을때, 흘러내림
        FALL_DUST+=rest_dust

    # 지나간 자리는 0이 됨.
    mat[rr][cc]=0

import sys
sys.stdin = open('input.txt', 'rt')

N=int(input())
L=N//2
ir, ic, id=L, L, 0
mat=[list(map(int, input().split())) for _ in range(N)]
FALL_DUST=0
rr, cc, dd=ir, ic, id
for ll in range(L):
    # level
    # move number
    M=8*ll+8
    for mm in range(M):
        rr, cc, dd=Mover(rr, cc, dd, mm, ll)
        Dust_spreader(rr, cc, dd, mat)

print(FALL_DUST)
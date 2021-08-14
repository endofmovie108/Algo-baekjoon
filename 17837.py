import sys
from collections import deque as dq
sys.stdin = open('input.txt', 'rt')
W = 0
R = 1
B = 2
# right, left, up, down,
dr = [0, 0, 0, -1, 1]
dc = [0, 1, -1, 0, 0]

# NxN 의 크기, K개의 말
N, K = map(int, input().split())

# maps: 맵의 색깔
maps = [list(map(int, input().split())) for _ in range(N)]

# hMaps: horse 배치 현황
hMaps = []
for r in range(N):
    hMaps_r = []
    for c in range(N):
        hMaps_r.append(dq([]))
    hMaps.append(hMaps_r)

# hInfos: horse의 위치 및 순서
hInfos = [list(map(int, input().split())) + [0] for _ in range(K)]
hIdx = 0
hTrn = 1

# hMaps_reverse: reverse hMaps_sub
def hMaps_reverse(hMaps_sub):
    ret_dq = dq([])
    for i in range(len(hMaps_sub)):
        ret_dq.appendleft(hMaps_sub[i])
    return ret_dq

# hMaps_pop: pop i~ hMaps_sub from hMaps[r][c][i:]
def hMaps_pop_from_idx(hMaps, r, c, i):
    num = len(hMaps[r][c])
    ret_dq = dq([])
    for i in range(i, num):
        ret_dq.appendleft(hMaps[r][c].pop())
    return ret_dq

# hMaps_append: append list to deque
def hMaps_extend(hMaps, r, c, hMaps_sub_list):
    for l in hMaps_sub_list:
        hMaps[r][c].append(l)

# Update index, turn
def updateIdx(hIdx, hTrn):
    global K
    hIdx_tmp = (hIdx+1)
    if hIdx_tmp >= K:
        hTrn += 1
        hIdx_tmp = 0
    return hIdx_tmp, hTrn

# Update location
def updateLoc(r, c, d):
    global dr, dc
    return [r+dr[d], c+dc[d]]

# Update hMaps
def updatehInfo(hMaps, hInfos, r_new, c_new):
    hIdxs = hMaps[r_new][c_new]
    cnt = 0
    for hIdx in hIdxs:
        [r_past, c_past, d_past, i_past] = hInfos[hIdx]
        hInfos[hIdx] = [r_new+1, c_new+1, d_past, cnt]
        cnt += 1

# What is next color
def whatIsColor(maps, ll):
    [r, c] = ll
    global W, R, B
    if 0<=r<N and 0<=c<N: return maps[r][c]
    else: return B

# reverse dir
def reverseDir(d):
    if d == 1: return 2
    elif d == 2: return 1
    elif d == 3: return 4
    elif d == 4: return 3

def max4chk(hMaps, r, c):
    #print(len(hMaps[r][c]))
    if len(hMaps[r][c]) >= 4:
        return True
    else:
        return False

# Main
# 1. 먼저 말들의 배치
for idx, hInfo in enumerate(hInfos):
    [r, c, d, i] = hInfo
    hMaps_extend(hMaps, r-1, c-1, [idx])

# 2. while
while True:
    hInfo = hInfos[hIdx]
    [r, c, d, i] = hInfo
    r-=1
    c-=1
    # 2-1. 다음번 색상은?
    nextColor = whatIsColor(maps, updateLoc(r, c, d))
    # 2-2. 색상별 처리
    hMaps_sub = hMaps_pop_from_idx(hMaps, r, c, i)
    if nextColor == W:
        [rt, ct] = updateLoc(r, c, d)
        hMaps_extend(hMaps, rt ,ct, hMaps_sub)
        # update info
        updatehInfo(hMaps, hInfos, rt, ct)
    elif nextColor == R:
        [rt, ct] = updateLoc(r, c, d)
        hMaps_sub = hMaps_reverse(hMaps_sub)
        hMaps_extend(hMaps, rt, ct, hMaps_sub)
        # update info
        updatehInfo(hMaps, hInfos, rt, ct)
    elif nextColor == B:
        #rt, ct = r, c
        dt = reverseDir(d)
        rt, ct = updateLoc(r, c, dt)
        hInfos[hIdx][2] = dt
        if B == whatIsColor(maps, [rt, ct]):
            rt, ct = r, c
            hMaps_extend(hMaps, rt, ct, hMaps_sub)
            # update info
            updatehInfo(hMaps, hInfos, rt, ct)

        elif W == whatIsColor(maps, [rt, ct]):
            hMaps_extend(hMaps, rt, ct, hMaps_sub)
            # update info
            updatehInfo(hMaps, hInfos, rt, ct)
        elif R == whatIsColor(maps, [rt, ct]):
            hMaps_sub = hMaps_reverse(hMaps_sub)
            hMaps_extend(hMaps, rt, ct, hMaps_sub)
            # update info
            updatehInfo(hMaps, hInfos, rt, ct)


    else:
        print('ColorErr!')
    outchk = max4chk(hMaps, rt, ct)

    if hTrn > 1000:
        print(-1)
        break

    elif outchk:
        print(hTrn)
        break

    hIdx, hTrn = updateIdx(hIdx, hTrn)

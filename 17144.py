import sys
from collections import deque as dq
sys.stdin = open('input.txt', 'rt')
R, C, T = map(int, input().split())
dust_map = [list(map(int, input().split())) for _ in range(R)]

dr = [0, 1, 0, -1]
dc = [1, 0, -1, 0]

def print_2d(dat):
    print()
    for d in dat:
        print(d)

def find_gong(dust_map):
    global R, C
    for r in range(R):
        for c in range(C):
            if dust_map[r][c] == -1:
                return r, c

def in_boundary(r, c):
    global R, C
    if 0 <= r and r <= R-1 and 0 <= c and c <= C-1:
        return True
    else:
        return False

def hwaksan(dust_map, r_gong, c_gong):
    # copy dust_map
    global R, C
    dust_map_tmp = [[0]*C for _ in range(R)]
    dust_map_tmp[r_gong][c_gong] = -1
    dust_map_tmp[r_gong+1][c_gong] = -1

    # search all points
    for r in range(R):
        for c in range(C):
            dust_curr = dust_map[r][c]
            if dust_curr < 1: # 먼지가 없거나, 공기청정기면 continue
                continue

            dust_hwaksan = int(dust_curr/5)
            cnt_hwaksan = 0
            for i in range(4):
                rr, cc = r + dr[i], c + dc[i]
                if in_boundary(rr, cc) and dust_map[rr][cc] != -1: # 공기청정기가 있거나, 칸이 없으면
                    dust_map_tmp[rr][cc] += dust_hwaksan # 누적
                    cnt_hwaksan += 1
            dust_rest = dust_curr - dust_hwaksan * cnt_hwaksan
            dust_map_tmp[r][c] += dust_rest # 누적
    return dust_map_tmp

def soonhwan(dust_map, r_gong, c_gong):
    global R, C

    # 위쪽 공기청정기 순환 먼지 deque에 넣기
    up_gong_tmp = dq([])
    for i in range(1, C):
        up_gong_tmp.append(dust_map[r_gong][i])
    for i in range(r_gong-1, -1, -1):
        up_gong_tmp.append(dust_map[i][C-1])
    for i in range(C-2, -1, -1):
        up_gong_tmp.append(dust_map[0][i])
    for i in range(1, r_gong-1):
        up_gong_tmp.append(dust_map[i][c_gong])
    # 회전!
    up_gong_tmp.pop()
    up_gong_tmp.appendleft(0)
    # 값 대입
    for i in range(1, C):
        dust_map[r_gong][i] = up_gong_tmp.popleft()
    for i in range(r_gong-1, -1, -1):
        dust_map[i][C-1] = up_gong_tmp.popleft()
    for i in range(C-2, -1, -1):
        dust_map[0][i] = up_gong_tmp.popleft()
    for i in range(1, r_gong-1):
        dust_map[i][c_gong] = up_gong_tmp.popleft()



    r_gong += 1
    # 아래쪽 공기청정기 순환 먼지 deque에 넣기
    up_gong_tmp = dq([])
    for i in range(1, C):
        up_gong_tmp.append(dust_map[r_gong][i])
    for i in range(r_gong+1, R):
        up_gong_tmp.append(dust_map[i][C-1])
    for i in range(C-2, -1, -1):
        up_gong_tmp.append(dust_map[R-1][i])
    for i in range(R-2, r_gong, -1):
        up_gong_tmp.append(dust_map[i][c_gong])
    # 회전!
    up_gong_tmp.pop()
    up_gong_tmp.appendleft(0)

    # 값 대입
    for i in range(1, C):
#        print(r_gong, i)
        dust_map[r_gong][i] = up_gong_tmp.popleft()
    for i in range(r_gong+1, R):
#        print(i, C-1)
        dust_map[i][C-1] = up_gong_tmp.popleft()
    for i in range(C-2, -1, -1):

        dust_map[R-1][i] = up_gong_tmp.popleft()
    for i in range(R-2, r_gong, -1):
#        print(i, c_gong)
        dust_map[i][c_gong] = up_gong_tmp.popleft()

    return dust_map



#print_2d(dust_map)
r_gong, c_gong = find_gong(dust_map)
for t in range(T):
    # 1. 확산
    dust_map = hwaksan(dust_map, r_gong, c_gong)
    #print_2d(dust_map)
    dust_map = soonhwan(dust_map, r_gong, c_gong)
    #print_2d(dust_map)

res = 0
for d in dust_map:
    res += sum(d)

print(res + 2)
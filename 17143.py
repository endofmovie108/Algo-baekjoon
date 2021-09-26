import sys
sys.stdin = open('input.txt', 'rt')

dr = [-1, 1, 0, 0] # up, down, right, left
dc = [0, 0, 1, -1]

R, C, M = map(int, input().split())
sharkStats_dict = dict()
maps = [[0]*C for _ in range(R)]
for i in range(M):
    sharkIdx = i+1
    sharkStats_dict[sharkIdx] = list(map(int, input().split()))
    [r, c, s, d, z] = sharkStats_dict[sharkIdx]
    r, c, d = r-1, c-1, d-1
    sharkStats_dict[sharkIdx] = [r, c, s, d, z]
    maps[r][c] = sharkIdx

# define functions
def reverseDir(d):
    if d == 0: return 1
    elif d == 1: return 0
    elif d == 2: return 3
    elif d == 3: return 2

def isInMaps(r, c):
    return 0<=r<R and 0<=c<C

def moveSharksDict(sharkStats_dict):
    maps = [[0]*C for _ in range(R)]
    sharkStats_dict_cpy = sharkStats_dict.copy()
    for sharkIdx, [r1, c1, s1, dt, z1] in sharkStats_dict_cpy.items():
        rt, ct = r1, c1
        for m_idx in range(s1):
            rt, ct = rt + dr[dt], ct + dc[dt]
            if not isInMaps(rt, ct):
                rt, ct = rt - dr[dt], ct - dc[dt]
                dt = reverseDir(dt)
                rt, ct = rt + dr[dt], ct + dc[dt]
        sharkStats_dict[sharkIdx] = [rt, ct, s1, dt, z1]

        if maps[rt][ct] != 0:
            sharkIdx2 = maps[rt][ct]
            [r2, c2, s2, d2, z2] = sharkStats_dict[sharkIdx2]
            if z2 > z1:
                del(sharkStats_dict[sharkIdx])
            else:
                del(sharkStats_dict[sharkIdx2])
                maps[rt][ct] = sharkIdx
        else:
            maps[rt][ct] = sharkIdx
    return sharkStats_dict, maps


kingFishSizeSum = 0
for kingCol in range(C):
    # 가장 가까운 상어 찾기
    for row in range(R):
        if maps[row][kingCol] != 0:
            sharkEatIdx = maps[row][kingCol]
            maps[row][kingCol] = 0
            [r, c, s, d, z] = sharkStats_dict[sharkEatIdx]
            kingFishSizeSum += z
            del(sharkStats_dict[sharkEatIdx])
            break

    # 상어의 이동
    sharkStats_dict, maps = moveSharksDict(sharkStats_dict)
print(kingFishSizeSum)
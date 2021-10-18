import sys
sys.stdin = open('input.txt', 'rt')
N, M = map(int, input().split())
maps_tmp = [list(map(int, input().split())) for _ in range(N)]
maps = [[[0, False] for _ in range(N)] for _ in range(N)]
move_orders = [list(map(int, input().split())) for _ in range(M)]

dr = [0, -1, -1, -1, 0, 1, 1, 1]
dc = [-1, -1, 0, 1, 1, 1, 0, -1]
cross_idxs = [1, 3, 5, 7]
BASKET_IDX = 0
CLOUD_EXT_IDX = 1

for m in range(M):
    move_orders[m][BASKET_IDX]-=1
    move_orders[m][CLOUD_EXT_IDX]%=N
for r in range(N):
    for c in range(N):
        maps[r][c] = [maps_tmp[r][c], False]
del(maps_tmp)

# functions
def printMaps():
    for m in maps:
        print(m)
    print()

def isInMaps(r, c): return 0<=r<N and 0<=c<N

def genClouds(locs):
    global cloud_stats
    cloud_stats = locs

def clearClouds():
    global cloud_stats
    cloud_stats.clear()

def moveClouds(move_order):
    global cloud_stats, maps
    [d, s] = move_order
    for i, [r, c] in enumerate(cloud_stats):
        r_new, c_new = (N + r + s * dr[d]) % N, (N + c + s * dc[d]) % N
        #update maps
        maps[r][c][CLOUD_EXT_IDX] = False
        maps[r_new][c_new][CLOUD_EXT_IDX] = True
        #update cloud_stats
        cloud_stats[i][0], cloud_stats[i][1] = r_new, c_new

def waterCopyBug():
    global maps, cloud_just_gone
    res = []
    for locs in cloud_just_gone.keys():
        [r, c] = locs
        cnt = 0
        for d in range(4):
            cross_idx = cross_idxs[d]
            rt, ct = r + dr[cross_idx], c + dc[cross_idx]
            if isInMaps(rt, ct) and maps[rt][ct][BASKET_IDX] > 0:
                cnt += 1
        if cnt > 0: res.append([r, c, cnt])
    for [r, c, cnt] in res: maps[r][c][BASKET_IDX] += cnt

def fallRains():
    global cloud_stats, maps, cloud_just_gone
    cloud_just_gone.clear()
    for [r, c] in cloud_stats:
        maps[r][c][BASKET_IDX] += 1
        maps[r][c][CLOUD_EXT_IDX] = False
        cloud_just_gone[(r, c)] = True
    waterCopyBug()
    cloud_stats.clear()

def changeWaterToCloud():
    global cloud_stats, maps, cloud_just_gone
    cloud_locs = []
    total_rain = 0
    for r in range(N):
        for c in range(N):
            if maps[r][c][BASKET_IDX] >= 2 and (cloud_just_gone.get((r, c)) is None):
                maps[r][c][CLOUD_EXT_IDX] = True
                maps[r][c][BASKET_IDX] -= 2
                cloud_locs.append([r, c])
            total_rain += maps[r][c][BASKET_IDX]
    genClouds(cloud_locs)
    return total_rain

# main
cloud_stats = []
cloud_just_gone = {}
genClouds([[N-1, 0],
           [N-1, 1],
           [N-2, 0],
           [N-2, 1]])
for [r, c] in cloud_stats:
    maps[r][c][CLOUD_EXT_IDX] = True

for move_order in move_orders:
    moveClouds(move_order)
    fallRains()
    total_rain = changeWaterToCloud()
print(total_rain)
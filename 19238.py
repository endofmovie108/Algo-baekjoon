import sys
from collections import deque as dq
sys.stdin = open('input.txt', 'rt')
N, M, taxi_fuel = map(int, input().split())
maps = [list(map(int, input().split())) for _ in range(N)]
taxi_r, taxi_c = map(int, input().split())
taxi_r, taxi_c = taxi_r-1, taxi_c-1
people_locs = [list(map(int, input().split())) for _ in range(M)]
people_locs_dict = dict()

dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]

WALL = -2
ROAD = -1

# functions
def isInMaps(r, c):
    return 0<=r<N and 0<=c<N

def isFuelIsNotEnough(people_locs_dict, taxi_r, taxi_c, taxi_fuel):
    res_flag = False
    for v in people_locs_dict.values():
        [r, c, _, _] = v
        if (taxi_fuel >= (abs(taxi_r-r)+abs(taxi_c-c))):
            res_flag = True
            break
    return not res_flag

def selectNearestPersonBFS(maps, maps_chk, maps_chk_ori, people_locs_dict, taxi_r, taxi_c, taxi_fuel):
    if isFuelIsNotEnough(people_locs_dict, taxi_r, taxi_c, taxi_fuel):
        working = False
        return working, -1, taxi_fuel
    # copy maps_chk_ori
    for r in range(N):
        maps_chk[r][:] = maps_chk_ori[r][:]

    # find nearest person BFS
    findDq = dq()
    findDq.append([taxi_r, taxi_c, 0])
    used_fuel = 0
    working = True
    p_idxs = []
    p_idx = -1
    find_flag = False
    find_lv = -1

    while findDq:
        [r, c, lv] = findDq.popleft()
        if taxi_fuel < lv:
            return
        if find_flag == True and find_lv != lv:
            break
        maps_chk[r][c] = 1
        if maps[r][c] >= 0:
            p_idxs.append(maps[r][c])
            find_flag = True
            find_lv = lv

        for d in range(4):
            rt, ct = r + dr[d], c + dc[d]
            if isInMaps(rt, ct) and maps_chk[rt][ct] == 0 and maps[rt][ct] != WALL:
                findDq.append([rt, ct, lv+1])

    if find_flag:
        used_fuel = find_lv
        taxi_fuel -= used_fuel
        if taxi_fuel < 0:
            working = False
        else:
            working = True
            # find p_idx
            people_locs_sel = []
            if len(p_idxs) > 1:
                for idx in p_idxs:
                    tmp = people_locs_dict[idx].copy()
                    tmp.append(idx)
                    people_locs_sel.append(tmp)
                people_locs_sel.sort(key = lambda x:(x[0], x[1]))
                p_idx = people_locs_sel[0][4]
                # sorting
            else:
                p_idx = p_idxs[0]
    else:
        working = False
    return working, p_idx, taxi_fuel

def findShortestWayBFS(maps, maps_chk, maps_chk_ori, taxi_r, taxi_c, taxi_fuel, pr, pc):
    # fuel condition
    if taxi_fuel < (abs(taxi_r-pr)+abs(taxi_c-pc)):
        working = False
        return working, taxi_fuel

    # copy maps_chk_ori
    for r in range(N):
        maps_chk[r][:] = maps_chk_ori[r][:]

    findDq = dq()
    findDq.append([taxi_r, taxi_c, 0])

    working = False
    while findDq:
        [r, c, lv] = findDq.popleft()
        maps_chk[r][c] = 1

        if taxi_fuel < lv:
            break

        if r == pr and c == pc:
            used_fuel = lv
            taxi_fuel -= used_fuel
            if taxi_fuel < 0:
                working = False
            else:
                taxi_fuel += (2 * used_fuel)
                working = True
            break

        for d in range(4):
            rt, ct = r + dr[d], c + dc[d]
            if isInMaps(rt, ct) and maps_chk[rt][ct] == 0 and maps[rt][ct] != WALL:
                findDq.append([rt, ct, lv+1])

    return working, taxi_fuel



# place people and refactor map
maps_chk_ori = [[0]*N for _ in range(N)]
maps_chk = [[0]*N for _ in range(N)]
for r in range(N):
    for c in range(N):
        if maps[r][c] == 0:
            maps[r][c] = ROAD
        if maps[r][c] == 1:
            maps[r][c] = WALL
            maps_chk_ori[r][c] = 1

for p_idx, p_loc in enumerate(people_locs):
    [r, c, rd, cd] = p_loc
    maps[r-1][c-1] = p_idx
    people_locs_dict[p_idx] = [r-1, c-1, rd-1, cd-1]

# main
while people_locs_dict:
    working, p_idx, taxi_fuel = selectNearestPersonBFS(maps, maps_chk, maps_chk_ori, people_locs_dict, taxi_r, taxi_c, taxi_fuel)
    if not working:
        print(-1)
        break

    # move taxi
    [pr, pc, pdr, pdc] = people_locs_dict.pop(p_idx)
    maps[pr][pc] = ROAD
    taxi_r, taxi_c = pr, pc

    # find shortest way
    working, taxi_fuel = findShortestWayBFS(maps, maps_chk, maps_chk_ori, taxi_r, taxi_c, taxi_fuel, pdr, pdc)
    if not working:
        print(-1)
        break

    # move taxi
    taxi_r, taxi_c = pdr, pdc
else:
    print(taxi_fuel)



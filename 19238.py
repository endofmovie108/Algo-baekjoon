import sys
from collections import deque as dq

sys.stdin = open('input.txt', 'rt')

N, M, taxi_fuel = map(int, sys.stdin.readline().rstrip().rsplit())
maps = [list(map(int, sys.stdin.readline().rstrip().rsplit())) for _ in range(N)]
taxi_r, taxi_c = map(int, sys.stdin.readline().rstrip().rsplit())
taxi_r, taxi_c = taxi_r-1, taxi_c-1
people_locs_ori = [list(map(int, sys.stdin.readline().rstrip().rsplit())) for _ in range(M)]

dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]

WALL = -2
ROAD = -1

# classes
class taxiSta:
    def __init__(self, r, c, fuel):
        self.r = r
        self.c = c
        self.fuel = fuel

class personSta:
    def __init__(self, r, c, r_dst, c_dst):
        self.r = r
        self.c = c
        self.r_dst = r_dst
        self.c_dst = c_dst

# functions
def isInMaps(r, c):
    return 0 <= r < N and 0 <= c < N

def copy2dMaps(dst_maps, src_maps):
    for r_idx, src_map in enumerate(src_maps):
        dst_maps[r_idx] = src_map[:]
    return True

def isFuelEmpty(taxi_fuel):
    if taxi_fuel<0: return True
    else: return False

def isPersonIsHere(maps, r, c):
    if maps[r][c] >= 0: return True
    else: return False

def moveTaxiToPerson(taxi_sta, people_stats_list, maps, maps_chk, maps_chk_ori):
    #copy2dMaps(maps_chk, maps_chk_ori)
    maps_chk_dict = dict()

    findDq = dq()
    findDq.append([taxi_sta.r, taxi_sta.c, taxi_sta.fuel])
    working, find_flag = True, False
    find_r, find_c, find_idx, find_fuel = 1e+10, 1e+10, -1, -1

    while findDq:
        [taxi_r, taxi_c, taxi_fuel] = findDq.popleft()
        maps_chk_dict[(taxi_r, taxi_c)] = True
        #maps_chk[taxi_r][taxi_c] = True

        if isFuelEmpty(taxi_fuel):
            working = False
            break
        if find_flag and find_fuel != taxi_fuel:
            break
        if isPersonIsHere(maps, taxi_r, taxi_c):
            if not find_flag:
                find_flag = True
                find_fuel = taxi_fuel
            if taxi_r <= find_r:
                find_r, find_c = taxi_r, taxi_c
                find_idx = maps[find_r][find_c]
                if taxi_c < find_c:
                    find_r, find_c, find_idx = taxi_r, taxi_c, maps[find_r][find_c]
        for d in range(4):
            rt, ct = taxi_r + dr[d], taxi_c + dc[d]
            if isInMaps(rt, ct) and (maps_chk_dict.get((rt, ct)) is None) and maps[rt][ct] != WALL:
                findDq.append([rt, ct, taxi_fuel-1])

    taxi_sta.r, taxi_sta.c, taxi_sta.fuel = find_r, find_c, find_fuel
    working &= find_flag
    if working:
        # update maps
        maps[find_r][find_c] = ROAD

    return working, taxi_sta, people_stats_list, maps, find_idx

def movePersonToDest(find_idx, taxi_sta, people_stats_list, maps, maps_chk, maps_chk_ori):
    #copy2dMaps(maps_chk, maps_chk_ori)
    maps_chk_dict = dict()
    working = True
    find_flag = False
    find_r, find_c, find_fuel = 1e+10, 1e+10, -1
    used_fuel = taxi_sta.fuel

    findDq = dq()
    findDq.append([taxi_sta.r, taxi_sta.c, taxi_sta.fuel])
    p_sta = people_stats_list[find_idx]
    p_r, p_c, p_r_dst, p_c_dst = p_sta.r, p_sta.c, p_sta.r_dst, p_sta.c_dst

    while findDq:
        [taxi_r, taxi_c, taxi_fuel] = findDq.popleft()
        maps_chk_dict[(taxi_r, taxi_c)] = True
        #maps_chk[taxi_r][taxi_c] = True
        if isFuelEmpty(taxi_fuel):
            working = False
            break
        if taxi_r == p_r_dst and taxi_c == p_c_dst:
            find_r, find_c, find_fuel = p_r_dst, p_c_dst, taxi_fuel
            find_flag = True
            break

        for d in range(4):
            rt, ct = taxi_r + dr[d], taxi_c + dc[d]
            if isInMaps(rt, ct) and (maps_chk_dict.get((rt, ct)) is None) and maps[rt][ct] != WALL:
                findDq.append([rt, ct, taxi_fuel-1])

    used_fuel -= find_fuel
    taxi_sta.r, taxi_sta.c, taxi_sta.fuel = find_r, find_c, find_fuel
    working &= find_flag
    if working:
        # get fuel
        taxi_sta.fuel += (used_fuel + used_fuel)

    return working, taxi_sta, people_stats_list, maps

# main
# prepare maps, check array
maps_chk = [[False]*N for _ in range(N)]
maps_chk_ori = [[False]*N for _ in range(N)]
for r in range(N):
    for c in range(N):
        if maps[r][c] == 0:
            maps[r][c] = ROAD
        elif maps[r][c] == 1:
            maps[r][c] = WALL
            maps_chk_ori[r][c] = True

# set people, taxi location
people_stats_list = list()
for i in range(M):
    [r, c, r_dst, c_dst] = people_locs_ori[i]
    p_sta = personSta(r=r-1, c=c-1, r_dst=r_dst-1, c_dst=c_dst-1)
    maps[p_sta.r][p_sta.c] = i
    people_stats_list.append(p_sta)
taxi_sta = taxiSta(r=taxi_r, c=taxi_c, fuel=taxi_fuel)

people_num = M
while people_num:
    working, taxi_sta, people_stats_list, maps, find_idx = moveTaxiToPerson(taxi_sta, people_stats_list, maps, maps_chk, maps_chk_ori)
    if not working:
        print(-1)
        break

    working, taxi_sta, people_stats_list, maps = movePersonToDest(find_idx, taxi_sta, people_stats_list, maps, maps_chk, maps_chk_ori)
    if not working:
        print(-1)
        break
    people_num -= 1
else:
    print(taxi_sta.fuel)
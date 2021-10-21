import sys
from collections import deque as dq
sys.stdin = open('input.txt', 'rt')

# global variables
N, M, K = map(int, sys.stdin.readline().rstrip().rsplit())
A = [list(map(int, sys.stdin.readline().rstrip().rsplit())) for _ in range(N)]
tree_stats = [list(map(int, sys.stdin.readline().rstrip().rsplit())) for _ in range(M)]
maps = [[5]*N for _ in range(N)]

tree_alv_locs = {}
dr = [-1, -1, -1, 0, 0, 1, 1, 1]
dc = [-1, 0, 1, -1, 1, -1, 0, 1]

# functions
def isInMaps(r, c): return 0<=r<N and 0<=c<N

def appendAgeTo(locs_dict, tree_loc, age):
    if locs_dict.get(tree_loc) is None:
        locs_dict[tree_loc] = []
    locs_dict[tree_loc].append(age)

def revIdx(idx, lenn):
    return lenn-1-idx

def isTreeCanEatYB(age, tree_loc):
    (r, c) = tree_loc
    if maps[r][c] >= age:
        return True
    else:
        return False

def spring_and_summer():
    global tree_alv_locs, maps
    tree_alv_locs_cpy = tree_alv_locs.copy()
    for tree_loc in tree_alv_locs_cpy.keys():
        (r, c) = tree_loc
        TREE_ALV_AGES_list = tree_alv_locs[tree_loc]
        #if len(TREE_ALV_AGES_list) > 1: TREE_ALV_AGES_list.sort()
        TREE_ALV_AGES_list_cpy = TREE_ALV_AGES_list.copy()
        for idx, age in enumerate(TREE_ALV_AGES_list_cpy):
            lenn = len(TREE_ALV_AGES_list_cpy)
            idx = revIdx(idx, lenn)
            age = TREE_ALV_AGES_list[idx]
            if isTreeCanEatYB(age, tree_loc):
                maps[r][c] -= age
                TREE_ALV_AGES_list[idx] += 1
            else:
                if len(TREE_ALV_AGES_list[:idx]) > 0:
                    TREE_DEAD_AGES_list = TREE_ALV_AGES_list[:idx]
                    for age in TREE_DEAD_AGES_list:
                        maps[r][c] += int(age/2)
                    del(TREE_ALV_AGES_list[:idx])
        if len(TREE_ALV_AGES_list) < 1:
            del(tree_alv_locs[tree_loc])

def fall():
    global tree_alv_locs
    tree_alv_locs_cpy = tree_alv_locs.copy()
    for tree_loc in tree_alv_locs_cpy.keys():
        (r, c) = tree_loc
        TREE_ALV_AGES_list = tree_alv_locs_cpy[tree_loc]
        for age in TREE_ALV_AGES_list:
            if age % 5 == 0:
                for d in range(8):
                    rt, ct = r + dr[d], c + dc[d]
                    if isInMaps(rt, ct):
                        appendAgeTo(tree_alv_locs, (rt, ct), 1)

def winter():
    global maps, A
    for r in range(N):
        for c in range(N):
            maps[r][c] += A[r][c]

# main
tree_stats.sort(key = lambda x:(x[2], x[1], x[0]), reverse=True)
for [x, y, z] in tree_stats:
    x, y = x-1, y-1
    appendAgeTo(tree_alv_locs, (x,y), z)

for k in range(K):
    spring_and_summer()
    fall()
    winter()

res = 0
for tree_loc in tree_alv_locs.keys():
    res += len(tree_alv_locs.get(tree_loc))
print(res)


import sys
import heapq
sys.stdin = open('input.txt', 'rt')

# global variables
N, M, K = map(int, sys.stdin.readline().rstrip().rsplit())
A = [list(map(int, sys.stdin.readline().rstrip().rsplit())) for _ in range(N)]
tree_stats = [list(map(int, sys.stdin.readline().rstrip().rsplit())) for _ in range(M)]
maps = [[5]*N for _ in range(N)]

tree_allive = {}
tree_dead = {}
dr = [-1, -1, -1, 0, 0, 1, 1, 1]
dc = [-1, 0, 1, -1, 1, -1, 0, 1]

# functions
def isInMaps(r, c): return 0<=r<N and 0<=c<N

def heapqPushTo(tgt_dict, tgt_key, dat):
    if tgt_dict.get(tgt_key) is None:
        tgt_dict[tgt_key] = []
    heapq.heappush(tgt_dict[tgt_key], dat)

def heapqCreate(tgt_dict, tgt_key, dat_list):
    if tgt_dict.get(tgt_key) is None:
        tgt_dict[tgt_key] = []
    tgt_dict[tgt_key] = dat_list

def appendDict(tgt_dict, tgt_key, dat):
    if tgt_dict.get(tgt_key) is None:
        tgt_dict[tgt_key] = []
    tgt_dict[tgt_key].append(dat)

def spring():
    global tree_allive, tree_dead, maps
    empty_tree_locs = []
    for tree_loc in tree_allive.keys():
        t_allive_hq = tree_allive.get(tree_loc)
        (r, c) = tree_loc
        z_buf = []
        while t_allive_hq:
            z = heapq.heappop(t_allive_hq)
            if maps[r][c] - z >= 0:
                maps[r][c] -= z
                z += 1
                z_buf.append(z)
            else:
                heapqPushTo(tree_allive, tree_loc, z)
                break
        if t_allive_hq:
            while t_allive_hq:
                appendDict(tree_dead, tree_loc, heapq.heappop(t_allive_hq))
        if z_buf:
            while z_buf:
                heapqPushTo(tree_allive, tree_loc, z_buf.pop())
        else:
            empty_tree_locs.append(tree_loc)

    for tree_loc in empty_tree_locs:
        del(tree_allive[tree_loc])

def summer():
    global tree_dead, maps
    for tree_loc in tree_dead.keys():
        t_dead_list = tree_dead[tree_loc]
        (r, c) = tree_loc
        for z in t_dead_list:
            maps[r][c] += int(z/2)

def fall():
    global maps, tree_allive
    tree_allive_cpy = tree_allive.copy()
    for tree_loc in tree_allive_cpy.keys():
        (r, c) = tree_loc
        t_allive_hq = tree_allive_cpy[tree_loc]
        for z in t_allive_hq.copy():
            if z > 0 and z % 5 == 0:
                for d in range(8):
                    rt, ct = r + dr[d], c + dc[d]
                    if isInMaps(rt, ct):
                        heapqPushTo(tree_allive, (rt, ct), 1)

def winter():
    global maps, A
    for r in range(N):
        for c in range(N):
            maps[r][c] += A[r][c]

# main
for i, [x, y, z] in enumerate(tree_stats):
    x, y = x-1, y-1
    heapqPushTo(tree_allive, (x, y), z)

for k in range(K):
    tree_dead = {}
    spring()
    summer()
    fall()
    winter()

cnt = 0
for tree_loc in tree_allive.keys():
    t_allive_hq = tree_allive[tree_loc]
    cnt += len(t_allive_hq)
print(cnt)




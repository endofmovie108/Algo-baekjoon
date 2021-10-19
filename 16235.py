import sys
import heapq
sys.stdin = open('input.txt', 'rt')

# global variables
N, M, K = map(int, input().split())
A = [list(map(int, input().split())) for _ in range(N)]
tree_stats = [list(map(int, input().split())) for _ in range(M)]
maps = [[5]*N for _ in range(N)]

TREE_ALLIVE = 0
TREE_DEAD = 1

tree_stats_allive_dict = {}
tree_stats_dead_dict = {}
for i, [x, y, z] in enumerate(tree_stats):
    x -= 1
    y -= 1
    if tree_stats_allive_dict.get((x, y)) is None:
        tree_stats_allive_dict[(x, y)] = []
    heapq.heappush(tree_stats_allive_dict[(x, y)], [z, x, y])

# functions
def spring():
    global maps, tree_stats_allive_dict, tree_stats_dead_dict
    for k in tree_stats_allive_dict.keys():
        tree_stats_sub = []
        for t in range(len(tree_stats_allive_dict[k])):
            [z, x, y] = heapq.heappop(tree_stats_allive_dict[k])
            if maps[x][y] >= z:
                maps[x][y] -= z
                z += 1
                tree_stats_sub.append([z, x, y])
            else: # all dead
                if tree_stats_dead_dict.get((x, y)) is None:
                    tree_stats_dead_dict[(x, y)] = []
                tree_stats_dead_dict[(x, y)].append([z, x, y])
                break
        tree_stats_allive_dict[k] = heapq.heapify(tree_stats_sub)

def summer():
    global maps, tree_stats_allive_dict, tree_stats_dead_dict
    for k in tree_stats_dead_dict.keys():
        for tree_dead_stat in tree_stats_dead_dict[k]:
            [z, x, y] = tree_dead_stat
            maps[x][y] += int(z/2)

def fall():
    global maps, tree_stats_allive_dict, tree_stats_dead_dict
    for k in tree_stats_allive_dict.keys():
        for tree_allive_stat in tree_stats_allive_dict[k]:
            [z, x, y] = tree_allive_stat

for k in range(K):
    spring()
    print(tree_stats_allive_dict)
    summer()
    print(tree_stats_allive_dict)

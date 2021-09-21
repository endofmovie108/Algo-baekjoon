import sys
from copy import deepcopy
sys.stdin = open('input.txt', 'rt')

maps = [list(map(int, input().split())) for _ in range(4)]
print(maps)

# up, left-up, left, left-down, down, right-down, right, right-up
dr = [-1, -1, 0, 1, 1, 1, 0, -1]
dc = [0, -1, -1, -1, 0, 1, 1, 1]

def isInMaps(row, col):
    return 0 <= row < 4 and 0 <= col < 4

def isFishIdx(maps, row, col):
    return 1 <= maps[row][col] <= 16

def isSharkCanEatAndMove(maps, row, col):
    return isInMaps(row, col) and isFishIdx(maps, row, col)

def moveShark(maps, row, col, fishStats_dict, sharkStat):
    fish_idx = maps[row][col]
    [fish_row, fish_col, fish_dir] = fishStats_dict[fish_idx]
    if fish_row != row or fish_col != col:
        print("ERR!!!")

    # erase prev shark location
    [row_old, col_old, dir_old] = sharkStat
    maps[row_old][col_old] = 0

    # apply to maps, sharkStat
    maps[row][col] = -1
    sharkStat = [row, col, fish_dir]

    # delete fish of fishStats_dict
    del(fishStats_dict[fish_idx])
    return maps, sharkStat

def isFishCanMoveThenMove(maps, fish_idx_1, fish_row_2, fish_col_2, fish_dir_1, fishStats_dict):
    # fish 1의 이동 전 row, col
    [fish_row_1, fish_col_1, _] = fishStats_dict[fish_idx_1]

    if isInMaps(fish_row_2, fish_col_2): # fish 1의 이동 후 row, col
        if isFishIdx(maps, fish_row_2, fish_col_2): # fish거나 -> 움직임
            fish_idx_2 = maps[fish_row_2][fish_col_2]
            [_, _, fish_dir_2] = fishStats_dict[fish_idx_2]

            fishStats_dict[fish_idx_2] = [fish_row_1, fish_col_1, fish_dir_2]
            fishStats_dict[fish_idx_1] = [fish_row_2, fish_col_2, fish_dir_1] # direction은 그대로 가져감

            maps[fish_row_1][fish_col_1] = fish_idx_2
            maps[fish_row_2][fish_col_2] = fish_idx_1

            return True, maps, fishStats_dict

        elif maps[fish_row_2][fish_col_2] == 0: # 빈칸이거나 -> 움직임

            maps[fish_row_1][fish_col_1] = 0
            maps[fish_row_2][fish_col_2] = fish_idx_1
            fishStats_dict[fish_idx_1] = [fish_row_2, fish_col_2, fish_dir_1]

            return True, maps, fishStats_dict
        else: # 상어인 경우
            return False, maps, fishStats_dict
    else:
        return False, maps, fishStats_dict


def playSharkDFS(maps, fishStats_dict, sharkStat, level, eat_sum):
    print(level, eat_sum)
    # 물고기들의 움직임
    for fish_idx, [fish_row, fish_col, fish_dir] in fishStats_dict.items():

        for dir_idx in range(8):
            fish_dir_t = (fish_dir + dir_idx) % 8
            fish_row_t = fish_row + dr[fish_dir_t]
            fish_col_t = fish_col + dc[fish_dir_t]
            fishMoveSuccess, maps, fishStats_dict = isFishCanMoveThenMove(maps, fish_idx, fish_row_t, fish_col_t, fish_dir_t, fishStats_dict)
            if fishMoveSuccess: break
    # 상어가 갈 수 있는곳을 찾기
    [shark_row, shark_col, shark_dir] = sharkStat
    shark_dir_t = shark_dir
    # for dir_idx in range(8):
    #     shark_dir_t = (shark_dir + dir_idx) % 8
    #     leastOneFlag = False
    for i in range(4):
        shark_row_t = shark_row + dr[shark_dir_t]
        shark_col_t = shark_col + dc[shark_dir_t]
        if not isInMaps(shark_row_t, shark_col_t): break
        if isFishIdx(maps, shark_row_t, shark_col_t):
            fish_idx = maps[shark_row_t][shark_col_t]
            maps, sharkStat = moveShark(maps, shark_row_t, shark_col_t, fishStats_dict, sharkStat)
            playSharkDFS(maps.copy(), fishStats_dict.copy(), sharkStat, level+1, eat_sum+fish_idx)
            leastOneFlag = True
        # if leastOneFlag: break


# 0-1. fishStats_dict / fish_idx: [row, col, dir]
fishStats_dict = dict()
for r in range(4):
    for c in range(4):
        fish_idx = maps[r][2*c+0]
        fish_dir = maps[r][2*c+1]
        fishStats_dict[fish_idx] = [r, c, fish_dir-1]
fishStats_tmp = sorted(fishStats_dict.items())
fishStats_dict = dict()
for k, v in fishStats_tmp:
    fishStats_dict[k] = v
del(fishStats_tmp)

# 0-2. reset maps
maps_legacy = maps.copy()
maps = [[0]*4 for _ in range(4)]
for r in range(4):
    for c in range(4):
        maps[r][c] = maps_legacy[r][2*c+0]
del(maps_legacy)

# 1. sharkStat_list / [row, col, dir]
sharkStat = []
fish_idx = maps[0][0]
[_, _, fish_dir] = fishStats_dict[fish_idx]
del(fishStats_dict[fish_idx])
sharkStat = [0, 0, fish_dir]
maps[0][0] = -1

# main, DFS
playSharkDFS(maps, fishStats_dict, sharkStat, 0, fish_idx)
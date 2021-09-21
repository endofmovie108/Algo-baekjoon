import sys
import copy
sys.stdin = open('input.txt', 'rt')

# define global variables
DR = [-1, -1, 0, 1, 1, 1, 0, -1] # up, up-left, left, down-left, down, down-right, right, up-right
DC = [0, -1, -1, -1, 0, 1, 1, 1]
MAP_SIZE = 4
DIR_NUM = 8
MAX_EATIDXSUM = -1


# set maps, fishStats
maps = [list(map(int, input().split())) for _ in range(MAP_SIZE)]
fishStats_dict = dict()
for row in range(MAP_SIZE):
    for col in range(MAP_SIZE):
        fishIdx = maps[row][2*col+0]
        fishDir = maps[row][2*col+1]-1
        fishStats_dict[fishIdx] = [row, col, fishDir]
mapsLegacy = maps.copy()
maps = [[0]*MAP_SIZE for _ in range(MAP_SIZE)]
for row in range(MAP_SIZE):
    for col in range(MAP_SIZE):
        maps[row][col] = mapsLegacy[row][2*col+0] # remain fish index only
del(mapsLegacy)

# set shark status, maps
def sharkEatFish(sharkStat, tgt_row, tgt_col, maps, fishStats_dict, eatIdxSum):
    [shark_row, shark_col, shark_dir] = sharkStat

    # maps
    fishIdx = maps[tgt_row][tgt_col]
    maps[shark_row][shark_col] = 0
    maps[tgt_row][tgt_col] = -1

    # stat
    [fish_row, fish_col, fish_dir] = fishStats_dict[fishIdx]
    del(fishStats_dict[fishIdx])
    if fish_row != tgt_row or fish_col != tgt_col: print('ERR! sharkEatFish()')
    sharkStat = [fish_row, fish_col, fish_dir]
    return maps, sharkStat, fishStats_dict, eatIdxSum+fishIdx

sharkStat = [0, 0, 0]
eatIdxSum = 0
maps, sharkStat, fishStats_dict, eatIdxSum = sharkEatFish(sharkStat, 0, 0, maps, fishStats_dict, eatIdxSum)

def isInMaps(r, c):
    return 0<=r<MAP_SIZE and 0<=c<MAP_SIZE

def isShark(maps, r, c):
    return maps[r][c] == -1

def isEmpty(maps, r, c):
    return maps[r][c] == 0

def isFish(maps, r, c):
    return 1<=maps[r][c]<=16

def moveFishes(maps, fishStats_dict):
    for fishIdx in sorted(list(fishStats_dict.keys())):
        [fish_row, fish_col, fish_dir] = fishStats_dict[fishIdx]
        for dirIdx in range(8):
            fish_dir_tmp = (fish_dir+dirIdx)%8
            fish_row_tmp = fish_row + DR[fish_dir_tmp]
            fish_col_tmp = fish_col + DC[fish_dir_tmp]
            if (not isInMaps(fish_row_tmp, fish_col_tmp)) or isShark(maps, fish_row_tmp, fish_col_tmp):
                continue
            elif isEmpty(maps, fish_row_tmp, fish_col_tmp):
                maps[fish_row_tmp][fish_col_tmp] = fishIdx
                maps[fish_row][fish_col] = 0
                fishStats_dict[fishIdx] = [fish_row_tmp, fish_col_tmp, fish_dir_tmp]
                break
            elif isFish(maps, fish_row_tmp, fish_col_tmp):
                fishIdx2 = maps[fish_row_tmp][fish_col_tmp]
                [fish_row2, fish_col2, fish_dir2] = fishStats_dict[fishIdx2]
                fishStats_dict[fishIdx] = [fish_row_tmp, fish_col_tmp, fish_dir_tmp]
                fishStats_dict[fishIdx2] = [fish_row, fish_col, fish_dir2]
                maps[fish_row_tmp][fish_col_tmp] = fishIdx
                maps[fish_row][fish_col] = fishIdx2
                break
            else:
                print("moveFishes ERR!")

    return maps, fishStats_dict

def isSharkCanMove(maps, shark_row, shark_col, shark_dir):
    flag = False
    res = []
    for i in range(4):
        shark_row_tmp = shark_row + DR[shark_dir]*i
        shark_col_tmp = shark_col + DC[shark_dir]*i
        if not isInMaps(shark_row_tmp, shark_col_tmp):
            break
        if isFish(maps, shark_row_tmp, shark_col_tmp):
            flag = True
            res.append(i)

    return flag, res


# DFS
def playSharkDFS(sharkStat, fishStats_dict, maps, level, eatIdxSum):
    global MAX_EATIDXSUM
    MAX_EATIDXSUM = max(eatIdxSum, MAX_EATIDXSUM)

    #print(level, eatIdxSum, MAX_EATIDXSUM)

    if not len(fishStats_dict) > 0: # if fish not exist
        return
    else:
        moveFishes(maps, fishStats_dict)

    [shark_row, shark_col, shark_dir] = sharkStat
    sharkMoveFlag, sharkMoveIdxList = isSharkCanMove(maps, shark_row, shark_col, shark_dir)

    if not sharkMoveFlag:
        return
    else:
        for i in sharkMoveIdxList:
            shark_row_tmp = shark_row + DR[shark_dir]*i
            shark_col_tmp = shark_col + DC[shark_dir]*i

            sharkStat_legacy        = copy.deepcopy(sharkStat)
            maps_legacy             = copy.deepcopy(maps)
            fishStats_dict_legacy   = copy.deepcopy(fishStats_dict)
            eatIdxSum_legacy        = eatIdxSum

            maps, sharkStat,fishStats_dict, eatIdxSum = sharkEatFish(sharkStat, shark_row_tmp, shark_col_tmp, maps, fishStats_dict, eatIdxSum)
            playSharkDFS(sharkStat, fishStats_dict, maps, level+1, eatIdxSum)

            sharkStat               = sharkStat_legacy
            maps                    = maps_legacy
            fishStats_dict          = fishStats_dict_legacy
            eatIdxSum               = eatIdxSum_legacy
            # restore!

# MAIN
playSharkDFS(sharkStat, fishStats_dict, maps, 0, eatIdxSum)
print(MAX_EATIDXSUM)
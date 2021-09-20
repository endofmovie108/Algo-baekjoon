import sys
sys.stdin = open('input.txt', 'rt')
maps = [list(map(int, input().split())) for _ in range(4)]
print(maps)

SHARK_IDX   = -1
EMPTY_IDX   = 0
GO_EMPTY    = 0
GO_FISH     = 1
NO_SHARK    = 2

# dirs - dict / dir_index: [dr, dc]
dirs_dict = dict()
# up, left-up, left, left-down, down, right-down, right, right-up
drs = [-1, -1, 0, 1, 1, 1, 0, -1]
dcs = [0, -1, -1, -1, 0, 1, 1, 1]
for i in range(8):
    dirs_dict[i+1] = [drs[i], dcs[i]]

# fish stats - dict / fish_index: [row, col, dir]
fishStats_dict = dict()
for r in range(4):
    for c in range(4):
        fishStats_dict[maps[r][2*c + 0]] = [r, c, maps[r][2*c + 1]]


def idxOfMaps(maps, r, c):
    return maps[r][2*c+0]

def dirOfMaps(maps, r, c):
    return maps[r][2*c+1]


def isFishCanMove(maps, row, col):
    tgt_idx = idxOfMaps(maps, row, col)
    if tgt_idx != SHARK_IDX:
        return NO_SHARK
    elif tgt_idx == EMPTY_IDX:
        return GO_EMPTY
    else:
        return GO_FISH

def isSharkCanMove(maps, row, col):
    tgt_idx = idxOfMaps(maps, row, col)
    if tgt_idx ==

# move fish
def moveFishes(maps, fishStats_dict):
    for fish_idx, [row, col, dir] in fishStats_dict:
        for dir_idx in range(8):
            dir_t = dir + dir_idx
            if dir_t >= 9: dir_t -= 8
            row_t = row + dirs_dict[dir_t][0]
            col_t = col + dirs_dict[dir_t][1]
            FISH_MOVE_CODE = isFishCanMove(maps, row_t, col_t)
            if FISH_MOVE_CODE == NO_SHARK:
                continue
            elif FISH_MOVE_CODE == GO_EMPTY:
                # move fish
                dirs_dict[dir_t][0] = row_t
                dirs_dict[dir_t][1] = col_t

                maps[row][2*col + 0] = EMPTY_IDX
                maps[row][2*col + 1] = EMPTY_IDX

                maps[row][2*col_t + 0] = fish_idx
                maps[row][2*col_t + 1] = dir_t
                break
            elif FISH_MOVE_CODE == GO_FISH:
                # change fish
                fish_idx1 = maps[row][2*col + 0]
                fish_idx2 = maps[row_t][2*col_t + 0]
                row_tt = row
                col_tt = col
                dir_tt = dir
                fishStats_dict[fish_idx1] = [row_t, col_t, dir_t]
                fishStats_dict[fish_idx2] = [row_tt, col_tt, dir_tt]
                maps[row_t][2*col_t + 0] = fish_idx1
                maps[row_t][2*col_t + 1] = dir_t
                maps[row_tt][2*col_tt + 0] = fish_idx2
                maps[row_tt][2 * col_tt + 0] = dir_tt
                break


# play shark DFS
def playShark_DFS(maps, fishStats_dict, sharkStats_dict, level):
    # 1. 물고기들의 움직임
    moveFishes(maps, fishStats_dict)
    # 2. 상어의 움직임
    sharkStats_dict
    for dir_idx in range(8):
        dir_t = dir + dir_idx
        if dir_t >= 9: dir_t -= 8
        if

# main
# shark location

import sys
sys.stdin = open('input.txt', 'rt')
infos = [list(map(int, input().split())) for _ in range(4)]
maps = [[-1]*4 for _ in range(4)]
stats_dict = dict()
shark_stat = [0, 0, 0]
# 반시계 회전
# dummy, 상, 상좌, 좌, 좌하, 하, 하우, 우, 우상
dr = [0, -1, -1, 0, 1, 1, 1, 0, -1]
dc = [0, 0, -1, -1, -1, 0, 1, 1, 1]

# 0. infos to stat dictionary
for r, info in enumerate(infos):
    for c in range(4):
        fish_idx = info[2*c + 0]
        fish_dir = info[2*c + 1]
        stats_dict[fish_idx] = [r, c, fish_dir]
        maps[r][c] = fish_idx

stats_dict_tmp = sorted(stats_dict.items())
stats_dict = dict()
for stat_dict in stats_dict_tmp:
    fish_idx = stat_dict[0]
    fish_sta = stat_dict[1]
    stats_dict[fish_idx] = fish_sta

def moveShark(stats_dict, r, c, shark_stat, maps):
    fish_idx = maps[r][c]
    [r, c, d] = stats_dict[fish_idx]

    # eat fish
    del(stats_dict[fish_idx])
    maps[r][c] = -1

    # get dir of fish
    shark_stat[0], shark_stat[1], shark_stat[2] = r, c, d
    maps[r][c] = 0 # shark_idx is 0

# 1. shark는 0, 0의 위치에 배치됨
moveShark(stats_dict, 0, 0, shark_stat, maps)
# 2. 모든 물고기들의 이동
for fish_idx in stats_dict:
    [r, c, d] = stats_dict[fish_idx]
    for d_idx in range(8):


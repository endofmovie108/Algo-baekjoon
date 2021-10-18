import sys
sys.stdin = open('input.txt', 'rt')

dr = [-1, -1, 0, 1, 1, 1, 0, -1]
dc = [0, 1, 1, 1, 0, -1, -1, -1]

N, M, K = map(int, input().split())
ball_infos_list = [list(map(int, input().split())) for _ in range(M)] # r, c, m, s, d

g_idx = -1

# functions

def printMaps(maps):
    for m in maps:
        print(m)
    print()

def getNewIdx():
    global g_idx
    g_idx += 1
    return g_idx

def moveBall(r, c, s, d):
    s%=N
    rt, ct = r + s*dr[d], c + s*dc[d]
    if rt < 0: rt = (N - abs(rt)%N)
    if ct < 0: ct = (N - abs(ct)%N)
    rt = rt % N
    ct = ct % N
    return rt, ct

# prepare maps, ball_infos_dicts
maps = [[[]*N for _ in range(N)] for _ in range(N)]
ball_infos_dict = dict()
for [r, c, m, s, d] in ball_infos_list:
    idx = getNewIdx()
    r, c = r-1, c-1
    ball_info_list = [r, c, m, s, d]
    ball_infos_dict[idx] = ball_info_list
    maps_sub = maps[r][c]
    maps_sub.append(idx)

# main
printMaps(maps)
for k in range(K):
    chk = [0] * 50 * 50
    more_than_two_loc = []
    for idx in ball_infos_dict.keys():
        ball_info_list = ball_infos_dict[idx]
        [r, c, m, s, d] = ball_info_list
        r_new, c_new = moveBall(r, c, s, d)
        # update dict
        ball_infos_dict[idx] = [r_new,c_new, m, s, d]
        # update maps
        maps[r][c].remove(idx)
        maps[r_new][c_new].append(idx)
        if len(maps[r_new][c_new]) >= 2 and chk[r_new*N + c_new] == 0:
            chk[r_new*N + c_new] = 1
            more_than_two_loc.append((r_new, c_new))

    printMaps(maps)
    for two_loc in more_than_two_loc:
        (tr, tc) = two_loc
        two_idxs = maps[tr][tc]
        new_ball_m = 0
        new_ball_s = 0
        new_ball_d = 0
        is_all_hol = True
        is_all_zzak = True
        zzak_d = False

        for idx in two_idxs:
            [_, _, m, s, d] = ball_infos_dict[idx]
            del(ball_infos_dict[idx])
            new_ball_m += m
            new_ball_s += s
            if d % 2 == 0:
                is_all_hol = False
            if d % 2 == 1:
                is_all_zzak = False

        if is_all_hol or is_all_zzak:
            zzak_d = True

        new_ball_m = int(new_ball_m / 5)
        new_ball_s = int(new_ball_s / len(two_idxs))

        # clear maps
        maps[tr][tc].clear()

        if new_ball_m != 0:
            if zzak_d: new_ball_d = 0
            else: new_ball_d = 1
            for i in range(4):
                idx = getNewIdx()
                ball_infos_dict[idx] = [tr, tc, new_ball_m, new_ball_s, new_ball_d]
                new_ball_d += 2
                maps[tr][tc].append(idx)
    printMaps(maps)

m_sum = 0
for idx in ball_infos_dict.keys():
    ball_info_list = ball_infos_dict[idx]
    [r, c, m, s, d] = ball_info_list
    m_sum += m
print(m_sum)
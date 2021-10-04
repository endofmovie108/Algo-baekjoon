import sys
sys.stdin = open('input.txt', 'rt')
N = int(input())
half_N = N//2
A_maps = [list(map(int, input().split())) for _ in range(N)]

# functions
def printMaps(maps):
    for tmp in maps:
        print(tmp)
    print()

def areaIdx(area_idx):
    return area_idx-1

minimum_ans = 1e+10
for x in range(N):
    for y in range(N):
        # d1, d2
        for d1 in range(1, y + 1):
            d2_max = min(N-y, N-x-d1)
            for d2 in range(1, d2_max):
                B_maps = [[0] * N for _ in range(N)]
                ct, cl, cr = y, y, y

                area_5_c_st = y
                area_5_c_ed = y
                area_5_r_st = x
                area_5_r_ed = x + d1 + d2 + 1

                area_num = [0]*5

                for r in range(N):
                    # area 5
                    if area_5_r_st <= r <= area_5_r_ed:
                        if r != area_5_r_st:
                            if r <= area_5_r_st + d1: area_5_c_st -= 1
                            else: area_5_c_st += 1

                            if r <= area_5_r_st + d2: area_5_c_ed += 1
                            else: area_5_c_ed -= 1

                    for c in range(N):

                        # if in area 5
                        if area_5_r_st <= r <= area_5_r_ed and \
                                area_5_c_st <= c <= area_5_c_ed:
                            B_maps[r][c] = 5
                            area_num[areaIdx(5)] += A_maps[r][c]
                        else:
                            # if in area 1                         # if in area 4
                            if r < area_5_r_st + d1 and \
                                    c <= area_5_c_st:
                                B_maps[r][c] = 1
                                area_num[areaIdx(1)] += A_maps[r][c]
                            # if in area 2
                            elif r <= area_5_r_st + d2 and \
                                    c > area_5_c_ed:
                                B_maps[r][c] = 2
                                area_num[areaIdx(2)] += A_maps[r][c]
                            # if in area 3
                            elif r >= area_5_r_st + d1 and \
                                    c <= area_5_c_ed:
                                B_maps[r][c] = 3
                                area_num[areaIdx(3)] += A_maps[r][c]
                            # if in area 4
                            elif r > area_5_r_st + d2 and \
                                    c > area_5_c_ed:
                                B_maps[r][c] = 4
                                area_num[areaIdx(4)] += A_maps[r][c]
                # print(max(area_num) - min(area_num))
                ans_cand = max(area_num) - min(area_num)
                minimum_ans = min(ans_cand, minimum_ans)
                # print(x, y, d1, d2)
                # printMaps(B_maps)
print(minimum_ans)
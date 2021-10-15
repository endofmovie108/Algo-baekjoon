import sys
sys.stdin = open('input.txt', 'rt')
dice_all = list(map(int, input().split()))

START_IDX = -1
END_IDX = -2
score_max = -1
scoreMaps = [
    2, 4, 6, 8, 10, 12, 14, 16, 18, 20,
    22, 24, 26, 28, 30, 32, 34, 36, 38, 40,
    13, 16, 19, 25, 28, 27, 26, 22, 24, 30,
    35]
mapSize = len(scoreMaps)

HORSE_STA_END = 0
HORSE_STA_OVERLAP = 1
HORSE_STA_GO = 2

# functions
def whatIsNextIdx(h_idx, first_flag):
    if h_idx == START_IDX: return 0
    if 0 <= h_idx <= 3:
        return h_idx+1
    if h_idx == 4:
        if first_flag: return 20
        else: return 5
    if 5 <= h_idx <= 8:
        return h_idx+1
    if h_idx == 9:
        if first_flag: return 27
        else: return 10
    if 10 <= h_idx <= 13:
        return h_idx+1
    if h_idx == 14:
        if first_flag: return 24
        else: return 15
    if 15 <= h_idx <= 18:
        return h_idx+1
    if 20 <= h_idx <= 21:
        return h_idx+1
    if 24 <= h_idx <= 25:
        return h_idx+1
    if h_idx == 27:
        return 28
    if h_idx == 29:
        return 30
    if h_idx == 30:
        return 19
    if h_idx == 22 or h_idx == 28 or h_idx == 26:
        return 23
    if h_idx == 23:
        return 29
    if h_idx == 19:
        return END_IDX

def isHorseCanGo(h1, dice_num, h2, h3, h4):
    first_flag = True
    h1_sta = HORSE_STA_GO
    h1_old = h1
    for i in range(dice_num):
        if i == 1: first_flag = False
        h1 = whatIsNextIdx(h1, first_flag)
        if h1 == END_IDX: break

    if h1 == END_IDX:
        h1_sta = HORSE_STA_END
        return h1_sta, h1
    if h1 == h2 or h1 == h3 or h1 == h4:
        h1_sta = HORSE_STA_OVERLAP
        return h1_sta, h1_old
    else:
        return h1_sta, h1

def playSharkDFS(lv, score, h1, h2, h3, h4):
    global score_max
    if score >= score_max:
        score_max = score
    # is all horse end?
    h1_sta, h2_sta, h3_sta, h4_sta = HORSE_STA_GO, HORSE_STA_GO, HORSE_STA_GO, HORSE_STA_GO
    if (h1 == END_IDX): h1_sta = HORSE_STA_END
    if (h2 == END_IDX): h2_sta = HORSE_STA_END
    if (h3 == END_IDX): h3_sta = HORSE_STA_END
    if (h4 == END_IDX): h4_sta = HORSE_STA_END
    if h1_sta == HORSE_STA_END and \
            h2_sta == HORSE_STA_END and \
            h3_sta == HORSE_STA_END and \
            h4_sta == HORSE_STA_END:
        return
    if lv >= 10:
        return
    dice_num = dice_all[lv]

    # is horse can go?
    if not h1_sta == HORSE_STA_END:
        h1_sta, h1_new = isHorseCanGo(h1, dice_num, h2, h3, h4)
        if h1_sta == HORSE_STA_GO:
            playSharkDFS(lv + 1, score + scoreMaps[h1_new], h1_new, h2, h3, h4)
        elif h1_sta == HORSE_STA_END:
            playSharkDFS(lv + 1, score, h1_new, h2, h3, h4)
        elif h1_sta == HORSE_STA_OVERLAP:
            pass

    if not h2_sta == HORSE_STA_END:
        h2_sta, h2_new = isHorseCanGo(h2, dice_num, h1, h3, h4)
        if h2_sta == HORSE_STA_GO:
            playSharkDFS(lv + 1, score + scoreMaps[h2_new], h1, h2_new, h3, h4)
        elif h2_sta == HORSE_STA_END:
            playSharkDFS(lv + 1, score, h1, h2_new, h3, h4)
        elif h2_sta == HORSE_STA_OVERLAP:
            pass

    if not h3_sta == HORSE_STA_END:
        h3_sta, h3_new = isHorseCanGo(h3, dice_num, h2, h1, h4)
        if h3_sta == HORSE_STA_GO:
            playSharkDFS(lv + 1, score + scoreMaps[h3_new], h1, h2, h3_new, h4)
        elif h3_sta == HORSE_STA_END:
            playSharkDFS(lv + 1, score, h1, h2, h3_new, h4)
        elif h3_sta == HORSE_STA_OVERLAP:
            pass

    if not h4_sta == HORSE_STA_END:
        h4_sta, h4_new = isHorseCanGo(h4, dice_num, h2, h3, h1)
        if h4_sta == HORSE_STA_GO:
            playSharkDFS(lv + 1, score + scoreMaps[h4_new], h1, h2, h3, h4_new)
        elif h4_sta == HORSE_STA_END:
            playSharkDFS(lv + 1, score, h1, h2, h3, h4_new)
        elif h4_sta == HORSE_STA_OVERLAP:
            pass


# main
playSharkDFS(0, 0, START_IDX, START_IDX, START_IDX, START_IDX)
print(score_max)


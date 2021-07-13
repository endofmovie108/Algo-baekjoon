import sys
sys.stdin = open('input.txt', 'rt')
BLOCK_0 = 1
BLOCK_1 = 2
BLOCK_2 = 3
N = int(input())
X, Y = 10, 10
# x: 행 , y: 열A
GRN = 0
BLU = 1
maps = [[0]*Y for _ in range(X)]
dx = [1, 0]
dy = [0, 1]

def outMaps(x, y):
    global X, Y
    if 0<=x<X and 0<=y<Y: return False
    else: return True

def meetBlock(x, y, maps):
    if maps[x][y] == 1: return True
    else: return False

def onlyUpdate(n_blocks, xs, ys, maps):
    for i in range(n_blocks):
        maps[xs[i]][ys[i]] = 1

def oneLineFull(maps, CLR):
    list_oneLineFull = []
    for i in range(4, 10):
        for j in range(4):
            if CLR == GRN and maps[i][j] == 0:
                break
            elif CLR == BLU and maps[j][i] == 0:
                break
        else: # 전부 1이여서 full line일 때
            list_oneLineFull.append(i)
    return list_oneLineFull

def pullAndUpdate(list_olf, maps, CLR):
    for olf in list_olf:
        for i in range(olf, 4, -1):
            for j in range(4):
                if CLR == GRN:
                    maps[i][j] = maps[i-1][j]
                    maps[i-1][j] = 0
                elif CLR == BLU:
                    maps[j][i] = maps[j][i-1]
                    maps[j][i-1] = 0

def pushAndPullUpdate(n_inBorder, maps, CLR):
    for i in range(10-1-n_inBorder, 4, -1):
        for j in range(4):
            if CLR == GRN:
                maps[i+n_inBorder][j] = maps[i][j]
                maps[i][j] = 0
            elif CLR == BLU:
                maps[j][i+n_inBorder] = maps[j][i]
                maps[j][i] = 0


def print_maps(maps):
    global X, Y
    for i in range(X):
        for j in range(Y):
            print(maps[i][j], end=' ')
        print()
    print()

def isBlockInBorder(maps, CLR):
    cnt = 0
    for i in range(4, 6):
        for j in range(4):
            if (CLR == GRN and maps[i][j] == 1) or (CLR == BLU and maps[j][i] == 1):
                cnt += 1
                break
    return cnt

def Mover(n_blocks, xs_ori, ys_ori, maps, CLR):
    xs = xs_ori.copy()
    ys = ys_ori.copy()
    score = 0
    STOP_FLAG = False
    while not STOP_FLAG:
        for i in range(n_blocks):
            xt, yt = xs[i] + dx[CLR], ys[i] + dy[CLR]
            if outMaps(xt, yt):
                STOP_FLAG = True
                break
            if meetBlock(xt, yt, maps):
                STOP_FLAG = True
                break
        else:
            # break 걸리지 않고 넘어왔으므로, update
            for i in range(n_blocks):
                xs[i], ys[i] = xs[i] + dx[CLR], ys[i] + dy[CLR]
    # 만약 STOP_FLAG == True 로 탈출했다면
    # 해당 상자의 이동이 끝난 것 이므로 한 줄이 전부 차있는 것이 있는지 check
    # maps에 업데이트
    onlyUpdate(n_blocks, xs, ys, maps)
    
    # 만약 one line full 인 라인이 있다면
    list_oneLinFull = oneLineFull(maps, CLR)
    if len(list_oneLinFull):
        score += len(list_oneLinFull)
        pullAndUpdate(list_oneLinFull, maps, CLR)


    # 만약 경계안에 block이 존재한다면
    n_inBorder = isBlockInBorder(maps, CLR)
    if n_inBorder:
        pushAndPullUpdate(n_inBorder, maps, CLR)
    return score

def Area_score(maps, CLR):
    score = 0
    for i in range(4, 10):
        for j in range(4):
            if CLR == GRN: score += maps[i][j]
            elif CLR == BLU: score += maps[j][i]
    return score


total_score = 0
for i in range(N):
    t, x, y = map(int, input().split())
    xs, ys = [x], [y]
    if t == BLOCK_0:
        n_blocks = 1
    elif t == BLOCK_1:
        n_blocks = 2
        xs.append(x)
        ys.append(y+1)
    elif t == BLOCK_2:
        n_blocks = 2
        xs.append(x+1)
        ys.append(y)


    total_score += Mover(n_blocks, xs, ys, maps, GRN)
    total_score += Mover(n_blocks, xs, ys, maps, BLU)
    print_maps(maps)

grn_score = Area_score(maps, GRN)
blu_score = Area_score(maps, BLU)

print(total_score)
print(grn_score+blu_score)





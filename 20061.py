import sys
sys.stdin = open('input.txt', 'rt')
BLOCK_0 = 1
BLOCK_1 = 2
BLOCK_2 = 3
N = int(input())
X, Y = 10, 10
# x: 행 , y: 열

def inMap(x, y):
    global X, Y
    if 0<=x<X and 0<=y<Y: return True
    else: return False

def meetBlock(x, y, maps):
    if maps[x][y] == 1: return True
    else: return False

def inGreenBorder(num_block, xs):
    cnt = 0
    for i_b in range(num_block):
        x = xs[i_b]
        if 4<=x<6: cnt+=1
    return cnt, True if cnt>0 else False

def setBlockToMap(xs, ys, maps):
    for i_b in range(num_block):
        maps[xs[i_b]][ys[i_b]] = 1

def mover_down(num_block, xs, ys, maps):
    global X, Y
    MOVE_END = False
    while not MOVE_END:

        flag_STOP = False
        for i_b in range(num_block):
            xt, yt = xs[i_b] + 1, ys[i_b]

            if not inMap(xt, yt):
                MOVER_STOP_CODE = 0 # 하나라도 맵 외부로 나갔을 때
                flag_STOP = True
                break

            if meetBlock(xt, yt, maps):
                MOVER_STOP_CODE = 1 # 하나라도 이미 놓여진 block을 만났을 때
                flag_STOP = True
                break

        if flag_STOP:
            if MOVER_STOP_CODE == 1: # 중단되었으며 경계에 있는 경우
                numRowGrnBrd, inGrnBrdFlg = inGreenBorder(num_block, xs)
                if (inGrnBrdFlg is False) or (numRowGrnBrd == 0): print("green border error!")
                # numRowGrnBrd 만큼 아래로 이동
                for r_idx in range(X-1-numRowGrnBrd, 3, -1):
                    for c_idx in range(4):
                        maps[r_idx+numRowGrnBrd][c_idx] = maps[r_idx][c_idx]
                        if 4<=r_idx<6: maps[r_idx][c_idx] = 0
                MOVE_END = True
                break

            elif MOVER_STOP_CODE == 0:
                # 중단되었으며 maps를 벗어난 경우, do nothing
                MOVE_END = True
                break

        else: # 정상적으로 block이 이동된 경우
            # 리스트 갱신 및 맵 반영
            for i_b in range(num_block):
                xs[i_b], ys[i_b] = xs[i_b] + 1, ys[i_b]
            setBlockToMap(xs, ys, maps)

def print_maps(maps):
    global X, Y
    for r in range(X):
        for c in range(Y):
            print(maps[r][c], end=' ')
        print()

def SEQ_MOVING(num_block, xs, ys, maps):
    # down, GREEN area
    mover_down(num_block, xs, ys, maps)
    # right, BLUE area
    #mover_right(num_block, xs, ys, maps)

maps = [[0] for _ in range(10)]
for i in range(N):
    t, x, y = map(int, input().split())

    xs = []
    ys = []
    xs.append(x)
    ys.append(y)
    if t == BLOCK_0:
        num_block = 1
    elif t == BLOCK_1:
        num_block = 2
        xs.append(x)
        ys.append(y+1)
    elif t == BLOCK_2:
        num_block = 2
        xs.append(x+1)
        ys.append(y)

    SEQ_MOVING(num_block, xs, ys, maps)
    print_maps(maps)

import sys
sys.stdin = open('input.txt', 'rt')

N, M = map(int, input().split())
maps = [list(map(int, input().split())) for _ in range(N)]
DS = [list(map(int, input().split()))for _ in range(M)]

r_shark = int((N+1)/2)-1
c_shark = int((N+1)/2)-1

# Sequence: down, right, up, left
dr = [1, 0, -1, 0]
dc = [0, 1, 0, -1]
nn = [1, 2, 2, 3]

def print_maps(m):
    global N
    for i in range(N):
        for j in range(N):
            print(m[i][j], end = ' ')
        print()
    print()

def isTornadoEnd(r, c):
    return True if (r==0 and c==0) else False

# Generate tornado indexed bag
l_tornado = []
FLAG_GO = True
r, c = r_shark, c_shark-1
while FLAG_GO:
    for d in range(4):
        for n in range(nn[d]):
            l_tornado.append([r, c])
            r += dr[d]
            c += dc[d]
            if isTornadoEnd(r, c):
                l_tornado.append([r, c])
                FLAG_GO = False
                break
        nn[d] += 2

#print(l_tornado)
# Sequence: dummy, up, down, left, right
dr = [0, -1, 1, 0, 0]
dc = [0, 0, 0, -1, 1]

def tornadoExplosion(maps):
    global l_tornado
    cnt = 1
    m_val_prev = 0
    FLAG_EXPLODE = False
    n_exp_1 = 0
    n_exp_2 = 0
    n_exp_3 = 0
    for i, (r, c) in enumerate(l_tornado):
        m_val = maps[r][c]
        if i == 0:
            m_val_prev = m_val
            continue
        else:
            if m_val_prev == m_val:
                cnt+= 1
            else: #다른 숫자가 나왔을 때,
                if cnt >= 4: # 연속이 총 4개 이상일 때,
                    # explosion
                    if m_val_prev == 1: n_exp_1 += cnt
                    elif m_val_prev == 2: n_exp_2 += cnt
                    elif m_val_prev == 3: n_exp_3 += cnt

                    FLAG_EXPLODE = True
                    for j in range(i-1, i-1-cnt, -1):
                        rr, cc = l_tornado[j][0], l_tornado[j][1]
                        maps[rr][cc] = 0
                cnt = 1
            m_val_prev = m_val
    return FLAG_EXPLODE, n_exp_1, n_exp_2, n_exp_3

def tornadoPull(maps):
    global l_tornado
    zero_cnt = 0
    for i, (r, c) in enumerate(l_tornado):
        if maps[r][c] == 0:
            zero_cnt += 1
        else:
            if zero_cnt > 0: # pull 조건 만족시
                # pull 수행
                for j in range(i, len(l_tornado)):
                    rr, cc = l_tornado[j][0], l_tornado[j][1]
                    rt, ct = l_tornado[j-zero_cnt][0], l_tornado[j-zero_cnt][1]
                    maps[rt][ct] = maps[rr][cc]
                    maps[rr][cc] = 0
                # pull 수행했다면 다시 tornadoPull 필요한지 체크해야 하므로 return True
                return True
    # for문이 다 돌았다면 더 pull할 것이 없다는 뜻.
    return False

def tornadoByeonHwa(maps_1, maps_2):
    global l_tornado
    cnt = 1
    cnt_2 = 0
    for i, (r, c) in enumerate(l_tornado):
        m_1_val = maps_1[r][c]
        if i == 0:
            m_1_val_prev = m_1_val
            continue
        else:
            if m_1_val == m_1_val_prev:
                cnt += 1
            else:
                # 다르다는건, 이전 까지가 그룹 이었음을 의미
                # 이전 그룹에 대해 반영

                A = cnt
                cnt = 1
                B = m_1_val_prev

                maps_2[l_tornado[cnt_2][0]][l_tornado[cnt_2][1]] = A
                cnt_2 += 1
                if cnt_2 == len(l_tornado): break

                maps_2[l_tornado[cnt_2][0]][l_tornado[cnt_2][1]] = B
                cnt_2 += 1
                if cnt_2 == len(l_tornado): break

            if maps[r][c] == 0:
                break

            if isTornadoEnd(r, c):
                A = cnt
                B = m_1_val

                maps_2[l_tornado[cnt_2][0]][l_tornado[cnt_2][1]] = A
                cnt_2 += 1
                if cnt_2 == len(l_tornado): break

                maps_2[l_tornado[cnt_2][0]][l_tornado[cnt_2][1]] = B
                cnt_2 += 1
                if cnt_2 == len(l_tornado): break

            m_1_val_prev = m_1_val

# Main
sum_n_exp_1 = 0
sum_n_exp_2 = 0
sum_n_exp_3 = 0
for i in range(M):
    d = DS[i][0]
    s = DS[i][1]

    # 0. 구슬 파괴
    rt = r_shark
    ct = c_shark
    for j in range(s):
        rt += dr[d]
        ct += dc[d]
        maps[rt][ct] = 0
    #print_maps(maps)

    # 1. 토네이도 회전하며 빈칸으로 당겨오기
    FLAG_PULL = True
    while FLAG_PULL:
        FLAG_PULL = tornadoPull(maps)
    #print_maps(maps)
    
    # 2. 구슬 폭발 단계
    FLAG_EXPLODE = True
    while FLAG_EXPLODE:
        FLAG_EXPLODE, n_exp_1, n_exp_2, n_exp_3 = \
            tornadoExplosion(maps)
        sum_n_exp_1 += n_exp_1
        sum_n_exp_2 += n_exp_2
        sum_n_exp_3 += n_exp_3
        #print_maps(maps)

        # 3. 만약 explode 가 일어났다면, pull 수행
        FLAG_PULL = FLAG_EXPLODE
        while FLAG_PULL:
            FLAG_PULL = tornadoPull(maps)
    #print_maps(maps)

    # 4. 구슬변화단계
    maps_2 = [[0]*N for _ in range(N)]
    tornadoByeonHwa(maps, maps_2)
    #print_maps(maps_2)

    # 5. 갱신 단계
    maps = maps_2.copy()
    #print_maps(maps)

print(1*sum_n_exp_1 + 2*sum_n_exp_2 + 3*sum_n_exp_3)



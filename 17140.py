import sys
sys.stdin = open('input.txt', 'rt')
r, c, k = map(int, input().split())
dats = [list(map(int, input().split())) for _ in range(3)] # 3x3

def op_sort(dat):
    d_ord = [[idx]+[1] for idx in range(101)]
    for d in dat:
        d_ord[d][1] += 1
    return True

def op_R(dats):
    for idx in range(3):
        dat = dats[idx][:]
        op_sort(dat)
    return True

def op_C(dats):
    for idx in range(3):
        dat = dats[:][idx]
        op_sort(dat)
    return True

cnt = 0
while True:
    cnt += 1
    if dats[r][c] == k:
        print(cnt)
        break
    else:
        r_size = len(dats)
        c_size = len(dats[0])
        if r_size >= c_size:
            op_R(dats)
            pass
        else:
            op_C(dats)
            pass

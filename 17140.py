import sys
sys.stdin = open('input.txt', 'rt')
r, c, k = map(int, input().split())
r, c = r-1, c-1
A = [list(map(int, input().split())) for _ in range(3)] # 3x3

rsize = 3
csize = 3
num_dict = {}

# functions
def isSuccess():
    global maps, rsize, csize
    if 0<=r<rsize and 0<=c<csize and A[r][c]==k:
        return True
    else:
        return False

def initNumDict():
    global num_dict
    num_dict = {}

def numlistToArr(num_list):
    res_list = []
    for [num, cnt] in num_list:
        res_list.append(num)
        res_list.append(cnt)
    return res_list

def numdictToList():
    res = []
    for num in num_dict.keys():
        res.append([num, num_dict[num]])
    res.sort(key=lambda x: (x[1], x[0]))
    res = numlistToArr(res)
    return res

def countNum(num):
    if num_dict.get(num) is None:
        num_dict[num] = 0
    num_dict[num] += 1

def printMaps(maps):
    for m in maps:
        print(m)
    print()

def solve():
    global rsize, csize, num_dict, A
    if rsize < csize:
        # R operation
        res_list_all = []
        rsize_max = 0
        for cidx in range(csize):
            initNumDict()
            for ridx in range(rsize):
                num = A[ridx][cidx]
                if not num == 0: countNum(num)
            num_list = []
            if len(num_dict)>0:
                num_list = numdictToList()
            rsize_tmp = len(num_list)

            if rsize_tmp > 100:
                num_list = num_list[:100]
                rsize_tmp = len(num_list)

            if rsize_max < rsize_tmp: rsize_max = rsize_tmp
            res_list_all.append(num_list)
        rsize = rsize_max
        maps_res = [[0]*csize for _ in range(rsize)]
        for cidx, res_list in enumerate(res_list_all):
            for ridx, val in enumerate(res_list):
                maps_res[ridx][cidx] = val
    else:
        # R operation
        res_list_all = []
        csize_max = 0
        for ridx in range(rsize):
            initNumDict()
            for cidx in range(csize):
                num = A[ridx][cidx]
                if not num == 0: countNum(num)
            num_list = []
            if len(num_dict)>0:
                num_list = numdictToList()
            csize_tmp = len(num_list)

            if csize_tmp > 100:
                num_list = num_list[:100]
                csize_tmp = len(num_list)

            if csize_max < csize_tmp: csize_max = csize_tmp
            res_list_all.append(num_list)
        csize = csize_max
        maps_res = [[0]*csize for _ in range(rsize)]
        for ridx, res_list in enumerate(res_list_all):
            for cidx, val in enumerate(res_list):
                maps_res[ridx][cidx] = val
    return maps_res

# main
end_flag = False
time = 0
while time < 101:
    if isSuccess():
        print(time)
        break
    A = solve()
    time += 1
else:
    print(-1)
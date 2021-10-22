import sys
from collections import deque as dq

# 중요 반례
# 5 5 5
# 1 4
# 4 1
# 3 1
# 4 3
# 5 1
# correct:
# 5 1 3 4
# 5 1 3 4
# wrong:
# 5 1 4 3
# 5 1 4 3

sys.stdin = open('input.txt', 'rt')
N, M, V = map(int, input().split())
connects = [list(map(int, input().split())) for _ in range(M)]
connectInfo = {}
chk = [0]*N

VISIT = 1
NOT_VISIT = 0

# functions
def appendSet(k, v):
    global connectInfo
    if connectInfo.get(k) is None:
        connectInfo[k] = set()
    connectInfo[k].add(v)

def DFS(lv):
    global chk, connectInfo, cnt, res, isDone
    if isDone:
        return
    if cnt == len(connectInfo.keys()):
        isDone = True
        return
    cnt += 1
    res.append(lv+1)
    for next_v in connectInfo[lv+1]:
        next_v -= 1
        if chk[next_v] == NOT_VISIT:
            chk[next_v] = VISIT
            DFS(next_v)
            chk[next_v] = NOT_VISIT

def BFS(lv):
    global chk
    findDq = dq()
    findDq.append([lv, 0])
    chk[lv] = VISIT
    while findDq:
        [v, level] = findDq.popleft()

        res.append(v+1)
        if len(res) == len(connectInfo.keys()):
            break
        chk[v] = VISIT
        for next_v in connectInfo[v+1]:
            next_v -= 1
            if chk[next_v] == NOT_VISIT:
                findDq.append([next_v, level+1])


# MAIN
for [v1, v2] in connects:
    appendSet(v1, v2)
    appendSet(v2, v1)

for tmp_key in connectInfo:
    tmp_vals = list(connectInfo[tmp_key])
    connectInfo[tmp_key] = sorted(tmp_vals)

res = []
chk[V-1] = VISIT
isDone, cnt = False, 0
DFS(V-1)
if res:
    for r in res: print(r, end = " ")
res = []
chk = [NOT_VISIT]*N
BFS(V-1)
if res:
    print()
    for r in res: print(r, end = " ")

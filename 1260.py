import sys
from collections import deque as dq

# DFS 탐색에서, 이 문제에서는 방문 해제를 할 이유가 없음
# dict 사용할때 key가 없을수 있으니 .get으로 None인지 체크 할 것!
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
    if connectInfo.get(k-1) is None:
        connectInfo[k-1] = set()
    connectInfo[k-1].add(v-1)

def DFS(v):
    global chk, res, v_tot_num, isDone
    if isDone: return
    chk[v] = VISIT
    res.append(v)
    tmp = connectInfo.get(v)
    if tmp is not None:
        for next_v in tmp:
            if chk[next_v] == NOT_VISIT:
                chk[next_v] = VISIT
                DFS(next_v)

def BFS(v):
    global chk, res, v_tot_num
    findDq = dq()
    findDq.append(v)
    chk[v] = VISIT
    while findDq:
        v = findDq.popleft()
        res.append(v)
        tmp = connectInfo.get(v)
        if tmp is not None:
            for next_v in tmp:
                if chk[next_v] == NOT_VISIT:
                    chk[next_v] = VISIT
                    findDq.append(next_v)

# MAIN
for [v1, v2] in connects:
    appendSet(v1, v2)
    appendSet(v2, v1)

for tmp_key in connectInfo.keys():
    tmp_vals = list(connectInfo[tmp_key])
    connectInfo[tmp_key] = sorted(tmp_vals)

res = []
chk[V-1] = VISIT
isDone, cnt = False, 0
DFS(V-1)
if res:
    for r in res: print(r+1, end = " ")

res = []
chk = [NOT_VISIT]*N
BFS(V-1)

if res:
    print()
    for r in res: print(r+1, end = " ")

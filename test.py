import heapq
a = [[5]*0 for _ in range(3)]

from collections import deque as dq
def size(twoDlist):
    r = len(twoDlist)
    res_r, res_c = 0, 0
    if r > 0:
        res_r, res_c = r, len(twoDlist[0])
    return (res_r, res_c)
print(size(a))
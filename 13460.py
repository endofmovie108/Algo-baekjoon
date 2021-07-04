# 최소 몇번만에 가능한지를 묻는 문제이기 때문에, BFS를 활용하는것이 바람직하다.

import sys
from collections import deque
sys.stdin = open('input.txt', 'rt')

N, M = map(int, input().split())
maps = [list(input()) for _ in range(N)]
# direction: 0->left, 1->down, 2->right, 3->up
R_loc = [0, 0, 0, 0] # row, col, dir, dist
B_loc = [0, 0, 0, 0]
O_loc = [0, 0]

R_chk = [[0]*M for _ in range(N)]
B_chk = [[0]*M for _ in range(N)]

dr = [0, 1, 0, -1]
dc = [-1, 0, 1, 0]

def BFS(l):
    for i in range(4):


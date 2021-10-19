import sys
import math
sys.stdin = open('input.txt', 'rt')
N = int(input())
A = list(map(int, input().split()))
B, C = map(int, input().split())
joo_cnt, boo_cnt = 0, 0
for a in A:
    a -= B
    joo_cnt += 1
    if a > 0:
        boo_cnt += math.ceil(a / C)
print(joo_cnt + boo_cnt)

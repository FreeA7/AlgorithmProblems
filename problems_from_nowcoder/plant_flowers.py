# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 14:07:04 2020

@author: FreeA7

https://www.nowcoder.com/practice/4ccd0888260d420ba3b4283274ff98da

牛牛有一个3*n的土地。这个土地有3行，n列。牛牛想在土地上种至少一朵花。

为了花儿能够茁壮成长，每一朵花的上下左右四个方向不能有其他的花。问有多少种种花的方案。

为防止答案过大，答案对1e9+7取模。

示例1
输入:
    1
输出:
    4
说明:
    只有1列，用1代表花，0代表空地。这一列的种法可能是[1,0,0],[0,1,0],[0,0,1],[1,0,1]四种
"""

import sys
sys.path.append("..")
from utils.utils import timer
import random


# 错误，因为很明显要用到上一列的状态，之前都想到了01为什么没想到泳mask呢，不是简单地加和就可以的
class Solution1:
    @timer
    def solve(self , n ):
        MOD = int(1e9+7)
        max_flower = 2*n-n//2
        dp = [[0 for flower in range(max_flower+1)] for land in range(n+1)]
        for i in range(1, n+1):
            dp[i][1] = 3*i
            if i % 2 == 1:
                dp[i][(2*i - i//2)] = 1
            else:
                dp[i][(2*i - i//2)] = 2
        for i in range(2, n+1):
            if i % 2 == 1:
                dp[i][(2*i - i//2)-1] = (2*i - i//2) + 1
            for k in range(2, (2*(i-1) - (i-1)//2)+1):
                dp[i][k] = dp[i-1][k] + 3*dp[i-1][k-1] + dp[i-1][k-2] - dp[i][k+1]
        return sum(dp[n])%MOD
                

# mask，还可以优化为重复使用一个mask，空间复杂度大大减小，不过很简单就不写了
class Solution2:
    @timer
    def solve(self , n ):
        MOD = int(1e9+7)
        dp = [[0 for flower in range(2**3)] for land in range(n+1)]
        dp[1][0] = dp[1][1] = dp[1][1<<1] = dp[1][1<<2] = dp[1][1|1<<2] = 1
        for land in range(2, n+1):
            dp[land][0] = sum(dp[land-1])%MOD
            dp[land][1] = (dp[land-1][1<<1] + dp[land-1][1<<2] + dp[land-1][0])%MOD
            dp[land][1<<1] = (dp[land-1][1] + dp[land-1][1<<2] + dp[land-1][1|1<<2] + dp[land-1][0])%MOD
            dp[land][1<<2] = (dp[land-1][1] + dp[land-1][1<<1] + dp[land-1][0])%MOD
            dp[land][1|1<<2] = (dp[land-1][1<<1] + dp[land-1][0])%MOD
        return sum(dp[n])%MOD - 1
        

# --------------------- 输出 ---------------------       
target1 = 10
target2 = random.randint(100,999)
tar = target2
s = Solution1()
print(s.solve(tar))

s = Solution2()
print(s.solve(tar))


'''
Reloaded modules: utils.utils
Solution1.solve 共用时：0.19461800000135554 s
377789230
Solution2.solve 共用时：0.0017810000008466886 s
835455447
'''

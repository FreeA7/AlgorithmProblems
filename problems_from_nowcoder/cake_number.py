# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 09:49:42 2020

@author: FreeA7

https://www.nowcoder.com/practice/1f7280d9897d4305b2da6790fe131729

众所周知，牛妹非常喜欢吃蛋糕
天牛妹吃掉蛋糕数三分之一多一，二天又将剩下的蛋糕吃掉三分之多一，以后每天吃掉前天剩下的三分之一多一，到第n天准备吃的时候只剩下蛋糕
牛想知道天开始吃的时候蛋糕一共有多少

示例1
输入:
    2
输出:
    3

示例2
输入:
    4
输出:
    10
"""

import sys
sys.path.append("..")
from utils.utils import timer
import random

class Solution1:
    @timer
    def cakeNumber(self , n ):
        if n == 1:
            return 1
        cake = 1
        for i in range(n-1):
            cake = (cake*3+3)//2
        return cake
    
    
# --------------------- 输出 ---------------------
target1 = 2
target2 = 4
target3 = 1
target4 = 29

tar = target4

s = Solution1()
print(s.cakeNumber(tar))


'''
Solution1.cakeNumber 共用时：1.1000000085914508e-05 s
311070
'''
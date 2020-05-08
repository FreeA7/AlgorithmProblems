# -*- coding: utf-8 -*-
"""
Created on Mon May  4 23:52:42 2020

@author: FreeA7

https://www.nowcoder.com/practice/99062f0877e047bb8c7374d241268a8b

牛妹有一个长度为n的排列p，她有q个询问。
每个询问包含l1l1，r1r1，l2l2，r2r2.
她想知道从[l1,r1][l1,r1]中选取xx，[l2,r2][l2,r2]中选取yy,有多少组(x,y)(x,y)满足min(x,y)==gcd(x,y)?min(x,y)==gcd(x,y)?

示例
输入：
    6,1,[1,2,3,4,5,6],[0],[1],[2],[3]
输出：
    [3]
说明：
    (1,3),(1,4),(2,4)三对
"""


import sys
sys.path.append("..")
from utils.utils import timer
import random
import math


class Solution:
    @timer
    def PermutationQuery(self , n , q , p , l1 , r1 , l2 , r2 ):
        res = {}
        for index in range(len(p)):
            res[index] = set()
        for i in range(len(p)):
            for j in range(i, len(p)):
                if min(p[i], p[j]) == math.gcd(p[i], p[j]):
                    res[i].add(j)
                    res[j].add(i)
        output = []
        for query in range(q):
            num = 0
            for l in range(l1[query],r1[query]+1):
                for r in range(l2[query],r2[query]+1):
                    if r in res[l]:
                        num += 1
            output.append(num)
        return output


# --------------------- 输出 ---------------------      
target1 = [6,1,[1,2,3,4,5,6],[0],[1],[2],[3]]
tar = target1

s = Solution()
print(s.PermutationQuery(tar[0], tar[1], tar[2], tar[3], tar[4], tar[5], tar[6]))


'''
Solution.PermutationQuery 共用时：9.750000003805326e-05 s
[3]
'''
                    
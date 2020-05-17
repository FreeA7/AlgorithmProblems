# -*- coding: utf-8 -*-
"""
Created on Fri May 15 16:19:46 2020

@author: FreeA7

https://www.nowcoder.com/practice/c29467f48afe4f53aaa97db5f7a95e18

牛牛作为牛客王国的探险先锋，来到了一片新的大陆。
这是一个工业化程度很高的大陆，遍地都是工厂，有些工厂之间有管道相连。
这片大陆一共有n个工厂，有n-1对工厂之间有管道相连，因为工厂之间需要合作，
所以这n-1个管道保证任意两个工厂都可以通过管道互相抵达。
牛牛发现，从这片大陆开始工业化以来，一共发生了m次原始生产力提升。
每一次原始生产力提升在一个工厂u发生，它会让工厂u以及和工厂u直接通过管道相连的工厂的生产力加1。
每个工厂最开始的生产力都是0。
现在牛牛知道了m次生产力提升发生的工厂位置。牛牛想知道这m次提升发生之后每个工厂的生产力是多少。

示例
输入:
    4,2,[1,2,2],[2,3,4],[2,1]
输出:
    [2,2,1,1]
说明:
    第一次生产力提升发生在工厂2，工厂1，2，3，4的生产力都提升了1点
    第二次生产力提升发生在工厂1，工厂1，2的生产力都提升了1点
    最终工厂1，2的生产力都为2，工厂3，4的生产力都为1
"""


import sys
sys.path.append("..")
from utils.utils import timer
import random


# 模拟每一次提升
class Solution1:
    def getMaps(self, n, u, v):
        maps = {}
        for i in range(n-1):
            if u[i] not in maps.keys():
                maps[u[i]] = [v[i]]
            else:
                maps[u[i]].append(v[i])
            if v[i] not in maps.keys():
                maps[v[i]] = [u[i]]
            else:
                maps[v[i]].append(v[i])
        return maps
        
    @timer
    def solve(self , n , m , u , v , q ):
        maps = self.getMaps(n, u, v)
        productivity = [0 for i in range(n)]
        for i in range(m):
            productivity[q[i]-1] += 1
            for j in maps[q[i]]:
                productivity[j-1] += 1
        return productivity
    
 
# 记录每一次节点提升次数，最后算生产力
class Solution2:
    def getMaps(self, n, u, v):
        maps = {}
        for i in range(n-1):
            if u[i] not in maps.keys():
                maps[u[i]] = [v[i]]
            else:
                maps[u[i]].append(v[i])
            if v[i] not in maps.keys():
                maps[v[i]] = [u[i]]
            else:
                maps[v[i]].append(v[i])
        return maps
        
    @timer
    def solve(self , n , m , u , v , q ):
        maps = self.getMaps(n, u, v)
        productivity = [0 for i in range(n)]
        promote = {}
        for i in range(n):
            promote[i+1] = 0
        for i in range(m):
            promote[q[i]] += 1
        for i in range(n):
            productivity[i] += promote[i+1]
            for j in maps[i+1]:
                productivity[j-1] += promote[i+1]
        return productivity
        
    
# --------------------- 输出 --------------------- 
target1 = [4,2,[1,2,2],[2,3,4],[2,1]]
tar = target1

s1 = Solution1()
print(s1.solve(tar[0], tar[1], tar[2], tar[3], tar[4]))

s2 = Solution2()
print(s2.solve(tar[0], tar[1], tar[2], tar[3], tar[4]))


'''
Solution1.solve 共用时：1.4899999996487168e-05 s
[2, 2, 1, 1]
Solution2.solve 共用时：2.2499999886349542e-05 s
[2, 2, 1, 1]
'''      
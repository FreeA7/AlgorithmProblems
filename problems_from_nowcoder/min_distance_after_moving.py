# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 12:32:17 2020

@author: FreeA7

https://www.nowcoder.com/practice/1b2c9a2ba11746958036b29f2e9ee72b

牛牛最近搬到了一座新的城镇，这个城镇可以看成是一个一维的坐标系。城镇上有n个居民，第i个居民的位置为ai。
现在牛牛有m个搬家方案，在第i个方案中他会搬到位置xi。
俗话说的好，远亲不如近邻。现在牛牛想知道，对于每个搬家方案，搬家后与最近的居民的距离为多少。

示例1
输入:
    3,2,[2,4,7],[5,8]
输出:
    [1,1]
说明:
    第一个方案搬到位置5，与5最近的居民在位置4，距离为1.
    第二个方案搬到位置8，与8最近的居民在位置7，距离为1
"""


import sys
sys.path.append("..")
from utils.utils import timer
import random
import copy
import bisect


class Solution1:
    def findLocation(self, loc, a, l, r):
        if l == r:
            return l
        mid = (l+r)//2
        if loc <= a[mid]:
            return self.findLocation(loc, a, l, mid)
        else:
            return self.findLocation(loc, a, mid+1, r)
     
    @timer
    def solve(self , n , m , a , x ):
        a = sorted(a)
        output = []
        for i in x:
            if i < a[0]:
                output.append(a[0]-i)
            elif i > a[-1]:
                output.append(i-a[-1])
            else:   
                loc = self.findLocation(i, a, 0, len(a)-1)
                output.append(min(i-a[loc-1], a[loc]-i))
        return output


class Solution2:
    @timer
    def solve(self , n , m , a , x ):
        a = sorted(a)
        output = []
        for i in x:
            if i < a[0]:
                output.append(a[0]-i)
            elif i > a[-1]:
                output.append(i-a[-1])
            else:   
                loc = bisect.bisect(a, i)
                output.append(min(i-a[loc-1], a[loc]-i))
        return output


# --------------------- 输出 ---------------------    
target1 = [3,2,[2,4,7],[5,8]]
target2 = [100000, 100, [random.randint(1,100000) for i in range(100000)], [random.randint(1,100) for i in range(100000)]]
tar = copy.deepcopy(target2)

s = Solution1()
s1 = s.solve(tar[0], tar[1], tar[2], tar[3])

tar = copy.deepcopy(target2)

s = Solution2()
s2 = s.solve(tar[0], tar[1], tar[2], tar[3])

print(s1==s2)


'''
Solution1.solve 共用时：1.1421160999998392 s
Solution2.solve 共用时：0.23478230000000622 s
True
'''
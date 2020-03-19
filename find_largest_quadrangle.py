# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 19:37:23 2020

@author: FreeA7

https://www.nowcoder.com/practice/0eaf4653f1d243d4a46b3d5d60a7362e

给定大小为n的整数集合A，代表n根木棍的长度。从A中任选4根木棍组成一个四边形，求其面积最大为多少。数据保证有解。
程序返回结果与正确答案的误差应小于0.00001

示例
输入:
    [1,2,3,4,5]
输出:
    10.95445
"""


from utils import timer
import random


# 布雷特施奈德公式 (Bretschneider's formula)，直接遍历
class Solution1:
    def getS(self, a,b,c,d):
        l = (a+b+c+d)/2
        return (((l-a)*(l-b)*(l-c)*(l-d))**0.5)
        
    @timer
    def solve(self , a ):
        li = sorted(a)
        tested = []
        max_s = 0
        k = 0
        for ai in range(len(li)-3):
            for bi in range(ai+1, len(li)-2):
                for ci in range(bi+1, len(li)-1):
                    for di in range(ci+1, len(li)):
                        a = li[ai]
                        b = li[bi]
                        c = li[ci]
                        d = li[di]
                        if d < (a+b+c) and [a,b,c,d] not in tested:
                            k += 1
                            tested.append([a,b,c,d])
                            s = self.getS(a,b,c,d)
                            if s > max_s:
                                max_s = s
        print(k)
        return max_s
    
    
# 不用tested
class Solution2:
    def getS(self, a,b,c,d):
        l = (a+b+c+d)/2
        return (((l-a)*(l-b)*(l-c)*(l-d))**0.5)
        
    @timer
    def solve(self , a ):
        li = sorted(a)
        max_s = 0
        k = 0
        for ai in range(len(li)-3):
            for bi in range(ai+1, len(li)-2):
                for ci in range(bi+1, len(li)-1):
                    for di in range(ci+1, len(li)):
                        a = li[ai]
                        b = li[bi]
                        c = li[ci]
                        d = li[di]
                        if d < (a+b+c):
                            s = self.getS(a,b,c,d)
                            k += 1
                            if s > max_s:
                                max_s = s
        print(k)
        return max_s

# --------------------- 输出 ---------------------
target1 = [1,2,3,4,5]
target2 = [random.randint(1,10000) for i in range(100)]

tar = target2

s = Solution1()
print(s.solve(tar))

s = Solution2()
print(s.solve(tar))

'''
n = 100 10以内:
    620
    solve 共用时：40.596589300000005 s
    100.0
    3366417
    solve 共用时：4.881192999999939 s
    100.0
'''
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 11:44:58 2020

@author: FreeA7

https://www.nowcoder.com/practice/6c5c3a9901ec4a90aa140348243da4e8

众所周知，牛能和牛可乐经常收到小粉丝们送来的礼物，每个礼物有特定的价值，他俩想要尽可能按照自己所得价值来平均分配所有礼物。

那么问题来了，在最优的情况下，他俩手中得到的礼物价值和的最小差值是多少呢？
p.s 礼物都很珍贵，所以不可以拆开算哦

示例1
输入:
    [1,2,3,4]
输出:
    0
说明：
    他俩一个人拿1,4 。另一个人拿2,3
    
示例2
输入:
    [1,3,5]
输出:
    1
说明：
    他俩一个人拿1，3.另一个人拿5
    
image: ./image/01knapsack.jpg
"""

from utils import timer
import random

# 每轮只测试首尾，相当于一个人拿的一定是首尾的数
class Solution1:
    @timer
    def maxPresent(self , presentVec ):
        li = sorted(presentVec)
        if li == []:
            return 0
        if len(li) == 1:
            return li[0]
        s_all = sum(li)
        diff_o = s_all
        a = 0
        temp_li = li.copy()
        while 1:
            diff_head = abs(s_all - (2*(a+temp_li[0])))
            diff_trail = abs(s_all - (2*(a+temp_li[-1])))
            if min([diff_head, diff_trail]) >= diff_o:
                break
            elif diff_head <= diff_trail:
                diff_o = diff_head
                a += temp_li[0]
                temp_li.pop(0)
            elif diff_trail < diff_head:
                diff_o = diff_trail
                a += temp_li[-1]
                temp_li.pop(-1)
        return diff_o
    
# 贪心算法
class Solution2:
    @timer
    def maxPresent(self , presentVec ):
        li = sorted(presentVec)
        if li == []:
            return 0
        if len(li) == 1:
            return li[0]
        s_all = sum(li)
        diff_o = s_all
        a = 0
        temp_li = li.copy()
        while 1:
            diff_min = diff_o
            for i in range(len(temp_li)):
                diff = abs(s_all - (2*(a+temp_li[i])))
                if diff < diff_min:
                    diff_min = diff
                    index_min = i
            if diff_min == diff_o:
                break
            else:
                diff_o = diff_min
                a += temp_li[index_min]
                temp_li.pop(index_min)
        return diff_o
    
# 01背包
class Solution3:
    @timer
    def maxPresent(self , presentVec ):
        li = sorted(presentVec)
        bag = sum(li) // 2
        item_num = len(li)
        matrx = [[0 for j in range(bag+1)] for i in range(item_num+1)]
        for i in range(1, bag+1):
            for j in range(1, item_num+1):
                if i < li[j-1]:
                    matrx[j][i] = matrx[j-1][i]
                else:
                    if matrx[j-1][i-li[j-1]]+li[j-1] >= matrx[j-1][i]:
                        matrx[j][i] = matrx[j-1][i-li[j-1]]+li[j-1]
                    else:
                        matrx[j][i] = matrx[j-1][i]
        return sum(li) - (2*matrx[item_num][bag])
    
    
# --------------------- 输出 ---------------------
target1 = [1,2,3,4,5]
target2 = [1,3,5]
target3 = [1,2,5,10,15,90]
target4 = [1,1,1,1,1]
target5 = [41,467,334,1,169,224,478,358]
target6 = [41,467,334,0,169,224,478,358,462,464,205]
target7 = [1,5,9,7,3,10,15,6,6]

tar = target5

s = Solution1()
print(s.maxPresent(tar))

s = Solution2()
print(s.maxPresent(tar))

s = Solution3()
print(s.maxPresent(tar))

'''
maxPresent 共用时：4.579999949783087e-05 s
384
maxPresent 共用时：3.5400000342633575e-05 s
26
maxPresent 共用时：0.020082799999727285 s
4
'''
                
                

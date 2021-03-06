# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 11:44:58 2020

@author: FreeA7

https://www.nowcoder.com/practice/6c5c3a9901ec4a90aa140348243da4e8

众所周知，牛能和牛可乐经常收到小粉丝送来的礼物，每个礼物有特定的价，他俩想尽能按照自己所得价值来平均分配有礼物

那么题来了，在最优的情况下，他俩手中得到的礼物价值和的最小差值是多少
p.s 礼物都很珍贵，所以不以拆算哦

示例1
输入:
    [1,2,3,4]
输出:
    0
说明
    他俩人拿1,4 。另人拿2,3
    
示例2
输入:
    [1,3,5]
输出:
    1
说明
    他俩人拿13.另一人拿5
    
image: ./image/01knapsack.jpg
"""

import sys
sys.path.append("..")
from utils.utils import timer
import random


# 模拟，每测试首尾，相当于人拿的一定是首尾的数
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
    
    
# 心算
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
    
    
# 01背包优化，空间杂度降
class Solution4:
    @timer
    def maxPresent(self , presentVec ):
        value_sum = sum(presentVec)
        space_half = value_sum // 2
        dp_this_item = [0 for s in range(space_half+1)]
        dp_last_item = [0 for s in range(space_half+1)]
        for item in range(1, len(presentVec)+1):
            for space in range(1, space_half+1):
                if presentVec[item-1] <= space:
                    dp_this_item[space] = max(dp_last_item[space], dp_last_item[space-presentVec[item-1]]+presentVec[item-1])
                else:
                    dp_this_item[space] = dp_last_item[space]
            dp_this_item, dp_last_item = dp_last_item, dp_this_item
        return value_sum - 2*dp_last_item[-1]
    

# 01背包优化，空间杂度极致降    
class Solution5:
    @timer
    def maxPresent(self , presentVec ):
        value_sum = sum(presentVec)
        space_half = value_sum // 2
        dp = [0 for s in range(space_half+1)]
        for item in range(1, len(presentVec)+1):
            for space in range(space_half, presentVec[item-1]-1, -1):
                if presentVec[item-1] <= space:
                    dp[space] = max(dp[space], dp[space-presentVec[item-1]]+presentVec[item-1])
        return value_sum - 2*dp[-1]
    
    
# --------------------- 输出 ---------------------
target1 = [1,2,3,4,5]
target2 = [1,3,5]
target3 = [1,2,5,10,15,90]
target4 = [1,1,1,1,1]
target5 = [41,467,334,1,169,224,478,358]
target6 = [41,467,334,0,169,224,478,358,462,464,205]
target7 = [1,5,9,7,3,10,15,6,6]
target8 = [41,467,334,500,169,724,478,358,962,464,705,145,281,827,961,491,995,942,827,436]

tar = target5

s = Solution1()
print(s.maxPresent(tar))

s = Solution2()
print(s.maxPresent(tar))

s = Solution3()
print(s.maxPresent(tar))

s = Solution4()
print(s.maxPresent(tar))

s = Solution5()
print(s.maxPresent(tar))


'''
Solution1.maxPresent 共用时：1.7899999875226058e-05 s
384
Solution2.maxPresent 共用时：6.209999992279336e-05 s
26
Solution3.maxPresent 共用时：0.018778800000291085 s
4
Solution4.maxPresent 共用时：0.012764099999913014 s
4
'''
                
                

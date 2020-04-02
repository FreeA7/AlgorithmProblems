# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 09:56:34 2020

@author: FreeA7

https://www.nowcoder.com/practice/2bd935b84b554a2fbd59cfc6df2ddf9c

有n箱子，i箱子始有ai球，你可以进行最多k次操作，每操作可以从箱子拿走球或者放入一球
第i箱子多能装wi球，装满了之后不能再这个箱子里面放球。果箱子为空，就不能从里面拿球
设相邻子的球的数量的的平方中的最大为x，求进最多k次操作之后x小可以是多少

示例
输入:
    5,4,[12,4,7,9,1],[15,15,15,15,15]
输出:
    36
说明
    2箱子2球，4箱子2球得到[12,6,7,9,3]
    此时相邻箱子的球数差值为[-6,1,2,-6],平方后为[36,1,4,36]，其大为36
"""

import sys
sys.path.append("..")
from utils.utils import timer
import random


'''
心算法，每都选择大的值进行减
值减少的方式放球在少的还取球在的则进行判
    设定plus和minus两个
    plus
        如果放球导致少的箱子的另边的值变大则 plus = -1
        如果放球导致少的箱子的另边的值变小则 plus = 1
        如果少的箱子已经旁边的子没有另一边的值则 plus = 0
        如果达到箱子大不能放球则 plus = -2
    minus
        如果取球导致多的箱子的另边的值变大则 minus = -1
        如果取球导致多的箱子的另边的值变小则 minus = 1
        如果多的箱子已经旁边的子没有另一边的值则 minus = 0
    然后比较plus和minus
        如果plus更大则放球在少的箱子
        如果minus更大则拿球在多的箱子
        如果样大
            都等1
                箱子另一边的值更大则对那边进行操
                值相等则无所
            都等-1
                箱子另一边的值更小则对那边进行操
                值相等则无所
'''
class Solution1:
    @timer
    def solve(self , n , k , a , w ):
        if n<=1:
            return 0
        diff_list = [abs(a[i]-a[i-1]) for i in range(1, len(a))]
        for i in range(k):
            max_now = max(diff_list)
            if max_now == 0:
                return 0
            index = diff_list.index(max_now)
            if a[index] > a[index+1]:
                # Plus
                if a[index+1] < w[index+1]:
                    if index == (n-2):
                        plus = 0
                    else:
                        plus = diff_list[index+1] - abs(a[index+2]-a[index+1]-1)
                else:
                    plus = -2
                # Minus
                if index == 0:
                    minus = 0
                else:
                    minus = diff_list[index-1] - abs(a[index]-1-a[index-1])
                if plus > minus:
                    a[index+1] += 1
                    if index < (n-2):
                        diff_list[index+1] = abs(a[index+2]-a[index+1])
                elif plus < minus:
                    a[index] -= 1
                    if index > 0:
                        diff_list[index-1] = abs(a[index]-a[index-1])
                else:
                    if plus == -1:
                        if diff_list[index+1] >= diff_list[index-1]:
                            a[index] -= 1
                            if index > 0:
                                diff_list[index-1] = abs(a[index]-a[index-1])
                        else:
                            a[index+1] += 1
                            if index < (n-2):
                                diff_list[index+1] = abs(a[index+2]-a[index+1])
                    elif plus == 1:
                        if diff_list[index+1] >= diff_list[index-1]:
                            a[index+1] += 1
                            if index < (n-2):
                                diff_list[index+1] = abs(a[index+2]-a[index+1])
                        else:
                            a[index] -= 1
                            if index > 0:
                                diff_list[index-1] = abs(a[index]-a[index-1])
            else:
                # Plus
                if a[index] < w[index]:
                    if index == 0:
                        plus = 0
                    else:
                        plus = diff_list[index-1] - abs(a[index]+1-a[index-1])
                else:
                    plus = -2
                # Minus
                if index == (n-2):
                    minus = 0
                else:
                    minus = diff_list[index+1] - abs(a[index+2]-a[index+1]+1)
                if plus > minus:
                    a[index] += 1
                    if index > 0:
                        diff_list[index-1] = abs(a[index]-a[index-1])
                elif plus < minus:
                    a[index+1] -= 1
                    if index < (n-2):
                        diff_list[index+1] = abs(a[index+2]-a[index+1])
                else:
                    if plus == -1:
                        if diff_list[index+1] >= diff_list[index-1]:
                            a[index] += 1
                            if index > 0:
                                diff_list[index-1] = abs(a[index]-a[index-1])
                        else:
                            a[index+1] -= 1
                            if index < (n-2):
                                diff_list[index+1] = abs(a[index+2]-a[index+1])
                    elif plus == 1:
                        if diff_list[index+1] >= diff_list[index-1]:
                            a[index+1] -= 1
                            if index < (n-2):
                                diff_list[index+1] = abs(a[index+2]-a[index+1])
                        else:
                            a[index] += 1
                            if index > 0:
                                diff_list[index-1] = abs(a[index]-a[index-1])
            diff_list[index] -= 1
        return pow(max(diff_list), 2)
                        

# --------------------- 输出 ---------------------
target1 = [5,4,[12,4,7,9,1],[15,15,15,15,15]]
target2 = [3,3,[3,3,3], [3,3,3]]
target3 = [5,0,[1,2,3,4,7], [7,7,7,7,7]]
target4 = [5,225,[162,27,210,150,263],[261,318,266,331,397]]
target5 = [7,347,[162,27,210,150,263,261,30],[261,318,266,331,397,420,43]]
target6 = [13,463,[162,27,210,150,263,261,30,116,43,130,20,215,23],[261,318,266,331,397,420,43,128,46,379,491,379,270]]

tar = target6

s = Solution1()
print(s.solve(tar[0], tar[1], tar[2], tar[3]))


'''
Solution1.solve 共用时：0.005447999999887543 s
6241
'''
            
            
        
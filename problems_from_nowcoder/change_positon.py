# -*- coding: utf-8 -*-
"""
Created on Fri May  8 09:02:02 2020

@author: FreeA7

https://www.nowcoder.com/practice/2fd53187e5c94d4f9fa4102c39b194bb

牛家村准备开会选举新任村长，村长安排了一个位置表Position（桌子是圆桌！！！所以第一个人和最后一个人是挨着坐的）。村长的候选人牛牛，牛妹，牛大三个。为了让选举进行的更加顺利，村长想让三位的支持者分别坐在一起。
他想知道最少多少人需要换座位才能使得三类支持者都分别坐在一起。

示例
输入:
    [1,2,2,1,3]
输出:
    2
说明:
    将最后一个人与倒数第二个人的位置互换
"""


import sys
sys.path.append("..")
from utils.utils import timer
import random
from collections import Counter


# 生成排好队的队列，每次把头的人放到尾与原数列对比，查看那一次改变最小
class Solution1:
    @timer
    def ChangePosition(self , Position ):
        c = Counter(Position)
        position_after_change = [1 for i in range(c[1])] + [2 for i in range(c[2])] + [3 for i in range(c[3])]
        min_change = float('inf')
        for i in range(len(Position)):
            position_after_change.append(position_after_change.pop(0))
            change = 0
            for j in range(len(Position)):
                if position_after_change[j] != Position[j]:
                    change += 1
                    if change > min_change:
                        break
            min_change = min(min_change, change)
        return min_change
    

# 类似于Solution1，但是查看前缀和什么时候最小，不过是错的，因为会凑数
class Solution2:
    @timer
    def ChangePosition(self , Position ):
        c = Counter(Position)
        position_after_change = [1 for i in range(c[1])] + [2 for i in range(c[2])] + [3 for i in range(c[3])]
        sum_l_after = sum(position_after_change[:len(position_after_change)//2])
        sum_r_after = sum(position_after_change[len(position_after_change)//2:])
        sum_no_head_after = sum(position_after_change[1:])
        sum_no_tail_after = sum(position_after_change[:1])
        sum_l_before = sum(Position[:len(Position)//2])
        sum_r_before = sum(Position[len(Position)//2:])
        sum_no_head_before = sum(Position[1:])
        sum_no_tail_before = sum(Position[:1])
        min_prefix_sum = float('inf')
        for i in range(len(Position)):
            sum_no_head_after -= position_after_change[1]
            sum_no_head_after += position_after_change[0]
            sum_no_tail_after -= position_after_change[0]
            sum_no_tail_after += position_after_change[1]
            sum_l_after -= position_after_change[0]
            sum_l_after += position_after_change[len(position_after_change)//2]
            sum_r_after -= position_after_change[len(position_after_change)//2]
            sum_r_after += position_after_change[0]
            position_after_change.append(position_after_change.pop(0))
            prefix_sum = abs(sum_l_before - sum_l_after) + abs(sum_r_before - sum_r_after) + abs(sum_no_head_before - sum_no_head_after) + abs(sum_no_tail_before - sum_no_tail_after)
            if prefix_sum < min_prefix_sum:
                min_positon = position_after_change.copy()
                min_prefix_sum = prefix_sum
        change = 0
        for i in range(len(Position)):
            if min_positon[i] != Position[i]:
                change += 1
        return change
    
    
# --------------------- 输出 --------------------- 
target1 = [1,2,2,1,3]
target2 = [random.randint(1,3) for _ in range(2000)]
target3 = [1, 2, 2, 3, 3, 1, 1, 3, 2, 1]
tar = target2
s = Solution1()
print(s.ChangePosition(tar))
s = Solution2()
print(s.ChangePosition(tar))


'''
Solution1.ChangePosition 共用时：0.9247126000000208 s
1302
Solution2.ChangePosition 共用时：0.015358399999968242 s
1326
'''
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 11:32:10 2020

@author: FreeA7

https://www.nowcoder.com/practice/c880afeeaeeb4316b19e784452216e23

有n个水桶，第i个水桶里面水的体积为Ai，你可以用1秒时间向一个桶里添加1体积的水。
有q次询问，每次询问一个整数pi,你需要求出使其中pi个桶中水的体积相同所花费的最少时间。
对于一次询问如果有多种方案，则采用使最终pi个桶中水的体积最小的方案。

示例
输入:
    4,3,[1,2,3,4],[2,2,4]
输出:
    [1,0,5]
说明:
    第一次：花费一秒变为 2 2 3 4

    第二次：已经存在两个水的体积一样的桶
    
    第三次：花费五秒从2 2 3 4变为4 4 4 4
"""

from utils import timer
from collections import Counter
import random

# @param n int整型 水桶的个数
# @param q int整型 询问的次数
# @param a int整型一维数组 n个水桶中初始水的体积
# @param p int整型一维数组 每次询问的值
# @return int整型一维数组

class Solution1:
    @timer
    def solve(self , n , q , a , p ):
        
        li = sorted(a)
        counter = Counter(li)
        max_same = max([counter[key] for key in counter.keys()])
        need_time_list = []
        
        flag = 0
        
        for pn in p:
            if max_same >= pn:
                need_time_list.append(0)
            else:
                min_need_time = li[-1]*(pn-1)
                min_index = len(li) - 1
                min_high = li[-1]
                for i in range(pn-1, len(li)):
                    flag+=1
                    need_time = ((pn-1)*li[i]) - sum(li[i-pn+1:i])
                    if need_time < min_need_time:
                        min_need_time = need_time
                        min_index = i
                        min_high = li[i]
                need_time_list.append(min_need_time)
                for i in range(min_index+1-pn, min_index+1):
                    li[i] = min_high
                counter = Counter(li)
                max_same = max([counter[key] for key in counter.keys()])
        print(flag)
        return need_time_list
    
    
class Solution2:
    @timer
    def solve(self , n , q , a , p ):
        
        li = sorted(a)
        counter = Counter(li)
        max_same = max([counter[key] for key in counter.keys()])
        need_time_list = []
        
        flag = 0
        
        for pn in p:
            if max_same >= pn:
                need_time_list.append(0)
            else:
                min_need_time = li[-1]*(pn-1)
                min_index = len(li) - 1
                min_high = li[-1]
                sorted_counter = sorted(counter.keys())
                index_start = sorted_counter.index(li[pn-1])
                for h in range(index_start, len(sorted_counter)):
                    flag+=1
                    high = sorted_counter[h]
                    index = li.index(high) + counter[high] - 1
                    need_time = ((pn-1)*li[index]) - sum(li[index-pn+1:index])
                    if need_time < min_need_time:
                        min_need_time = need_time
                        min_index = index
                        min_high = high
                need_time_list.append(min_need_time)
                for i in range(min_index+1-pn, min_index+1):
                    li[i] = min_high
                counter = Counter(li)
                max_same = max([counter[key] for key in counter.keys()])
        print(flag)
        return need_time_list
                    
    
    
target1 = [4,3,[1,2,3,4],[2,2,4]]
target2 = [50,10,[278,125,679,818,337,683,245,67,922,43,310,505,254,951,378,733,373,643,170,632,711,766,256,620,570,51,494,907,388,126,580,823,485,693,969,931,209,455,533,414,318,777,862,102,742,257,550,706,492,968],[28,15,19,38,27,13,23,38,11,30]]
target3 = [10000, 500, [random.randint(0, 10000) for i in range(10000)], [random.randint(0, 100) for i in range(1000)]]

tar = target2

s = Solution1()
print(s.solve(tar[0], tar[1], tar[2], tar[3]))

s = Solution2()
print(s.solve(tar[0], tar[1], tar[2], tar[3]))


'''
36
solve 共用时：0.00036920000002282904 s
[6189, 0, 0, 5748, 0, 0, 0, 0, 0, 0]
33
solve 共用时：0.0002461000003677327 s
[6189, 0, 0, 5748, 0, 0, 0, 0, 0, 0]
'''
            
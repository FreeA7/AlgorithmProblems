# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 14:48:34 2020

@author: FreeA7

https://www.nowcoder.com/practice/d0907f3982874b489edde5071c96754a

牛牛有一个数组array，牛牛可以每次选择一个连续的区间，让区间的数都加1，他想知道把这个数组变为严格单调递增，最少需要操作多少次？

示例
输入:
    [1,2,1]
输出:
    2
说明:
    把第三个数字+2可以构成1，2，3
"""

import sys
sys.path.append("..")
from utils.utils import timer
import random


class Solution1:
    @timer
    def IncreasingArray(self , array ):
        times = 0
        for i in range(1, len(array)):
            if array[i] > array[i-1]:
                continue
            else:
                difference = array[i-1]+1-array[i]
                for j in range(i, len(array)):
                    times += difference
                    array[j] += difference
        return times
    
    
class Solution2:
    @timer
    def IncreasingArray(self , array ):
        times = 0
        for i in range(1, len(array)):
            if array[i] > array[i-1]:
                continue
            else:
                times += array[i-1]+1-array[i]
        return times


# --------------------- 输出 ---------------------          
target1 = [1,2,1]
target2 = [random.randint(1, 10000) for _ in range(10000)]
tar = target2

s = Solution1()
print(s.IncreasingArray(tar.copy()))

s = Solution2()
print(s.IncreasingArray(tar.copy()))


'''
Solution1.IncreasingArray 共用时：7.796719600000188 s
16707683
Solution2.IncreasingArray 共用时：0.00324840000007498 s
16707683
'''
                        
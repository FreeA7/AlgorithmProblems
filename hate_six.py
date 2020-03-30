# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 14:02:02 2020

@author: FreeA7

https://www.nowcoder.com/practice/05dab66e4e814e21a9a3496fbddb69f1

众所周知，牛牛不喜欢6这个数字（因为牛牛和66发音相近）
所以他想知道，不超过n位十进制数中有多少个数字不含有连续的6（从1开始算的）
输入只包含一个正整数n（1<=n<20）

示例1
输入：
    1
输出：
    10
说明：
    1,2,3,4,5,6,7,8,9,10 这十个数字中都满足条件
    
示例2
输入：
    2
输出：
    99
说明：
    因为66不可以
"""

from utils import timer

class Solution1:
    @timer
    def calculate(self , n ):
        if n == 1:
            return 10**n
        if n == 2:
            return 10**n-1
        dp = [[0,0] for i in range(n)]
        dp[1] = [0,1]
        for i in range(2, n):
            dp[i][0] = 9*(dp[i-1][0]+dp[i-1][1])
            dp[i][1] = dp[i-1][0]+10**(i-1)
        return 10**n - sum(dp[n-1])
        
target1 = 4

s = Solution1()
print(s.calculate(target1))


'''
Solution1.calculate 共用时：0.00029850000009901123 s
4015114464816913999505087179044648463596359486913966399969910852418116748818843453877429608863986040
'''
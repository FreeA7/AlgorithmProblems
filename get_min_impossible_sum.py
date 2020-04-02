# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 14:06:28 2020

@author: FreeA7

https://www.nowcoder.com/practice/4921c3ebdffc4c4eab344fa78de89c67

牛妹在和牛牛玩扔骰子，他们的游戏规则有所不同；
每个人可以扔nn次mm面骰子，来获得nn个数
得分为任意选取nn个数中的某些数求和所不能得到的最小的正整数
得分大的人获胜
例如扔骰子33次得到了 11 22 55，那么这个人的得分是44

牛妹想知道这回合她是否能赢
牛妹的n个数存在数组a中，牛牛的n个数存在数组b中
数组下标从0开始

示例
输入：
    2,4,[1,2],[1,3]
输出：
    "Happy"
说明：
    牛妹能构成 11 22 33，牛妹的得分为4
    而牛牛只能构成11 33 55，牛牛的得分为2
    故牛妹胜利！
"""

from utils import timer
import random

        
class Solution1:
    def getMinImpossibleSum(self, li):
        if li[0] != 1:
            return 1
        min_sum = 2
        for i in li[1:]:
            if i <= min_sum:
                min_sum = min_sum + i
            else:
                return min_sum
        return min_sum
        
    @timer    
    def Throwdice(self , n , m , a , b ):
        a = sorted(a)
        b = sorted(b)
        if self.getMinImpossibleSum(a) > self.getMinImpossibleSum(b):
            return 'Happy'
        else:
            return 'Sad'
        
target1 = [2,4,[1,2],[1,3]]
target2 = [20,10,[4,9,7,10,3,7,8,4,6,6,3,10,9,3,5,9,1,8,3,2],[9,9,8,2,6,7,4,8,10,1,6,5,3,3,6,2,4,6,4,3]]
n = 2000000
m = 1000000000
target3 = [n, m, [random.randint(1,m) for _ in range(n)], [random.randint(1,m) for _ in range(n)]]

tar = target3

s = Solution1()
print(s.Throwdice(tar[0], tar[1], tar[2], tar[3]))
        

'''
Solution1.Throwdice 共用时：2.1336306999999124 s
Sad
'''

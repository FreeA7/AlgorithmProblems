# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 14:52:34 2020

@author: FreeA7
"""


from utils import timer
import random


# 每次都模拟操作
class Solution1:
    def getCutOut(self, li, i):
        li.pop(li.index(i))
        li = [i] + li
        return li
    
    @timer
    def countDislocation(self , n , cutIn ):
        li = list(range(1,n+1))
        for i in cutIn:
            li = self.getCutOut(li, i)
        li_o = list(range(1,n+1))
        k = 0
        for i in range(len(li)):
            if (li[i] - li_o[i]) == 0:
                k+=1
        return len(li)-k
            
            
# --------------------- 输出 ---------------------
target1 = [3,[3, 2, 3]]
target2 = [3,[]]
target3 = [10000, [random.randint(1, 10000) for i in range(10000)]]

tar = target3

s = Solution1()
print(s.countDislocation(tar[0], tar[1]))
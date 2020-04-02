# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 10:53:51 2020

@author: FreeA7

https://www.nowcoder.com/practice/efc16ce46397436a8d1a0008c52093c1

有两长度为n的数组a,b,希望统有多少数(l,r)满足
1. 0<=l<=r<=n-1
2. al + .. + ar == bl + br

示例1
输入:
    [1,2,3,4],[2,1,4,5]
输出:
    4
说明:
    满足条件的数对有(0, 1), (0, 2), (1, 1), (1, 2)(0,1),(0,2),(1,1),(1,2)
"""

import sys
sys.path.append("..")
from utils.utils import timer
import random

# 直接遍历
class Solution1:
    @timer
    def countLR(self , a , b ):
        nums = 0
        for i in range(len(a)):
            if a[i] == (2*b[i]):
                nums += 1
#                print('(%d,%d)'%(i, i))
        for i in range(len(a)-1):
            for j in range(i+1, len(a)):
                if sum(a[i:j+1]) == (b[i]+b[j]):
                    nums += 1
#                    print('(%d,%d)'%(i, j))
        return nums
    
# 不用sum，每次依次向后求和，边做比边求和
class Solution2:
    @timer
    def countLR(self , a , b ):
        nums = 0
        for i in range(len(a)):
            if a[i] == (2*b[i]):
                nums += 1
#                print('(%d,%d)'%(i, i))
        for i in range(len(a)-1):
            sum_temp = a[i]
            for j in range(i+1, len(a)):
                sum_temp += a[j]
                if sum_temp == (b[i]+b[j]):
                    nums += 1
#                    print('(%d,%d)'%(i, j))
                
        return nums
    

# 次求和，之后每减去上的
class Solution3:
    @timer
    def countLR(self , a , b ):
        nums = 0
        for i in range(len(a)):
            if a[i] == (2*b[i]):
                nums += 1
#                print('(%d,%d)'%(i, i))
        
        sum_list = []
        sum_temp = a[0]
        for i in range(1,len(a)):
            sum_temp += a[i]
            sum_list.append(sum_temp)
            if sum_temp == b[0] + b[i]:
                nums += 1
#                print('(%d,%d)'%(0, i))
        
        for i in range(1, len(a)-1):
            sum_list.pop(0)
            sum_list = list(map(lambda t:t-a[i-1], sum_list))
            n = 0
            for j in range(i+1, len(a)):
                if sum_list[n] == b[i] + b[j]:
                    nums += 1
#                    print('(%d,%d)'%(i, j))
                n += 1

        return nums
    
# 不用lambda函数，自行减
class Solution4:
    @timer
    def countLR(self , a , b ):
        nums = 0
        for i in range(len(a)):
            if a[i] == (2*b[i]):
                nums += 1
#                print('(%d,%d)'%(i, i))
        
        sum_list = []
        sum_temp = a[0]
        for i in range(1,len(a)):
            sum_temp += a[i]
            sum_list.append(sum_temp)
            if sum_temp == b[0] + b[i]:
                nums += 1
#                print('(%d,%d)'%(0, i))
        
        for i in range(1, len(a)-1):
            sum_list.pop(0)
            n = 0
            for j in range(i+1, len(a)):
                sum_list[n] = sum_list[n] - a[i-1]
                if sum_list[n] == b[i] + b[j]:
                    nums += 1
#                    print('(%d,%d)'%(i, j))
                n += 1
        
        return nums
    
# 不用pop
class Solution5:
    @timer
    def countLR(self , a , b ):
        nums = 0
        for i in range(len(a)):
            if a[i] == (2*b[i]):
                nums += 1
#                print('(%d,%d)'%(i, i))
        
        sum_list = []
        sum_temp = a[0]
        for i in range(1,len(a)):
            sum_temp += a[i]
            sum_list.append(sum_temp)
            if sum_temp == b[0] + b[i]:
                nums += 1
#                print('(%d,%d)'%(0, i))
        
        for i in range(1, len(a)-1):
            for j in range(i+1, len(a)):
                sum_list[j-1] = sum_list[j-1] - a[i-1]
                if sum_list[j-1] == b[i] + b[j]:
                    nums += 1
#                    print('(%d,%d)'%(i, j))
        
        return nums
    
# --------------------- 输出 ---------------------
target1 = [[1,2,3,4], [2,1,4,5]]
target2 = [[0,0,1,1,1],[2,0,4,3,3]]
target3 = [[52,3,65,78,0,69,87,79,44,54,85,8,6,35,25,84,66,77,12],[79,1367,942,757,864,1871,1379,5,640,1691,1585,1167,448,1819,2,573,260,918,724]]
target4 = [[random.randint(0,100) for i in range(2000)], [random.randint(0,100) for i in range(2000)]]

s = Solution1()
print(s.countLR(target4[0], target4[1]))

s = Solution2()
print(s.countLR(target4[0], target4[1]))

s = Solution3()
print(s.countLR(target4[0], target4[1]))

s = Solution4()
print(s.countLR(target4[0], target4[1]))

s = Solution5()
print(s.countLR(target4[0], target4[1]))

'''
countLR 共用时：21.897154299999784 s
38
countLR 共用时：0.40534389999993437 s
38
countLR 共用时：0.9579296000001705 s
38
countLR 共用时：0.9323930000000473 s
38
countLR 共用时：1.0634281000002375 s
38
'''

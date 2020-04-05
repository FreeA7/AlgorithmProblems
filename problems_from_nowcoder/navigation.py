# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 15:37:28 2020

@author: FreeA7

二维平面的海上有nn只船，每只船所在位置为(Xi,Yi)，每只船还有一个权值Wi,
现在他们需要聚在一起商讨捕鱼大业，他们想请你找到一个点使得该点到其他点的带权曼哈顿距离之和最小。
带权曼哈顿距离=实际曼哈顿距离*∗权值。

输入：
    2,[2,1],[1,1],[1,1]
输出：
    1
说明：
    可以选取(1,1)点，答案为1
"""


import sys
sys.path.append("..")
from utils.utils import timer
import random


# 设一个点左边有x个点，右边有n-x个点
# 那么如果这个点右移，那么cost=cost+x-(n-x)
# cost = cost+2x-n，可得cost是一个类似于二次函数
# 其中当x=n/2为最小值，而且在x=n/2时，点左右移动最小值不发生变化
# 当x<n/2，点右移cost变小，反之cost变大
# 故找到n/2即可
# 权值即可看做这个点上有w个船
class Solution1:
    @staticmethod
    def takeKeys(elem):
        return elem[0]
    
    def findMid(self, n_w, half_w):
        temp_w = 0
        for i in range(len(n_w)):
            temp_w += n_w[i][1]
            if temp_w >= half_w:
                break
        n = n_w[i][0]
        sum_distance = 0
        for i in range(len(n_w)):
            sum_distance += abs(n_w[i][0]-n)*n_w[i][1]
        return sum_distance
        
    @timer
    def MinimumDistance(self , n , x , y , w ):
        if len(x) == 0:
            return 0
        if len(x) == 1:
            return w[0]
        half_w = sum(w)//2
        x_w = sorted([(x[i],w[i]) for i in range(len(x))], key=Solution1.takeKeys)
        y_w = sorted([(y[i],w[i]) for i in range(len(y))], key=Solution1.takeKeys)
        return self.findMid(x_w, half_w) + self.findMid(y_w, half_w)
    

# 枚举，设有A B C三个点
# 那么对于A点：
#   distance = wb(B-A) + wc(C-A)
#   distance = (wbB + wcC) - A(wb+wc)
# 同理可以得C点：
#   distance = wb(C-B) + wa(C-A)
#   distance = C(wb+wa) - (wbB + waA)
# 故可设wa+wb+wc+...+wn 和 A+B+C+...+N
# 不断更新进行枚举，较少计算次数
class Solution2:
    @staticmethod
    def takeKeys(elem):
        return elem[0]
    
    def findMid(self, n_w, sum_weight_right):
        sum_distance_right = 0
        for n in n_w:
            sum_distance_right += n[0] * n[1]
        distance_list = set()
        sum_distance_left = 0
        sum_weight_left = 0
        for n in n_w:
            sum_weight_right -= n[1]
            sum_distance_right -= n[0]*n[1]
            distance_list.add(abs(sum_distance_right-n[0]*sum_weight_right) + abs(n[0]*sum_weight_left-sum_distance_left))
            sum_weight_left += n[1]
            sum_distance_left += n[0]*n[1]
        return min(distance_list)
    
    @timer
    def MinimumDistance(self , n , x , y , w ):
        if len(x) == 0:
            return 0
        if len(x) == 1:
            return w[0]
        sum_w = sum(w)
        x_w = sorted([(x[i],w[i]) for i in range(len(x))], key=Solution2.takeKeys)
        y_w = sorted([(y[i],w[i]) for i in range(len(y))], key=Solution2.takeKeys)
        return self.findMid(x_w, sum_w) + self.findMid(y_w, sum_w)
    
    
# --------------------- 输出 ---------------------
target1 = [2,[2,1],[1,1],[1,1]]
target2 = [10] + [[random.randint(1,100) for point in range(10)] for _ in range(3)]
target3 = [3] + [[random.randint(1,10) for point in range(3)] for _ in range(3)]
target4 = [1000000] + [[random.randint(1,10000) for point in range(1000000)] for _ in range(3)]

tar = target4

s = Solution1()
print(s.MinimumDistance(tar[0], tar[1], tar[2], tar[3]))

s = Solution2()
print(s.MinimumDistance(tar[0], tar[1], tar[2], tar[3]))


'''
Solution1.MinimumDistance 共用时：4.581264399999782 s
25002319564118
Solution2.MinimumDistance 共用时：7.3676331999995455 s
25002319564118
'''
    

        
        
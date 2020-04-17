# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 12:16:46 2020

@author: FreeA7

https://www.nowcoder.com/practice/6b0ab827bdde4d6a8b612545bbdf9685

给定一段线段树构造代码，按如下方式构造线段树。
你的任务是，对于T组询问，每个询问给出n，求对于每个n，运行build(1,1,n)后，输出ans。对于每个n，询问相互独立，即ans在上一个询问结束后归零。
输入时T单独给出，每个n会存储在数组a中给出。

示例
输入:
    2,[4,5]
输出:
    [7,9]
说明:
    当n=4时，构造出的线段树的区间编号及其对应的区间为
    1[1,4],2[1,2],3[3,4],4[1,1],5[2,2],6[3,3],7[4,4]
    当n=5时，构造出的线段树的区间编号及其对应的区间为
    1[1,5],2[1,3],3[4,5],4[1,2],5[3,3],6[4,4],7[5,5],8[1,1],9[2,2]
    其中[]外的是编号，[]内表示区间的起始位置和终末位置。
    可知，当n=4时编号最大为7，当n=5时编号最大为9
"""


import sys
sys.path.append("..")
from utils.utils import timer
import random


# 递归构造线段树
class Solution1:
    @staticmethod
    def build(x, y, z):
        ans = x
        if y == z:
            return ans
        mid = (y + z)//2
        ans_left = Solution1.build(x*2, y, mid)
        ans_right = Solution1.build(x*2+1, mid+1, z)
        return max(ans, ans_left, ans_right)

    @timer
    def wwork(self , T , a ):
        return [self.build(1,1,i) for i in a]
    

# 直接寻找最深的线段树
class Solution2:
    @staticmethod
    # 计算线段子树的深度
    def getDepth(l, r):
        i = r-l+1
        n = 0
        while i-(1<<n) > 0:
            n += 1
        return n
    
    @staticmethod
    def build(x, y, z):
        ans = x
        if y == z:
            return ans
        mid = (y + z)//2
        # 右边大于等于左边，或者虽然左边长，但是两边的子树深度一样，都选择右边
        if (z-(mid+1)) >= (mid-y) or Solution2.getDepth(y, mid) == Solution2.getDepth((mid+1), z):
            ans_child = Solution2.build(x*2+1, mid+1, z)
        else:
            ans_child = Solution2.build(x*2, y, mid)
        return max(ans, ans_child)

    @timer
    def wwork(self , T , a ):
        return [self.build(1,1,i) for i in a]
    

# --------------------- 输出 ---------------------  
target1 = [2,[4,5,10]]
target2 = [20,[28,55,87,93,50,65,10,43,45,28,22,18,32,46,17,29,67,35,70,94]]
target3 = [1000, [random.randint(10, 1000) for _ in range(1000)]]
tar = target3

s = Solution1()
res1 = s.wwork(tar[0], tar[1])

s = Solution2()
res2 = s.wwork(tar[0], tar[1])

print(res1==res2)


'''
Solution1.wwork 共用时：0.6933627999987948 s
Solution2.wwork 共用时：0.022634700000708108 s
True
'''

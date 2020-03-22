# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 14:52:34 2020

@author: FreeA7

https://www.nowcoder.com/practice/31c1ae9d1c804b66b6ae17181e76f4f0

你有一个长度为 n 的队伍，从左到右依次为 1~n，有 m 次插队行为，用数组 cutIn 进行表示
cutIn 的元素依次代表想要插队的人的编号，每次插队，这个人都会直接移动到队伍的最前方。
你需要返回一个整数，代表这 m 次插队行为之后，有多少个人已经不在原来队伍的位置了。

示例
输入:
    3,[3, 2, 3]
输出:
    2
说明：
    初始队伍为 [1, 2, 3]
    3 开始插队 [3, 1, 2]
    2 开始插队 [2, 3, 1]
    3 开始插队 [3, 2, 1]
    所以2还在原来的尾置，3和1两个人已经不在原来的位置了。
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
    

# 直接由cutIn反推出最后的数列
class Solution2:
    @timer
    def countDislocation(self , n , cutIn ):
        n = list(range(1,n+1))
        cutset = []
        cutIn.reverse()
        for i in cutIn:
            if i not in cutset:
                cutset.append(i)
        for i in n:
            if i not in cutset:
                cutset.append(i)
        k = 0
        for i in range(len(n)):
            if n[i] - cutset[i] == 0:
                k+=1
        return len(n) - k
   
    
# 方法二的优化版，减少循环次数
class Solution3:
    @timer
    def countDislocation(self , n , cutIn ):
        l = n
        n = list(range(1,n+1))
        cutset = []
        cutIn.reverse()
        for i in cutIn:
            if i not in cutset:
                cutset.append(i)
                n.remove(i)
        cutset += n
        k = 0
        for i in range(len(cutset)):
            if i+1 == cutset[i]:
                k+=1
        return l - k
    
    
# 方法二继续优化，直接在循环时进行最终值求解
class Solution4:
    @timer
    def countDislocation(self , n , cutIn ):
        l = n
        n = list(range(1,n+1))
        cutset = []
        cutIn.reverse()
        k = 0
        lc = 0
        for i in range(len(cutIn)):
            if cutIn[i] not in cutset:
                cutset.append(cutIn[i])
                n.remove(cutIn[i])
                lc += 1
                if i+1 == cutIn[i]:
                    k += 1
        for i in range(l - lc):
            if lc+i+1 == n[i]:
                k += 1
        return l - k
            
            
# --------------------- 输出 ---------------------
target1 = [3,[3, 2, 3]]
target2 = [3,[]]
target3 = [30000, [random.randint(1, 30000) for i in range(30000)]]
target4 = [10000, [random.randint(1, 10000) for i in range(10000)]]

tar = target3

s = Solution1()
print(s.countDislocation(tar[0], tar[1]))

s = Solution2()
print(s.countDislocation(tar[0], tar[1]))

s = Solution3()
print(s.countDislocation(tar[0], tar[1]))

s = Solution4()
print(s.countDislocation(tar[0], tar[1]))

'''
countDislocation 共用时：17.863019299998996 s
30000
countDislocation 共用时：16.10261950000131 s
30000
countDislocation 共用时：10.618880999994872 s
30000
countDislocation 共用时：10.696929699995962 s
30000
'''
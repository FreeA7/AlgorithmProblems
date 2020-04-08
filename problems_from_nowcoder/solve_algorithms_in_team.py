# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 12:25:50 2020

@author: FreeA7

https://www.nowcoder.com/practice/397cf1012db14edebe6e91479d536171

牛牛有一个算法交流群，它是这个群的群主，也是这个群实力最强的人。

算法交流群里一共有n个人，每个人都有一个等级ai表示它能解决难度小于等于ai的算法问题。

除了牛牛以外，群里的每个编号为i的人都在群里有一个等级比他高的朋友编号为pi。
群友i会解决那些他产生和接收的等级小于等于ai的问题，并把解决不了的问题全部交给pi
保证牛牛的编号为1。保证牛牛的等级全场唯一且全场最高。如果牛牛解决不了他接收的问题，他将不管这些问题。

这天群里的每个人都产生了一个问题，牛牛知道了每个人产生问题等级ki ，他想知道群里的每个人在这天解决了多少问题。

示例1
输入：
    4,[4,3,2,1],[1,2,3],[1,2,3,4]
输出：
    [2,2,0,0]
说明：
    群里一共有4个人
    4产生了等级为4的问题，4的能力值为1，无法解决，所以4号把这个问题交给了3号.4号解决问题个数为0
    3号产生了等级为3的问题，接受到等级为4的问题。3号本身等级为2，无法解决这两个问题，于是把这两个问题交给了2，自身解决问题个数为0.
    2号产生了等级为2的问题，接受到等级为3，4的两个问题。2号等级为3，解决了等级为2，3的问题，把等级为4的问题交给了1.自身解决问题个数为2
    1号产生了等级为1的问题，接受到等级为4的问题。1号自身等级为4，解决了这两个问题。自身解决问题个数为2
"""

import sys
sys.path.append("..")
from utils.utils import timer
import random
import copy
import sys

class Tree1(object):
    def __init__(self, capacity, parent):
        self.capacity = capacity
        self.parent = parent
        self.problems = 0
        
    def solveProblem(self, difficulty):
        if difficulty <= self.capacity:
            self.problems += 1
        elif self.parent:
            self.parent.solveProblem(difficulty)
        

# 第一次循环构造树，第二次循环认parent
class Solution1:
    @timer
    def solve(self , n , a , p , k ):
        a[0] = Tree1(a[0], None)
        for i in range(1, len(a)):
            a[i] = Tree1(a[i], p[i-1])
        for i in range(1, len(a)):
            a[i].parent = a[a[i].parent-1]
        for i in range(len(k)):
            a[i].solveProblem(k[i])
        return [tree.problems for tree in a]
  
    
class Tree2(object):
    def __init__(self, capacity, parent):
        self.capacity = capacity
        self.parent = parent
        self.problems = 0
        
    def solveProblem(self, difficulty):
        if difficulty <= self.capacity:
            self.problems += 1
        elif self.parent:
            self.parent[0].solveProblem(difficulty)
    
   
# 利用list的指针，一次循环直接构造树和认parent
class Solution2:
    @timer
    def solve(self , n , a , p , k ):
        a = [[i] for i in a]
        a[0][0] = Tree2(a[0][0], None)
        for i in range(1, len(a)):
            a[i][0] = Tree2(a[i][0], a[p[i-1]-1])
        for i in range(len(k)):
            a[i][0].solveProblem(k[i])
        return [tree[0].problems for tree in a]
    

# --------------------- 输出 ---------------------    
sys.setrecursionlimit(5000)

target1 = [4,[4,3,2,1],[1,2,3],[1,2,3,4]]

person_num = 3500
target2 = [person_num, list(range(person_num,0,-1)), list(range(1,person_num)), [random.randint(1,person_num) for i in range(person_num)]]

tar = copy.deepcopy(target2)

s = Solution1()
s1 = s.solve(tar[0], tar[1], tar[2], tar[3])

tar = copy.deepcopy(target2)

s = Solution2()
s2 = s.solve(tar[0], tar[1], tar[2], tar[3])

print(s1==s2)


'''
Solution1.solve 共用时：1.010118900000002 s
Solution2.solve 共用时：1.0882784 s
True
'''
            
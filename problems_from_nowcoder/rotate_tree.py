# -*- coding: utf-8 -*-
"""
Created on Tue May 12 08:45:59 2020

@author: FreeA7

https://www.nowcoder.com/practice/895faf01a4d84984af76899b80d15f15

牛牛很喜欢玩二叉树。这天牛能送给了他一个以1为根结点的{n}n个结点的二叉树，他想对这个二叉树进行一些加工。

牛牛刚刚学会转圈圈，所以很喜欢旋转。现在他想对这颗二叉树进行m次旋转。

每次旋转牛牛会指定一个结点，并让以这个结点为根的子树中的所有结点的左右儿子互换。

多次操作之后，牛牛希望以中序遍历的方式输出操作完之后的二叉树。

示例
输入:
    5,3,[4,3,0,0,0],[2,0,0,5,0],[3,1,5]
输出:
    [2,3,1,5,4]
说明:
    最开始1的左儿子为4，右儿子为2
    2的左儿子为3.
    4的右儿子为5.
    第一次操作结点3，结点3没有儿子，所以没有发生变化
    第二次操作结点1，结点1的左儿子变为2，右儿子变为4. 
    结点4的左儿子变为5，右儿子变为不存在。结点
    结点2的左儿子变为不存在，右儿子变成3
    第三次操作结点5，结点5没有儿子，不发生变化。
    最开始1的左儿子为2，右儿子为4
    2的右儿子为3.
    4的左儿子为5.
    中序遍历结果为[2,3,1,5,4]
"""


import sys
sys.path.append("..")
from utils.utils import timer
import random


class Tree:
    def __init__(self, value, parent):
        self.value = value
        self.parent = parent
        self.left_child = None
        self.right_child = None
        
    def rotate(self):
        if self.left_child:
            self.left_child.rotate()
        if self.right_child:
            self.right_child.rotate()
        self.left_child, self.right_child = self.right_child, self.left_child
        
    def printTree(self):
        output = []
        if self.left_child:
            output += self.left_child.printTree()
        output.append(self.value)
        if self.right_child:
            output += self.right_child.printTree()
        return output


class Solution:
    def createTree(self, l, r):
        root = Tree(1, None)
        nodes = {1:root}
        parents = [root]
        index = 0
        while len(parents) != 0 and index < len(l):
            node = parents.pop(0)
            if l[index]:
                tree_l = Tree(l[index], node)
                node.left_child = tree_l
                parents.append(tree_l)
                nodes[l[index]] = tree_l
            if r[index]:
                tree_r = Tree(r[index], node)
                node.right_child = tree_r
                parents.append(tree_r)
                nodes[r[index]] = tree_r
            index += 1
        return root, nodes
        
    @timer
    def solve(self , n , m , l , r , k ):
        root, nodes = self.createTree(l, r)
        for i in k:
            nodes[i].rotate()
        return root.printTree()
        
 
# --------------------- 输出 --------------------- 
target1 = [5,3,[4,3,0,0,0],[2,0,0,5,0],[3,1,5]]
tar = target1

s = Solution()
print(s.solve(tar[0], tar[1], tar[2], tar[3], tar[4]))


'''
Solution.solve 共用时：4.0500000068277586e-05 s
[2, 1, 4, 3, 5]
'''
        
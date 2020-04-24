# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 10:41:23 2020

@author: FreeA7

https://www.nowcoder.com/practice/313783d094ec41d49215ffa2097d9b54

题面
n-1条道路连通的 n座城市，城市两两之间有且只有一条路径，每条都道路都有一个权值 w。

现在城市之间要建立通讯网络，两座城市之间通讯质量取决于链路所经路径的权值和，权值和越大则链路的通讯质量越高。
一条路径被破坏后，经过这条路径的所有通讯线路均被破坏。
牛牛想知道哪条道路一旦被破坏，对整个城市通讯网络的影响最大。

示例
输入:
    5,[1,4,5,4],[5,1,2,3],[9,25,30,8]
输出:
    150
说明:
    经过第二条边的城市对有 （1,4), (1,3), (5, 4), (5, 3), (2, 4), (2, 3), 第二条边对通信网络的贡献为 25 * 6 = 150
"""


import sys
sys.path.append("..")
from utils.utils import timer
import random


# 对于每一个边，所经过的路径数量即左边的城市数量乘以右边的城市数量
# 所以记录每一个节点的子节点数也就是城市数量
# 那么通过其和其parent的路所拥有的路径就是总节点数量减去其子节点数量 * 其子节点数量
# 最后再乘上权重就行了
# 所以首先建立树，然后dfs计算每个节点城市数量，然后dfs寻找最大
class Tree:
    def __init__(self, value, parent, distance):
        self.value = value
        self.parent = parent
        self.distance = distance
        self.number = -1
        self.children = []
        
    def addChild(self, child):
        self.children.append(child)

class Solution:
    def getDistance(self, n, u, v, w):
        distance = {}
        for node in range(1, n+1):
            distance[node] = {}
            for i in range(len(u)):
                if u[i] == node:
                    distance[node][v[i]] = w[i]
            for i in range(len(v)):
                if v[i] == node:
                    distance[node][u[i]] = w[i]
        return distance
    
    def createTree(self, root, distance):
        tree = Tree(root, None, 0)
        nodes = [tree]
        while len(nodes) > 0:
            node = nodes.pop()
            for key in distance[node.value].keys():
                if not node.parent or key != node.parent.value:
                    tree_this_node = Tree(key, node, distance[key][node.value])
                    node.addChild(tree_this_node)
                    nodes.append(tree_this_node)
        return tree
    
    def dfsSetNumber(self, tree):
        number = 1
        for child in tree.children:
            if child.number == -1:
                self.dfsSetNumber(child)
            number += child.number
        tree.number = number
        
    def dfsFindMax(self, tree):
        number = tree.number
        nodes = tree.children
        max_contribution = 0
        while len(nodes) > 0:
            node = nodes.pop()
            max_contribution = max(max_contribution, (number-node.number)*node.number*node.distance)
            for child in node.children:
                nodes.append(child)
        return max_contribution
        
    @timer
    def solve(self , n , u , v , w ):
        if len(u) == 1:
            return w[0]
        distance = self.getDistance(n, u, v, w)
        tree = self.createTree(u[0], distance)
        self.dfsSetNumber(tree)
        return self.dfsFindMax(tree)


# --------------------- 输出 ---------------------     
target1 = [5,[1,4,5,4],[5,1,2,3],[9,25,30,8]]
target2 = [1000, list(range(1, 501)) + list(range(1,500)), list(range(1000, 500, -1)) + list(range(2,501)), [random.randint(1, 100) for _ in range(999)]]
tar = target2
s = Solution()
print(s.solve(tar[0], tar[1], tar[2], tar[3]))


'''
Solution.solve 共用时：0.24098720000074536 s
24999600
'''
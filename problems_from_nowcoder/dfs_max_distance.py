# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 00:53:27 2020

@author: FreeA7

https://www.nowcoder.com/practice/430ded6b482d4d8bbcf2eca6f20e62e3

城市 AA 新建了 nn 个座房子，城市规划处用 n-1n−1 条双向街道将房子连在一起，使得任意两座房子之间有且仅有一条道路可达。
牛牛和牛妹将被随机分到两个房子，现在牛牛想知道，他和牛妹房子的最长路径是多少。

示例
输入:
    7,[2,3,5,4,5,5],[5,2,1,6,7,4],[15,6,14,4,1,6]
输出：
    35
"""


import sys
sys.path.append("..")
from utils.utils import timer
import random
from collections import Counter


# 直接当做图来处理，首先找到所有的末端节点
# 然后以每一个末端节点为出发点进行dfs计算与其他末端节点的距离
# 最终计算每一次dfs距离的最大值即可
class Solution1:
    def dfs(self, start_node, n, distance):
        distance_this_node = {start_node:0}
        seen = set()
        seen.add(start_node)
        li = list(distance[start_node].keys())
        li = [(i, start_node) for i in li]
        while len(seen) < n:
            node = li.pop()
            if node[0] not in seen:
                seen.add(node[0])
                distance_this_node[node[0]] = distance_this_node[node[1]] + distance[node[1]][node[0]]
                for key in distance[node[0]].keys():
                    if key not in seen:
                        li.append((key, node[0]))
        return distance_this_node
                
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
      
    @timer
    def solve(self , n , u , v , w ):
        c = Counter(u+v)
        nodes = []
        for key in c.keys():
            if c[key] == 1:
                nodes.append(key)
        distance = self.getDistance(n, u, v, w)
        distance_nodes = {}
        max_distance = 0
        for node in nodes:
            distance_nodes[node] = self.dfs(node, n, distance)
            max_distance = max(max_distance, distance_nodes[node][max(distance_nodes[node], key=distance_nodes[node].get)])
        return max_distance
 
    
# Solution2
# 以任意一个非末端节点为根建立树
# 然后依次计算每一个节点的距离
# 根节点的最大距离就是最大的两个子树距离之和
# 但是这么做有一个问题，就是这道题中路径是可以不经过根节点的
# 并且这个算法写的很丑陋还是错的，不符合target3
class Tree:
    def __init__(self, value, parent):
        self.value = value
        self.parent = parent
        self.distance = -1
        self.children = []
        
    def addChild(self, child):
        self.children.append(child)
    
    
class Solution2:
    def createTree(self, root, distance):
        tree_root = Tree(root, None)
        node_list = list(distance[root].keys())
        # 等待被建立的子树
        node_list = [(i, tree_root) for i in node_list]
        # 所有子树的list
        tree_list = []
        while len(node_list) > 0:
            node = node_list.pop()
            value = node[0]
            parent = node[1]
            tree_node = Tree(value, parent)
            parent.addChild(tree_node)
            leaf_flag = 1
            for key in distance[value].keys():
                if key != parent.value:
                    node_list.append((key, tree_node))
                    leaf_flag = 0
            # 如果是末端节点的话写上距离
            if leaf_flag:
                tree_node.distance = distance[value][parent.value]
            else:
                tree_list.append(tree_node)
        # 对所有子树进行操作（非根非叶）
        while len(tree_list) > 0:
            # 每一轮找一个所有子节点都已经设定距离的子树
            for tree in tree_list:
                do_flag = 1
                max_distance = 0
                for child in tree.children:
                    if child.distance == -1:
                        do_flag = 0
                        break
                    else:
                        max_distance = max(max_distance, child.distance)
                # 所有子节点都有distance，所以设定这个节点的distance
                if do_flag:
                    tree_list.remove(tree)
                    tree.distance = max_distance + distance[tree.value][tree.parent.value]
        return tree_root
        
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
        
    @timer
    def solve(self , n , u , v , w ):
        distance = self.getDistance(n, u, v, w)
        for root in distance.keys():
            if len(distance[root]) > 1:
                break
        tree = self.createTree(root, distance)
        distance_list = []
        for child in tree.children:
            distance_list.append(child.distance)
        distance_list.sort()
        # 返回的是通过子树的最大距离
        return distance_list[-1] + distance_list[-2]


# Solution3
# 任选一个根建立树
# 然后dfs设定distance
# 这个不同之处在于在设定distance时顺便设定了max_distance
# 即过这个节点的最大距离，算法就是最大的和第二大的子节点distance加和，和Solution2对根节点的处理一样
# 最后使用一个dfs找到所有节点的最大的max_distance
class TreeDis:
    def __init__(self, value, parent):
        self.value = value
        self.parent = parent
        self.max_distance = -1
        self.distance = -1
        self.children = []
        
    def addChild(self, child):
        self.children.append(child)
   
     
class Solution3:
    def createTree(self, root, distance):
        tree = TreeDis(root, None)
        nodes = [tree]
        while len(nodes) > 0:
            node = nodes.pop()
            for key in distance[node.value]:
                if not node.parent or key != node.parent.value:
                    tree_this_node = TreeDis(key, node)
                    node.addChild(tree_this_node)
                    nodes.append(tree_this_node)
        return tree
    
    def dfsSetDistance(self, tree, distance):
        max_distance = 0
        max_second_distance = 0
        for child in tree.children:
            if child.distance == -1:
                self.dfsSetDistance(child, distance)
            if child.distance > max_distance:
                max_distance = child.distance
            elif child.distance <= max_distance and child.distance > max_second_distance:
                max_second_distance = child.distance
        if tree.parent:
            tree.distance = max_distance + distance[tree.value][tree.parent.value]
        tree.max_distance = max_distance + max_second_distance
        
    def dfsGetMax(self, tree):
        nodes = [tree]
        max_distance = 0
        while len(nodes) > 0:
            node = nodes.pop()
            for child in node.children:
                nodes.append(child)
            max_distance = max(max_distance, node.max_distance)
        return max_distance
  
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
       
    @timer
    def solve(self , n , u , v , w ):
        if len(u) == 1:
            return w[0]
        distance = self.getDistance(n, u, v, w)
        tree = self.createTree(u[0], distance)
        self.dfsSetDistance(tree, distance)
        return self.dfsGetMax(tree)


# --------------------- 输出 ---------------------    
target1 = [7,[2,3,5,4,5,5],[5,2,1,6,7,4],[15,6,14,4,1,6]]
target2 = [5,[2,3,1,3],[1,5,5,4],[13,6,8,6]]
target3 = [9, [1,1,3,3,4,5,6,7], [2,3,4,5,6,7,8,9], [1,1,1,1,1,1,1,1,1]]
target4 = [1000, list(range(1, 501)) + list(range(1,500)), list(range(1000, 500, -1)) + list(range(2,501)), [random.randint(1, 100) for _ in range(999)]]
tar = target4
s = Solution1()
print(s.solve(tar[0], tar[1], tar[2], tar[3]))

s = Solution2()
print(s.solve(tar[0], tar[1], tar[2], tar[3]))

s = Solution3()
print(s.solve(tar[0], tar[1], tar[2], tar[3]))
        

'''
Solution1.solve 共用时：1.621202600000288 s
23897
Solution2.solve 共用时：0.3040048000002571 s
23897
Solution3.solve 共用时：0.3493035999999847 s
23808
'''     
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 00:53:27 2020

@author: FreeA7
"""

from collections import Counter

class Solution:
    def dfs(self, start_node, n, distance):
        distance_this_node = {start_node:0}
        seen = set()
        seen.add(start_node)
        li = [(list(distance[start_node].keys())[0], start_node)]
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
    
target1 = [7,[2,3,5,4,5,5],[5,2,1,6,7,4],[15,6,14,4,1,6]]
tar = target1
s = Solution()
print(s.solve(tar[0], tar[1], tar[2], tar[3]))
        
        


# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 16:57:45 2020

@author: FreeA7
"""

from heapq import heappush, heappop

graph = {
    'A':{'B':5, 'C':1},
    'B':{'A':5, 'C':2, 'D':1},
    'C':{'A':1, 'B':2, 'D':4, 'E':8},
    'D':{'B':1, 'C':4, 'E':3, 'F':6},
    'E':{'C':8, 'D':3},
    'F':{'D':6}
}

def dijkstra(graph, s):
    # 设定优先队列
    priority_queue = []
    # (距， node node的parent)
    heappush(priority_queue, (0, s, None))
    # 小已经输出
    seen = set()
    # parent的映
    parent = {}
    # 队列为空则结
    while len(priority_queue) != 0:
        # 取出个node
        node = heappop(priority_queue)
        # 如果还没输出过则说明这是小进行输出并记录parent和距
        if node[1] not in seen:
            seen.add(node[1])
            parent[node[1]] = [node[0], node[2]]
            print(node)
            # 没输出过明他相关的距信还没输入则进行输
            # 如果输出过则信息已经用最小考虑了，重输出没有意
            for w in graph[node[1]].keys():
                # 他相关的距信如果已经输出说明已经找到了最小则不用再找
                # 因为小的会优先考虑，所以不能出现输出了还发现更小的
                if w not in seen:
                    # 以加上一个distance设每点初始距离为正无穷，有距离更小再放进队列
                    # 如果像我这样不进行判则是通过前后出队列顺序自动判也可以，因为如果大了输出的也晚也不会计入
                    heappush(priority_queue, (node[0]+graph[node[1]][w], w, node[1]))
    return parent

print(dijkstra(graph, 'A'))
    
'''
(0, 'A', None)
(1, 'C', 'A')
(3, 'B', 'C')
(4, 'D', 'B')
(7, 'E', 'D')
(10, 'F', 'D')
{'A': [0, None], 'C': [1, 'A'], 'B': [3, 'C'], 'D': [4, 'B'], 'E': [7, 'D'], 'F': [10, 'D']}
'''
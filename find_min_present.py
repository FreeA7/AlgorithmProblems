# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 16:13:06 2020

@author: FreeA7

https://www.nowcoder.com/practice/c4f777778e3040358e1e708750bb7fb9

众所周知，牛妹有很多很多粉丝，粉丝送了很多很多礼物给牛妹，牛妹的礼物摆满了地板。
地板是N×M的格子，每个格子有且只有一个礼物，牛妹已知每个礼物的体积。
地板的坐标是左上角(1,1)  右下角（N, M）。
牛妹只想要从屋子左上角走到右下角，每次走一步，每步只能向下走一步或者向右走一步或者向右下走一步
每次走过一个格子，拿起（并且必须拿上）这个格子上的礼物。
牛妹想知道，她能走到最后拿起的所有礼物体积最小和是多少？

示例
输入:
    [[1,2,3],[2,3,4]]
输出:
    7
说明：
    (1,1)->(1,2)->(2,3)
"""

from utils import timer
import random

from heapq import heappush, heappop
# Dijkstra
class Solution1:
    @timer
    def selectPresent(self , presentVolumn ):
        li = presentVolumn
        if li == []:
            return 0
        priority_queue = [[li[0][0], [0, 0]]]
        seen = []
        while len(priority_queue) != 0:
            node = heappop(priority_queue)
            if node[1] == [len(li)-1, len(li[0])-1]:
                    return node[0]
            if node[1] not in seen:
                seen.append(node[1])
                try:
                    heappush(priority_queue, [li[node[1][0]+1][node[1][1]+1]+node[0], [node[1][0]+1, node[1][1]+1]])
                    heappush(priority_queue, [li[node[1][0]+1][node[1][1]]+node[0], [node[1][0]+1, node[1][1]]])
                    heappush(priority_queue, [li[node[1][0]][node[1][1]+1]+node[0], [node[1][0], node[1][1]+1]])
                except IndexError:
                    try:
                        heappush(priority_queue, [li[node[1][0]+1][node[1][1]]+node[0], [node[1][0]+1, node[1][1]]])
                    except IndexError:
                        try:
                            heappush(priority_queue, [li[node[1][0]][node[1][1]+1]+node[0], [node[1][0], node[1][1]+1]])
                        except IndexError:
                            pass
   
# 动态规划                     
class Solution2:
    @timer
    def selectPresent(self , presentVolumn ):
        if presentVolumn == []:
            return 0
        N = len(presentVolumn)
        M = len(presentVolumn[0])
        for i in range(1, M):
            presentVolumn[0][i] += presentVolumn[0][i-1]
        for i in range(1, N):
            presentVolumn[i][0] += presentVolumn[i-1][0]
            for j in range(1, M):
                presentVolumn[i][j] += min([presentVolumn[i][j-1],presentVolumn[i-1][j], presentVolumn[i-1][j-1]])
        return presentVolumn[N-1][M-1]
                
# --------------------- 输出 ---------------------
target1 = [[1,2,3],[2,3,4]]
target2 = [[1,1,1],[1,1,1]]
target3 = [[random.randint(0, 100) for i in range(100)] for j in range(100)]

tar = target3

s = Solution1()
print(s.selectPresent(tar))

s = Solution2()
print(s.selectPresent(tar))
                
'''
selectPresent 共用时：4.9216074000000845 s
2841
selectPresent 共用时：0.007432699999753822 s
2841
'''
        

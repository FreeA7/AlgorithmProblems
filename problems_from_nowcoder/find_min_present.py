# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 16:13:06 2020

@author: FreeA7

https://www.nowcoder.com/practice/c4f777778e3040358e1e708750bb7fb9

众所周知，牛妹有很很多粉丝，粉丝送了很很多礼物给牛，牛的礼物摆满了地板
地板是N×M的格子，每个格子有且有一礼物，牛妹已知每礼物的体
地板的坐标是左上(1,1)  右下角（N, M）
牛只想从屋子左上角走到右下，每走步，每只能向下走步或者向右走步或者向右下走一
每走过一格子，拿起（并且必须拿上）这格子上的礼物
牛想知道，她能走到最后拿起的有礼物体小和多少

示例
输入:
    [[1,2,3],[2,3,4]]
输出:
    7
说明
    (1,1)->(1,2)->(2,3)
"""

import sys
sys.path.append("..")
from utils.utils import timer
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
   
# 动划                     
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
        

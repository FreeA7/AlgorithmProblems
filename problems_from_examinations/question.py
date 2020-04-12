# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 22:11:08 2020

@author: FreeA7

给定一个二维的矩阵，包含 ‘X’ 和 ‘O’（字母 O）。

找到所有被 ‘X’ 围绕的区域，并将这些区域里所有的 ‘O’ 用 ‘X’ 填充。

    X X X X
    X O O X
    X X O X
    X O X X

return:
    
    X X X X
    X X X X
    X X X X
    X O X X

华为技术面试
"""

def replaceO(area):
    if len(area) <= 2:
        return area
    no_replace_node = []
    for i in range(1, len(area)-1):
        for j in range(1, len(area[i])-1):
            if area[i][j] == 'O' and [i,j] not in no_replace_node:
                oarea = DFS(i, j)
                for node in oarea:
                    if node.x == 0 or node.x == len(area) - 1 or node.y == 0 or node.y == len(area[i])-1:
                        no_replace_node += oarea
                        oarea = []
                        break
                for node in oarea:
                    area[node.x][node.y] = 'X'
    return area

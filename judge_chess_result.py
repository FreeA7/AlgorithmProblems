# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 11:48:33 2020

@author: FreeA7

https://www.nowcoder.com/practice/2b0f51e8b1594d7091576dab05e00693

牛妹在和牛牛下牛客象棋。现在轮到牛妹了，牛妹想知道她在这一回合能否战胜牛牛。

棋盘chessboard上只可能包含：炮，将，车，兵

示例
输入:
    ["......", "..B...", "P.C.j.", "......", "..b..."," ...J.." ]
输出:
    "Happy"
说明：
    牛妹的炮可以攻击到牛牛的将，所以获胜
"""

from utils import timer
import random


class Solution:   
    @timer
    def playchess(self , chessboard ):
        chessboard = [line.strip() for line in chessboard]
        H = len(chessboard)
        W = len(chessboard[0])
        for h in range(H):
            for w in range(W):
                if chessboard[h][w] == 'j':
                    if w > 0:
                        chess_num = 0
                        if chessboard[h][w-1] == 'B' or chessboard[h][w-1] == 'J':
                            return 'Happy'
                        for x in range(w-1, -1, -1):
                            if chessboard[h][x] != '.':
                                if chessboard[h][x] == 'P' and chess_num == 1:
                                    return 'Happy'
                                if chessboard[h][x] == 'C' and chess_num == 0:
                                    return 'Happy'
                                chess_num += 1
                                if chess_num > 1:
                                    break
                    if w < W-1:
                        chess_num = 0
                        if chessboard[h][w+1] == 'B' or chessboard[h][w+1] == 'J':
                            return 'Happy'
                        for x in range(w+1, W):
                            if chessboard[h][x] != '.':
                                if chessboard[h][x] == 'P' and chess_num == 1:
                                    return 'Happy'
                                if chessboard[h][x] == 'C' and chess_num == 0:
                                    return 'Happy'
                                chess_num += 1
                                if chess_num > 1:
                                    break
                    if h > 0:
                        chess_num = 0
                        if chessboard[h-1][w] == 'B' or chessboard[h-1][w] == 'J':
                            return 'Happy'
                        for y in range(h-1, -1, -1):
                            if chessboard[y][w] != '.':
                                if chessboard[y][w] == 'P' and chess_num == 1:
                                    return 'Happy'
                                if chessboard[y][w] == 'C' and chess_num == 0:
                                    return 'Happy'
                                chess_num += 1
                                if chess_num > 1:
                                    break
                    if h < H-1:
                        chess_num = 0
                        if chessboard[h+1][w] == 'B' or chessboard[h+1][w] == 'J':
                            return 'Happy'
                        for y in range(h+1, H):
                            if chessboard[y][w] != '.':
                                if chessboard[y][w] == 'P' and chess_num == 1:
                                    return 'Happy'
                                if chessboard[y][w] == 'C' and chess_num == 0:
                                    return 'Happy'
                                chess_num += 1
                                if chess_num > 1:
                                    break
                    return 'Sad'

              
# --------------------- 输出 ---------------------              
target1 = ["......", "..B...", "P.C.j.", "......", "..b...","...J.." ]
target2 = ["....j.", "......", "......", "......", "......","....P." ]
chess = 'PCBpcb' + ('.'*94)

target3 = [[chess[random.randint(0, 99)] for w in range(1000)] for h in range(1000)]
target3[random.randint(0, 999)][random.randint(0, 999)] = 'j'
target3[random.randint(0, 999)][random.randint(0, 999)] = 'J'
target3 = [''.join(line) for line in target3]

tar = target3
s = Solution()
print(s.playchess(tar))


'''
Solution.playchess 共用时：0.02213099999971746 s
Sad
'''
                        
                    
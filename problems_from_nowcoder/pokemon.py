# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 15:38:24 2020

@author: FreeA7

https://www.nowcoder.com/practice/a4cc4ef629f146f68c5d02e06dfd6b99?tpId=110

牛牛是励志成为世界第一宝可梦大师的宝可梦训练家。
现在他遇到了一个强劲的野生宝皮卡丘，野生宝皮卡丘的生命值是HP，攻击力是ACK，牛牛召唤的宝可梦是杰尼龟。
杰尼龟的生命值是HP2，攻击力是ACK2，除此之外身为训练家还可以给宝可梦吃药让他满血复活(吃药发生在双方发动攻击之前，并且吃药一方不得在本回合发动攻击)。
牛牛想知道他最少多少回合才能能打败野生宝皮卡丘？因为皮卡丘会电光一闪，所以皮卡丘总是比杰尼龟先发动攻击。如果牛牛无法战胜野生皮卡丘则返回-1。

示例1
输入：
    8,3,8,1
输出：
    14
说明：
    至少需要14回合战胜野生皮卡丘
示例2
输入：
    1,1,1,1
输出：
    -1
说明：
    皮卡丘先出招就直接打死了杰尼龟，所以无法获胜
"""


import sys
sys.path.append("..")
from utils.utils import timer
import random
import math


class Solution1:
    @timer
    def Pokemonfight(self , HP , ACK , HP2 , ACK2 ):
        HP2_all = HP2
        i = 0
        while HP > 0:
            i+=1
            if ACK >= HP2 and HP2 < HP2_all:
                HP2 = HP2_all - ACK
            elif ACK >= HP2 and HP2 == HP2_all:
                return -1
            elif ACK < HP2:
                HP -= ACK2
                HP2 -= ACK
        return i
   

class Solution2:
    @timer
    def Pokemonfight(self , HP , ACK , HP2 , ACK2 ):
        if ACK >= HP2:
            return -1
        k1 = math.ceil(HP2 / ACK)-1
        if (HP-k1*ACK2) <= 0:
            return math.ceil(HP / ACK2)
        b = math.ceil((HP-k1*ACK2) / ACK2)
        k = math.ceil((HP2-ACK) / ACK) - 1
        if k == 0: 
            return -1
        a = math.ceil(b / k)
        return a+b+k1


# --------------------- 输出 ---------------------     
target1 = [8,3,8,1]
target2 = [1,1,1,1]
target3 = [1000000000000,3,8,1]
target4 = [random.randint(1000000, 10000000), 3, 8, 1]
tar = target4

s = Solution1()
print(s.Pokemonfight(tar[0], tar[1], tar[2], tar[3]))

s = Solution2()
print(s.Pokemonfight(tar[0], tar[1], tar[2], tar[3]))



'''
Solution1.Pokemonfight 共用时：6.92606380000143 s
15112292
Solution2.Pokemonfight 共用时：1.3700002455152571e-05 s
15112292
'''
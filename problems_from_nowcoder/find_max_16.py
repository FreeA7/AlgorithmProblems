# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 13:19:49 2020

@author: FreeA7

https://www.nowcoder.com/practice/ac72e27f34c94856bf62b19f949b8f36

给定一个包含大写英文字母和数字的句子，找出这个句子所包含的最大的十六进制整数，返回这个整数的值。数据保证该整数在int表示范围内

示例
输入:
    "012345BZ16"
输出:
    1193051
说明:
    12345B对应十进制为1193051
"""


import sys
sys.path.append("..")
from utils.utils import timer
import random
import re

class Solution1:
    @timer
    def solve(self , s ):
        numbers = re.sub(r'[G-Z]+', ' ', s).split(' ')
        number_max = 0
        for number in numbers:
            if number == '':
                continue
            number_max = max(number_max, int(number, 16))
        return number_max
    

class Solution2:
    @timer
    def solve(self , s ):
        return max([int(i,16) for i in re.compile(r'[A-F0-9]+').findall(s)])
    

class Solution3:
    @timer
    def solve(self , s ):
        numbers = re.compile(r'[A-F0-9]+').findall(s)
        max_length = max([len(number) for number in numbers])
        max_number = 0
        for number in numbers:
            if len(number) == max_length:
                max_number = max(max_number, int(number, 16))
        return max_number
        

# --------------------- 输出 ---------------------    
charactors = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
target1 = "UR11645E64O45CACC1GR1560C303X1A24CDCBYLX1616D491I"
target2 = ''.join([charactors[random.randint(0,35)] for _ in range(10000000)])
tar = target2

s = Solution1()
print(s.solve(tar))

s = Solution2()
print(s.solve(tar))

s = Solution3()
print(s.solve(tar))


'''
Solution1.solve 共用时：4.902208800000153 s
47937775429066617955122
Solution2.solve 共用时：2.8536591000001863 s
47937775429066617955122
Solution3.solve 共用时：2.4415796000002956 s
47937775429066617955122
'''
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 14:58:31 2020

@author: FreeA7

数字连接求最小
华为在线笔试
"""

line = '4589 101 41425 9999'
line = '32 321'
line = '2 1'
line = '5 1 9 1 3 5 7 8 9 3 3 4 5 8 7 9 5'

import sys 
for line in sys.stdin:
    array = line.split()
    array = [int(i) for i in array]
    for i in range(len(array)):
        for j in range(0, len(array)-i-1):
            ab = int(str(array[j]) + str(array[j+1]))
            ba = int(str(array[j+1]) + str(array[j]))
            if ba < ab:
                array[j], array[j+1] = array[j+1], array[j]
    output = ''
    for i in array:
        output += str(i)
        
    print(int(output))
    
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 10:52:49 2020

@author: FreeA7

https://www.nowcoder.com/practice/6309d58571b94aff96951f6a7ee84e7b

一年一度的春招就要到来了，牛牛为了备战春招，在家刷了很多道题，所以牛牛非常喜欢AC这两个字母。
他现在有一个只包含A和C的字符串，你可以任意修改最多k个字符，让A变成C，或者C变成A。请问修改完之后，最长连续相同字符的长度是多少。

示例
输入:
    1,"AAAC"
输出:
    4
说明:
    样例一：将最后一位C改成A即可
"""


import sys
sys.path.append("..")
from utils.utils import timer
import random


# 遍历
class Solution1:
    @timer
    def Solve(self , k , s ):
        if k >= len(s):
            return len(s)
        s_list = [len(i) for i in s.replace('AC', 'A C').replace('CA', 'C A').split(' ')]
        if k == 0:
            return max(s_list)
        max_length = 0
        for i in range(len(s_list)):
            length = s_list[i]
            change_length = 0
            j = i + 1
            end_flag = 1
            while change_length < k and j < len(s_list):
                if (j-i) % 2 == 1:
                    if change_length + s_list[j] > k:
                        length += k - change_length
                        change_length = k
                        end_flag = 0
                    else:
                        length += s_list[j]
                        change_length += s_list[j]
                else:
                    length += s_list[j]
                j += 1
            if end_flag and j < len(s_list):
                length += s_list[j]
            max_length = max(max_length, length)
        return max_length
    
  
# 滑动窗口
class Solution2:
    @timer
    def Solve(self , k , s ):
        if k >= len(s):
            return len(s)
        s_list = [len(i) for i in s.replace('AC', 'A C').replace('CA', 'C A').split(' ')]
        if k == 0:
            return max(s_list)
        l = r = c_lenght = length = max_length = 0
        a_length = s_list[0]
        while r < len(s_list)-1:
            while min(a_length, c_lenght) <= k and r+1 < len(s_list):
                r += 1
                if r % 2 == 1:
                    c_lenght += s_list[r]
                else:
                    a_length += s_list[r]
            length = min(max(a_length, c_lenght) + k, len(s))
            max_length = max(max_length, length)
            if l % 2 == 1:
                c_lenght -= s_list[l]
            else:
                a_length -= s_list[l]
            l += 1
        return max_length
  

# --------------------- 输出 ---------------------            
target1 = [1,"AAAC"]
target2 = [5, 'ACACACCCACCACACAACACAAACACAAAAACACACCACCCACA']
target3 = [1, 'AACAA']
target4 = [0,"CAAACCCCACCCCAAACCCACCACCACCCCCCCAAACACAAAACAACAAAACACCACAACACAAACAACAACCCCACCAAAACACCACAAACAAACCAAAAAAAAACACCCCACCCCCCACACCACCAACCACCCCCCAAAAAACCAAAAACCCCCCCCAACCCCACCCAACCACCACCACCCCACCCCCACAACCACCACCACCCCACACACAACCAAACCACCCAACACACCCAAAAACAAACCAAACAAACAAACACAAAAACCCCACCAAAAACCACAACCAACAACAAACAAACAAAACACCAACCCCCAACCCCACAACAAAAACCAAAAACCAAAAACAAACAAAACACACCCAACACACCCCCCACACCAACAACACACCAAAACACAACCCCAAACACAAAACAAACCCACCCCCACCCAACAAAACCCCAAAACAAAAAACCACAAAACCAACACCAACCAAACACCCCACAAACCCCACCACAACAAAAACCAAAACAAACCACACCCAACAACAAAAAACCCAACCACACCCAAACAAACCAAACAACCAACCAAAACCAAACAACCACAAACCACCCAACCCCACAACACCCAACACACCACACCCACAAACCCCCCACCCAAAAAAACCACCCACACCACAAAACACAAAACACACCCCACAACACACAACCAAACCACACCCACACCACCCACCCACCCCAAACACCACCAAAACAAACCCAAACACACAACCCCCCAAAACCCAACAAAACCACCCAAACACACCCCCCCCCCACCAACAAAACCACCCCCCCCCCCACACCCACCACCAAACACAACAACAAAAAACCCAACAAAAAACAACAAAAAAAAACACACACAACAAACCAAACCACAAACCCCAACAAACCAAAACCCCCAAAACCAACCCACCAAAAAAACCCCCCCACCAAAACAAAAAAACCCCCCCCCACAAAACCCACACAAACACCCCCACCACCCAAAA"]
target5 = [1000, ''.join(['AC'[random.randint(0,1)] for _ in range(10000)])]

tar = target5

s = Solution1()
print(s.Solve(tar[0], tar[1]))

s = Solution2()
print(s.Solve(tar[0], tar[1]))


'''
Solution1.Solve 共用时：3.5345658999995067 s
2089
Solution2.Solve 共用时：0.012739800000417745 s
2089
'''
            
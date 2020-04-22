# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 13:24:42 2020

@author: FreeA7

https://www.nowcoder.com/practice/e7df3cc4a1534a499dcb1f6553e23799

牛妹有括号序列brackets，因为过了太久，导致里面有些括号看不清了，所以用??代替
她想知道这个括号序列能不能恢复成合法的括号序列。具体操作是将??改为'('或者')'。brackets只由'?','(',')'构成。
合法的括号序列的定义：
1.空字符为合法括号序列
2.(+合法括号序列+) 为合法括号序列
3.()+合法括号序列为合法括号序列

示例
输入:
    "()?)"
输出:
    "()()"
说明:
    把?替换为(即可
"""


import sys
sys.path.append("..")
from utils.utils import timer
import random
from collections import Counter


# Bitmasking，可以找到所有的可能性
class Solution1:
    def countOne(self, n):
        count = 0
        while n > 0:
            if (n % 2) == 1:
                count += 1
            n >>=  1
        return count
        
    def check(self, s):
        stack = []
        for i in s:
            if i == '(':
                stack.append(i)
            else:
                try:
                    stack.pop()
                except IndexError:
                    return False
        if stack == []:
            return True
        else:
            return False
        
    @timer
    def MissingBrackets(self , brackets ):
        c = Counter(brackets)
        list_brackets = list(brackets)
        if c['?'] == 0:
            if self.check(brackets):
                return brackets
            else:
                return 'Impossible'
        if min(c['('], c[')']) + c['?'] < max(c['('], c[')']):
            return 'Impossible'
        for mask in range(2**c['?']):
            number_l = self.countOne(mask)
            number_r = c['?'] - number_l
            if c['('] + number_l != c[')'] + number_r:
                continue
            temp_list = list_brackets.copy()
            for i in range(c['?']):
                if mask&(1<<i):
                    temp_list[temp_list.index('?')] = '('
                else:
                    temp_list[temp_list.index('?')] = ')'
            temp_list = ''.join(temp_list)
            if self.check(temp_list):
                return temp_list
            else:
                continue
        return 'Impossible'


# 使用最优的可能性，即先放左括号后放右括号    
class Solution2:
    def check(self, s):
        stack = []
        for i in s:
            if i == '(':
                stack.append(i)
            else:
                try:
                    stack.pop()
                except IndexError:
                    return False
        if stack == []:
            return True
        else:
            return False
      
    @timer
    def MissingBrackets(self , brackets ):
        c = Counter(brackets)
        list_brackets = list(brackets)
        if c['?'] == 0:
            if self.check(brackets):
                return brackets
            else:
                return 'Impossible'
        if min(c['('], c[')']) + c['?'] < max(c['('], c[')']) or len(brackets)%2 == 1:
            return 'Impossible'
        l_number = len(brackets)//2 - c['(']
        r_number = len(brackets)//2 - c[')']
        for i in range(len(brackets)):
            if list_brackets[i] == '?':
                if l_number:
                    list_brackets[i] = '('
                    l_number -= 1
                else:
                    list_brackets[i] = ')'
                    r_number -= 1
        list_brackets = ''.join(list_brackets)
        if self.check(list_brackets):
            return list_brackets
        else:
            return 'Impossible'
    

# --------------------- 输出 ---------------------    
target1 = "()?)"
target2 = ''.join(['()?'[random.randint(0,2)] for _ in range(30)])
target3 = '??))()(()(())?)()(??'
tar = target2

s = Solution1()
print(s.MissingBrackets(tar))

s = Solution2()
print(s.MissingBrackets(tar))


'''
Solution1.MissingBrackets 共用时：5.779999992228113e-05 s
(((())((()(()))()))((())()))()
Solution2.MissingBrackets 共用时：3.590000051190145e-05 s
(((())((()(()))()))((())()))()
'''
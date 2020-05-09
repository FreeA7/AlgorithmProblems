# -*- coding: utf-8 -*-
"""
Created on Sat May  9 08:46:09 2020

@author: FreeA7

https://www.nowcoder.com/practice/162f79e68d6c4b9988a994344181d366

牛牛有一个正整数数组A和一个正整数X，设A的长度为N，数组中的元素依次为A[0]~A[N - 1]。
牛牛要挑选出符合以下条件的所有整数对(l, r)：
1、0<=l<=r<=N−1
2、存在至少X个不同的质数，每个质数都可以整除A[l]~A[r]之间的每一个数(A[l], A[l + 1], A[l + 2], ... A[r])。
现在定义一个整数对(l, r)的长度为r - l + 1，牛牛希望知道所有符合条件的整数对中，长度第K大的整数对长度是多少。
如果符合条件的数对不足K个，那么返回-1

示例
输入:
    [2, 2],1,2
输出:
    1
说明:
    有三个合法的数对(0, 0), (0, 1), (1, 1)，长度分别为1, 2, 1，第2大的长度是1
"""


import sys
sys.path.append("..")
from utils.utils import timer
import random


# 先找到所有的质数，然后遍历数列求公因数
class Solution:
    @timer
    def GetKthLength(self , A , X , K ):
        up_range = max(A)//2
        down_range = 4
        primes = set([2,3])
        for i in range(down_range, up_range+1):
            prime_flag = 1
            for prime in primes:
                if i % prime == 0:
                    prime_flag = 0
                    break
            if prime_flag:
                primes.add(i)
        primes = sorted(list(primes))
        res = []
        for i in range(len(A)):
            for j in range(i, len(A)):
                res.append(0)
                min_num = min(A[i:j+1])
                for prime in primes:
                    if prime > min_num:
                        break
                    n_flag = 1
                    for n in A[i:j+1]:
                        if n % prime != 0:
                            n_flag = 0
                            break
                    if n_flag:
                        res[-1] += 1
        output = []
        for i in range(len(res)):
            if res[i] >= X:
                output.append(res[i])
        if len(output) < K:
            return -1
        output = sorted(output)
        return output[-1*K]


# --------------------- 输出 ---------------------    
target1 = [[2, 2],1,2]
target2 = [[30, 8, 30, 6, 2],1,2]
target3 = [[random.randint(2,30) for _ in range(1000)], 1, 2]
tar = target3

s = Solution()
print(s.GetKthLength(tar[0], tar[1], tar[2]))
        

'''
Solution.GetKthLength 共用时：12.024021699999594 s
3
'''
                            
                    
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 23:52:42 2020

@author: FreeA7
"""
import math

class Solution:
    def PermutationQuery(self , n , q , p , l1 , r1 , l2 , r2 ):
        res = {}
        for index in range(len(p)):
            res[index] = set()
        for i in range(len(p)):
            for j in range(i, len(p)):
                if min(p[i], p[j]) == math.gcd(p[i], p[j]):
                    res[i].add(j)
                    res[j].add(i)
        output = []
        for query in range(q):
            num = 0
            for l in range(l1[query],r1[query]+1):
                for r in range(l2[query],r2[query]+1):
                    if r in res[l]:
                        num += 1
            output.append(num)
        return output
        
target1 = [6,1,[1,2,3,4,5,6],[0],[1],[2],[3]]
tar = target1

s = Solution()
print(s.PermutationQuery(tar[0], tar[1], tar[2], tar[3], tar[4], tar[5], tar[6]))
                    
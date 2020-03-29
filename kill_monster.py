# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 20:53:15 2020

@author: FreeA7
"""


from utils import timer
import random

# Bitmasking & bp O(2^n*n)
class Solution1:
    @timer
    def attackMonster(self , monsterLength , monsterPoint):
        inf = float('inf')
        monsterPoint = sorted(monsterPoint)
        dp = [inf for _ in range(2**len(monsterPoint))]
        dp[0] = 0
        for mask in range(2**len(monsterPoint)):
            for k in range(len(monsterPoint)):
                if not mask&(1<<k):
                    plus = monsterLength
                    max_j = -1
                    for j in range(len(monsterPoint)):
                        if j == k:
                            if max_j != -1:
                                plus -= monsterPoint[max_j]
                            break
                        elif mask&(1<<j):
                            max_j = j
                    max_j = -1
                    for j in range(len(monsterPoint)-1, -1, -1):
                        if j == k:
                            if max_j != -1:
                                plus -= (monsterLength - monsterPoint[max_j])
                            break
                        elif mask&(1<<j):
                            max_j = j
                    dp[mask|(1<<k)] = min([dp[mask|(1<<k)], dp[mask]+plus])
        return dp[-1]
    

# DP    
class Solution2:
    @timer
    def attackMonster(self , monsterLength , monsterPoint):
        monsterPoint.append(0)
        monsterPoint.append(monsterLength)
        monsterPoint = sorted(monsterPoint)
        dp = [[float('inf') for r in range(l+2, len(monsterPoint))] for l in range(len(monsterPoint)-1)]
        dp = list(map(lambda x:[0]+x, dp))
        for l in range(len(monsterPoint)-3, -1, -1):
            for r in range(l+2, len(monsterPoint)):
                for i in range(l+1,r):
                    dp[l][r - (l+1)] = min(dp[l][r - (l+1)], dp[l][i - (l+1)]+dp[i][r - (i+1)]+monsterPoint[r]-monsterPoint[l])
        return(dp[0][-1])
    
                
# --------------------- 输出 ---------------------
def getTest(l, n):
    output = []
    t = 0
    for i in range(n):
        while t in output:
            t = random.randint(0, l)
        output.append(t)
    return [l, output]


target1 = [20,[2,5,10,18]]
target2 = getTest(100, 15)

tar = target2

s = Solution1()
print(s.attackMonster(tar[0], tar[1]))

s = Solution2()
print(s.attackMonster(tar[0], tar[1]))


'''
Solution1.attackMonster 共用时：1.8083917000039946 s
371
Solution2.attackMonster 共用时：0.0007362999967881478 s
371
'''

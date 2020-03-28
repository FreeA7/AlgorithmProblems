# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 20:53:15 2020

@author: 98732
"""

class Solution:
    def getBit(self, mask, n):
        output = []
        for i in range(n-1, -1, -1):
            res = mask % (2**i)
            if res == mask:
                output.append(0)
            else:
                output.append(1)
            mask = res
        for i in range(len(output)-1, -1, -1):
            yield output[i]
    
    def attackMonster(self , monsterLength , monsterPoint):
        inf = float('inf')
        monsterPoint = sorted(monsterPoint)
        dp = [inf for _ in range(2**len(monsterPoint))]
        for i in range(0, len(monsterPoint)):
            dp[2**i] = monsterLength
        for mask in range(2**len(monsterPoint)):
            for k in range(len(monsterPoint)):
                if not mask&(1<<k):
                    
                    for bit in self.getBit(mask, k):
                        

                            
                    dp[mask|(1<<k)] = min([dp[mask|(1<<k)], dp[mask]+plus])
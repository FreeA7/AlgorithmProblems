# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 16:09:47 2020

@author: FreeA7

最小体力爬楼
华为在线笔试
"""

import sys 
for line in sys.stdin:
    cost = line.split()
    cost = [int(cost[i]) for i in range(len(cost))]
    if len(cost) == 0:
        print(0)
    elif len(cost) == 1:
        if cost[0] != -1:
            print(cost[0])
        else:
            print(float('inf'))
    else:
        cost.append(0)
        dp = [0 for _ in range(len(cost))]
        dp[0] = cost[0]
        dp[1] = cost[1]
        for i in range(2, len(cost)):
            if cost[i] == -1:
                dp[i] = -1
            else:
                if dp[i-2] != -1 and dp[i-1] != -1:
                    dp[i] = min([dp[i-2]+cost[i], dp[i-1]+cost[i]])
                elif dp[i-2] != -1:
                    dp[i] = dp[i-2]+cost[i]
                elif dp[i-1] != -1:
                    dp[i] = dp[i-1]+cost[i]  
                else:
                    dp[i] = -1
        if dp[-1] == -1:
            print(float('inf'))
        else:
            print(dp[-1])
    
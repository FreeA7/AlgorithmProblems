# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 11:23:23 2020

@author: FreeA7

https://www.nowcoder.com/practice/9053c1dc96e5480e8a4d2a63e34c45d0

众所周知，牛妹需要很多衣服，有直播的时候穿的、有舞剑的时候穿的、有跳舞的时候穿的、有弹琴的时候穿的，等等
这些衣服都是由固定大小的矩形布料裁剪而成，心灵手巧的牛妹也知道每件衣服所需要的具体矩形布料的长和宽
然而，她只有一块大的布料可供她裁剪。裁剪的时候可以随便剪
那么问题来了，美腻的牛妹能最多可以做出多少件衣服呢？

示例
输入:
    3,5,[[3 ,1],[4,1],[2,2],[2,2]]
输出:
    5
"""

from utils import timer
import random


# DP，不考虑l和w大小关系 O(l*w*n)  space complexity O(l*w)
class Solution1:
    @timer
    def clothNumber(self , L , W , clothSize ):
        if not L or not W or not clothSize:
            return 0
        if W > L:
            L, W = W, L
        clothSize = list(map(lambda i:[i[1], i[0]] if i[0]<i[1] else [i[0], i[1]], clothSize))
        dp = [[0 for l in range(L+1)] for w in range(W+1)]
        for w in range(1, W+1):
            for l in range(L+1):
                for cloth in clothSize:
                    c_l = cloth[0]
                    c_w = cloth[1]
                    if w <= l:
                        if c_l <= w:
                            dp1 = dp[w-c_l][l]+dp[c_l][l-c_w]+1
                            dp2 = dp[w][l-c_w]+dp[w-c_l][c_w]+1
                        else:
                            dp1 = dp2 = 0
                        if cloth[0] <= l and cloth[1] <= w:
                            dp1 = max(dp1, dp[w-c_w][l]+dp[c_w][l-c_l]+1)
                            dp2 = max(dp2, dp[w][l-c_l]+dp[w-c_w][c_l]+1)
                            dp[w][l] = max(dp1, dp2, dp[w][l]) 
                    else:
                        dp[w][l] = dp[l][w]
        return dp[W][L]


# DP，设定l>=w O(w*(l-w)*n) 时间复杂度减少了w^2*n space complexity O(w*(l-w))
class Solution2:
    @timer
    def clothNumber(self , L , W , clothSize ):
        if not L or not W or not clothSize:
            return 0
        if W > L:
            L, W = W, L
        clothSize = list(map(lambda i:[i[1], i[0]] if i[0]<i[1] else [i[0], i[1]], clothSize))
        dp = [[0 for l in range(w, L+1)] for w in range(W+1)]
        for w in range(1, W+1):
            for l in range(w, L+1):
                for cloth in clothSize:
                    c_l = cloth[0]
                    c_w = cloth[1]
                    if c_l <= w:
                        if c_l <= l-c_w:
                            dp1 = dp[w-c_l][l - (w-c_l)] + dp[c_l][l-c_w - c_l] + 1
                        else:
                            dp1 = dp[w-c_l][l - (w-c_l)] + dp[l-c_w][c_l - (l-c_w)] + 1
                        if w <= l-c_w:
                            if c_w <= w-c_l:
                                dp2 = dp[w][l-c_w - w] + dp[c_w][w-c_l - c_w] + 1
                            else:
                                dp2 = dp[w][l-c_w - w] + dp[w-c_l][c_w - (w-c_l)] + 1
                        else:
                            if c_w <= w-c_l:
                                dp2 = dp[l-c_w][w - (l-c_w)] + dp[c_w][w-c_l - c_w] + 1
                            else:
                                dp2 = dp[l-c_w][w - (l-c_w)] + dp[w-c_l][c_w - (w-c_l)] + 1
                    else:
                        dp1 = dp2 = 0
                    if cloth[0] <= l and cloth[1] <= w:
                        if c_w <= l-c_l:
                            dp1 = max(dp1, dp[w-c_w][l - (w-c_w)] + dp[c_w][l-c_l - c_w] + 1)
                        else:
                            dp1 = max(dp1, dp[w-c_w][l - (w-c_w)] + dp[l-c_l][c_w - (l-c_l)] + 1)
                        if w <= l-c_l:
                            if w-c_w <= c_l:
                                dp2 = max(dp2, dp[w][l-c_l - w] + dp[w-c_w][c_l - (w-c_w)] + 1)
                            else:
                                dp2 = max(dp2, dp[w][l-c_l - w] + dp[c_l][w-c_w - c_l] + 1)
                        else:
                            if w-c_w <= c_l:
                                dp2 = max(dp2, dp[l-c_l][w - (l-c_l)] + dp[w-c_w][c_l - (w-c_w)] + 1)
                            else:
                                dp2 = max(dp2, dp[l-c_l][w - (l-c_l)] + dp[c_l][w-c_w - c_l] + 1)
                        dp[w][l - w] = max(dp1, dp2, dp[w][l - w])
        return dp[W][L - W]

 
# --------------------- 输出 ---------------------
target1 = [3,5,[[3 ,1],[4,1],[2,2],[2,2]]]
target2 = [7,7,[[2,2],[2,3],[3,2],[2,2],[6,1],[7,1],[4,4],[5,1],[5,2],[5,3]]]
target3 = [28,25,[[7,15],[10,28]]]
target4 = [28,25,[[7,15]]]
target5 = [500, 500, [[random.randint(1,20) for i in range(2)] for j in range(10)]]

tar = target5

s = Solution1()
print(s.clothNumber(tar[0], tar[1], tar[2]))

s = Solution2()
print(s.clothNumber(tar[0], tar[1], tar[2]))


'''
Solution1.clothNumber 共用时：3.680370099999891 s
6249
Solution2.clothNumber 共用时：4.430451700000049 s
6249
'''
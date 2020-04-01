# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 11:22:11 2020

@author: FreeA7

https://www.nowcoder.com/practice/f0ebe2aa29da4a4a9d0ea71357cf2f91

牛妹是一家口罩厂家的老板，由于现在疫情严重，牛妹想重新分配每条生产线上的人数来使得能生产的口罩最多。
牛妹所在的公司一共有mm名员工，nn条生产线(0.....n-1)，每条生产线有strategy[i].size种人数安排策略。
例如：33个人在aa生产线上，aa生产线每天生产88个口罩；55个人在aa生产线上，每天aa生产线能生产1515个口罩。
牛妹想知道通过合理的策略安排最多每天能生产多少口罩？（可以不用将所有员工都分配上岗，生产线可以选择闲置

示例
输入：
    3,5,[[(1,3),(2,4)],[(3,4),(4,4)],[(8,8)]]
输出：
    8
说明：
    11号生产线采用策略22，22号生产线采用策略11，33号生产线不生产
    
这个问题相当于是一个01背包问题，人数相当于背包空间。
01背包的时间复杂度是固定的，但是空间复杂度可以进行优化
这里尝试了一下：
O(M*N*S) -> O(M*N) -> O(M*2) -> O(M)
"""

from utils import timer
import random


# states最多，production_line person strategy
# 但是时间复杂度并没有变高，因为没有对每一个生产线便利max_num_strategies
# 只是便利了所拥有的strategy，但是空间复杂度最高
# 从代码中可以理解，对于每一个已经计算过的production_line我们只需要知道其dp[production_line][person][last strategy]就够了
class Solution1:
    @timer
    def producemask(self , n , m , strategies):
        strategies_max_num = max([len(strategy) for strategy in strategies])
        dp = [[[0 for strategy in range(strategies_max_num+1)] for person in range(m+1)] for production_line in range(n+1)]
        for production_line in range(1,n+1):
            for person in range(1,m+1):
                dp[production_line][person][0] = dp[production_line-1][person][len(strategies[production_line-2])]
                for strategy in range(1,len(strategies[production_line-1])+1):
                    if strategies[production_line-1][strategy-1][0] <= person:
                        dp[production_line][person][strategy] = max(dp[production_line][person][strategy-1],
                                                                    dp[production_line-1][person-strategies[production_line-1][strategy-1][0]][
                                                                        len(strategies[production_line-2])] + strategies[production_line-1][strategy-1][1])
                    else:
                        dp[production_line][person][strategy] = dp[production_line][person][strategy-1]
        return dp[-1][-1][len(strategies[-1])]


# 所以我们去掉state中的strategy，只记录production_line和person
# 我们从代码中又能理解，我们其实也不用需要知道当前生产线和前一个生产线之前的结果
# 因为我们最终的转移只发生在当前生产线和前一个生产线
class Solution2:
    @timer
    def producemask(self , n , m , strategies):
        dp = [[0 for person in range(m+1)] for production_line in range(n+1)]
        for production_line in range(1,n+1):
            for person in range(1,m+1):
                dp[production_line][person] = dp[production_line-1][person]
                for strategy in strategies[production_line-1]:
                    if strategy[0] <= person:
                        dp[production_line][person] = max(dp[production_line][person], 
                                                          dp[production_line-1][person-strategy[0]] + strategy[1],
                                                          dp[production_line-1][person])
        return dp[-1][-1]
    

# 因此我们继续减少，只记录当前生产线和前一个生产线的情况，减少的空间复杂度 
# 此时可以发现，当前生产线在转移person时，只需要用到的前一个生产线比person更少的存储值
class Solution3:
    @timer
    def producemask(self , n , m , strategies):
        dp_last_production_line = [0 for person in range(m+1)]
        dp_this_production_line = [0 for person in range(m+1)]
        for production_line in range(n):
            for person in range(1,m+1):
                dp_this_production_line[person] =  dp_last_production_line[person]
                for strategy in strategies[production_line]:
                    if strategy[0] <= person:
                        dp_this_production_line[person] = max(dp_this_production_line[person], 
                                                              dp_last_production_line[person-strategy[0]] + strategy[1],
                                                              dp_last_production_line[person])
            dp_last_production_line, dp_this_production_line = dp_this_production_line, dp_last_production_line
        return dp_last_production_line[-1]
    

# 把前一个生产线的结果和当前生产线的结果存储在同一个dp中
# 以当前正在转移的person为界
# 大于等于person的位置存储的是当前生产线的dp
# 小于person的位置存储的是前一个生产线的dp
# 极致优化空间复杂度
class Solution4:
    @timer
    def producemask(self , n , m , strategies):
        dp = [0 for person in range(m+1)]
        for production_line in range(n):
            for person in range(m, 0, -1):
                for strategy in strategies[production_line]:
                    if strategy[0] <= person:
                        dp[person] = max(dp[person-strategy[0]] + strategy[1], dp[person])
        return dp[-1]
                    
    
    
# --------------------- 输出 ---------------------      
target1 = [3,5,[[(1,3),(2,4)],[(3,4),(4,4)],[(8,8)]]]
target2 = [3,5,[[(1,3),(2,4)],[(3,4),(4,4)],[(5,10)]]]
target3 = [3,5,[[(1,3),(2,4)],[(3,4),(4,4)],[(5,10), (3,10)]]]

tar = target2

s = Solution1()
print(s.producemask(tar[0], tar[1], tar[2]))

s = Solution2()
print(s.producemask(tar[0], tar[1], tar[2]))
                
s = Solution3()
print(s.producemask(tar[0], tar[1], tar[2]))

s = Solution4()
print(s.producemask(tar[0], tar[1], tar[2]))


'''
Solution1.producemask 共用时：8.309999975608662e-05 s
14
Solution2.producemask 共用时：5.110000074637355e-05 s
14
Solution3.producemask 共用时：0.612368900000547 s
14
'''

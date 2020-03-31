# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 20:00:32 2020

@author: FreeA7

https://www.hackerearth.com/zh/practice/algorithms/dynamic-programming/state-space-reduction/tutorial/

The array in the original question is distinct
So I moditify the question as the numbers in the array can be repeated.
-1 : the num is a barrier
 0 : the num is not in an ordered subsequence just now
 1 : the num is in a continuous subsequence
 
The third dimension of dp[i] is a multiplier
e.g. 333636 <- 4
The increment is 5 [3336364, 336364, 36364, 6364, 364], just is the distance between the first min/max with the last min/max
"""

class Solution(object):
    def getSubSeqNums(self, array, minimum, maximum):
        min_a = min(array)
        max_a = max(array)
        if not array:
            return 0
        if len(array) == 1 and array[0] == minimum and array[0] == maximum:
            return 1
        elif len(array) == 1:
            return 0
        elif minimum < min_a or maximum > max_a:
            return 0
        # 2,3,4,5,6，都可以省略，因为知道是-1/0/1就可以推导出来
        # 但是如果就相当于每次1更新都要向前追溯，时间复杂度会*n
        # 所以索性记录下来，因为每次从0设定到1的时候都能得到这些数值
        # 算是用空间交换时间了
        dp = [[-1,-1,1,0,0,-1,-1,-1] for _ in range(len(array))]
        if array[0] < minimum or array[0] > maximum:
            dp[0][-1] = 0
        else:
            dp[0][0] = 0
        for i in range(1, len(array)):
            
            # ----------------- 1 -----------------
            # i-1为1，ai在最大值最小值之间
            if dp[i-1][1] != -1 and array[i] < maximum and array[i] > minimum:
                dp[i][2] = dp[i-1][2] # 乘数 default=1
                dp[i][3] = dp[i-1][3] # 最小值数量 default=0
                dp[i][4] = dp[i-1][4] # 最大值数量 default=0
                dp[i][5] = dp[i-1][5] # 最前边是最小0还是最大1 default=-1
                dp[i][6] = dp[i-1][6] # 最前边的位置 default=-1
                dp[i][1] = dp[i-1][1] + dp[i-1][2]
            # i-1为1，ai为最大值
            elif dp[i-1][1] != -1 and array[i] == maximum:
                # 最大值个数加1，这个数决定如果 i 是最小值，会增加的子数列的数量
                dp[i][4] = dp[i-1][4] + 1
                # 如果最前边的数是最小值，i是最大值
                if dp[i-1][5] == 0:
                    # 乘数大小不变
                    dp[i][2] = dp[i-1][2]
                    dp[i][3] = dp[i-1][3]
                    dp[i][5] = dp[i-1][5]
                    dp[i][6] = dp[i-1][6]
                    dp[i][1] = dp[i-1][1] + dp[i-1][2]
                else:
                    # 如果最前边的数是最大值，i是最大值，乘数变成i-第一个最大值的index
                    dp[i][2] = i - dp[i-1][6] + 1
                    dp[i][3] = dp[i-1][3]
                    dp[i][5] = dp[i-1][5]
                    dp[i][6] = dp[i-1][6]
                    # 不仅要加上之前的乘数还要加上最小值的数量
                    dp[i][1] = dp[i-1][1] + dp[i-1][2] + dp[i][3]
            # i-1为1，ai在最小值
            elif dp[i-1][1] != -1 and array[i] == minimum:
                # 最小值个数加1，这个数决定如果 i 是最大值，会增加的子数列的数量
                dp[i][3] = dp[i-1][3] + 1
                # 如果最前边的数是最大值，i是最小值
                if dp[i-1][5] == 1:
                    # 乘数不变
                    dp[i][2] = dp[i-1][2]
                    dp[i][4] = dp[i-1][4]
                    dp[i][5] = dp[i-1][5]
                    dp[i][6] = dp[i-1][6]
                    dp[i][1] = dp[i-1][1] + dp[i-1][2]
                else: 
                    # 如果最前边的数是最小值，i是最小值，乘数变成i-第一个最小值的index
                    dp[i][2] = i - dp[i-1][6] + 1
                    dp[i][4] = dp[i-1][4]
                    dp[i][5] = dp[i-1][5]
                    dp[i][6] = dp[i-1][6]
                    # 不仅要加上之前的乘数还要加上最大值的数量
                    dp[i][1] = dp[i-1][1] + dp[i-1][2] + dp[i][4]
            # i-1为1，i大于最大值或者小于最小值
            elif dp[i-1][1] != -1:
                dp[i][-1] = dp[i-1][1]  
                
            # ----------------- 0 -----------------
            # i-1为0，ai在最大值最小值之间
            elif dp[i-1][0] != -1 and array[i] < maximum and array[i] > minimum:
                dp[i][0] = dp[i-1][0]
            # i-1为0，ai等于最大值
            elif dp[i-1][0] != -1 and array[i] == maximum:
                # 向前找最小值
                for j in range(i-1, -1, -1):
                    # 存在最小值
                    if dp[j][0] != -1 and array[j] == minimum:
                        # 最大值最小值数量更新
                        dp[i][3] += 1
                        dp[i][4] += 1
                        # 第一个极值是最小值
                        dp[i][5] = 0
                        # 第一个极值的初始位置，会继续向前找进行更新
                        dp[i][6] = j
                        # 防止j-1==-1，t就不会设定值
                        t = j
                        # 向前找到最前边不是-1的
                        for t in range(j-1, -1, -1):
                            if dp[t][-1] != -1:
                                # 遇到-1跳出，设定数量增加j-t
                                dp[i][1] = dp[i-1][0] + (j-t)
                                break
                            elif array[t] == minimum:
                                # 重复遇到最小值更新最小值数量并增加乘数，就是第一个最小值到最后一个最小值距离
                                # 更新第一个极值的位置
                                dp[i][3] += 1
                                dp[i][2] = j-t+1
                                dp[i][6] = t
                        if dp[i][1] == -1:
                            # 说明找到了0都是符合的，那么数量增加(j-t)+1
                            dp[i][1] = dp[i-1][0] + (j-t) + 1 
                        break
                    # 一旦遇上-1说明没找到subseq不用向前找了
                    elif dp[j][-1] != -1:
                        dp[i][0] = dp[i-1][0]
                        break
                    # 如果没有break，说明找到0也没有最小值，继续为0
                    dp[i][0] = dp[i-1][0]
            # i-1为0，ai等于最小值，操作和i为最大值相反，即向前找最大值
            elif dp[i-1][0] != -1 and array[i] == minimum:
                for j in range(i-1, -1, -1):
                    if dp[j][0] != -1 and array[j] == maximum:
                        dp[i][3] += 1
                        dp[i][4] += 1
                        dp[i][5] = 1
                        dp[i][6] = 6
                        t = j
                        for t in range(j-1, -1, -1):
                            if dp[t][-1] != -1:
                                dp[i][1] = dp[i-1][0] + (j-t)
                                break
                            elif array[t] == maximum:
                                dp[i][4] += 1
                                dp[i][2] = j-t+1
                                dp[i][6] = t
                        if dp[i][1] == -1:
                            dp[i][1] = dp[i-1][0] + (j-t) + 1                        
                        break
                    elif dp[j][-1] != -1:
                        dp[i][0] = dp[i-1][0]
                        break
                    dp[i][0] = dp[i-1][0]
            # i-1为0，ai大于最大值小于最小值
            elif dp[i-1][0] != -1:
                dp[i][-1] = dp[i-1][0]
                
            # ----------------- -1 -----------------
            # i-1为-1，ai在最大值最小值之间，可以相等
            elif dp[i-1][-1] != -1 and array[i] <= maximum and array[i] >= minimum:
                dp[i][0] = dp[i-1][-1]
            # i-1为-1，ai大于最大值小于最小值
            elif dp[i-1][-1] != -1:
                dp[i][-1] = dp[i-1][-1]
        return max(dp[-1][-1], dp[-1][0], dp[-1][1])
   
    
# --------------------- 输出 ---------------------
target1 = [[3,0,3,6,6,4], 3, 6] # 3
target2 = [[3,3,6,6,3], 3, 6] # 8
target3 = [[3,3,6,6,3,6], 3, 6] # 13
target4 = [[3,6,1,9,3,5,4,6,5,7,3,3,6,6,3,6], 3, 6] # 1+2+13
target5 = [[7,3,3,6,6,3,6,5], 3, 6] # 18
target6 = [[3,6,1,9,3,5,4,6,5,7,3,3,6,6,3,6,5], 3, 6] # 1+2+18
target7 = [[3,6], 3, 6] # 1

tar = target5

s = Solution()
print(s.getSubSeqNums(tar[0], tar[1], tar[2]))


'''
18
3,3,6,6,3,6,5
一共有6+5+4+3+2+1=21个子序列
其中33,66,65不行所以没问题
'''


                
            


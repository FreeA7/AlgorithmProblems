# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 11:12:12 2020

@author: FreeA7

https://www.nowcoder.com/practice/69205d499ec74ff7b32419c652cfba34

给你边长 a 的六边形 01 矩阵，找到一大的 1 子三角形，输出三角形的边 b

示例1
输入:
    2,[0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1]
输出:
    2
"""


import sys
sys.path.append("..")
from utils.utils import timer
import random


# 分解成层，层递进找最大
class Solution1:
    def getMapList(self, a, maps):
        map_lists = []
        for i in range(a):
            temp = maps[:((2*(a+i))+1)]
            temp = list(map(lambda x:[1,1] if x==1 else [0,0], temp))
            map_lists.append(temp)
            maps = maps[((2*(a+i))+1):]
        for i in range(a):
            temp = maps[:(((4*a)-1)-(2*i))]
            temp = list(map(lambda x:[1,1] if x==1 else [0,0], temp))
            map_lists.append(temp)
            maps = maps[(((4*a)-1)-(2*i)):]
        return map_lists
        
    def judgeTenDown(self, i, j, map_lists):
        if i == (len(map_lists)-1):
            return 0
        try:
            if i < ((len(map_lists)//2)-1):                
                if map_lists[i+1][j][0] and map_lists[i+1][j+1][0] and map_lists[i+1][j+2][0]:
                    return [[i+1,j], [i+1,j+2]]
                else:
                    return 0
            elif i == ((len(map_lists)//2)-1):
                if j == 0 or j == (len(map_lists[i])-1):
                    return 0
                if map_lists[i+1][j][0] and map_lists[i+1][j-1][0] and map_lists[i+1][j+1][0]:
                    return [[i+1,j-1], [i+1,j+1]]
                else:
                    return 0
            else:
                if map_lists[i+1][j][0] and map_lists[i+1][j-1][0] and map_lists[i+1][j-2][0]:
                    return [[i+1,j], [i+1,j-2]]
                else:
                    return 0
        except IndexError:
            return 0
    
    def judgeTenUp(self, i, j, map_lists):
        if i == 0:
            return 0
        try:
            if i < (len(map_lists)//2):                
                if map_lists[i-1][j][0] and map_lists[i-1][j-1][0] and map_lists[i-1][j-2][0]:
                    return [[i-1,j], [i-1,j-2]]
                else:
                    return 0
            elif i == (len(map_lists)//2):
                if j == 0 or j == (len(map_lists[i])-1):
                    return 0
                if map_lists[i-1][j][0] and map_lists[i-1][j-1][0] and map_lists[i-1][j+1][0]:
                    return [[i-1,j-1], [i-1,j+1]]
                else:
                    return 0
            else:
                if map_lists[i-1][j][0] and map_lists[i-1][j+1][0] and map_lists[i-1][j+2][0]:
                    return [[i-1,j], [i-1,j+2]]
                else:
                    return 0
        except IndexError:
            return 0
        
    @timer
    def largestSubTriangle(self , a , maps ):
        map_lists = self.getMapList(a , maps)
        max_l = 0
        for i in range(2*a):
            for j in range(len(map_lists[i])):
                if map_lists[i][j][0] and map_lists[i][j][1]:
                    temp_l = 0
                    need_tests = []
                    temp_tests = [[i,j]]
                    flag = 1
                    if i <= ((len(map_lists)//2)-1):
                        if (j+1)%2 == 1:                            
                            while flag:
                                temp_l += 1
                                need_tests = temp_tests
                                temp_tests = []
                                for need_test in need_tests:
                                    if self.judgeTenDown(need_test[0], need_test[1], map_lists):
                                        for node in self.judgeTenDown(need_test[0], need_test[1], map_lists):
                                            temp_tests.append(node)
                                    else:
                                        flag = 0
                                        break
                        else:
                            while flag:
                                temp_l += 1
                                need_tests = temp_tests
                                temp_tests = []
                                for need_test in need_tests:
                                    if self.judgeTenUp(need_test[0], need_test[1], map_lists):
                                        for node in self.judgeTenUp(need_test[0], need_test[1], map_lists):
                                            temp_tests.append(node)
                                    else:
                                        flag = 0
                                        break
                    else:
                        if (j+1)%2 == 1:
                            while flag:
                                temp_l += 1
                                need_tests = temp_tests
                                temp_tests = []
                                for need_test in need_tests:
                                    if self.judgeTenUp(need_test[0], need_test[1], map_lists):
                                        for node in self.judgeTenUp(need_test[0], need_test[1], map_lists):
                                            temp_tests.append(node)
                                    else:
                                        flag = 0
                                        break
                        else:
                            while flag:
                                temp_l += 1
                                need_tests = temp_tests
                                temp_tests = []
                                for need_test in need_tests:
                                    if self.judgeTenDown(need_test[0], need_test[1], map_lists):
                                        for node in self.judgeTenDown(need_test[0], need_test[1], map_lists):
                                            temp_tests.append(node)
                                    else:
                                        flag = 0
                                        break
                    if temp_l > max_l:
                        max_l = temp_l  
        return max_l


# 冗余代码重写
class Solution2:
    def getMapList(self, a, maps):
        map_lists = []
        for i in range(a):
            temp = maps[:((2*(a+i))+1)]
            temp = list(map(lambda x:[1,1] if x==1 else [0,0], temp))
            map_lists.append(temp)
            maps = maps[((2*(a+i))+1):]
        for i in range(a):
            temp = maps[:(((4*a)-1)-(2*i))]
            temp = list(map(lambda x:[1,1] if x==1 else [0,0], temp))
            map_lists.append(temp)
            maps = maps[(((4*a)-1)-(2*i)):]
        return map_lists
        
    def judgeTenDown(self, i, j, map_lists):
        if i == (len(map_lists)-1):
            return 0
        try:
            if i < ((len(map_lists)//2)-1):                
                if map_lists[i+1][j][0] and map_lists[i+1][j+1][0] and map_lists[i+1][j+2][0]:
                    return [[i+1,j], [i+1,j+2]]
                else:
                    return 0
            elif i == ((len(map_lists)//2)-1):
                if j == 0 or j == (len(map_lists[i])-1):
                    return 0
                if map_lists[i+1][j][0] and map_lists[i+1][j-1][0] and map_lists[i+1][j+1][0]:
                    return [[i+1,j-1], [i+1,j+1]]
                else:
                    return 0
            else:
                if map_lists[i+1][j][0] and map_lists[i+1][j-1][0] and map_lists[i+1][j-2][0]:
                    return [[i+1,j], [i+1,j-2]]
                else:
                    return 0
        except IndexError:
            return 0
    
    def judgeTenUp(self, i, j, map_lists):
        if i == 0:
            return 0
        try:
            if i < (len(map_lists)//2):                
                if map_lists[i-1][j][0] and map_lists[i-1][j-1][0] and map_lists[i-1][j-2][0]:
                    return [[i-1,j], [i-1,j-2]]
                else:
                    return 0
            elif i == (len(map_lists)//2):
                if j == 0 or j == (len(map_lists[i])-1):
                    return 0
                if map_lists[i-1][j][0] and map_lists[i-1][j-1][0] and map_lists[i-1][j+1][0]:
                    return [[i-1,j-1], [i-1,j+1]]
                else:
                    return 0
            else:
                if map_lists[i-1][j][0] and map_lists[i-1][j+1][0] and map_lists[i-1][j+2][0]:
                    return [[i-1,j], [i-1,j+2]]
                else:
                    return 0
        except IndexError:
            return 0
    
    def judge(self, i, j, direction, map_lists):
        if direction == 'up':
            self.findTen = self.judgeTenUp
        elif direction == 'down':
            self.findTen = self.judgeTenDown
        flag = 1
        temp_l = 0
        need_tests = []
        temp_tests = [[i,j]]
        while flag:
            temp_l += 1
            need_tests = temp_tests
            temp_tests = []
            for need_test in need_tests:
                if self.findTen(need_test[0], need_test[1], map_lists):
                    temp_tests += self.findTen(need_test[0], need_test[1], map_lists)
                else:
                    flag = 0
                    break
        return temp_l
              
    @timer
    def largestSubTriangle(self , a , maps ):
        map_lists = self.getMapList(a , maps)
        max_l = 0
        for i in range(2*a):
            for j in range(len(map_lists[i])):
                if map_lists[i][j][0] and map_lists[i][j][1]:
                    if i <= ((len(map_lists)//2)-1):
                        if (j+1)%2 == 1:                            
                            temp_l = self.judge(i,j,'down', map_lists)
                        else:
                            temp_l = self.judge(i,j,'up', map_lists)
                    else:
                        if (j+1)%2 == 1:
                            temp_l = self.judge(i,j,'up', map_lists)
                        else:
                            temp_l = self.judge(i,j,'down', map_lists)
                    if temp_l > max_l:
                        max_l = temp_l      
        return max_l          

# 想改进，认为子三角形不可能为顶点，但想错了，做法错的                         
class Solution3:
    def getMapList(self, a, maps):
        map_lists = []
        for i in range(a):
            temp = maps[:((2*(a+i))+1)]
            temp = list(map(lambda x:[1,1] if x==1 else [0,0], temp))
            map_lists.append(temp)
            maps = maps[((2*(a+i))+1):]
        for i in range(a):
            temp = maps[:(((4*a)-1)-(2*i))]
            temp = list(map(lambda x:[1,1] if x==1 else [0,0], temp))
            map_lists.append(temp)
            maps = maps[(((4*a)-1)-(2*i)):]
        return map_lists
        
    def judgeTenDown(self, i, j, map_lists):
        if i == (len(map_lists)-1):
            return 0, map_lists, []
        try:
            if i < ((len(map_lists)//2)-1): 
                if map_lists[i+1][j][0] and map_lists[i+1][j+1][0] and map_lists[i+1][j+2][0]:
                    map_lists[i+1][j][1] = 0
                    map_lists[i+1][j+2][1] = 0
                    return 1, map_lists, [[i+1,j], [i+1,j+2]]
                else:
                    return 0, map_lists, []
            elif i == ((len(map_lists)//2)-1):
                if j == 0 or j == (len(map_lists[i])-1):
                    return 0, map_lists, []
                if map_lists[i+1][j][0] and map_lists[i+1][j-1][0] and map_lists[i+1][j+1][0]:
                    map_lists[i+1][j-1][1] = 0
                    map_lists[i+1][j+1][1] = 0
                    return 1, map_lists, [[i+1,j-1], [i+1,j+1]]
                else:
                    return 0, map_lists, []
            else:
                if map_lists[i+1][j][0] and map_lists[i+1][j-1][0] and map_lists[i+1][j-2][0]:
                    map_lists[i+1][j][1] = 0
                    map_lists[i+1][j-2][1] = 0
                    return 1, map_lists, [[i+1,j], [i+1,j-2]]
                else:
                    return 0, map_lists, []
        except IndexError:
            return 0, map_lists, []
        
    def judgeTenUp(self, i, j, map_lists):
        if i == 0:
            return 0, map_lists, []
        try:
            if i < (len(map_lists)//2): 
                if map_lists[i-1][j][0] and map_lists[i-1][j-1][0] and map_lists[i-1][j-2][0]:
                    map_lists[i-1][j][1] = 0
                    map_lists[i-1][j-2][1] = 0
                    return 1, map_lists, [[i-1,j], [i-1,j-2]]
                else:
                    return 0, map_lists, []
            elif i == (len(map_lists)//2):
                if j == 0 or j == (len(map_lists[i])-1):
                    return 0, map_lists, []
                if map_lists[i-1][j][0] and map_lists[i-1][j-1][0] and map_lists[i-1][j+1][0]:
                    map_lists[i-1][j-1][1] = 0
                    map_lists[i-1][j+1][1] = 0
                    return 1, map_lists, [[i-1,j-1], [i-1,j+1]]
                else:
                    return 0, map_lists, []
            else:
                if map_lists[i-1][j][0] and map_lists[i-1][j+1][0] and map_lists[i-1][j+2][0]:
                    map_lists[i-1][j][1] = 0
                    map_lists[i-1][j+2][1] = 0
                    return 1, map_lists, [[i-1,j], [i-1,j+2]]
                else:
                    return 0, map_lists, []
        except IndexError:
            return 0, map_lists, []
            
    def judge(self, i, j, direction, map_lists):
        if direction == 'up':
            self.findTen = self.judgeTenUp
        elif direction == 'down':
            self.findTen = self.judgeTenDown
        flag = 1
        temp_l = 0
        need_tests = []
        temp_tests = [[i,j]]
        while flag:
            temp_l += 1
            need_tests = temp_tests
            temp_tests = []
            for need_test in need_tests:
                ju_flag, map_lists, judged = self.findTen(need_test[0], need_test[1], map_lists)
                if ju_flag:
                    temp_tests += judged
                else:
                    flag = 0
                    break
        return temp_l
        
    @timer
    def largestSubTriangle(self , a , maps ):
        map_lists = self.getMapList(a , maps)
        max_l = 0
        for i in range(2*a):
            for j in range(len(map_lists[i])):
                if map_lists[i][j][0] and map_lists[i][j][1]:
                    if i <= ((len(map_lists)//2)-1):
                        if (j+1)%2 == 1:                            
                            temp_l = self.judge(i,j,'down', map_lists)
                        else:
                            temp_l = self.judge(i,j,'up', map_lists)
                    else:
                        if (j+1)%2 == 1:
                            temp_l = self.judge(i,j,'up', map_lists)
                        else:
                            temp_l = self.judge(i,j,'down', map_lists)
                    if temp_l > max_l:
                        max_l = temp_l  
        return max_l 


# DP args为四边形高度h，每能的三形构点(i,j)
# dp[h][i][j] = max(dp[h-1][x][y]+1 if (x,y)的长度为dp[h-1][x][y]+1在加了一行后以成)
# 但是这样做会有很多空，空间杂度是thta(a*a*a)，时间杂度是thta(a*a*a)
# 以写作dp[h][l] = [(i,j)]
class Solution4:  
    def getMapList(self, a, maps):
        map_lists = []
        for i in range(a):
            temp = maps[:((2*(a+i))+1)] + [0]*(4*a-((2*(a+i))+1))
            map_lists.append(temp)
            maps = maps[((2*(a+i))+1):]
        for i in range(a):
            temp = [0]*(4*a-(((4*a)-1)-(2*i))) + maps[:(((4*a)-1)-(2*i))]
            map_lists.append(temp)
            maps = maps[(((4*a)-1)-(2*i)):]
        return map_lists
    
    @timer
    def largestSubTriangle(self , a , maps ):
        if 1 not in maps:
            return 0
        maps = self.getMapList(a , maps)
        dp = [[[] for l in range(h+1)] for h in range(2*a)]
        max_l = 1
        for h in range(2*a):
            for i in range(4*a):
                if maps[h][i] == 1:
                    dp[h][0].append([h, i])
            for l in range(1, h+1):
                for tri in dp[h-1][l-1]:
                    h_tri = tri[0]
                    i_tri = tri[1]
                    if i_tri%2 == 0 and i_tri+(l*2)-1 != (4*a-1):           
                        flag_tri = 1
                        for i in range(i_tri, i_tri+((l+1)*2)-1):
                            if maps[h_tri+l][i] == 0:
                                flag_tri = 0
                                break
                        if flag_tri == 1:
                            max_l = max(max_l, l+1)
                            dp[h][l].append([h_tri, i_tri])
                    elif i_tri%2 == 1 and i_tri+(l*2)-2 != (4*a-1):
                        flag_tri = 1
                        for j in range(h_tri, h_tri+l):
                            if maps[j][i_tri+(l*2)] == 0 or maps[j][i_tri+(l*2)-1] == 0:
                                flag_tri = 0
                                break
                        if maps[h_tri+l][i_tri+(l*2)] == 0:
                            flag_tri = 0
                        if flag_tri == 1:
                            max_l = max(max_l, l+1)
                            dp[h][l].append([h_tri, i_tri])
        return max_l
                            
                   
# --------------------- 输出 ---------------------
target1 = [2,[0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1]]
target2 = [1, [1,1,1,1,1,1]]
target3 = [1, [0,0,0,0,0,0]]
target4 = [5,[0,0,1,1,0,1,1,1,0,0,1,0,1,1,0,1,1,0,1,1,1,1,0,0,0,0,1,1,0,0,0,0,1,0,1,1,1,1,0,1,1,0,1,1,0,1,1,0,0,0,0,0,0,1,0,0,1,1,1,0,1,1,0,1,0,0,0,1,1,1,1,1,1,1,0,1,0,1,0,1,1,1,0,1,1,0,1,1,0,1,1,1,1,0,1,0,0,0,0,1,0,1,1,1,0,0,1,1,0,1,0,0,0,0,0,0,1,1,0,1,0,0,1,0,0,0,1,1,1,0,1,0,0,1,1,1,0,0,1,0,1,1,1,1,1,0,0,0,0,1]]
target5 = [20, [random.randint(0,1) for i in range(2400)]]
target6 = [50, [random.randint(0,1) for i in range(15000)]]
target7 = [500, [random.randint(0,1) for i in range(1500000)]]


tar = target7

s = Solution1()
print(s.largestSubTriangle(tar[0], tar[1]))

s = Solution2()
print(s.largestSubTriangle(tar[0], tar[1]))

s = Solution3()
print(s.largestSubTriangle(tar[0], tar[1]))

s = Solution4()
print(s.largestSubTriangle(tar[0], tar[1]))


'''
Solution1.largestSubTriangle 共用时：18.904844799999864 s
4
Solution2.largestSubTriangle 共用时：19.17056730000013 s
4
Solution3.largestSubTriangle 共用时：16.424521200000072 s
4
Solution4.largestSubTriangle 共用时：10.718646499999977 s
4
'''

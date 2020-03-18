# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 11:12:12 2020

@author: FreeA7

https://www.nowcoder.com/practice/69205d499ec74ff7b32419c652cfba34

给你一个边长为 a 的六边形 01 矩阵，请找到一个最大的全 1 子三角形，输出三角形的边长 b。

示例1
输入:
    2,[0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1]
输出:
    2
"""


from utils import timer
import random


# 分解成多层，逐层递进找最大值
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

# 想改进，认为子三角形不可能为顶点，但是想错了，做法是错的                         
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
                        
# --------------------- 输出 ---------------------
target1 = [2,[0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1]]
target2 = [1, [1,1,1,1,1,1]]
target3 = [1, [0,0,0,0,0,0]]
target4 = [5, [random.randint(0,1) for i in range(150)]]
target5 = [20, [random.randint(0,1) for i in range(2400)]]
target6 = [50, [random.randint(0,1) for i in range(15000)]]
target7 = [100, [random.randint(0,1) for i in range(60000)]]
target8 = [6, [1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1,0,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,0,1,1,1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,1,0,1,1,1,0,0,1,0,0,1,1,1,1,0,0,0,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,0,1,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0,1,0,1,1,1,1,0,0,1,0,1,0,1,1,1,1,1,1,1,1,0,0,0,1,1,1,0,1,0,0,1,1,0,1,1,1,1,1,0,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,0,0,1,1,1,1,1,0,0,1,0,0,1,1,1,0]]
target9 = [60, [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,0,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,0,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,1,1,1,1]]

tar = target9

s = Solution1()
print(s.largestSubTriangle(tar[0], tar[1]))

s = Solution2()
print(s.largestSubTriangle(tar[0], tar[1]))

s = Solution3()
print(s.largestSubTriangle(tar[0], tar[1]))

'''
largestSubTriangle 共用时：0.20480859999952372 s
10
largestSubTriangle 共用时：0.17626190000009956 s
10
largestSubTriangle 共用时：0.0606313999996928 s
9
'''

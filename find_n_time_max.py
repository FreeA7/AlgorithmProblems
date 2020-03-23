# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 11:30:20 2020

@author: FreeA7

https://www.nowcoder.com/practice/df2ebc45eab84099b843f0bfd8989516

给定n个数字的序列a，对位置i进行一次操作将使得a_{i-1},a_i,a_{i+1}a，都变成max(a_{i-1},a_i,a_{i+1})
并且操作过位置i之后，位置0到i都不能再操作

设最多可以操作k(k≤n)次，最后得到的整个序列的总和最大可以是m_k你需要求出m_1,m_2,...m_n 

示例
输入:
    5,[1,2,3,4,5]
输出:
    [18,21,22,22,22]
说明：
    输入：
        n=5, 输入序列为[1,2,3,4,5]
        
        [1,2,3,4,5]对应位置0,1,2,3,4
        只能操作1次的时候，对位置1操作得到[3,3,3,4,5]
        或者对位置2操作可以得到[1,4,4,4,5]
        或者对位置3操作可以得到[1,2,5,5,5]，都可以得m_1=18m 

        只能操作2次的时候，按次序操作位置1和位置3可以得到[3,3,5,5,5]，其他操作不会得到更优的结果，所以m_2=21m 

        能操作3次以上的时候可以得到的最优序列为[3,4,5,5,5]（依次操作位置1，位置2，位置3）,所以m_3=22,m_4=22,m_5=22m 
"""

# 单步最优，错误
from utils import timer
import random


class Solution1:
    def getMax(self, li, i):
        if i == 0:
            max_i = max([li[0], li[1]])
            li[0] = max_i
            li[1] = max_i
        elif i == len(li)-1:
            max_i = max([li[i], li[i]-1])
            li[i] = max_i
            li[i-1] = max_i
        else:
            max_i = max([li[i-1], li[i], li[i+1]])
            li[i] = max_i
            li[i-1] = max_i
            li[i+1] = max_i
        return li
        
    @timer
    def solve(self , n , a ):
        k = n
        li = a
        list_dict = [{'list':li.copy(), 'sum':sum(li), 'sum_list':[sum(li)], 'index_list':[0]}]
        
        while k:
            k = k-1
            list_dict_this_k = []
            for record_i in range(len(list_dict)):
                max_this = list_dict[-1]['sum']
                list_dict_this_re = []
                for i in range(list_dict[record_i]['index_list'][-1], len(a)):
                    li = list_dict[record_i]['list'].copy()
                    li = self.getMax(li, i)
                    sum_li = sum(li)
                    if sum_li >= max_this:
                        list_dict_this_re.append({'list':li.copy(), 'sum':sum_li, 
                                               'sum_list':list_dict[record_i]['sum_list'] + [sum_li], 
                                               'index_list':list_dict[record_i]['index_list'] + [i]})
                        max_this = sum_li
                list_dict_this_re_temp = []
                for i in range(len(list_dict_this_re)):
                    if list_dict_this_re[i]['sum'] == max_this:
                        list_dict_this_re_temp.append(list_dict_this_re[i])
                list_dict_this_k.append(list_dict_this_re_temp)
            max_k = max([i[-1]['sum'] for i in list_dict_this_k])
            list_dict = []
            for i in range(len(list_dict_this_k)):
                if list_dict_this_k[i][-1]['sum'] == max_k:
                    list_dict += list_dict_this_k[i]
        
        return list_dict[-1]['sum_list'][1:]
    
    
# 遍历，正确
class Solution2:
    def getMax(self, li, i):
        if i == 0:
            max_i = max([li[0], li[1]])
            li[0] = max_i
            li[1] = max_i
        elif i == len(li)-1:
            max_i = max([li[i], li[i]-1])
            li[i] = max_i
            li[i-1] = max_i
        else:
            max_i = max([li[i-1], li[i], li[i+1]])
            li[i] = max_i
            li[i-1] = max_i
            li[i+1] = max_i
        return li
        
    def everyK(self , n , a ):
        k = n
        li = a
        list_dict = [{'list':li.copy(), 'sum':sum(li), 'sum_list':[sum(li)], 'index_list':[0]}]
        
        while k:
            k = k-1
            list_dict_this_k = []
            for record_i in range(len(list_dict)):
                list_dict_this_re = []
                for i in range(list_dict[record_i]['index_list'][-1], len(a)):
                    li = list_dict[record_i]['list'].copy()
                    li = self.getMax(li, i)
                    sum_li = sum(li)
                    list_dict_this_re.append({'list':li.copy(), 'sum':sum_li, 
                                           'sum_list':list_dict[record_i]['sum_list'] + [sum_li], 
                                           'index_list':list_dict[record_i]['index_list'] + [i]})
                list_dict_this_k.append(list_dict_this_re)
            list_dict = []
            for i in range(len(list_dict_this_k)):
                list_dict += list_dict_this_k[i]
        
        max_end = max([i['sum'] for i in list_dict])
        print(len(list_dict))
        for i in list_dict:
            if i['sum'] == max_end:
                return i['sum_list'][-1]
            
    @timer
    def solve(self , n , a ):
        return [self.everyK(i,a) for i in range(1,n+1)]
 
    
# 遍历，正确，排除首位以及重复
class Solution3:
    def getMax(self, li, i):
        if i == 0:
            max_i = max([li[0], li[1]])
            li[0] = max_i
            li[1] = max_i
        elif i == len(li)-1:
            max_i = max([li[i], li[i]-1])
            li[i] = max_i
            li[i-1] = max_i
        else:
            max_i = max([li[i-1], li[i], li[i+1]])
            li[i] = max_i
            li[i-1] = max_i
            li[i+1] = max_i
        return li
        
    def everyK(self , n , a ):
        k = n
        li = a
        list_dict = [{'list':li.copy(), 'sum':sum(li), 'sum_list':[sum(li)], 'index_list':[0]}]
        
        while k:
            k = k-1
            list_dict_this_k = []
            for record_i in range(len(list_dict)):
                list_dict_this_re = []
                for i in range(list_dict[record_i]['index_list'][-1]+1, len(a)-1):
                    li = list_dict[record_i]['list'].copy()
                    li = self.getMax(li, i)
                    sum_li = sum(li)
                    list_dict_this_re.append({'list':li.copy(), 'sum':sum_li, 
                                           'sum_list':list_dict[record_i]['sum_list'] + [sum_li], 
                                           'index_list':list_dict[record_i]['index_list'] + [i]})
                if list_dict_this_re != []:
                    list_dict_this_k.append(list_dict_this_re)
            if list_dict_this_k != []:
                list_dict = []
                for i in range(len(list_dict_this_k)):
                    list_dict += list_dict_this_k[i]
        
        
        max_end = max([i['sum'] for i in list_dict])
        print(len(list_dict))
        for i in list_dict:
            if i['sum'] == max_end:
                return i['sum_list'][-1]
            
    @timer
    def solve(self , n , a ):
        return [self.everyK(i,a) for i in range(1,n+1)]
 
# --------------------- 输出 ---------------------
target1 = [5,[1,2,3,4,5]]
target2 = [10, [1 for i in range(10)]]
target3 = [20, [1 for i in range(20)]]

tar = target1

s = Solution1()
print(s.solve(tar[0], tar[1]))

s = Solution2()
print(s.solve(tar[0], tar[1]))

s = Solution3()
print(s.solve(tar[0], tar[1]))
                
'''
solve 共用时：0.0001869000006990973 s
[18, 21, 21, 21, 21]
5
15
35
70
126
solve 共用时：0.002977199999804725 s
[18, 21, 22, 22, 22]
3
3
1
1
1
solve 共用时：0.000523599999723956 s
[18, 21, 22, 22, 22]
'''
                    
                
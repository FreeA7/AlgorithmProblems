# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 18:03:10 2020

@author: FreeA7

QuickSort
"""


import random
from utils import timer

# Select the last element as the pivot
class Sort1(object):
    def partition(self, arr, pi):
        arr_low = []
        arr_high = []
        pi_num = 0
        for i in arr:
            if i > arr[pi]:
                arr_high.append(i)
            elif i < arr[pi]:
                arr_low.append(i)
            else:
                pi_num += 1
        return arr_low, arr_high, pi_num
    
    def quickSort(self, arr):
        if len(arr) == 0:
            return []
        elif len(arr) == 1:
            return arr
        pi = len(arr) - 1
        arr_low, arr_high, pi_num = self.partition(arr, pi)
        li = [arr[pi]] * pi_num
        li = self.quickSort(arr_low) + li
        li = li + self.quickSort(arr_high)
        return li
    
    
# In-place Sort, select the first element as the pivot
class Sort2(object):
    def partition(self, arr, low, high):
        i = high+1
        pivot = arr[low]
        for j in range(high, low, -1):
            if pivot < arr[j]:
                i -= 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i-1], arr[low] = arr[low], arr[i-1]
        return i-1
    
    def quickSort(self, arr, low, high):
        if low < high:
            pi = self.partition(arr, low, high)
            self.quickSort(arr, low, pi-1)
            self.quickSort(arr, pi+1, high)


# --------------------- 输出 ---------------------
            
target1 = [3,2,1,1]
target2 = [10, 80, 30, 90, 40, 50, 70]
N = 2000
target3 = list(range(1, N+1))
target4 = list(range(N, 0, -1))

target5 = [random.randint(0,100) for _ in range(2000)]

@timer
def useQuickSort1(arr):
    s = Sort1()
    return s.quickSort(arr)

@timer
def useQuickSort2(arr):
    s = Sort2()
    s.quickSort(arr, 0, len(arr)-1)

tar = target2
useQuickSort1(tar)
useQuickSort2(tar)
print(tar)


'''
useQuickSort1 共用时：3.97000003431458e-05 s
useQuickSort2 共用时：1.8799999452312477e-05 s
[10, 30, 40, 50, 70, 80, 90]
'''


useQuickSort2(target3)
useQuickSort2(target4)


'''
useQuickSort2 共用时：0.5605863000000681 s
useQuickSort2 共用时：1.5235310000000482 s
'''
        
    
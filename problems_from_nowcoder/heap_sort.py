# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 01:44:28 2020

@author: FreeA7

HeapSort
"""


class HeapSort(object):
    def heapify(self, arr, i, n):
        largest_index = i
        l = i * 2 + 1
        r = i * 2 + 2
        if l < n and arr[l] > arr[largest_index]:
            largest_index = l
        if r < n and arr[r] > arr[largest_index]:
            largest_index = r
        if largest_index != i:
            arr[i], arr[largest_index] = arr[largest_index], arr[i]
            self.heapify(arr, largest_index, n)
    
    def heapSort(self, arr):
        n = len(arr)
        for i in range(n-1, -1, -1):
            self.heapify(arr, i, n)
        for i in range(n-1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]
            self.heapify(arr, 0, i)
        
        
target1 = [5,1,9,7,8,5,3,1]

tar = target1

s = HeapSort()
s.heapSort(tar)
print(tar)
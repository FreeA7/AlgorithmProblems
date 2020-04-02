# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 01:44:28 2020

@author: FreeA7

HeapSort

Heap can be implemented using a list,
the first number of list is the root of the entire heap.
Index*2 + 1 is left child and index*2 + 2 is right child.
(The reason why we can get these index is the properties
of heap.) ==>
A Heap is a special Tree-based data structure in which
the tree is a complete binary tree.


So in the process to create heap using list must
traverse the list from the tail. Then you wil create
the heap from the leaf and create partial heaps and eventually
figure out the max/min number as the root of heap.

After creating the heap, we exchange the min/max number(the root
of heap) with the last number of list(a leaf). Then we heapify
the heap from the root, and we will get the second min/max
number.
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
target2 = [1,2,3,4,5,6,7,8]

tar = target2

s = HeapSort()
s.heapSort(tar)
print(tar)

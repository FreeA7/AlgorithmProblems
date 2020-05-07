# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 23:38:18 2020

@author: FreeA7

MergeSort
"""

# return merge output
class MergeSort1(object):
    def merge(self, left_list, right_list):
        i = j = 0
        merge_output = []
        while i!=len(left_list) and j !=len(right_list):
            if left_list[i] <= right_list[j]:
                merge_output.append(left_list[i])
                i+=1
            else:
                merge_output.append(right_list[j])
                j+=1
        if i!=len(left_list):
            for i in range(i, len(left_list)):
                merge_output.append(left_list[i])
        if j!=len(right_list):
            for j in range(j, len(right_list)):
                merge_output.append(right_list[j])
        return merge_output
    
    def mergeSort(self, arr, left, right):
        if left < right:
            mid = (left+right)//2
            left_list = []
            right_list = []
            left_list += self.mergeSort(arr, left, mid)
            right_list += self.mergeSort(arr, mid+1, right)
            return self.merge(left_list, right_list)
        else:
            return [arr[left]]


# change array
class MergeSort2(object):
    def merge(self, arr, left, mid, right):
        i = j = 0
        k = left
        left_list = arr[left:mid+1]
        right_list = arr[mid+1:right+1]
        while i!=len(left_list) and j!=len(right_list):
            if left_list[i] <= right_list[j]:
                arr[k] = left_list[i]
                i += 1
            else:
                arr[k] = right_list[j]
                j += 1
            k += 1
        if i!=len(left_list):
            for i in range(i, len(left_list)):
                arr[k] = left_list[i]
                k += 1
        if j!=len(right_list):
            for j in range(j, len(right_list)):
                arr[k] = right_list[j]
                k += 1
    
    def mergeSort(self, arr, left, right):
        if left < right:
            mid = (left+right)//2
            self.mergeSort(arr, left, mid)
            self.mergeSort(arr, mid+1, right)
            self.merge(arr, left, mid, right)
            
            
# --------------------- 输出 ---------------------
    
target1 = [3,2,1]
target2 = [12, 11, 13, 5, 6, 7]

tar = target2

s = MergeSort1()
print(s.mergeSort(tar, 0, len(tar)-1))

s = MergeSort2()
s.mergeSort(tar, 0, len(tar)-1)
print(tar)
        

'''
[5, 6, 7, 11, 12, 13]
[5, 6, 7, 11, 12, 13]
'''
    
    
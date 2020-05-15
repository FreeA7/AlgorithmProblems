# -*- coding: utf-8 -*-
"""
Created on Tue May 12 10:49:37 2020

@author: FreeA7
"""

class SegmentTree(object):
    def __init__(self, start, end):
        self.l = None
        self.r = None
        self.start = start
        self.end = end
    
    def set_value(self, value):
        self.value = value
        
    def set_l(self, l):
        self.l = l
        
    def set_r(self, r):
        self.r = r
        
    @staticmethod
    def build(array, l, r):
        tree = SegmentTree(l, r)
        if l == r:
            tree.set_value(array[l])
            return tree
        mid = (l+r)//2
        tree.set_l(SegmentTree.build(array, l, mid))
        tree.set_r(SegmentTree.build(array, mid+1, r))
        tree.set_value(sum([tree.l.value, tree.r.value]))
        return tree
        
    def ldr(self):
        output = []
        if self.l:
            output += self.l.ldr()
        output.append(self.value)
        if self.r:
            output += self.r.ldr()
        return output
    
    def __str__(self):
        return ' '.join([str(i) for i in self.ldr()])
    
    def query(self, l, r):
        if r < self.start or l > self.end:
            return 0
        if self.end <= r and self.start >= l:
            return self.value
        output = 0
        if self.l:
            output += self.l.query(l, r)
        if self.r:
            output += self.r.query(l, r)
        return output
    
    def update(self, index, value):
        if self.start == self.end:
            self.value = value
        else:
            mid = (self.start + self.end) // 2
            if index <= mid:
                self.l.update(index, value)
            else:
                self.r.update(index, value)
            self.value = sum([self.l.value, self.r.value])

        
array = list(range(1, 11))
segment_tree = SegmentTree.build(array, 0, len(array)-1)
print(segment_tree)
print(segment_tree.query(1,4))
segment_tree.update(1, 10)
print(segment_tree)

        


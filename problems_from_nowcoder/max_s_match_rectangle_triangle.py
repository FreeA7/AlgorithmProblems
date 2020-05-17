# -*- coding: utf-8 -*-
"""
Created on Sun May 17 18:29:30 2020

@author: FreeA7
"""

class Solution:
    # Can these matchs in Stick make up m sides with length l
    def checkLength(self, Stick, l, m):
        i = 0
        counter = 0
        while i < len(Stick) and counter == m:
            if Stick[i] > l:
                Stick.pop(i)
            elif l == Stick[i]:
                counter += 1
                Stick.pop(i)
            else:
                indexs = self.checkLength(Stick[:i]+Stick[i+1:], l-Stick[i], 1)
                for index in indexs:
                    Stick.pop(index)
                    
    
    def maxRectangle(self, sum_l, Stick):
        max_l = sum_l//4
        for l in range(max_l, 0, -1):
            
        
    def MaxArea(self , n , Stick ):
        sum_l = sum(Stick)
        
# -*- coding: utf-8 -*-
"""
Created on Sun May 17 18:29:30 2020

@author: FreeA7
"""

class Solution:
    # Can these matchs in Stick make up m sides with length l
    def checkLength(self, Stick, l, m, used):
        i = 0
        counter = 0
        indexs = []
        while i < len(Stick) and counter < m:
            if i in used or Stick[i] > l:
                pass
            elif Stick[i] == l:
                indexs.append(i)
                counter += 1
                pass
            elif Stick[i] < l:
                possible_indexs = self.checkLength(Stick, l-Stick[i], 1, indexs)
                if len(possible_indexs) == 0:
                    pass
                else:
                    indexs += possible_indexs
            i += 1
        if counter == m:
            return indexs
        else:
            return []
                    
    def maxShape(self, sum_l, Stick, k):
        max_l = sum_l//k
        for l in range(max_l, 0, -1):
            indexs = self.checkLength(Stick, l, k, [])
            if len(indexs) != 0:
                break
        return l
        
    def MaxArea(self , n , Stick ):
        sum_l = sum(Stick)
        max_triangle_l = self.maxShape(sum_l, Stick, 3)
        max_rectangle_l = self.maxShape(sum_l, Stick, 4)
        if (((max_triangle_l**2) * (3**0.5)) / 4) < max_rectangle_l**2:
            return [0, max_rectangle_l**2]
        else:
            return [max_triangle_l**2, 0]
        
        
target1 = [4,[1,1,1,1]]
target2 = [6,[1,1,1,1,1,1]]
target3 = [8,[1,1,1,1,1,1,1,1]]
target4 = [7,[1,2,3,4,5,6,7]]
tar = target4

s = Solution()
print(s.MaxArea(tar[0], tar[1]))
        
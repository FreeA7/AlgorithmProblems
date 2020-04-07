# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 11:00:54 2020

@author: FreeA7
"""

class Solution:
    def CycleString(self , S1 , S2 ):
        s = S1 * 2
        index = max_time = 0
        length = len(S1)
        while 1:
            max_temp = 0
            start = i = temp_i = s[index:].find(S2) + index
            if start != index-1 and start+length < (2*length):
                while i != -1:
                    temp_i += 1
                    max_temp += 1
                    i = s[temp_i:start+length].find(S2)
                if max_temp > max_time: 
                    max_time = max_temp
                    max_str = s[start:start+length]
                index = start + 1
            else:
                break
        if max_time > 0:
            return max_str
        else:
            return 'IMPOSSIBLE'
    
target1 = ["aaabaaa","aaaa"]

tar = target1

s = Solution()
print(s.CycleString(tar[0], tar[1]))
            
                
                
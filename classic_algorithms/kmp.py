# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 17:26:39 2020

@author: FreeA7

KMP
"""

class KMP(object):
    @staticmethod
    def __createPrefixTable(p):
        prefix_table = [0]
        max_len = 0
        i = 1
        while len(p) != len(prefix_table):
            if p[i] == p[max_len]:
                prefix_table.append(max_len + 1)
                max_len += 1
                i += 1
            else:
                if max_len > 0:
                    max_len = prefix_table[max_len-1]
                else:
                    prefix_table.append(0)
                    i += 1
        return prefix_table
    
    @classmethod
    def kmpCompare(cls, s, p):
        '''
            s is the target string of kmp
            p is the string used to compare
        '''
        prefix_table = cls.__createPrefixTable(p)
        results = []
        head = i = 0
        while head+len(p) <= len(s):
            if s[head+i] == p[i] and i < len(p)-1:
                i += 1
            # Record an all match
            elif s[head+i] == p[i] and i == len(p)-1:
                results.append(head)
                # If prefix_table[-1] == len(prefix_table)-1 means the max same prefix postfix is len(prefix_table)-1
                if i == prefix_table[i]:
                    head += 1
                else:
                    head += (i - prefix_table[i])
                i = prefix_table[i]
            # i match fail
            else:
                if i > 0:
                    head += (i - prefix_table[i-1])
                    i = prefix_table[i-1]
                # if i == 0, prefix_table[i-1] doesn't exist, so must set it
                else:
                    head += 1
        return results


# --------------------- test --------------------- 
#s = 'aaaaaaaabaaaabaaaaaaaaaaaaaabbbbbbbaaaabaaaaaaaaaaabbbbb'
#p = 'aaaab'
#print(KMP.kmpCompare(s,p))
#
#s = 'ababababcabaab'
#p = 'ababcabaa'
#print(KMP.kmpCompare(s,p))
        

'''
[4, 9, 24, 35, 47]
[4]
'''
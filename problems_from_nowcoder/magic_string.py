# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 11:00:54 2020

@author: FreeA7

https://www.nowcoder.com/practice/7c76ecb05da44b0aa696a9f4d23a3730

牛妹有有两个字符串S1S1与S2S2，她想知道S2S2在S1S1中的哪一个循环同构串中的出现次数最多，如果有多个，请输出字典序最小的一个。
例：abccabcc的循环同构串为：abccabcc,bccabcca,ccabccab,cabccabc。

示例1
输入：
    "aaabaaa","aaaa"
输出：
    "aaaaaab"
说明：
    aaaaaabaaaaaab包含aaaaaaaa 33次并且字典序最小
"""

import sys
sys.path.append("..")
from utils.utils import timer
from classic_algorithms.kmp import KMP
import random


# 遍历
class Solution1:
    @timer
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
            print(max_time)
            return max_str
        else:
            return 'IMPOSSIBLE'
   
    
# kmp匹配，对每一个匹配结果查看向后的len(S1)中有多少匹配成功即这个字符串的max O(s*s)
class Solution2:
    @timer
    def CycleString(self , S1 , S2 ):
        s = 2*S1
        results = KMP.kmpCompare(s, S2)
        if len(results) == 0:
            return 'IMPOSSIBLE'
        max_num = max_index = 0
        for i in range(len(results)):
            if results[i]+len(S1)+1 > len(s): break
            end_index = results[i]+len(S1)-len(S2)
            temp_max = 1
            for j in range(i+1, len(results)):
                if results[j] <= end_index:
                    temp_max += 1
                else:
                    break
            if temp_max > max_num:
                max_num = temp_max
                max_index = results[i]
        print(max_num)
        return s[max_index:max_index+len(S1)]
     

# kmp匹配，对每一个匹配结果查看向后的len(S1)中有多少匹配成功即这个字符串的max
# 优化，对于每一个匹配结果的后一个匹配结果，其实就是前一个的max-1
# 这样只需要对kmp匹配结果遍历一遍就可以了 O(s)
class Solution3:
    @timer
    def CycleString(self , S1 , S2 ):
        s = 2*S1
        results = KMP.kmpCompare(s, S2)
        if len(results) == 0:
            return 'IMPOSSIBLE'
        max_num = max_index = temp_max = 0
        j = 1
        for i in range(len(results)):
            if not temp_max: temp_max += 1
            if results[i]+len(S1)+1 > len(s): break
            end_index = results[i]+len(S1)-len(S2)
            for j in range(j, len(results)):
                if results[j] <= end_index:
                    temp_max += 1
                else:
                    break
            if temp_max > max_num:
                max_num = temp_max
                max_index = results[i]
            temp_max -= 1
        print(max_num)
        return s[max_index:max_index+len(S1)]

    

    

# --------------------- 输出 ---------------------         
target1 = ["aaabaaa","aaaa"]
target2 = ['abcbaabbbcccbcababababacccbcaaacbccabbccbaaaacbcbacaccaababaababcabbcabaccacbcccbcacccabacaacaacaaaccbbbcbacbbcaacccbbaaccaaacbacbbabcbcccacaabbabacaaabbbbabbbcbaaaababcccbbbcacbaabbacaacaacaccabaabbcbcbababacbccbbaccbbcccaabbbcabcabcccbbcbcaaaaccbaaaabbaabcabccbacabbcaaaaacaacbcbbbcbbcabcacbcccaaacbcabbccbbbbccabcccabcbcaccbbaacabbbcbbbcabacaacbaaaababbacbccacacaaabbaaababaabacccacbbabaaabacbcccbbaacaaccbaaabaaabacbabcbcbbababbbbcbbaaaaabccacaaccaacbcacacbcbacacbbabbbbbacbacbcbbccaaabccbbcbcbacaaccaaabcacbbbbcababcaacbbacacbabababcbbaaabaabccabababacccaabcbabbababacbcbbacacccacbcabbabbaabacbcaaabbaccababbaaaabbbaaccbaaabbababcacbbcaaaacbccbacbbabaaccbbabccacacaccabcccccaaaaacccaccabbacacbbcacbacacaccaccbcabbcccaaabacaaaababccbabcaacbcacacabbabcbaaaaacacbbacaccbbcbcbccbcbbbbabccbcaacbaaabcaaccccccbacccabcbcbcacbbcacbabbcbaaababbbbaabcccabcacbccbbbccabcaaaccbbacaccaaccaacbabcbbbaacbaabcaaccbcbbaccaabaaabbacbcaaaccbaaccbccaabaaaaabaaabbccbbccacbbbcbbbbbcabaacbaccbabbabbbbcabaccbbcaaaccbbccabaabcaa', 'abc']
target3 = [''.join([['a','b','c'][random.randint(0,2)] for i in range(1000000)]), 'abc']

tar = target3

s = Solution1()
s1 = s.CycleString(tar[0], tar[1])

s = Solution2()
s2 = s.CycleString(tar[0], tar[1])

s = Solution3()
s3 = s.CycleString(tar[0], tar[1])

print(s1==s2)
print(s2==s3)

'''
length = 10000
9998
Solution1.CycleString 共用时：4.990891499999634 s

length = 1000000
37078
Solution2.CycleString 共用时：> 2 min
37078
Solution2.CycleString 共用时：2.723836000001029 s
True
'''
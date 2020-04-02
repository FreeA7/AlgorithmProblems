# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 11:23:51 2020

@author: FreeA7

https://www.nowcoder.com/practice/82bd533cd9c34df29ba15bbf1591bedf

给定两个长度相等的，由小写字母组成的字串S1和S2，定义S1和S2的距离为两个字串有少位置上的字母不相等
现在牛牛以定两个字母X1和X2，将S1的所有字母X1均替换成X2。（X1和X2以相同）
牛牛希望知道执一次替之后，两字串的距离最少为多少

示例1
输入:
    "aaa","bbb"
输出:
    0
说明
    牛牛以将S1的字'a'全部替换成字'b'，这样S1就变成了"bbb"，那么S1和S2的距离就0

示例2
输入:
    "aabb","cdef"
输出:
    3
说明
    种可行的方是将S1的字'a'全部替换成字'c'，那么S1变成"ccbb"，和S2的距离是3
"""

import sys
sys.path.append("..")
from utils.utils import timer
import random

from collections import Counter
# 对S2的在S1找，后算字母增加相似度减去损失相似度再加上其他字母相似度
class Solution1:
    @timer
    def GetMinDistance(self , S1 , S2 ):
        max_dict = {}
        self_dict = {}
        for i in set(S1):
            index = S1.find(i)
            counter = Counter()
            while index!=-1:
                counter.update(S2[index])
                index = S1.find(i, index+1)
            max_num_replace = counter.most_common(1)[0][1]
            max_num_self = counter[i]
            max_dict[i] = max_num_replace
            self_dict[i] = max_num_self
        
        res_dict = {}
        sum_num = sum(self_dict.values())
        for i in max_dict.keys():
            res_dict[i] = max_dict[i] + sum_num - self_dict[i]
        return len(S1) - res_dict[max(res_dict, key=res_dict.get)]
    
# 直接遍历
class Solution2:
    @timer
    def GetMinDistance(self , S1 , S2 ):
        a = set(S1)
        b = set(S2)
        max_ = 0
        for i in a:
            for j in b:
                if i!=j:
                    S3 = S1.replace(i,j)
                    max_this = 0
                    for x in range(len(S1)):
                        if S2[x] == S3[x]:
                            max_this += 1
                    if max_this > max_:
                        max_ = max_this
        return len(S1) - max_
    
# --------------------- 输出 ---------------------
target1 = ["aaa","bbb"]
target2 = ["aabb","cdef"]
target3 = ["aabbaacf","cdefdeae"]
target4 = ["gjogdifqfphsemodxfwdsvkndlszgbecajgfsaolxievlmrrnfkrerejyzbdvquafmfdzmgqquummejagjvufmftrmznkdtpiutb","eutkejclmistcgmcfpyqishultptuchwzxrzwifajkrdwfkomanzfrgxezmrbcfzmcvtdcwuqeykdpfquxmueshewiktgjshcjsw"]
target5 = ["mbbvtspqgsjmrktqiawxfqafqkpzoilcbcedhslvolesvzarbmchhcendqexcewxzaqmfizwdvzfosrkibyxfdkkiuhizobzgfotitnlkgkbuxqbnggbgheitdioofrxfuxdyusdawiivbassesilvupstgivzeotcruxxmphuzealszygxbazbimzkfwyqgpfoyfqdlxaxvvduzytucbsgnqeinzpenhdzvimqzxubvbtepsixdvnwhkpmyzjdanjpvggqexlyvvdqpkphbbstpdbtddsryfwsimkjjsmuh","kbldyexrjxiscjywxnwhpauxbalgpzzltlryjenxpjvwnlpqvlrdjxcdmhglygbbigsifwsbplzcrdvntvuinzjrsnjbtrryuwhdtzbxnnxwwhwddujsqdxdqoidmdcbzgfkxdenwhtzvtvwgiwlnaefkudkwiewydmyhlzkjezostxymifukuvpyuwdgeqbmjqtptghecuarowulaxullpioffxukwupkcahpbqlohyqiqhgqcjxgmkyphxuxyzdnhrlfwnzdyzpsivmdbhoeogmrchmrawcsxiyheewzxk"]
ab = 'qwertyuiopasdfghjklzxcvbnm'
target6 = [''.join([ab[random.randint(0,25)] for i in range(10000)]), ''.join([ab[random.randint(0,25)] for i in range(10000)])]
target7 = [''.join([ab[random.randint(0,25)] for i in range(100000)]), ''.join([ab[random.randint(0,25)] for i in range(100000)])]

tar = target7

s = Solution1()
print(s.GetMinDistance(tar[0], tar[1]))

s = Solution2()
print(s.GetMinDistance(tar[0], tar[1]))

'''
GetMinDistance 共用时：0.2799970000005487 s
96122
GetMinDistance 共用时：9.319937299999765 s
96122
'''

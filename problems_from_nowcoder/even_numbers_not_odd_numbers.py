# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 11:08:38 2020

@author: FreeA7

https://www.nowcoder.com/practice/9e1551271e074f3eb7e9232f6e7846a3

有n个只包含小写字母的串s1,s2,..sn,每次给你一个只包含小写字母的串t。
如果串S存在前缀S'，它的奇数位的字符与t的奇数位字符完全相同，称S为t的单匹配串
如果串S的偶数位字符与t的偶数位的字符全都相同，称S为t的双匹配串。
牛牛喜欢单数，并且觉得"双"非常的可恨。现在给你m个字符串，对于每个字符串ti
求s1,s2,...sn中有多少个串是t的单匹配串但不是t的双匹配串。

示例1
输入：
    3,["abc", "bbc", "cbd"],3,["abc","cad","bac"]
输出：
    [0,1,1]
说明：
    对于字符串"abc"。没有满足条件的单匹配串
    字符串“cad"有满足条件的串: "cbd" ,第一个位置都是c，第三个位置都是d，是单匹配串，但是第二个位置不同，不是双匹配串
    字符串"bac"有满足条件的串: "bbc" ,第一个位置都是b，第三个位置都是c，是单匹配串，但是第二个位置不同，不是双匹配串
"""


import sys
sys.path.append("..")
from utils.utils import timer
import random

# 遍历
class Solution1:
    @timer
    def solve(self , n , s , m , t ):
        output = {}
        for i in range(m):
            t_str = t[i]
            if t_str in output.keys():
                continue
            output[t_str] = 0
            t_dict = {}
            for j in range(n):
                s_str = s[j]
                if s_str in t_dict.keys():
                    output[t_str] += t_dict[s_str]
                    continue
                t_dict[s_str] = 0
                even = 1
                odd = 1
                for index in range(len(t_str)):
                    if not odd and not even:
                        break
                    if t_str[index] != s_str[index]:
                        if index % 2 == 1 and even:
                            even = 0
                        if index % 2 == 0 and odd:
                            odd = 0
                if odd and len(t_str) == 1:
                    output[t_str] += 1
                    t_dict[s_str] += 1
                elif odd and not even:
                    output[t_str] += 1
                    t_dict[s_str] += 1
        return [output[t[i]] for i in range(m)]
    

# 对于每一个字符串s记录其所有前缀偶字符串和前缀奇字符串
# 然后对于每一个t在遍历每一个s的时候，直接查看对应长度的前缀字符串
# 对t和s都使用字典，便于直接处理重复的t和s
class Solution2:
    @timer
    def solve(self , n , s , m , t ):
        s_odd = {}
        s_even = {}
        for i in range(len(s)):
            if s[i] in s_odd.keys():
                continue
            if len(s[i])<3:
                if len(s[i]) == 1:
                    s_even[s[i]] = []
                    s_odd[s[i]] = [s[i][0]]
                elif len(s[i]) == 2: 
                    s_even[s[i]] = [s[i][1]]
                    s_odd[s[i]] = [s[i][0]]
                continue
            j = 2
            s_odd[s[i]] = [s[i][0]]
            s_even[s[i]] = [s[i][1]]
            while j < len(s[i]):
                s_odd[s[i]].append(s_odd[s[i]][-1]+s[i][j])
                j += 2
            j = 3
            while j < len(s[i]):
                s_even[s[i]].append(s_even[s[i]][-1]+s[i][j])
                j += 2
        output = {}
        for t_str in t:
            if t_str in output.keys():
                continue
            if len(t_str) == 1:
                t_odd = t_str
                t_even = ''
            else:
                t_odd = t_even = ''
                for i in range(len(t_str)):
                    if i % 2 == 0:
                        t_odd += t_str[i]
                    elif i % 2 == 1:
                        t_even += t_str[i]
            output[t_str] = 0
            for s_str in s:
                try:
                    if t_odd == s_odd[s_str][len(t_odd)-1] and t_even != s_even[s_str][len(t_even)-1]:
                        output[t_str] += 1
                    else:
                        output[t_str] += 0
                except IndexError:
                    if t_odd == s_odd[s_str][len(t_odd)-1]:
                        output[t_str] += 1
                    else:
                        output[t_str] += 0
        return [output[t[i]] for i in range(m)]
                

# --------------------- 输出 ---------------------        
chars = 'qwertyuiopasdfghjklzxcvbnm' 
    
target1 = [3,["abc", "bbc", "cbd"],3,["abc","cad","bac"]]
target2 = [5,["uviefpqedyopqpyrxqzvmiitlypurvpzxhjfmavjsusjtonuoywrckasziuy","bezpdpuxiiwkhgycwmsvtttpqpssmdybkikyjtadokxzuirueoxphzyishnl","voiggicbaixxdukycfiungpcewtyrqtnzqnbkrnlzpwjmwkbkvmbcvmyatlx","kdmrpdwxrjvkoywlzssxtwvllnpexgvowfbdlbfgolddcyruxhnkdpdhheop","gzgvbtoaqrgybcerjisgnfjarjlmviinivjylpxroxxjcpcmaiyvltlvokdh"],300,["m","q","g","e","p","n","k","r","j","t","j","h","t","b","d","u","a","l","w","c","x","s","j","d","a","a","m","r","m","f","q","e","r","f","g","w","g","m","h","i","o","s","i","u","x","o","a","q","y","i","y","t","q","v","g","m","x","z","e","s","y","k","p","d","b","a","f","y","s","f","e","r","o","h","j","g","l","q","f","a","k","a","h","y","e","l","j","f","o","i","c","x","p","l","q","m","s","r","a","r","q","k","e","n","o","i","i","y","a","z","e","f","j","a","j","t","s","g","a","n","l","q","f","m","i","o","b","s","w","b","u","t","p","e","l","q","l","q","p","i","z","i","i","y","h","n","g","i","u","s","w","o","m","m","e","i","w","v","i","e","p","i","i","o","v","u","y","m","p","m","o","j","v","o","j","s","p","j","k","o","u","q","w","y","c","u","r","x","c","z","n","k","o","q","p","j","d","d","l","x","s","y","m","j","l","w","d","n","n","n","p","b","m","p","w","z","m","b","k","q","t","b","n","l","b","n","s","j","k","k","h","m","g","u","s","b","a","l","g","b","y","r","q","z","f","e","h","w","y","s","j","y","h","f","h","e","b","z","j","j","o","t","y","x","j","f","z","k","j","g","l","o","k","v","r","s","c","x","i","x","k","a","s","n","h","s","t","z","d","j","q","a","v","o","n","c","i","e","f","r"]]
target3 = [3,["bqcraoonfusewlwlnrqamprwjedavesdbjdwfrspsqwrwbqyjbeddmholrmtttzhxa","qtbihfiytzvjjyerhkiitvajckadhmqbbvncanqyqjvzeqzjwjcnrczlerwkxioplvh","bdwmmvhxfsghskjprpqbeeqbqsoqwlshujrwoprnrurmhdkomftrjyrkioqyoueejqz"],100,["ls","fp","oa","bq","pd","rt","oq","zl","pa","gp","mh","cc","xs","le","ps","ln","og","ek","bm","vi","ri","vw","wc","sa","zs","tt","me","pp","cy","ps","lo","xx","ta","fb","fh","hg","oh","cz","pd","ts","qj","tm","yc","xl","op","ux","jy","iw","hn","fp","is","bh","bk","ul","ea","ti","yd","en","of","gc","ek","gd","qr","eu","qf","lg","eh","cb","cp","rm","rz","is","yq","ql","rs","th","qu","vs","mw","xm","rq","hs","qp","mp","do","jm","ku","qh","ux","hu","wi","us","df","vf","pp","lq","mj","ej","mt","ob"]]
target4 = [300,["fu","jf","ci","ib","og","sh","zs","ja","sz","sg","wg","ex","em","lq","go","rz","af","re","je","mq","tf","lx","fx","oj","ph","qs","nd","kb","vn","et","yl","kt","cv","oa","al","iv","hm","wg","bq","qt","bd","ls","fp","oa","bq","pd","rt","oq","zl","pa","gp","mh","cc","xs","le","ps","ln","og","ek","bm","vi","ri","vw","wc","sa","zs","tt","me","pp","cy","ps","lo","xx","ta","fb","fh","hg","oh","cz","pd","ts","qj","tm","yc","xl","op","ux","jy","iw","hn","fp","is","bh","bk","ul","ea","ti","yd","en","of","gcb","eko","gdw","qrv","eue","qfe","lgg","ehw","cbc","cpm","rmj","rza","isj","yqq","qlj","rst","thg","quk","vsp","mwg","xmv","rqp","hsx","qpz","mpi","dof","jmy","kup","qhm","uxv","huy","wiv","use","dfo","vfq","ppe","lqy","mjs","ejj","mtb","obx","uvi","bez","voi","kdm","gzg","mxk","qfg","ggk","enj","pyf","nke","kzd","rle","jma","thu","jtp","hvw","tfc","bym","dgc","uhw","ayn","lvl","wjk","cna","xmc","sfe","jik","dqd","acz","ayx","mtg","rmh","mnr","fxa","qwd","ewc","rrj","fuz","gyc","wmj","gzx","mcc","hva","iqh","owm","sui","ien","uga","xba","olc","azy","qyj","ylw","ihd","yal","twt","qnf","vqp","gtu","mdl","xzh","zed","ecm","swv","ygp","kve","pcm","drv","bmd","alw","fxj","ykp","smv","fnn","ehn","rtx","otj","hak","jaw","gva","lbd","qdv","fal","aea","kom","afc","hlo","yky","eok","lne","jky","ftg","odt","ivd","cdh","xvn","puw","lzs","qiv","mdd","sqs","rvi","aiz","rix","qkz","kjp","eif","nlf","oys","ics","ift","ycn","atx","zzc","eme","fje","jjf","ans","jsx","tcm","scc","goj","ami","nih","luy","qzf","flj","moc","izc","ogi","boh","svb","wte","bvo","ubw","trj","paa","eoc","lsu","qhb","ljk","qao","pdx","iei","zan","iue","iak","yoe","hrm","nrt","gvo","iej","uim","stp","wzi","olb","mth","mhc"],26,['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm']]
target5 = [3000,[''.join([chars[random.randint(0,25)] for l in range(random.randint(100,300))]) for i in range(3000)], 10000, [''.join([chars[random.randint(0,25)] for l in range(random.randint(1,100))]) for i in range(10000)]]
tar = target5

s = Solution1()
s1 = s.solve(tar[0], tar[1], tar[2], tar[3])

s = Solution2()
s2 = s.solve(tar[0], tar[1], tar[2], tar[3])
    
print(s1==s2)


'''
Solution1.solve 共用时：58.81871350000074 s
Solution2.solve 共用时：23.09672859999955 s
True
'''
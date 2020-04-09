# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 11:33:18 2020

@author: FreeA7

Huawei技术面试题目

根据每日饮水机水温列表，请重新生成一个列表，对应位置的输出是你需要再等待多久
水温才会升高超过该日的水温，如果之后都不会升高，请在该位置用0来代替。
"""


def getTemTime(tem):
	result = [0]
	for i in range(len(tem)-2, -1, -1):
		j = i+1
		while 1:
			if tem[j] > tem[i]:
				result.append(j-i)
				break
			else:
				if result[-1*(j-i)] == 0:
					result.append(0)
					break
				else:
					j = result[-1*(j-i)] + j
	result.reverse()
	return result


# --------------------- 输出 ---------------------
tem = [73,74,75,71,69,72,76,73]
print(getTemTime(tem))
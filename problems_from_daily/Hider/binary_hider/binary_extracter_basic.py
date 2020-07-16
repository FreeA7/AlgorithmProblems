# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 23:03:43 2020

@author: FreeA7
"""

from PIL import Image
from sys import byteorder
from binary_hider_basic import EncryptionBinary


THRESHOLD = 160
   
class DecryptionBinary(object):
    # 解密类初始化，传入需要解密的图片位置
    def __init__(self, path, threshold=THRESHOLD):
        # 需要解密的图片位置
        self.__path = path
        # 阈值
        self.__threshold = 150
        # 二值化打开需要解密的图片
        self.img = EncryptionBinary.openBinaryImage(self.__path, self.__threshold)
        # 计算此图片能存储的最大数据，以及要预留多大空间来存储文件长度
        self.max_size, self.info_length = EncryptionBinary.calculateSize(self.img)
    
    # 解密函数，传入被解密数据的存储位置
    def decrypt(self, path):
        info = []
        index = 0
        # 初始设定文件长度为无穷大
        length = float('inf')
        pixels = self.img.load()
        for w in range((self.img.size[0]-2)//2):
            for h in range((self.img.size[1]-2)//2):
                if (pixels[w*2+1, h*2+1] + pixels[w*2+2, h*2+1] + pixels[w*2+1, h*2+2] + pixels[w*2+2, h*2+2]) in [0,4]:
                    continue
                elif (pixels[w*2+1, h*2+1] + pixels[w*2+2, h*2+1] + pixels[w*2+1, h*2+2] + pixels[w*2+2, h*2+2]) in [1,3]:
                    info.append(pixels[w*2+1, h*2+1])
                    info.append(pixels[w*2+2, h*2+1])
                    info.append(pixels[w*2+1, h*2+2])
                    index += 3
                elif (pixels[w*2+1, h*2+1] + pixels[w*2+2, h*2+1] + pixels[w*2+1, h*2+2] + pixels[w*2+2, h*2+2]) == 2:
                    info.append(pixels[w*2+2, h*2+1])
                    info.append(pixels[w*2+1, h*2+2])
                    index += 2
                # 设定文件长度，即找到结尾位置
                if length == float('inf') and index >= self.info_length:
                    length = int(''.join([str(i) for i in info[:self.info_length]]), 2) + self.info_length
                # 所有加密数据都已经被读取出来
                if index >= length:
                    info = ''.join([str(i) for i in info[self.info_length:length]])#
                    # 写入文件
                    with open(path, 'wb') as f:
                        while info:
                            f.write(int(info[:8], 2).to_bytes(1, byteorder = byteorder))
                            info = info[8:]
                        print('DecryptionBinary => 解密完毕: %s'%path)
                    return


# -------------------- Basic_Binary --------------------
if __name__ == '__main__':
    # 初始化解密类，传入需要解密的图片
    d = DecryptionBinary('./image_demos/demo_encrypted_binary_1.jpg')
    # 解密文件一，是一个txtx
    d.decrypt('./image_demos/decrypted_binary_info_1.txt')
    
    # 初始化解密类，传入需要解密的图片
    d = DecryptionBinary('./image_demos/demo_encrypted_binary_2.jpg')
    # 解密文件二，是一个png
    d.decrypt('./image_demos/decrypted_binary_info_2.png')
                    
                


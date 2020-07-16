# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 11:33:56 2020

@author: FreeA7
"""

from PIL import Image
from sys import byteorder
from rle_hider import EncryptionRLE


# 二值化图片的阈值
THRESHOLD = 150
# 游程长度的阈值
RLE_LENGTH = 20

class DecryptionRLE(object):
    # 解密类初始化，传入需要解密的图片位置
    def __init__(self, path, threshold=THRESHOLD, rle_length=RLE_LENGTH):
        # 需要解密的图片位置
        self.__path = path
        # 阈值
        self.__threshold = 150
        self.__rle_length = rle_length
        # 二值化打开需要解密的图片
        self.img = EncryptionRLE.openBinaryImage(self.__path, self.__threshold)
        # 计算此图片能存储的最大数据，以及要预留多大空间来存储文件长度，以及游程的长度列表
        self.max_size, self.info_length, self.rle_list = EncryptionRLE.calculateSize(self.img, self.__rle_length)
    
    # 解密函数，传入被解密数据的存储位置
    def decrypt(self, path):
        info = []
        index = 0
        # 初始设定文件长度为无穷大
        length = float('inf')
        for rle in range(len(self.rle_list)//2):
            if len(self.rle_list[rle*2]) + len(self.rle_list[rle*2+1]) >= self.__rle_length:
                # 直接添加第一个游程长度的取余
                info.append(len(self.rle_list[rle*2]) % 2)
                index += 1
            # 获得信息长度
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
                    print('DecryptionRLE => 解密完毕: %s'%path)
                return


# -------------------- rle --------------------
if __name__ == '__main__':
    # 初始化解密类，传入需要解密的图片
    d = DecryptionRLE('./image_demos/demo_encrypted_binary_1.jpg')
    # 解密文件一，是一个txtx
    d.decrypt('./image_demos/decrypted_binary_info_1.txt')
    
    # 初始化解密类，传入需要解密的图片
    d = DecryptionRLE('./image_demos/demo_encrypted_binary_2.jpg')
    # 解密文件二，是一个png
    d.decrypt('./image_demos/decrypted_binary_info_2.png')

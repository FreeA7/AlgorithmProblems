# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 17:16:07 2020

@author: FreeA7
"""

# 图片处理
from PIL import Image

# byte和01进行转换规则
from sys import byteorder

# 随机数
from random import randint

# md5校验算法
import hashlib

# AES加密解密算法
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

from binary_hider_enhanced import AESEncryption, EncryptionBinary


# AES加密秘钥
KEY = 'buyuan'

        
class DecryptionBinary(object):
    # 解密类初始化，传入需要解密的图片位置，因为阈值是加密时求的最优，所以要传入
    def __init__(self, path, threshold):
        # 需要解密的图片位置
        self.__path = path
        # 阈值
        self.__threshold = threshold
        # 二值化打开需要解密的图片
        self.img = EncryptionBinary.openBinaryImage(self.__path, self.__threshold)
        # 计算此图片能存储的最大数据，以及要预留多大空间来存储文件长度
        self.max_size, self.info_length = EncryptionBinary.calculateSize(self.img)
        # 校验码长度
        self.verify_length = EncryptionBinary.getVerifyLength()
    
    # 将一个01字符串转换为byte
    @staticmethod
    def str2bytes(s):
        b = b''
        while len(s):
            b += int(s[:8], 2).to_bytes(1, byteorder = byteorder)
            s = s[8:]
        return b
    
    # 解密函数，传入被解密数据的存储位置
    def decrypt(self, path):
        print('\n-------------------------------')
        print('DecryptionBinary: 开始解密')
        info = []
        index = 0
        # 初始设定文件长度为无穷大
        content_length = float('inf')
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
                if content_length == float('inf') and index >= self.info_length:
                    content_length = int(''.join([str(i) for i in info[:self.info_length]]), 2)
                # 寻找校验码
                if content_length < float('inf') and index >= (self.info_length + self.verify_length):
                    verify = ''.join([str(i) for i in info[self.info_length:(self.info_length + self.verify_length)]])
                # 所有加密数据都已经被读取出来
                if index >= (self.info_length + self.verify_length + content_length):
                    # AES解密数据
                    info = AESEncryption.AESDecrypt(DecryptionBinary.str2bytes(''.join([str(i) for i in info[(self.info_length + self.verify_length):(self.info_length + self.verify_length + content_length)]])), KEY)
                    # 数据保存
                    with open(path, 'wb') as f:
                        f.write(info)
                    print('DecryptionBinary: 解密完毕')
                    # 文件完整性校验
                    if verify == ''.join(list(map(lambda byte: byte if len(byte)==8 else '0'*(8-len(byte))+byte, [bin(byte)[2:] for byte in EncryptionBinary.verify(path)]))):
                        print('DecryptionBinary: 校验信息正确 => %s'%path)
                    else:
                        print('DecryptionBinary: 校验信息错误 => %s'%path)
                    print('-------------------------------')
                    return


# -------------------- Enhanced_Binary --------------------
if __name__ == '__main__':  
    # 初始化解密类，传入需要解密的图片
    d = DecryptionBinary('./image_demos/demo_encrypted_binary_1.jpg', e.threshold)
    # 解密文件一，是一个txtx
    d.decrypt('./image_demos/decrypted_binary_info_1.txt')
    
    # 初始化解密类，传入需要解密的图片
    d = DecryptionBinary('./image_demos/demo_encrypted_binary_2.jpg', e.threshold)
    # 解密文件二，是一个png
    d.decrypt('./image_demos/decrypted_binary_info_2.png')

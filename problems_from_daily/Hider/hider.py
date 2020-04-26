# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 23:03:43 2020

@author: FreeA7
"""

from PIL import Image
from sys import byteorder


class EncryptionBinary(object):
    # 类实例化时的初始化函数，传入原始图片位置
    def __init__(self, path, threshold=150):
        # 对灰度图进行二值化时的阈值，默认为150，即通道大于150为1，小于150为0
        self.__threshold = threshold
        # 对输入的图片path进行解析，分别得出图片名称，图片后缀，图片位置
        self.__img_name = path.split('/')[-1].split('.')[0]
        self.__img_suffix = '.'+path.split('/')[-1].split('.')[-1]
        self.__img_path = '/'.join(path.split('/')[:-1])+'/'
        # 将输入的图片进行二值化处理
        self.__convertImageToBinary()
        # 打开二值化处理之后的图片
        self.img = EncryptionBinary.openBinaryImage(self.__img_path + self.__img_name + '_binary' + self.__img_suffix, self.__threshold)
        # 计算此图片能存储的最大数据，以及要预留多大空间来存储文件长度
        self.max_size, self.info_length = EncryptionBinary.calculateSize(self.img)
       
    # 打印出图片可以存储的最大文件大小
    def __str__(self):
        return 'EncryptionBinary => 此图片最多可以存储%.2fKB的文件'%(((self.max_size-self.info_length)//8)/1024)

    # 把一张普通的图片转换为二值图片
    def __convertImageToBinary(self):
        # 打开图片
        img = Image.open(self.__img_path + self.__img_name + self.__img_suffix)
        # 转换为灰度图
        img = img.convert('L')
        # 保存灰度图
        img.save(self.__img_path + self.__img_name + '_grey' + self.__img_suffix)
        # 设定二值化的阈值映射，即通道大于150为1，小于150为0
        table = list(map(lambda i:0 if i < self.__threshold else 1, list(range(256))))
        # 转换为二值图
        img = img.point(table, '1')
        # 保存二值图
        img.save(self.__img_path + self.__img_name + '_binary' + self.__img_suffix)
        
    # 打开二值化之后的图片
    @staticmethod
    def openBinaryImage(path, threshold):
        img = Image.open(path)
        table = list(map(lambda i:0 if i < threshold else 1, list(range(256))))
        img = img.convert('L')
        img = img.point(table, '1')
        return img
    
    # 计算此图片能存储的最大数据，以及要预留多大空间来存储文件长度
    @staticmethod
    def calculateSize(img):
        # 宽度上有多少个矩阵
        width = (img.size[0]-2)//2
        # 长度上有多少个矩阵
        height = (img.size[1]-2)//2
        # 能存储的bit数据量
        number = 0
        # 像素值
        pixels = img.load()
        # 矩阵：
        # ---------------------------------------------------
        # | pixels[w*2+1, h*2+1]   |  pixels[w*2+2, h*2+1]  |
        # ---------------------------------------------------
        # | pixels[w*2+2, h*2+1]   |  pixels[w*2+2, h*2+2]  |
        # ---------------------------------------------------
        for w in range(width):
            for h in range(height):
                # 和为0和4
                if (pixels[w*2+1, h*2+1] + pixels[w*2+2, h*2+1] + pixels[w*2+1, h*2+2] + pixels[w*2+2, h*2+2]) in [0,4]:
                    continue
                # 和为2
                elif (pixels[w*2+1, h*2+1] + pixels[w*2+2, h*2+1] + pixels[w*2+1, h*2+2] + pixels[w*2+2, h*2+2]) == 2:
                    number += 3
                # 和为1和3
                elif (pixels[w*2+1, h*2+1] + pixels[w*2+2, h*2+1] + pixels[w*2+1, h*2+2] + pixels[w*2+2, h*2+2]) in [1,3]:
                    number += 2
        return number, len(bin(width*height*3)[2:])

    # 加密函数，传入需要加密的文件和加密后的图片保存位置
    def encrypt(self, file, path):
        # 1.用二进制方式读取文件
        # 2.对每一个byte转为二进制
        # 3.对每一个byte不足8位的在前边补零（因为byte转二进制的时候会去前边的0）
        # 4.把所有的二进制连接起来就变成了我们要保存的数据
        # 5.字符串转为int类型
        with open(file, 'rb') as f:
            content = f.read()
            info = [int(i) for i in ''.join(list(map(lambda byte: byte if len(byte)==8 else '0'*(8-len(byte))+byte, [bin(byte)[2:] for byte in content])))]
        # 6.计算文件大小，并将文件大小放到存储数据的开始位置
        length = bin(len(content)*8)[2:]
        length = (self.info_length - len(length))*'0' + length
        info = [int(i) for i in length] + info
        # 7.判断文件是否可能放入图片中
        if len(info) > self.max_size:
            raise ValueError('EncryptionBinary => 文件过大，此图片最多可以存储%.2fKB的文件'%(((self.max_size-self.info_length)//8)/1024))
        pixels = self.img.load()
        index = 0
        try:
            for w in range((self.img.size[0]-2)//2):
                for h in range((self.img.size[1]-2)//2):
                    if (pixels[w*2+1, h*2+1] + pixels[w*2+2, h*2+1] + pixels[w*2+1, h*2+2] + pixels[w*2+2, h*2+2]) in [0,4]:
                        continue
                    elif (pixels[w*2+1, h*2+1] + pixels[w*2+2, h*2+1] + pixels[w*2+1, h*2+2] + pixels[w*2+2, h*2+2]) == 2:
                        pixels[w*2+1, h*2+1] = info[index]
                        pixels[w*2+2, h*2+1] = info[index+1]
                        pixels[w*2+1, h*2+2] = info[index+2]
                        pixels[w*2+2, h*2+2] = (info[index] + info[index+1] + info[index+2] + 1)%2
                        index += 3
                    elif (pixels[w*2+1, h*2+1] + pixels[w*2+2, h*2+1] + pixels[w*2+1, h*2+2] + pixels[w*2+2, h*2+2]) in [1,3]:
                        pixels[w*2+2, h*2+1] = info[index]
                        pixels[w*2+1, h*2+2] = info[index+1]
                        if (info[index] + info[index+1]) == 0:
                            pixels[w*2+1, h*2+1] = 1
                            pixels[w*2+2, h*2+2] = 1
                        elif (info[index] + info[index+1]) == 2:
                            pixels[w*2+1, h*2+1] = 0
                            pixels[w*2+2, h*2+2] = 0
                        elif (info[index] + info[index+1]) == 1:
                            r1 = pixels[w*2, h*2] + pixels[w*2, h*2+1] + pixels[w*2, h*2+2] + pixels[w*2+1, h*2] + pixels[w*2+2, h*2]
                            r2 = pixels[w*2+3, h*2+3] + pixels[w*2+3, h*2+2] + pixels[w*2+3, h*2+1] + pixels[w*2+2, h*2+3] + pixels[w*2+1, h*2+3]
                            if r1 >= r2:
                                pixels[w*2+1, h*2+1] = 1
                                pixels[w*2+2, h*2+2] = 0
                            else:
                                pixels[w*2+1, h*2+1] = 0
                                pixels[w*2+2, h*2+2] = 1
                        index += 2
        # 如果IndexError错误，说明所有的info都已经被存储完了
        except IndexError:
            pass
        # 存储加密后的图片
        self.img.save(path)
        # 重新打开二值化之后但没有被加密的图片，准备下一次加密
        self.img = EncryptionBinary.openBinaryImage(self.__img_path + self.__img_name + '_binary' + self.__img_suffix, self.__threshold)
        print('EncryptionBinary => 加密完毕: %s'%path)
        
        
class DecryptionBinary(object):
    # 解密类初始化，传入需要解密的图片位置
    def __init__(self, path, threshold=150):
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
                        print('EncryptionBinary => 解密完毕: %s'%path)
                    return
       
         
class EncryptionRGB(object):
    def __init__(self, path):
        # 对输入的图片path进行解析，分别得出图片名称，图片后缀，图片位置
        self.__img_name = path.split('/')[-1].split('.')[0]
        self.__img_suffix = '.'+path.split('/')[-1].split('.')[-1]
        self.__img_path = '/'.join(path.split('/')[:-1])+'/'
        self.img, self.max_size, self.info_length = self.__openRGBImage()
       
    # 打印出图片可以存储的最大文件大小
    def __str__(self):
        return 'EncryptionRGB => 此图片最多可以存储%.2fKB的文件'%(((self.max_size-self.info_length)//8)/1024)
    
    @staticmethod
    def getPixel(pixel):
        return pixel[0]%2
    
    @staticmethod
    def checkPixel(pixel):
        if pixel[0] == 255:
            pixel = (pixel[0]-1, pixel[1], pixel[2])
        return pixel
    
    @staticmethod
    def changePixel(pixel, info):
        if EncryptionRGB.getPixel(pixel) != info:
            pixel = (pixel[0]+1, pixel[1], pixel[2])

    # 打开二值化之后的图片
    def __openRGBImage(self):
        img = Image.open(self.__img_path + self.__img_name + self.__img_suffix)
        width = (img.size[0]-2)//2
        height = (img.size[1]-2)//2
        number = 0
        pixels = img.load()
        # 矩阵：
        # ---------------------------------------------------
        # | pixels[w*2+1, h*2+1]   |  pixels[w*2+2, h*2+1]  |
        # ---------------------------------------------------
        # | pixels[w*2+2, h*2+1]   |  pixels[w*2+2, h*2+2]  |
        # ---------------------------------------------------
        for w in range(width):
            for h in range(height):
                pixels[w*2+1, h*2+1] = EncryptionRGB.checkPixel(pixels[w*2+1, h*2+1])
                pixels[w*2+2, h*2+1] = EncryptionRGB.checkPixel(pixels[w*2+2, h*2+1])
                pixels[w*2+1, h*2+2] = EncryptionRGB.checkPixel(pixels[w*2+1, h*2+2])
                pixels[w*2+2, h*2+2] = EncryptionRGB.checkPixel(pixels[w*2+2, h*2+2])
                # 和为0和4
                if (EncryptionRGB.getPixel(pixels[w*2+1, h*2+1]) + EncryptionRGB.getPixel(pixels[w*2+2, h*2+1]) + 
                    EncryptionRGB.getPixel(pixels[w*2+1, h*2+2]) + EncryptionRGB.getPixel(pixels[w*2+2, h*2+2])) in [0,4]:
                    continue
                # 和为2
                elif (EncryptionRGB.getPixel(pixels[w*2+1, h*2+1]) + EncryptionRGB.getPixel(pixels[w*2+2, h*2+1]) + 
                      EncryptionRGB.getPixel(pixels[w*2+1, h*2+2]) + EncryptionRGB.getPixel(pixels[w*2+2, h*2+2])) == 2:
                    number += 3
                # 和为1和3
                elif (EncryptionRGB.getPixel(pixels[w*2+1, h*2+1]) + EncryptionRGB.getPixel(pixels[w*2+2, h*2+1]) + 
                      EncryptionRGB.getPixel(pixels[w*2+1, h*2+2]) + EncryptionRGB.getPixel(pixels[w*2+2, h*2+2])) in [1,3]:
                    number += 2
        img.save(self.__img_path + self.__img_name + '_rgb_preprocess' + self.__img_suffix)
        return img, number, len(bin(width*height)[2:])
        
    # 加密函数，传入需要加密的文件和加密后的图片保存位置
    def encrypt(self, file, path):
        # 1.用二进制方式读取文件
        # 2.对每一个byte转为二进制
        # 3.对每一个byte不足8位的在前边补零（因为byte转二进制的时候会去前边的0）
        # 4.把所有的二进制连接起来就变成了我们要保存的数据
        # 5.字符串转为int类型
        with open(file, 'rb') as f:
            content = f.read()
            info = [int(i) for i in ''.join(list(map(lambda byte: byte if len(byte)==8 else '0'*(8-len(byte))+byte, [bin(byte)[2:] for byte in content])))]
        # 6.计算文件大小，并将文件大小放到存储数据的开始位置
        length = bin(len(content)*8)[2:]
        length = (self.info_length - len(length))*'0' + length
        info = [int(i) for i in length] + info
        # 7.判断文件是否可能放入图片中
        if len(info) > self.max_size:
            raise ValueError('EncryptionRGB => 文件过大，此图片最多可以存储%.2fKB的文件'%(((self.max_size-self.info_length)//8)/1024))
        pixels = self.img.load()
        index = 0
        try:
            for w in range((self.img.size[0]-2)//2):
                for h in range((self.img.size[1]-2)//2):
                    if (EncryptionRGB.getPixel(pixels[w*2+1, h*2+1]) + EncryptionRGB.getPixel(pixels[w*2+2, h*2+1]) + 
                        EncryptionRGB.getPixel(pixels[w*2+1, h*2+2]) + EncryptionRGB.getPixel(pixels[w*2+2, h*2+2])) in [0,4]:
                        continue
                    elif (EncryptionRGB.getPixel(pixels[w*2+1, h*2+1]) + EncryptionRGB.getPixel(pixels[w*2+2, h*2+1]) + 
                          EncryptionRGB.getPixel(pixels[w*2+1, h*2+2]) + EncryptionRGB.getPixel(pixels[w*2+2, h*2+2])) == 2:
                        EncryptionRGB.changePixel(pixels[w*2+1, h*2+1], info[index])
                        EncryptionRGB.changePixel(pixels[w*2+2, h*2+1], info[index+1])
                        EncryptionRGB.changePixel(pixels[w*2+1, h*2+2], info[index+2])
                        EncryptionRGB.changePixel(pixels[w*2+2, h*2+2], (info[index] + info[index+1] + info[index+2] + 1)%2)
                        index += 3
                    elif (EncryptionRGB.getPixel(pixels[w*2+1, h*2+1]) + EncryptionRGB.getPixel(pixels[w*2+2, h*2+1]) + 
                          EncryptionRGB.getPixel(pixels[w*2+1, h*2+2]) + EncryptionRGB.getPixel(pixels[w*2+2, h*2+2])) in [1,3]:
                        EncryptionRGB.changePixel(pixels[w*2+2, h*2+1], info[index])
                        EncryptionRGB.changePixel(pixels[w*2+1, h*2+2], info[index+1])
                        if (info[index] + info[index+1]) == 0:
                            EncryptionRGB.changePixel(pixels[w*2+1, h*2+1], 1)
                            EncryptionRGB.changePixel(pixels[w*2+2, h*2+2], 1)
                        elif (info[index] + info[index+1]) == 2:
                            EncryptionRGB.changePixel(pixels[w*2+1, h*2+1], 0)
                            EncryptionRGB.changePixel(pixels[w*2+2, h*2+2], 0)
                        elif (info[index] + info[index+1]) == 1:
                            r1 = (EncryptionRGB.getPixel(pixels[w*2, h*2]) + EncryptionRGB.getPixel(pixels[w*2, h*2+1]) + 
                                  EncryptionRGB.getPixel(pixels[w*2, h*2+2]) + EncryptionRGB.getPixel(pixels[w*2+1, h*2]) + 
                                  EncryptionRGB.getPixel(pixels[w*2+2, h*2]))
                            r2 = (EncryptionRGB.getPixel(pixels[w*2+3, h*2+3]) + EncryptionRGB.getPixel(pixels[w*2+3, h*2+2]) + 
                                  EncryptionRGB.getPixel(pixels[w*2+3, h*2+1]) + EncryptionRGB.getPixel(pixels[w*2+2, h*2+3]) + 
                                  EncryptionRGB.getPixel(pixels[w*2+1, h*2+3]))
                            if r1 >= r2:
                                EncryptionRGB.changePixel(pixels[w*2+1, h*2+1], 1)
                                EncryptionRGB.changePixel(pixels[w*2+2, h*2+2], 0)
                            else:
                                EncryptionRGB.changePixel(pixels[w*2+1, h*2+1], 0)
                                EncryptionRGB.changePixel(pixels[w*2+2, h*2+2], 1)
                        index += 2
        # 如果IndexError错误，说明所有的info都已经被存储完了
        except IndexError:
            pass
        # 存储加密后的图片
        self.img.save(path)
        # 重新打开二值化之后但没有被加密的图片，准备下一次加密
        self.img = self.__openRGBImage()
        print('EncryptionRGB => 加密完毕: %s'%path)
        
class DecryptionRGB(object):
    # 解密类初始化，传入需要解密的图片位置
    def __init__(self, path,):
        self.__path = path
        self.img = self.__openRGBImage()
        # 计算此图片能存储的最大数据，以及要预留多大空间来存储文件长度
        self.max_size, self.info_length = self.__calculateSize()
        
    # 打开一个二值图片
    def __openRGBImage(self):
        img = Image.open(self.__path)
        return img
    
    # 计算此图片能存储的最大数据，以及要预留多大空间来存储文件长度
    def __calculateSize(self):
        width = (self.img.size[0]-2)//2
        height = (self.img.size[1]-2)//2
        number = 0
        pixels = self.img.load()
        # 矩阵：
        # ---------------------------------------------------
        # | pixels[w*2+1, h*2+1]   |  pixels[w*2+2, h*2+1]  |
        # ---------------------------------------------------
        # | pixels[w*2+2, h*2+1]   |  pixels[w*2+2, h*2+2]  |
        # ---------------------------------------------------
        for w in range(width):
            for h in range(height):
                # 和为0和4
                if (EncryptionRGB.getPixel(pixels[w*2+1, h*2+1]) + EncryptionRGB.getPixel(pixels[w*2+2, h*2+1]) + 
                    EncryptionRGB.getPixel(pixels[w*2+1, h*2+2]) + EncryptionRGB.getPixel(pixels[w*2+2, h*2+2])) in [0,4]:
                    continue
                # 和为2
                elif (EncryptionRGB.getPixel(pixels[w*2+1, h*2+1]) + EncryptionRGB.getPixel(pixels[w*2+2, h*2+1]) + 
                      EncryptionRGB.getPixel(pixels[w*2+1, h*2+2]) + EncryptionRGB.getPixel(pixels[w*2+2, h*2+2])) == 2:
                    number += 3
                # 和为1和3
                elif (EncryptionRGB.getPixel(pixels[w*2+1, h*2+1]) + EncryptionRGB.getPixel(pixels[w*2+2, h*2+1]) + 
                      EncryptionRGB.getPixel(pixels[w*2+1, h*2+2]) + EncryptionRGB.getPixel(pixels[w*2+2, h*2+2])) in [1,3]:
                    number += 2
        return number, len(bin(width*height)[2:])
    
    # 解密函数，传入被解密数据的存储位置
    def decrypt(self, path):
        info = []
        index = 0
        # 初始设定文件长度为无穷大
        length = float('inf')
        pixels = self.img.load()
        for w in range((self.img.size[0]-2)//2):
            for h in range((self.img.size[1]-2)//2):
                if (EncryptionRGB.getPixel(pixels[w*2+1, h*2+1]) + EncryptionRGB.getPixel(pixels[w*2+2, h*2+1]) + 
                    EncryptionRGB.getPixel(pixels[w*2+1, h*2+2]) + EncryptionRGB.getPixel(pixels[w*2+2, h*2+2])) in [0,4]:
                    continue
                elif (EncryptionRGB.getPixel(pixels[w*2+1, h*2+1]) + EncryptionRGB.getPixel(pixels[w*2+2, h*2+1]) + 
                      EncryptionRGB.getPixel(pixels[w*2+1, h*2+2]) + EncryptionRGB.getPixel(pixels[w*2+2, h*2+2])) in [1,3]:
                    info.append(EncryptionRGB.getPixel(pixels[w*2+1, h*2+1]))
                    info.append(EncryptionRGB.getPixel(pixels[w*2+2, h*2+1]))
                    info.append(EncryptionRGB.getPixel(pixels[w*2+1, h*2+2]))
                    index += 3
                elif (EncryptionRGB.getPixel(pixels[w*2+1, h*2+1]) + EncryptionRGB.getPixel(pixels[w*2+2, h*2+1]) + 
                      EncryptionRGB.getPixel(pixels[w*2+1, h*2+2]) + EncryptionRGB.getPixel(pixels[w*2+2, h*2+2])) == 2:
                    info.append(EncryptionRGB.getPixel(pixels[w*2+2, h*2+1]))
                    info.append(EncryptionRGB.getPixel(pixels[w*2+1, h*2+2]))
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
                        print('EncryptionRGB => 解密完毕: %s'%path)
                    return

# -------------------- Binary --------------------
#if __name__ == '__main__':
#    # 初始化加密类，传入原始图片
#    e = EncryptionBinary('./image_demos/demo.jpg')
#    # 打印存储空间
#    print(e)
#    # 加密文件一，是一个txt
#    e.encrypt('./image_demos/need_encrypt_info_1.txt', './image_demos/demo_encrypted_binary_1.jpg')
#    # 加密文件二，是一个png
#    e.encrypt('./image_demos/need_encrypt_info_2.png', './image_demos/demo_encrypted_binary_2.jpg')
#    
#    # 初始化解密类，传入需要解密的图片
#    d = DecryptionBinary('./image_demos/demo_encrypted_binary_1.jpg')
#    # 解密文件一，是一个txtx
#    d.decrypt('./image_demos/decrypted_binary_info_1.txt')
#    
#    # 初始化解密类，传入需要解密的图片
#    d = DecryptionBinary('./image_demos/demo_encrypted_binary_2.jpg')
#    # 解密文件二，是一个png
#    d.decrypt('./image_demos/decrypted_binary_info_2.png')
                    
                
# -------------------- RGB --------------------
if __name__ == '__main__':
    e = EncryptionRGB('./image_demos/demo.jpg')
    print(e)
    e.encrypt('./image_demos/need_encrypt_info_1.txt', './image_demos/demo_encrypted_rgb_1.jpg')
    d = DecryptionRGB('./image_demos/demo_encrypted_rgb_1.jpg')
    d.decrypt('./image_demos/decrypted_rgb_info_1.txt')
    

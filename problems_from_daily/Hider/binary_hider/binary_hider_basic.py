# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 23:03:43 2020

@author: FreeA7
"""

from PIL import Image
from sys import byteorder


THRESHOLD = 160

class EncryptionBinary(object):
    # 类实例化时的初始化函数，传入原始图片位置
    def __init__(self, path, threshold=THRESHOLD):
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


# -------------------- Basic_Binary --------------------
if __name__ == '__main__':
    # 初始化加密类，传入原始图片
    e = EncryptionBinary('./image_demos/demo.jpg')
    # 打印存储空间
    print(e)
    # 加密文件一，是一个txt
    e.encrypt('./image_demos/need_encrypt_info_1.txt', './image_demos/demo_encrypted_binary_1.jpg')
    # 加密文件二，是一个png
    e.encrypt('./image_demos/need_encrypt_info_2.png', './image_demos/demo_encrypted_binary_2.jpg')                


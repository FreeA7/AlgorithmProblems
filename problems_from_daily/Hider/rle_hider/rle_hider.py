# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 11:33:56 2020

@author: FreeA7
"""

from PIL import Image
from sys import byteorder


# 二值化图片的阈值
THRESHOLD = 150
# 游程长度的阈值
RLE_LENGTH = 20

class EncryptionRLE(object):
    # 类实例化时的初始化函数，传入原始图片位置
    def __init__(self, path, threshold=THRESHOLD, rle_length=RLE_LENGTH):
        # 对灰度图进行二值化时的阈值，默认为150，即通道大于150为1，小于150为0
        self.__threshold = threshold
        # 游程长度的阈值，如果大于等于则可以存入数据
        self.__rle_length = rle_length
        # 对输入的图片path进行解析，分别得出图片名称，图片后缀，图片位置
        self.__img_name = path.split('/')[-1].split('.')[0]
        self.__img_suffix = '.'+path.split('/')[-1].split('.')[-1]
        self.__img_path = '/'.join(path.split('/')[:-1])+'/'
        # 将输入的图片进行二值化处理
        self.__convertImageToBinary()
        # 打开二值化处理之后的图片
        self.img = EncryptionRLE.openBinaryImage(self.__img_path + self.__img_name + '_binary' + self.__img_suffix, self.__threshold)
        # 计算此图片能存储的最大数据，以及要预留多大空间来存储文件长度，以及游程的长度列表
        self.max_size, self.info_length, self.rle_list = EncryptionRLE.calculateSize(self.img, self.__rle_length)
       
    # 打印出图片可以存储的最大文件大小
    def __str__(self):
        return 'EncryptionRLE => 此图片最多可以存储%.2fKB的文件'%(((self.max_size-self.info_length)//8)/1024)

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
    
    # 计算此图片能存储的最大数据，以及要预留多大空间来存储文件长度，以及游程的长度列表
    @staticmethod
    def calculateSize(img, rle_length):
        rle_img = list(img.getdata())
        rle_list = [[rle_img[0]]]
        for i in range(1, len(rle_img)):
            if rle_img[i] == rle_img[i-1]:
                rle_list[-1].append(rle_img[i])
            else:
                rle_list.append([rle_img[i]])
        number = 0
        for i in range(len(rle_list)//2):
            if len(rle_list[i*2]) + len(rle_list[i*2+1]) >= rle_length:
                number += 1
        return number, len(bin(number)[2:]), rle_list
    
    # 根据图片向量位置得到在图片中的坐标进行像素的修改
    @staticmethod
    def getCoordinate(size, loc):
        return loc%size[0], loc//size[0]
        
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
            raise ValueError('EncryptionRLE => 文件过大，此图片最多可以存储%.2fKB的文件'%(((self.max_size-self.info_length)//8)/1024))
        pixels = self.img.load()
        # 当前图片向量位置
        loc = 0
        # 要存入信息的位置
        index = 0
        try:
            for rle in range(len(self.rle_list)//2):
                # 现将图片向量位置移动到两个游程中间
                loc += len(self.rle_list[rle*2])
                # 判断游程长度大小关系
                if len(self.rle_list[rle*2]) + len(self.rle_list[rle*2+1]) >= self.__rle_length:
                    # 信息与第一个游程的取余不同
                    if info[index] != (len(self.rle_list[rle*2]) % 2):
                        # 获得更大的游程的临界坐标
                        if len(self.rle_list[rle*2]) >= len(self.rle_list[rle*2+1]):
                            w, h = EncryptionRLE.getCoordinate(self.img.size, loc-1)
                        else:
                            w, h = EncryptionRLE.getCoordinate(self.img.size, loc)
                        # 修改临界像素值
                        pixels[w, h] = int(not pixels[w, h])
                    index += 1
                # 图片向量位置移动到两个向量末尾
                loc += len(self.rle_list[rle*2+1])
        except IndexError:
            pass
        # 保存加密后的图片
        self.img.save(path)
        # 重新打开图片等待加密
        self.img = EncryptionRLE.openBinaryImage(self.__img_path + self.__img_name + '_binary' + self.__img_suffix, self.__threshold)
        print('EncryptionRLE => 加密完毕: %s'%path)


# -------------------- rle --------------------
if __name__ == '__main__':
    # 初始化加密类，传入原始图片
    e = EncryptionRLE('./image_demos/demo.jpg')
    # 打印存储空间
    print(e)
    # 加密文件一，是一个txt
    e.encrypt('./image_demos/need_encrypt_info_1.txt', './image_demos/demo_encrypted_binary_1.jpg')
    # 加密文件二，是一个png
    e.encrypt('./image_demos/need_encrypt_info_2.png', './image_demos/demo_encrypted_binary_2.jpg')
    

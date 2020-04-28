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


# AES加密秘钥
KEY = 'buyuan'


# AES加密解密类
class AESEncryption(object):
    key = KEY
    
    # AES加密只能加密长度为16的倍数的文本，所以对长度不足的补零
    def __add_to_16(text):
        if len(text) % 16:
            add = 16 - (len(text) % 16)
        else:
            add = 0
        text = text + (b'\0' * add)
        return text

    # AES加密秘钥必须是16,24,32位，所以对不足进行补0，过长报错
    def __checkKey(key):
        if len(key) > 32:
            raise ValueError('秘钥最长不得超过32位！')
        elif len(key) > 24:
            key = (32-len(key))*'0' + key
        elif len(key) > 16:
            key = (24-len(key))*'0' + key
        else:
            key = (16-len(key))*'0' + key
        return key.encode('utf-8')
    
    # AES加密，输入bytes，输出bytes
    @classmethod
    def AESEncrypt(cls, text, key):
        print('AESEncryption: 秘钥加密文件')
        key = cls.__checkKey(key)
        mode = AES.MODE_ECB
        text = cls.__add_to_16(text)
        cryptos = AES.new(key, mode)
        cipher_text = cryptos.encrypt(text)
        return b2a_hex(cipher_text)
    
    # AES解密，输入bytes，输出bytes
    @classmethod
    def AESDecrypt(cls, text, key):
        print('AESEncryption: 秘钥解密文件')
        key = cls.__checkKey(key)
        mode = AES.MODE_ECB
        cryptor = AES.new(key, mode)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip(b'\0')
  
    
# 阈值寻找类
class ThresholdSearcher(object):
    # 使用二分法分别对像素均值左右进行求最大阈值，最终比较左右的最大得到整体最大
    @classmethod
    def dichotomyGetThreshold(cls, img):
        print('ThresholdSearcher: 使用二分法寻找最佳阈值')
        print('  *********************')
        mid = cls.__averageGetThreshold(img)
        l = cls.__dichotomy(img, 0, mid)
        r = cls.__dichotomy(img, mid+1, 255)
        print('  l:%d, r:%d, mid:%d'%(l,r,mid))
        print('  *********************')
        if cls.__compareLR(img, l, r):
            print('ThresholdSearcher: 最佳阈值为 => %d'%l)
            return l
        else:
            print('ThresholdSearcher: 最佳阈值为 => %d'%r)
            return r
        
    # 求灰度图像素的均值
    def __averageGetThreshold(img):
        return sum(list(img.getdata()))//(img.size[0]*img.size[1])
    
    # 二分法
    @classmethod
    def __dichotomy(cls, img, l, r):
        if r == l:
            return l
        mid = (l+r)//2        
        print('  l:%d, r:%d, mid:%d'%(l,r,mid))
        if cls.__compareLR(img, l, r):
            return cls.__dichotomy(img, l, mid)
        else:
            return cls.__dichotomy(img, mid+1, r)
     
    # 比较两个像素哪个存储量更大
    def __compareLR(img, l, r):
        table_l = list(map(lambda i:0 if i < l else 1, list(range(256))))
        table_r = list(map(lambda i:0 if i < r else 1, list(range(256))))
        
        img_l = img.point(table_l, '1')
        img_r = img.point(table_r, '1')
        
        number_l, info_number_l = EncryptionBinary.calculateSize(img_l)
        number_r, info_number_r = EncryptionBinary.calculateSize(img_r)
        if number_l >= number_r:
            return 1
        else:
            return 0


# 二值图片加密类
class EncryptionBinary(object):
    # 类实例化时的初始化函数，传入原始图片位置
    def __init__(self, path):
        print('\n-------------------------------')
        print('EncryptionBinary: 正在加载图片 => %s'%path)
        # 对输入的图片path进行解析，分别得出图片名称，图片后缀，图片位置
        self.__img_name = path.split('/')[-1].split('.')[0]
        self.__img_suffix = '.'+path.split('/')[-1].split('.')[-1]
        self.__img_path = '/'.join(path.split('/')[:-1])+'/'
        # 将输入的图片进行二值化处理
        self.__convertImageToBinary()
        # 打开二值化处理之后的图片
        self.img = EncryptionBinary.openBinaryImage(self.__img_path + self.__img_name + '_binary_random' + self.__img_suffix, self.threshold)
        # 计算此图片能存储的最大数据，以及要预留多大空间来存储文件长度
        self.max_size, self.info_length = EncryptionBinary.calculateSize(self.img)
        # 校验码长度，随算法类别而定
        self.verify_length = EncryptionBinary.getVerifyLength()
        # 除去文件长度记录，校验码长度记录，使用AES加密后最大能存储的文件大小
        self.max_file = self.getMaxFileSize()
        # 打印能存储的文件大小
        print(self)
        print('-------------------------------')
       
    # 除去文件长度记录，校验码长度记录，使用AES加密后最大能存储的文件大小
    def getMaxFileSize(self):
        # 除以第一个8是变成byte，除以32乘以16是AES每16位byte变成32位byte，最后1024是变成KB
        return ((self.max_size - self.info_length - self.verify_length) //8 // 32 * 16)/1024
       
    # 打印出图片可以存储的最大文件大小
    def __str__(self):
        return 'EncryptionBinary: 此图片最多可以存储%.2fKB的文件'%self.max_file
        
    # 把一张普通的图片转换为二值图片
    def __convertImageToBinary(self):
        # 打开图片
        img = Image.open(self.__img_path + self.__img_name + self.__img_suffix)
        # 转换为灰度图
        img = img.convert('L')
        # 保存灰度图
        img.save(self.__img_path + self.__img_name + '_grey' + self.__img_suffix)
        print('EncryptionBinary: 图片灰度变换 => %s'%(self.__img_path + self.__img_name + '_grey' + self.__img_suffix))
        print('EncryptionBinary: 开始计算最佳阈值')
        # 计算最佳阈值
        self.threshold = ThresholdSearcher.dichotomyGetThreshold(img)
        # 设定二值化的阈值映射，即通道大于150为1，小于150为0
        table = list(map(lambda i:0 if i < self.threshold else 1, list(range(256))))
        # 转换为二值图
        img = img.point(table, '1')
        # 保存二值图
        img.save(self.__img_path + self.__img_name + '_binary' + self.__img_suffix)
        print('EncryptionBinary: 二值化图片 => %s'%(self.__img_path + self.__img_name + '_binary' + self.__img_suffix))
        # 二值图进行随机预处理
        EncryptionBinary.preprocessImage(img)
        img.save(self.__img_path + self.__img_name + '_binary_random' + self.__img_suffix)
        print('EncryptionBinary: 随机预处理图片 => %s'%(self.__img_path + self.__img_name + '_binary_random' + self.__img_suffix))
        
    # 打开二值化之后的图片
    @staticmethod
    def openBinaryImage(path, threshold):
        img = Image.open(path)
        table = list(map(lambda i:0 if i < threshold else 1, list(range(256))))
        img = img.convert('L')
        img = img.point(table, '1')
        return img
    
    # 随机预处理，方法和算法设计完全一样，但是填入的值是0/1随机值
    @staticmethod
    def preprocessImage(img):
        pixels = img.load()
        for w in range((img.size[0]-2)//2):
            for h in range((img.size[1]-2)//2):
                if (pixels[w*2+1, h*2+1] + pixels[w*2+2, h*2+1] + pixels[w*2+1, h*2+2] + pixels[w*2+2, h*2+2]) in [0,4]:
                    continue
                elif (pixels[w*2+1, h*2+1] + pixels[w*2+2, h*2+1] + pixels[w*2+1, h*2+2] + pixels[w*2+2, h*2+2]) == 2:
                    pixels[w*2+1, h*2+1] = randint(0, 1)
                    pixels[w*2+2, h*2+1] = randint(0, 1)
                    pixels[w*2+1, h*2+2] = randint(0, 1)
                    pixels[w*2+2, h*2+2] = (pixels[w*2+1, h*2+1] + pixels[w*2+2, h*2+1] + pixels[w*2+1, h*2+2] + 1)%2
                elif (pixels[w*2+1, h*2+1] + pixels[w*2+2, h*2+1] + pixels[w*2+1, h*2+2] + pixels[w*2+2, h*2+2]) in [1,3]:
                    pixels[w*2+2, h*2+1] = randint(0, 1)
                    pixels[w*2+1, h*2+2] = randint(0, 1)
                    if (pixels[w*2+2, h*2+1] + pixels[w*2+1, h*2+2]) == 0:
                        pixels[w*2+1, h*2+1] = 1
                        pixels[w*2+2, h*2+2] = 1
                    elif (pixels[w*2+2, h*2+1] + pixels[w*2+1, h*2+2]) == 2:
                        pixels[w*2+1, h*2+1] = 0
                        pixels[w*2+2, h*2+2] = 0
                    elif (pixels[w*2+2, h*2+1] + pixels[w*2+1, h*2+2]) == 1:
                        r1 = pixels[w*2, h*2] + pixels[w*2, h*2+1] + pixels[w*2, h*2+2] + pixels[w*2+1, h*2] + pixels[w*2+2, h*2]
                        r2 = pixels[w*2+3, h*2+3] + pixels[w*2+3, h*2+2] + pixels[w*2+3, h*2+1] + pixels[w*2+2, h*2+3] + pixels[w*2+1, h*2+3]
                        if r1 >= r2:
                            pixels[w*2+1, h*2+1] = 1
                            pixels[w*2+2, h*2+2] = 0
                        else:
                            pixels[w*2+1, h*2+1] = 0
                            pixels[w*2+2, h*2+2] = 1
    
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
    
    # 根据校验算法不同返回校验码长度
    @staticmethod
    def getVerifyLength():
        # MD5
        return 32 * 8
    
    # 对一个文件提取校验值
    @staticmethod
    def verify(file):
        print('FileVerify: 文件校验码')
        with open(file, 'rb') as f:
            content = f.read()
        return hashlib.md5(content).hexdigest().encode()

    # 加密函数，传入需要加密的文件和加密后的图片保存位置
    def encrypt(self, file, path):
        print('\n-------------------------------')
        print('EncryptionBinary: 开始加密文件 => %s'%file)
        # 1.用二进制方式读取文件
        # 2.把文件使用秘钥进行AES加密
        # 3.对每一个byte转为二进制
        # 4.对每一个byte不足8位的在前边补零（因为byte转二进制的时候会去前边的0）
        # 5.把所有的二进制连接起来就变成了我们要保存的数据
        # 6.字符串转为int类型
        with open(file, 'rb') as f:
            content = AESEncryption.AESEncrypt(f.read(), KEY)
            info = [int(i) for i in ''.join(list(map(lambda byte: byte if len(byte)==8 else '0'*(8-len(byte))+byte, [bin(byte)[2:] for byte in content])))]
        # 7.计算文件大小，并将文件大小放到存储数据的开始位置
        length = bin(len(content)*8)[2:]
        length = (self.info_length - len(length))*'0' + length
        info = [int(i) for i in length] + info
        # 8.信息校验码计算
        verify = [int(i) for i in ''.join(list(map(lambda byte: byte if len(byte)==8 else '0'*(8-len(byte))+byte, [bin(byte)[2:] for byte in EncryptionBinary.verify(file)])))]
        info = info[:self.info_length] + verify + info[self.info_length:]
        # 9.判断文件是否可能放入图片中
        if len(info) > self.max_size:
            raise ValueError('EncryptionBinary => 文件过大，此图片最多可以存储%.2fKB的文件'%self.max_file)
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
        self.img = EncryptionBinary.openBinaryImage(self.__img_path + self.__img_name + '_binary' + self.__img_suffix, self.threshold)
        print('EncryptionBinary: 加密完毕 => %s'%path)
        print('-------------------------------')
        
        
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
    # 初始化加密类，传入原始图片
    e = EncryptionBinary('./image_demos/demo.jpg')
    # 加密文件一，是一个txt
    e.encrypt('./image_demos/need_encrypt_info_1.txt', './image_demos/demo_encrypted_binary_1.jpg')
    # 加密文件二，是一个png
    e.encrypt('./image_demos/need_encrypt_info_2.png', './image_demos/demo_encrypted_binary_2.jpg')
    
    # 初始化解密类，传入需要解密的图片
    d = DecryptionBinary('./image_demos/demo_encrypted_binary_1.jpg', e.threshold)
    # 解密文件一，是一个txtx
    d.decrypt('./image_demos/decrypted_binary_info_1.txt')
    
    # 初始化解密类，传入需要解密的图片
    d = DecryptionBinary('./image_demos/demo_encrypted_binary_2.jpg', e.threshold)
    # 解密文件二，是一个png
    d.decrypt('./image_demos/decrypted_binary_info_2.png')

#!/usr/bin/python3 
# coding:utf-8
import sys
from imp import reload
reload(sys)

from PIL import Image

class pixel2Char():

    def __init__(self, image, output_width = 150, output_height = 150):
        self.image = image
        self.output_width = output_width
        self.output_height = output_height
    
    #原始图像按照输入尺寸缩放处理
    def resizeImg(self):
        #打开图片，默认是以只读打开，且pillow目前只支持只读打开
        image = Image.open(self.image)
        #图像模式转换，RGBA/P/
        if image.mode is not 'RGB':
            image = image.convert('RGB')
        #获取原始图片尺寸
        image_width, image_height = image.size
        #获取图片缩放宽高比例
        w_scale = self.output_width * 1.0 / image_width
        h_scale = self.output_height * 1.0 / image_height
        
        #防止输入尺寸比例造成图片变形，等比缩放获取缩放值处理
        scale = w_scale if w_scale < h_scale else h_scale
        #等到最终宽高值
        res_width = int(scale * image_width)
        res_height = int(scale * image_height)
        #图片重置 并且做防锯齿过滤，取值0-5
        image = image.resize((res_width, res_height), Image.HAMMING)
        return image
    
    #图像像素转换
    def pixel2Chars(self, image_pixels, image_width, image_height):
        #定义替换的字符串字符或数字，自定义，注意因为空白地方需要“ ”空
        replace_chars = '0123456789 '
        terminal_chars = ''
        for h in range(image_height):
            for w in range(image_width):
                #RGB值转换为对应数字
                point_pixel = image_pixels[w, h]
                terminal_chars += replace_chars[int(sum(point_pixel) / 3.0 / 256.0 * len(replace_chars))]
            terminal_chars += '\n'
        return terminal_chars

    #输出显示
    def show(self):
        image = self.resizeImg()
        image_pixels = image.load()
        out_width ,out_height = image.size
        #RGB转化字符或数字
        return self.pixel2Chars(image_pixels, out_width, out_height)

if __name__ == "__main__":
    
    if len(sys.argv) < 2 :
        print('please excute : python ' + sys.argv[0] + ' source.png')
        exit(0)
    
    image = sys.argv[1]
    
    output_width = int(sys.argv[2]) if len(sys.argv) > 3 else 150
    output_height = int(sys.argv[3]) if len(sys.argv) > 4 else 150

    img = pixel2Char(image, output_width, output_height).show()
    print(img)
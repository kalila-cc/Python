# -*- coding: utf-8  -*-

from PIL import Image, ImageFilter, ImageOps, ImageChops, ImageEnhance
import os


charset = list("/\|()1{}$@B%8&WM#ZO0QLCJUYX*hkbdpqwmoahkbdpqwmzcvunxrjft[]?-_+~<>i!lI;:,\"^`'. ")
step = 256 / len(charset)


def main():
    # 必要参数
    img_path = r"image.jpg"
    width_scale, height_scale = 2.0, 1.0
    max_pixel = 180
    # 生成文字
    if img_path:
        try:
            img = Image.open(img_path)
        except:
            print(f"图片'{img_path}'打开失败")
            exit(-1)
        img = img.convert('L')
        edge = ImageOps.invert(img.filter(ImageFilter.CONTOUR))
        img = ImageChops.subtract(img, edge)
        img = ImageEnhance.Contrast(img).enhance(1.2)
        width, height = img.size
        width, height = int(width * width_scale), int(height * height_scale)
        common_scale = (lambda w: max_pixel / w if w > max_pixel else 1.0)(max(width, height))
        if common_scale < 1.0:
            width, height = int(width * common_scale), int(height * common_scale)
        img = img.resize((width, height))
        txt = ''
        for i in range(height):
            row = [charset[int(img.getpixel((j, i)) / step)] for j in range(width)]
            txt += ''.join(row) + '\n'
        save_path = f"{os.path.splitext(img_path)[0]}.txt"
        with open(save_path, 'w') as f:
            f.write(txt)
        print(f"图片转字符成功，文本已保存至文件'{save_path}'")
    else:
        print("请填写必要参数")


if __name__ == '__main__':
    main()

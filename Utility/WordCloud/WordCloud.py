# -*- coding: utf-8  -*-

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import jieba
import wordcloud


def main():
    # 路径设置（需要用户设置）
    txt_path = r"" # 必需
    mask_path = r"./mask.jpg"
    save_path = r"./wordcloud.jpg"
    stopwords_path = r"./stopwords.txt"
    font_path = r"C:\Windows\Fonts\msyh.ttc"
    # 自定义参数设置（需要用户设置）
    txt_encoding = 'gbk'
    stopwords_encoding = 'utf-8'
    max_words = 100
    width, height = 500, 500
    min_font_size, max_font_size = 8, 64
    show_img = True
    # 检查必需项
    if not txt_path:
        print('ERROR: 请指定文本文件的路径')
        exit(-1)
    # 默认参数值
    mask = None
    stopwords = set()
    # 若有 mask 则执行
    if mask_path:
        mask = np.array(Image.open(mask_path))
    # 若有 stopwords 则调用
    if stopwords_path:
        with open(stopwords_path, 'r', encoding=stopwords_encoding) as f:
            stopwords = {x.strip() for x in f.readlines()}
    # 生成词云
    with open(txt_path, "r", encoding=txt_encoding) as f:
        text = f.read()
        cut_text = jieba.cut(text)
        result = ' '.join(cut_text)
        wc = wordcloud.WordCloud(
            width=width,
            height=height,
            max_words=max_words,
            background_color='white',
            max_font_size=max_font_size,
            min_font_size=min_font_size,
            mask=mask,
            font_path=font_path,
            stopwords=stopwords,
        )
        wc.generate(result)
        if save_path:
            wc.to_file(save_path)
        # 成功生成
        print("INFO: 成功生成词云")
        # 可选生成后显示图片
        if show_img:
            plt.figure('word cloud')
            plt.imshow(wc)
            plt.axis('off')
            plt.show()


if __name__ == '__main__':
    main()

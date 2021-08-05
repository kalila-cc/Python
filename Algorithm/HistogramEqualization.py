# -*- coding: utf-8 -*-

import cv2
import numpy as np
import matplotlib.pyplot as plt


def readGreyImg(filepath: str) -> np.ndarray:
    img = cv2.imread(filepath)
    greyImg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return greyImg


def equalizeHist(img: np.ndarray, depth: int) -> np.ndarray:
    h, w = img.shape[:2]
    hist = np.zeros(depth)
    for row in img:
        for col in row:
            hist[col] += 1
    transformFunc = (depth - 1) * (hist.cumsum() / img.size)
    transformedImg = img.copy()
    for i in range(h):
        for j in range(w):
            transformedImg[i][j] = transformFunc[transformedImg[i][j]]
    return transformedImg


def showHist(img: np.ndarray, depth: int, title: str = ''):
    img_data = img.reshape(img.size)
    plt.hist(img_data, bins=depth)
    plt.title(title)


def showImg(img: np.ndarray, title: str = ''):
    plt.imshow(img, cmap='Greys_r')
    plt.axis('off')
    plt.title(title)


def main():
    fp = './image.jpg'
    depth = 256

    greyImg = readGreyImg(fp)
    transformedImg = equalizeHist(greyImg, depth)

    plt.subplot(1, 2, 1)
    showImg(greyImg, 'original')
    plt.subplot(1, 2, 2)
    showImg(transformedImg, 'My Code')
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()

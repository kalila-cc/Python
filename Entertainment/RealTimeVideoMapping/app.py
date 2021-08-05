# -*- coding: utf-8 -*-

import numpy as np
import cv2

# 全局变量
classifier = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
shade = cv2.imread('./funny.png', cv2.IMREAD_UNCHANGED)
win_name = 'camera'
cv2.namedWindow(win_name)
key_dict = {}
kernel_size = 11


def add_alpha_channel(img) -> np.ndarray:
    (b, g, r) = cv2.split(img)
    a = np.ones(b.shape, dtype=b.dtype) * 255
    img = cv2.merge((b, g, r, a))
    return img


def cond_proc(cur_key: str, cur_img: np.ndarray, key: str, proc_func, *args, **kwargs) -> np.ndarray:
    global key_dict
    if key not in key_dict:
        key_dict[key] = True
    if cur_key == ord(key):
        key_dict[key] = not key_dict[key]
    if key_dict[key]:
        cur_img = proc_func(cur_img, *args, **kwargs)
    return cur_img


def equalizeHist(img: np.ndarray) -> np.ndarray:
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    equalized_gray_img = cv2.equalizeHist(gray_img)
    return equalized_gray_img


def face_recognition(img: np.ndarray, bg_img: np.ndarray) -> np.ndarray:
    # 增加通道
    png = add_alpha_channel(bg_img)
    # 人脸识别
    faces = classifier.detectMultiScale(img, minNeighbors=4, minSize=(100, 100))
    for face in faces:
        # 获取人脸位置大小
        (x, y, w, h) = face
        # 计算贴图
        shade_w = min(w, h)
        resized_shade = cv2.resize(shade, (shade_w, shade_w))
        # 确定需要修改的位置和大小
        (x, y, w, h) = (x + w // 2 - shade_w // 2, y + h // 2 - shade_w // 2, shade_w, shade_w)
        # 计算 alpha
        shade_alpha = resized_shade[:, :, 3] / 255.0
        png_alpha = 1.0 - shade_alpha
        # 融合每个通道
        for c in range(3):
            png[y: y + h, x: x + w, c] = png_alpha * png[y: y + h, x: x + w, c] + shade_alpha * resized_shade[:, :, c]
    # 取 BGR 通道
    marked_img = png[:, :, :3]
    return marked_img


def update_variables(x) -> None:
    global kernel_size
    kernel_size = (lambda n: n if n & 1 else n + 1)(cv2.getTrackbarPos('kernel_size', win_name))


def main():
    # 创建滑动条
    cv2.createTrackbar('kernel_size', win_name, kernel_size, 17, update_variables)
    # 创建相机对象
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # 实时处理视频
    while True:
        # 获取 keyCode 同时使循环进行
        keyCode = cv2.waitKey(5)
        if keyCode == 27:
            break
        # 获取 frame
        success, frame = camera.read()
        if not success:
            break

        """ 处理图像 """
        # 水平翻转
        raw_img = cv2.flip(frame, 1)
        # 直方图均衡化
        img = cond_proc(keyCode, raw_img, 'e', equalizeHist)
        # 高斯模糊
        img = cond_proc(keyCode, img, 'g', cv2.GaussianBlur, (kernel_size, kernel_size), 0)
        # 人脸贴图
        img = cond_proc(keyCode, img, 'r', face_recognition, raw_img)

        # 确定需要显示的图片
        img_to_show = img
        # 显示图像
        cv2.imshow(win_name, img_to_show)
    # 释放对象并清除窗口
    camera.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
    exit(0)

'''
Created on 2020-06-08
@author: zhengjin
@desc: 寻找图像的凸包（convex hull）
'''

import cv2
import os
import numpy as np


def create_img_polygon(img_path):
    if os.path.exists(img_path):
        return

    # 新建 512*512 3通道 空白图片
    img = np.zeros((512, 512, 3), np.uint8)
    # 平面点集
    pts = np.array([[200, 250], [250, 300], [300, 270],
                    [270, 200], [120, 240]], np.int32)
    pts.reshape(-1, 1, 2)
    # 绘制填充的多边形
    cv2.fillPoly(img, [pts], (255, 255, 255))
    cv2.imwrite(img_path, img)


def create_img_convexhull(img_path):
    img = cv2.imread(img_path, 1)

    # 灰度模式
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 二值化
    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # 图片轮廓
    contours, hierarchy = cv2.findContours(thresh, 2, 1)
    cnt = contours[0]
    hull = cv2.convexHull(cnt)
    print(hull.shape)

    length = len(hull)
    for i in range(length):
        cv2.line(img, tuple(hull[i][0]), tuple(
            hull[(i+1) % length][0]), (0, 255, 0), 2)

    # 显示图片
    # pip3 install opencv-python==4.1.0.25 -i https://pypi.tuna.tsinghua.edu.cn/simple
    cv2.imshow('convexhull_line', img)
    cv2.waitKey()


if __name__ == '__main__':

    img_path = '/tmp/test/polygon.png'
    create_img_polygon(img_path)
    create_img_convexhull(img_path)
    print('opencv convex hull demo done.')
